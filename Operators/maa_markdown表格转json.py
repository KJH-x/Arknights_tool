# md table to json
import os
import sys
import re
import json


os.chdir(sys.path[0])
table_pattern = r'(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\n'
table_group = []
# 读取Markdown文件
with open('.\\ref\\operators.md', 'r', encoding='utf-8') as file:
    table_group = file.read().split("\n\n")
tables_data = dict()

for rank, table in enumerate(table_group, start=1):
    write_c=dict()
    lines = table.splitlines()
    table_head = lines[0].split("|")
    table_content = lines[2:]
    for operator in table_content:
        names = operator.split("|")
        write_c[f"{names[0]}"]=dict()
    
        for i in range(1,len(names)):
            write_c[f"{names[0]}"][table_head[i]]=names[i]

    tables_data[f"{rank}"]=dict(write_c)


# 将提取的表格数据保存为JSON文件
with open('.\\ref\\operator.json', 'w', encoding='utf-8') as json_file:
    json.dump(tables_data, json_file, ensure_ascii=False, indent=4)

print("表格数据已提取并保存为output.json文件。")
