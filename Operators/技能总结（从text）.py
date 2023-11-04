# skill conclude
import os
import re
import json

# 获取脚本所在文件夹的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
html_extract_dir = os.path.join(script_dir, 'htmls_extract')  # 存放提取后HTML文件的目录
conclusion_file = os.path.join(script_dir, 'conclusion.json')  # 结果保存文件路径

# 定义一个正则表达式模式来匹配技能名
skill_pattern = r"\|技能名\s*=\s*(.*?)\n"

# 用于保存提取的数据
result_data = []

# 遍历html_extract目录下的所有txt文件
for filename in os.listdir(html_extract_dir):
    if filename.endswith('.txt'):
        # 读取txt文件内容
        with open(os.path.join(html_extract_dir, filename), 'r', encoding='utf-8') as txt_file:
            txt_content = txt_file.read()

        # 使用正则表达式匹配技能名
        skills = re.findall(skill_pattern, txt_content)

        # 只保留前三个技能，如果不足三个则保留实际数量
        skills = skills[:3]

        # 构建数据项
        data_item = {
            "operator": os.path.splitext(filename)[0],
        }
        data_item["skill"]=[]

        for i, skill in enumerate(skills, start=1):
            data_item["skill"].append(skill)

        result_data.append(data_item)

# 保存提取的数据到JSON文件
with open(conclusion_file, 'w', encoding='utf-8') as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=2)

print(f"提取完成，结果已保存到 {conclusion_file}")
