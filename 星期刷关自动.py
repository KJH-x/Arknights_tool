from datetime import datetime,timedelta
import json
import time
import sys
import os
import re
from urllib.error import URLError


os.chdir(sys.path[0])

with open(".\\MaaPlan.json", 'r', encoding='utf8') as plan:
    TASKS = json.load(plan)
with open(".\\MaaConnect.json", 'r', encoding='utf8') as connect:
    PATH = json.load(connect)


sys.path.append(
    (PATH['Maa_core']+"\\Python")
)
from asst.asst import Asst
from asst.utils import Message, Version, InstanceOptionType
from asst.updater import Updater


@Asst.CallBackType
def my_callback(msg, details, arg):
    repot_time = datetime.now().strftime(TLF)
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))
    msg_print = re.sub('Message.', '', str(m))

    try:
        match msg_print:
            case 'SubTaskStart' | 'SubTaskCompleted':
                print(
                    f"[{repot_time}]信息:子任务:{映射[re.sub('SubTask','',msg_print)]}"
                )
                print(f"  - 父任务序号:{d['taskid']:2d}  - ", end='')

                if 'task' in d['details']:
                    print(f"当前任务：{d['details']['task']}")
                else:
                    print(f"当前任务：未知")
                if arg:
                    print(f"  - 额外参数:{arg}")

            case 'ConnectionInfo':
                print(f"[{repot_time}]信息:模拟器连接:行为:{d['what']}")
                if d['why']:
                    print(f"[{repot_time}]信息:模拟器连接:原因:{d['why']}")

            case 'TaskChainStart' | 'TaskChainCompleted' | 'TaskChainStopped':
                print(
                    f"[{repot_time}]信息:任务链:{映射[re.sub('TaskChain','',msg_print)]}"
                )
                print(f"  - 任务链名:{d['taskchain']}")

            case 'SubTaskExtraInfo':
                print(f"[{repot_time}]信息:子任务信息:已忽略")

            case 'AllTasksCompleted':
                print(f"[{repot_time}]全部任务完成，退出")

            case 'SubTaskError':
                if 'first' in d and d['first']:
                    print(f"[{repot_time}]信息:子任务错误{d['first'][0]}")
                else:
                    print(f"[{repot_time}]信息:子任务错误")
            case _:
                print(f"[Cannot comprehense]:\n{m}\n{d}\n{arg}")

    except KeyError:
        print("回应理解错误：")
        print(f"[Cannot comprehense]:\n{m}\n{d}\n{arg}")
    return


def fight_task_selector() -> int:
    wd = (datetime.now()-timedelta(hours=4)).weekday()
    return [0, 1, 0, 1, 0, 1, 1][wd]


# TASKS
#   - FIGHT
#   - [  0,  1,  2,  3,  4,  5,  6]
#   - [MON,TUE,WEN,THU,FRI,SAT,SUN]
#   CE-6: (1 for open)
#   - [  0,  1,  0,  1,  0,  1,  1]
TLF = "%H:%M:%S.%f"

映射 = {
    "Start": "开始",
    "Completed": "完成",
    "Stopped": "停止"
}


if __name__ == "__main__":
    try:
        Updater(PATH["Maa_core"], Version.Beta).update()

    except TimeoutError or URLError:
        pass
    except Exception as ex:
        input(ex)
    except KeyboardInterrupt:
        exit()

    Asst.load(path=PATH["Maa_core"])
    asst = Asst(callback=my_callback)
    
    try:
        asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
        asst.set_instance_option(InstanceOptionType.deployment_with_pause, '1')

        retry = 0
        while 1:
            if asst.connect(PATH["Adb"], PATH["Address"]):
                print(f"[{datetime.now().strftime(TLF)}]连接成功")
                del retry
                break
            else:
                retry += 1
                print(
                    f"[{datetime.now().strftime(TLF)}]连接失败，尝试重连{retry:2d}")
                pass

        TASKS["Fight"] = TASKS["Fight"][fight_task_selector()]

        print(f"[{datetime.now().strftime(TLF)}]正在加载任务列表:")
        for task_name in TASKS["Sequence"]:
            print(
                f"  - {task_name:10s}:{asst.append_task(task_name,TASKS[task_name]):2d}"
            )

        print(
            f"[{datetime.now().strftime(TLF)}]当前客户端版本：{asst.get_version()}，正在启动"
        )

        del TASKS, PATH
        asst.start()

        while asst.running():
            time.sleep(0)
        asst.stop()
        input()

    except KeyboardInterrupt:
        asst.stop()
        input()
        exit()

    except Exception as ex:
        print("意外错误:", ex)
        asst.stop()
        input()
        exit()
