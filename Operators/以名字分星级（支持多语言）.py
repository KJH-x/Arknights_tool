# sort names
import os
import sys
import json
import shutil
os.chdir(sys.path[0])

with open(".\\ref\\operator.json",  mode='r', encoding="utf-8") as json_file:
    data_set = json.load(json_file)

data_set = dict(data_set)
new_construct_sheet = dict()
for key in data_set.keys():
    for op in data_set[key].keys():
        new_construct_sheet[f"{data_set[key][op]['中文']}"] = key

need_sorted = set()
check_dir = sys.path[0]+"\\downloaded_images\\头像"
for filename in os.listdir(check_dir):
    need_sorted.add(filename)

for i in range(1, 7):
    os.makedirs(f"{check_dir}\\{i}", exist_ok=True)

for file_name in need_sorted:
    for name in new_construct_sheet.keys():
        if f"_{name}_" in file_name:
            shutil.move(os.path.join(check_dir, file_name), os.path.join(
                check_dir, new_construct_sheet[name], file_name))
