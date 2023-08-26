import win32gui
# import win32com
import win32con
import win32api

VK_MENU = 0x12


def match_title(partial_title: str):
    """
    通过部分标题查找窗口
    :param partial_title: 部分标题
    :return: 匹配到的窗口列表
    """
    def callback(hwnd, windows: list):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if partial_title.lower() in window_title.lower():
                windows.append((hwnd, window_title))
        return True
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows


def set_pos(hwnd, pos: tuple) -> None:
    """
    设置窗口位置
    :param hwnd: 窗口句柄
    :param pos: 窗口位置信息，包括左上角坐标和宽高
    :return: None
    """
    # 设置位置
    x, y, width, height = pos
    win32gui.SetWindowPos(
        hwnd,
        0, x, y, width, height, win32con.SWP_SHOWWINDOW
    )

    # 处于某些原因，调用SetForegroundWindow前需要按一下alt，不然会报错
    # (0, 'SetForegroundWindow', 'No error message is available')
    win32api.keybd_event(VK_MENU, 0, 0, 0)
    win32api.keybd_event(VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 设为当前最高
    win32gui.SetForegroundWindow(hwnd)
    return


def test_pos(title: str, x, y, w, h) -> tuple:
    """
    测试窗口位置并返回窗口矩形信息
    :param title: 窗口标题
    :param x: 窗口左上角横坐标
    :param y: 窗口左上角纵坐标
    :param w: 窗口宽度
    :param h: 窗口高度
    :return: 窗口矩形信息元组 (left, top, right, bottom)
    """
    win32gui.SetWindowPos(
        win32gui.FindWindow(None, title),
        0, x, y, w, h, win32con.SWP_SHOWWINDOW
    )

    return win32gui.GetWindowRect(win32gui.FindWindow(None, title))


# 三个模拟器，三个MAAGUI，对于屏幕分辨率3840x2160，Windows缩放1.5x
presets = {
    "sim_1": {"name": "Nox_Sim_1",
              "pos": [0, 32, 895, 514]},
    "sim_2": {"name": "Nox_Sim_2",
              "pos": [852, 32, 895, 514]},
    "sim_3": {"name": "Nox_Sim_3",
              "pos": [1705, 32, 895, 514]},
    "MAA_1": {"name": "MAA (A1)",
              "pos": [-1, 544, 853, 600]},
    "MAA_2": {"name": "MAA (A2)",
              "pos": [852, 544, 853, 600]},
    "MAA_3": {"name": "MAA (A3)",
              "pos": [1705, 544, 855, 600]},
}


# 搜索标题完整名称（同时确保了窗口存在）
for key in presets.keys():
    info = match_title(presets.get(key).get("name"))

    # 返回为空，窗口不存在，设名称为空（后续判据）
    if info == []:
        presets[key]["name"] = ""

    # 返回不为空，查询hwnd并写入
    else:
        presets[key]["name"] = info[0][1]
        presets[key]["hwnd"] = win32gui.FindWindow(None, info[0][1])

# 拷贝需要操作的目标和信息
target_set = [
    presets.get(x)
    for x in presets.keys()
    if presets.get(x).get("name") != ""
]

# 设置窗口位置
for target in target_set:
    set_pos(target["hwnd"], target["pos"])
