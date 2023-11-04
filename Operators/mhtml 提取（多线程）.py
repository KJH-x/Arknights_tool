# mhtml extract
import os
import json
from bs4 import BeautifulSoup
import re
import sys
import concurrent.futures

os.chdir(sys.path[0])
pattern = r"https://prts.wiki/images/[0-9]{1,}/[0-9]{1,}/.*"
seen_values=set()

# 定义函数来提取数据
def extract_data(file_path):
    global seen_values
    # 读取MHTML文件内容
    with open(file_path, "rb") as mhtml_file:
        mhtml_content = mhtml_file.read().decode(
            encoding="utf-8").replace("=\r\n", "").encode("utf-8")

    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(mhtml_content, "html.parser")

    # 使用XPath提取所有匹配的img元素
    img_elements = soup.find_all("img", attrs={"src": True})

    # 提取src内容并构造数据项
    src_data = {}
    src_data_unique={}

    # 使用re模块进行匹配
    for idx, img in enumerate(img_elements, start=1):
        matchs =  re.findall(pattern, img["src"])
        if len(matchs)>0:
            src_data[f"src_{idx}"] = matchs[0]
        else:
            pass
    for key, value in src_data.items():
        if value not in seen_values:
            src_data_unique[key] = value
            seen_values.add(value)
    # 构造数据项并添加到列表中
    return src_data_unique


# 定义保存提取数据的列表
data_list = []

# 遍历指定文件夹中的所有MHTML文件
mhtml_folder = "./operator_full_mhtml"  # 替换为你的MHTML文件夹路径
mhtml_files = [os.path.join(mhtml_folder, filename) for filename in os.listdir(mhtml_folder) if filename.endswith(".mhtml")]

# 定义进度显示函数
def show_progress(total_count, current_count):
    print(f"Progress: {current_count}/{total_count}")

# 使用16线程来提取数据并显示进度
total_count = len(mhtml_files)
current_count = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    future_to_file = {executor.submit(extract_data, file_path): file_path for file_path in mhtml_files}
    for future in concurrent.futures.as_completed(future_to_file):
        file_path = future_to_file[future]
        current_count += 1
        show_progress(total_count, current_count)
        try:
            result = future.result()
            data_item = {
                "name": os.path.basename(file_path),
                "src": result
            }
            data_list.append(data_item)
        except Exception as e:
            print(f"Error extracting data from {file_path}: {str(e)}")

# 将数据列表保存为JSON文件
output_file = "img_src_export.json"  # 输出JSON文件名
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print("提取并保存完成。")
