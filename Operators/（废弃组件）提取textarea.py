import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 获取脚本所在文件夹的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
html_dir = os.path.join(script_dir, 'htmls')  # 存放原HTML文件的目录
html_extract_dir = os.path.join(script_dir, 'htmls_extract')  # 存放提取后HTML文件的目录

# 创建'html_extract'子文件夹（如果不存在）
os.makedirs(html_extract_dir, exist_ok=True)

# 定义一个函数来处理单个HTML文件


def process_html_file(filename):
    # 读取原HTML文件
    with open(os.path.join(html_dir, filename), 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找id为wpTextbox1的<textarea>元素
    textarea = soup.find('textarea', {'id': 'wpTextbox1'})

    if textarea:
        # 提取<textarea>元素的内容
        extracted_content = textarea.text

        # 构建保存提取后内容的新HTML文件名
        new_filename = os.path.splitext(filename)[0]  # 去掉文件扩展名
        new_html_filename = f"{new_filename}.txt"

        # 保存提取后的内容到新的HTML文件
        with open(os.path.join(html_extract_dir, new_html_filename), 'w', encoding='utf-8') as new_html_file:
            new_html_file.write(extracted_content)

        print(f"已保存提取后的内容到 {new_html_filename}")
    else:
        print(f"在 {filename} 中找不到id为wpTextbox1的<textarea>元素")


# 使用16个线程处理HTML文件
with ThreadPoolExecutor(max_workers=16) as executor:
    html_files = [filename for filename in os.listdir(
        html_dir) if filename.endswith('.html')]
    executor.map(process_html_file, html_files)

print("提取完成")
