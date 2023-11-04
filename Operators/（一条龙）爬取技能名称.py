# Request Html
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import urllib.parse
import requests


def download_raw_html(index_name: str) -> None:
    global page_count,proxy

    # 标准化index_name，合成url
    safe_index_name = urllib.parse.quote(index_name, safe='')
    url = f"https://prts.wiki/index.php?title={safe_index_name}&action=edit"

    try:
        response = requests.get(url,proxies=proxy)
        if response.status_code == 200:
            page_count += 1

            # 保存HTML内容到文件
            html_file_name = f"{index_name}.html"
            with open(os.path.join(html_dir, html_file_name), 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
            print(f"[{page_count:3d}/{len(op_names)}] 已保存 {html_file_name}")

        else:
            print(f"HTTP_Error:返回值不为200:无法下载 {index_name} 的页面，检查网络连接")

    except Exception as e:
        print(f"下载 {index_name} 的页面时出错：{e}")

    return


def extract_text(filename):
    # 读取原HTML文件
    with open(os.path.join(html_dir, filename), 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # 解析HTML查找
    soup = BeautifulSoup(html_content, 'html.parser')
    textarea = soup.find('textarea', {'id': 'wpTextbox1'})

    if textarea:
        # 提取<textarea>元素的内容
        extracted_content = textarea.text
        # 替换HTML内容中的`&lt;`为`<`
        modified_html = textarea.text.replace('&lt;', '<')

        # 保存
        text_filename = f"{os.path.splitext(filename)[0]}.txt"
        with open(os.path.join(html_extract_dir, text_filename), 'w', encoding='utf-8') as new_html_file:
            new_html_file.write(extracted_content)

        print(f"已保存提取后的内容到 {text_filename}")
    else:
        print(f"在 {filename} 中找不到指定元素")

local_html_dir = 'raw_html'
local_extract_text_dir = 'raw_text'

proxy = {
    'http': 'http://127.0.0.1:?',
    'https': 'http://127.0.0.1:?',
}

# 获取脚本所在文件夹的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
html_dir = os.path.join(script_dir, local_html_dir)
os.makedirs(html_dir, exist_ok=True)
html_extract_dir = os.path.join(script_dir, local_extract_text_dir)
os.makedirs(html_extract_dir, exist_ok=True)

# 读取文件中的索引名称
with open(os.path.join(script_dir, 'ref\\operator_name_list.txt'), 'r', encoding='utf-8') as index_file:
    op_names = index_file.read().splitlines()


# 记录已下载的页面文件
downloaded_files = set()
for filename in os.listdir(html_dir):
    downloaded_files.add(os.path.splitext(filename)[0])

# 请求进度计数器
page_count = 0

# 遍历下载
for op_name in op_names:
    if op_name in downloaded_files:
        page_count += 1
        pass
    else:
        download_raw_html(op_name)


print("全部页面已下载完成")


# 使用16个线程处理HTML文件
with ThreadPoolExecutor(max_workers=16) as executor:
    html_files = [filename for filename in os.listdir(
        html_dir) if filename.endswith('.html')]
    threads= executor.map(extract_text, html_files)
    for result in threads:
        print(result)

print("提取完成")
