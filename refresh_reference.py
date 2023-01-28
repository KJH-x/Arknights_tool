# encoding=utf-8
'''
Filename : tool.py
Datatime : 2023/01/25 
Author :KJH-x
'''
import requests
import sys
import os
os.chdir(sys.path[0])

value_json_url = "https://houduan.yituliu.site/file/export/item/value/json"

with open(".\\material_value.json", "wb") as mv:
    mv.write(requests.get(value_json_url).content)
