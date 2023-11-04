# img download
import urllib.request
import time
import json
import os
import sys
import urllib.parse


def read_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def get_all_download_links(data):
    download_links = []
    for item in data:
        for urls in data:
            for url in urls["url"]:
                download_links.append(url)
    # for item in data:
    #     if 'src' in item:
    #         for key, value in item['src'].items():
    #             download_links.append(value)

    return download_links


def download_images(image_urls, save_path):
    global downloaded_files
    os.makedirs(save_path, exist_ok=True)
    url_amount = len(image_urls)
    download_count = 0
    for image_url in image_urls:
        unquote_url = urllib.parse.unquote(image_url)
        pic_name = os.path.basename(unquote_url)
        if pic_name not in downloaded_files:
            try:
                file_name = os.path.join(save_path, pic_name)
                urllib.request.urlretrieve(image_url, file_name)
                print(f"[{download_count}/{url_amount}] {pic_name} 已下载")
                time.sleep(0.2)
            except Exception as e:
                print(f"[{download_count}/{url_amount}] 下载失败：{pic_name}, 错误：{str(e)}")
                input("等待操作")
        else:
            print(f"[{download_count}/{url_amount}] {pic_name} 已下载，跳过")
        download_count += 1


os.chdir(sys.path[0])

json_file_path = '.\\data\\json\\goods_extract_img.json'
data = read_json(json_file_path)
download_links = get_all_download_links(data)
save_path = '.\\downloaded_goods_images'
os.makedirs(os.path.join(sys.path[0],save_path),exist_ok=True)
# 记录已下载的页面文件
downloaded_files = set()
for filename in os.listdir(save_path):
    downloaded_files.add(filename)

# 下载图片
download_images(download_links, save_path)
