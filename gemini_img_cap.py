
import os
# 设置代理服务器地址和端口
proxy_host = '127.0.0.1'
proxy_port = '7890'
os.environ['http_proxy'] = f'http://{proxy_host}:{proxy_port}'
os.environ['https_proxy'] = f'http://{proxy_host}:{proxy_port}'

import google.generativeai as genai
import pathlib

genai.configure(api_key='')


import PIL.Image
import os
import google.generativeai as genai

#Choose a Gemini model.
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

prompt = """
角色概述：作为一名人像照片评价官，你的主要职责是协助用户建立一个全面、可搜索的人像照片数据库。你的工作包括对用户输入的图像进行详细的描述，并为每张图像生成准确的主题词，方便用户后续根据这些主题词索引、搜索和参考相关图像。
主要职责：
生成主题词：
提取关键元素： 根据图像内容，生成准确、简洁的主题词列表。
主题词类别：
环境类： 城市、海边、森林、乡村、山脉等。
季节和天气类： 春天、夏天、秋天、冬天、下雨、下雪、晴天等。
人物类： 男人、女人、儿童、老人、情侣、家庭等。
人物动作： 坐、立、跳跃、挥手、掐腰、抬头、低头、侧脸等。
人物特征： 可爱、性感、瘦弱、肤色偏黑、肤色偏白、圆脸等。
活动类： 散步、跑步、跳舞、游泳、工作、学习等。
色彩类： 红色、黄色、蓝色、绿色、彩色、黑白等。
情感和氛围类： 快乐、悲伤、浪漫、宁静、热闹等。
拍摄距离：近摄、特写、远场、等。
周围的物体：路灯、街道、汽车、轮胎等等。
其他： 动物、花朵、树木、建筑物、河流等。
协助构建数据库：
确保信息准确： 描述和主题词应准确且具有代表性，方便用户根据关键词快速搜索到所需的图像。
支持后期检索： 帮助用户在后期通过输入相关词汇直接获取对应的参考图像进行拍照或创作。
执行标准和专业态度：
细致严谨： 在描述中注重细节，确保信息的准确性和完整性。
以用户为中心： 始终关注用户需求，提供有价值的意见和建议。
客观公正： 避免主观偏见，描述应基于客观事实。
高效明确： 语言表达简洁明了，避免使用过于复杂或模糊的词汇。
保密和安全： 遵守隐私政策，不泄露用户的任何个人信息或敏感内容。
遵循规范： 确保所有输出内容符合道德标准和相关法律法规，避免不适当或受限制的内容。注意：只需生成主题词即可，无需其他内容。
"""

# image_path_1 = "./images/data_2.jpg"  # Replace with the actual path to your first image
# sample_file_1 = PIL.Image.open(image_path_1)
# response = model.generate_content([prompt, sample_file_1])
# print(response.text)


import os
import pandas as pd
import time
from PIL import Image

# 假设 model 是你已经加载好的模型对象
# prompt 是你之前定义的提示词

def generate_keywords_for_images(directory, model, prompt):
    # 创建一个空的 CSV 文件，并写入表头
    with open('image_keywords.csv', 'w') as f:
        f.write('File Path,Keywords\n')

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):  # 检查文件是否为图像
            image_path = os.path.join(directory, filename)
            try:
                # 打开图像
                image = Image.open(image_path)
                
                # 使用模型生成主题词
                response = model.generate_content([prompt, image])
                
                # 获取生成的主题词
                keywords = response.text
                
                # 将结果写入 CSV 文件
                with open('image_keywords.csv', 'a') as f:
                    f.write(f'"{image_path}","{keywords}"\n')
                
                # 打印当前处理的文件
                print(f"Processed {image_path}")

                # 等待 4 秒
                time.sleep(4)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

# 使用示例
directory = './images'  # 替换为你的图像目录路径
generate_keywords_for_images(directory, model, prompt)