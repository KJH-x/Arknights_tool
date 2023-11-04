# getCP
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import os
import sys
import time


def delete_element_by_attribute(driver: WebDriver, attribute_name, attribute_value):
    # 使用JavaScript来查找并删除具有指定属性的元素
    js_code = f'document.querySelector(\'[{attribute_name}="{attribute_value}"]\').remove();'
    driver.execute_script(js_code)


def scroll_to(driver: WebDriver, percentage: float) -> None:
    # 计算要滚动到的垂直位置
    # scroll_height = driver.execute_script(
    #     "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    # target_scroll_position = scroll_height * percentage / 100
    # 使用JavaScript滚动到指定位置
    driver.execute_script(
        f"window.scrollTo(0, {page_full_height(driver) * percentage / 100});")
    print(f"  - SCT {percentage}%")


def click_buttons(driver: WebDriver):
    table_xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table"
    div_xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/div/div/div/div[1]/a"

    table_buttons = driver.find_elements(
        By.XPATH, f"{table_xpath}//tbody/tr[1]/th/span[1]/a")
    div_buttons = driver.find_elements(By.XPATH, div_xpath)

    for button in table_buttons:
        try:
            if button.text == "展开":
                try:
                    button.click()
                    time.sleep(0.2)
                except ElementClickInterceptedException:
                    scroll_to(driver, 0)
                    button.click()
            else:
                pass

        except NoSuchElementException:
            print(f"XPath不存在: {button}")

    for button in div_buttons:
        try:
            if button.text == "展开":
                button.click()
                time.sleep(0.2)
            else:
                pass

        except NoSuchElementException:
            print(f"XPath不存在: {button}")


def page_full_height(driver: WebDriver) -> int:
    return int(driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"))


def get_mhtml(index_name: str, driver: WebDriver) -> None:
    # driver = webdriver.Chrome(options=chrome_options)
    safe_index_name = urllib.parse.quote(index_name, safe='')
    driver.get(f"http://prts.wiki/w/{safe_index_name}")
    time.sleep(1)
    delete_element_by_attribute(driver, "class", "backToTop")

    if page_full_height(driver) > 8000:
        for percentage in [15, 30, 45, 60, 75, 90]:
            scroll_to(driver, percentage)
            time.sleep(0.5)
        click_buttons(driver)
        scroll_to(driver, 90)

    else:
        for percentage in [20, 40, 60, 80]:
            scroll_to(driver, percentage)
            time.sleep(0.5)
        click_buttons(driver)
        scroll_to(driver, 90)

    time.sleep(1)

    mhtml_data = str(driver.execute_cdp_cmd(
        'Page.captureSnapshot', {})['data'])
    with open(os.path.join(mhtml_dir, f"{index_name}.mhtml"), "wb") as file:
        file.write(mhtml_data.encode(encoding="utf-8"))
    # driver.quit()


proxy_server = "http://127.0.0.1:24680"
mlocal_html_dir = 'operator_full_mhtml'
# local_extract_text_dir = 'raw_text'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f'--proxy-server={proxy_server}')
chrome_options.add_argument(f'user-agent={user_agent}')
# chrome_options.add_argument('--headless')
button_xpaths = [
    "/html/body/div[3]/div[3]/div[5]/div[1]/table[21]/tbody/tr[1]/th/span[1]/a",
    "/html/body/div[3]/div[3]/div[5]/div[1]/div[14]/div/div/div[1]/a",
    "/html/body/div[3]/div[3]/div[5]/div[1]/table[22]/tbody/tr[1]/th/span[1]/a",
    "/html/body/div[3]/div[3]/div[5]/div[1]/table[23]/tbody/tr[1]/th/span[1]/a",
]


# 获取脚本所在文件夹的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
mhtml_dir = os.path.join(script_dir, mlocal_html_dir)
os.makedirs(mhtml_dir, exist_ok=True)
# html_extract_dir = os.path.join(script_dir, local_extract_text_dir)
# os.makedirs(html_extract_dir, exist_ok=True)

# 读取文件中的索引名称
with open(os.path.join(script_dir, 'ref\\operator_name_list.txt'), 'r', encoding='utf-8') as index_file:
    op_names = index_file.read().splitlines()


# 记录已下载的页面文件
downloaded_files = set()
for filename in os.listdir(mhtml_dir):
    downloaded_files.add(os.path.splitext(filename)[0])

# 请求进度计数器
page_count = 0

# 遍历下载
driver = webdriver.Chrome(options=chrome_options)
try:
    for op_name in op_names:
        if op_name in downloaded_files:
            print(f"[{page_count}/{len(op_names)}]已完成，{op_name}已存在，跳过")
            page_count += 1
            pass
        else:
            print(f"[{page_count}/{len(op_names)}]已完成，正在下载：{op_name}")
            get_mhtml(op_name, driver)
            page_count += 1
except Exception as e:
    input(e)
finally:
    driver.quit()

input(f"[{page_count}/{len(op_names)}]全部完成")