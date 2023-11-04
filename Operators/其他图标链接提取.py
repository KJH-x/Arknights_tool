# mhtml extract
import os
import json
import re
import sys
import concurrent.futures

os.chdir(sys.path[0])
pattern1 = r'"https://prts.wiki/images/[0-9a-f]{1,}/[0-9a-f]{1,}/.*.png" '

seen_values = set()


def extract_data(file_path):
    global seen_values
    with open(file_path, "rb") as mhtml_file:
        mhtml_content = mhtml_file.read().decode(
            encoding="utf-8").replace("=\r\n", "")

    urls = re.findall(pattern1, mhtml_content)
    src_data_unique = {}

    for idx, url in enumerate(urls, start=1):
        if  url not in seen_values:
            src_data_unique[f"src_{idx}"] = str(url)
    # 构造数据项并添加到列表中
    return src_data_unique


data_list = []
mhtml_folder = "./operator_full_mhtml"
mhtml_files = [os.path.join(mhtml_folder, filename) for filename in os.listdir(
    mhtml_folder) if filename.endswith(".mhtml")]


def show_progress(total_count, current_count):
    print(f"Progress: {current_count}/{total_count}")


# 使用16线程
total_count = len(mhtml_files)
current_count = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    future_to_file = {executor.submit(
        extract_data, file_path): file_path for file_path in mhtml_files}
    for future in concurrent.futures.as_completed(future_to_file):
        file_path = future_to_file[future]
        current_count += 1
        # show_progress(total_count, current_count)
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
output_file = "img_src_export.other.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print("提取并保存完成。")
