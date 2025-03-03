# 安装依赖：pip install streamlit pandas pillow
import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
from collections import defaultdict

# 配置页面
st.set_page_config(page_title="拍个好照片", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('image_fixed.csv', 
                        sep=',', 
                        engine='python',
                        quotechar='"',
                        skipinitialspace=True,
                        header=0,
                        names=['File Path', 'Keywords'],
                        dtype={'File Path': str, 'Keywords': str})
        
        # 清理文件路径
        df['File Path'] = df['File Path'].apply(
            lambda x: re.sub(r'[\n\\"]', '', x).strip()
        )
        
        # 处理关键词
        def process_keywords(text):
            text = re.sub(r'[，、\s]+', ',', str(text))
            text = re.sub(r'[“”"\'\\()（）]', '', text)
            return [k.lower().strip() for k in text.split(',') if k.strip()]
        
        df['Keywords'] = df['Keywords'].apply(process_keywords)
        df = df[df['Keywords'].apply(len) > 0]
        return df

    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        st.stop()

# 智能搜索类
class SmartSearch:
    def __init__(self, df):
        self.df = df
        self._build_index()

    def _build_index(self):
        """创建倒排索引加速搜索"""
        self.inverted_index = defaultdict(set)
        for idx, keywords in enumerate(self.df['Keywords']):
            for kw in keywords:
                self.inverted_index[kw].add(idx)

    def search(self, query, top_n=100):
        """带相关性评分的搜索"""
        raw_terms = [t.strip().lower() for t in query.split() if t.strip()]
        if not raw_terms:
            return pd.DataFrame()

        results = []
        for idx, row in self.df.iterrows():
            score = 0
            matched = []
            for term in raw_terms:
                # 完全匹配+2分，部分匹配+1分
                if term in row['Keywords']:
                    score += 2
                    matched.append(term)
                elif any(term in kw for kw in row['Keywords']):
                    score += 1
                    matched.append(f"*{term}")  # 标记部分匹配
            if score > 0:
                results.append({
                    'row': row,
                    'score': score,
                    'matched_terms': len(matched),
                    'exact_match': len([t for t in matched if not t.startswith('*')]) == len(raw_terms)
                })

        # 排序逻辑：完全匹配优先 -> 分数降序 -> 匹配词数量
        results.sort(key=lambda x: (
            -x['exact_match'], 
            -x['score'], 
            -x['matched_terms']
        ))
        
        return pd.DataFrame([r['row'] for r in results[:top_n]])

# 初始化
df = load_data()
smart_searcher = SmartSearch(df)

# 构建界面
st.title("📸 拍个好照片")
with st.expander("💡 使用说明"):
    st.markdown("""
    1. 输入关键词（多个用空格分隔）
    2. 完全匹配的结果优先显示
    3. 点击图片查看大图
    4. 支持中英文混合搜索
    """)

search_input = st.text_input("🔍 输入搜索关键词（如：微笑 毛衣 花瓣 蹲下 蓝色）", key="search")

if search_input:
    results = smart_searcher.search(search_input)
    if not results.empty:
        st.success(f"找到 {len(results)} 张匹配图片（按相关度排序）")
        
        cols = st.columns(3)
        for idx, (_, row) in enumerate(results.iterrows()):
            with cols[idx % 3]:
                try:
                    img = Image.open(os.path.join("images", row['File Path']))
                    caption = f"匹配关键词：{', '.join(row['Keywords'][:5])}..."
                    st.image(img, 
                           caption=caption,
                           width=300,
                           use_column_width=True)
                except Exception as e:
                    st.error(f"无法加载图片：{row['File Path']}")
    else:
        st.warning("未找到匹配图片，请尝试其他关键词")
else:
    st.info("请输入关键词开始搜索")

# 侧边栏统计
with st.sidebar:
    st.subheader("📊 数据概览")
    st.markdown(f"总图片数量：{len(df)}")
    all_keywords = [k for sublist in df['Keywords'] for k in sublist]
    st.write("热门关键词：", pd.Series(all_keywords).value_counts().head(10))