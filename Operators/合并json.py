# join json
import json
import os

# 获取脚本所在文件夹的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
op_data_file = os.path.join(script_dir, 'op_data.json')  # op_data.json 文件路径
conclusion_file = os.path.join(
    script_dir, 'conclusion.json')  # conclusion.json 文件路径
joined_file = os.path.join(script_dir, 'joined.json')  # 合并后的 JSON 文件路径

# 读取 op_data.json 文件
with open(op_data_file, 'r', encoding='utf-8') as op_data_json:
    op_data = json.load(op_data_json)

# 读取 conclusion.json 文件
with open(conclusion_file, 'r', encoding='utf-8') as conclusion_json:
    conclusion_data = json.load(conclusion_json)

# 创建一个新的 JSON 数据结构
joined_data = []

# 遍历 op_data 中的 "chars" 字段
for char_id, char_info in op_data["chars"].items():
    # 从 char_info 中获取角色名字
    char_name = char_info["name"]

    # 在 conclusion_data 中查找包含对应角色名的 operator 数据
    for operator_data in conclusion_data:
        if operator_data["operator"] == char_name:
            # 复制 operator 数据的 "skill" 字段到 char_info 中
            char_info["skill"] = operator_data["skill"]
            break  # 找到匹配的数据后，不再继续搜索

    joined_data.append(char_info)

# 将合并后的数据保存到 joined.json 文件中
with open(joined_file, 'w', encoding='utf-8') as joined_json:
    json.dump(joined_data, joined_json, ensure_ascii=False, indent=2)

print(f"合并完成，结果已保存到 {joined_file}")
