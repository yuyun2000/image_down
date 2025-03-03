# 📸 拍个好照片

基于Streamlit构建的智能图片检索工具，可通过CSV文件中存储的关键词快速定位图片，支持多关键词组合搜索和相关性排序。

辅助摄影师进行人像构图、动作设计、灵感提供等等


![Demo Screenshot](./assets/demo.png)

## 🚀 核心功能

- **关键词搜索**：支持中英文/混合关键词搜索
- **智能排序**：完全匹配 > 相关性评分 > 匹配词数量
- **多关键词支持**：用空格分隔多个搜索词（如：`女人 蓝色 户外`）
- **实时统计**：显示数据集概况和热门关键词
- **响应式布局**：自动适配电脑/手机端显示
- **快速预览**：点击图片查看大图模式

## 📦 安装指南

### 环境要求
- Python 3.8+
- pip 20.0+

### 快速开始
```bash
# 克隆仓库
git clone https://github.com/yuyun2000/take-a-good-photo.git

# 安装依赖
pip install streamlit pandas pillow

# 运行系统
streamlit run search.py
🛠 文件配置
数据结构要求
准备 image_keywords.csv：
File Path,Keywords
data1.jpg,关键词1,关键词2,关键词3
data2.jpg,关键词A,关键词B
图片存放路径：
项目根目录/
├── images/      # 存放所有图片
├── search.py    # 主程序
└── image_keywords.csv  # 关键词数据
```

# 说明
无意侵权，没有盈利，联系删除