import datetime
import json
import time
import sys
import re
sys.path.insert(
    0, "C:\\_Paths\\MAA\\Isolate1\\MAA-v4.8.0-beta.2-win-x64\\Python"
)
from asst.updater import Updater
from asst.utils import Message, Version, InstanceOptionType
from asst.asst import Asst


@Asst.CallBackType
def my_callback(msg, details, arg):
    repot_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))
    msg_print = re.sub('Message.', '', str(m))
    
    try:
        match msg_print:
            case 'SubTaskStart' | 'SubTaskCompleted':
                print(f"[{repot_time}]回报信息:子任务:{re.sub('SubTask','',msg_print)}")
                print(f"  - 父任务序号:{d['taskid']:2d}  - ",end='')
                
                if 'task' in d['details']:
                    print(f"当前任务：{d['details']['task']}")
                else:
                    print(f"当前任务：未知")
                if arg:
                    print(f"  - 额外参数:{arg}")

            case 'ConnectionInfo':
                print(f"[{repot_time}]回报信息:模拟器连接:行为:{d['what']}")
                if d['why']:
                    print(f"[{repot_time}]回报信息:模拟器连接:原因:{d['why']}")

            case 'TaskChainStart' | 'TaskChainCompleted' | 'TaskChainStopped':
                print(f"[{repot_time}]回报信息:任务链:{re.sub('TaskChain','',msg_print)}")
                print(f"  - 任务链名:{d['taskchain']}")

            case 'SubTaskExtraInfo':
                print(f"[{repot_time}]回报信息:子任务信息:已忽略")

            case 'AllTasksCompleted':
                print(f"[{repot_time}]全部任务完成，退出")
                
            case 'SubTaskError':
                if 'first' in d and d['first']:
                    print(f"[{repot_time}]回报信息:子任务错误{d['first'][0]}")
                else:
                    print(f"[{repot_time}]回报信息:子任务错误")
            case _:
                print(f"[Cannot comprehense]:\n{m}\n{d}\n{arg}")

    except KeyError:
        print("回应理解错误：")
        print(f"[Cannot comprehense]:\n{m}\n{d}\n{arg}")
    return


def fight_task_selector() -> int:
    wd = datetime.datetime.now().weekday()
    return [0, 1, 0, 1, 0, 1, 1][wd]


# TASKS
#   - FIGHT
#   - [  0,  1,  2,  3,  4,  5,  6]
#   - [MON,TUE,WEN,THU,FRI,SAT,SUN]
#   CE-6: (1 for open)
#   - [  0,  1,  0,  1,  0,  1,  1]

TASKS = {
    'Fight': [
        {
            "enable": True, "DrGrandet": False,
            "stage": "1-7", "medicine": 2, "stone": 0,
            "server": "CN", "client_type": "Official",
            "report_to_penguin": True, "penguin_id": "34004401",
        },
        {
            "enable": True, "DrGrandet": False,
            "stage": "CE-6", "medicine": 2, "stone": 0,
            "server": "CN", "client_type": "Official",
            "report_to_penguin": True, "penguin_id": "34004401",
        },
    ],
    'Recruit': {
        "enable": True, "refresh": True, "times": 1, "expedite": True,
        "select": [3, 4], "confirm": [3, 4], "skip_robot": True,
        "recruitment_time": {"3": 540, "4": 540, },
        "report_to_penguin": True, "penguin_id": "34004401",
    },
    'Infrast': {
        "enable": True,
        "mode": 0, "drones": "CombatRecord", "threshold": 0.3,
        "facility": [
            "Mfg", "Trade", "Reception", "Office", "Control", "Power", "Dorm"
        ],
        "dorm_notstationed_enabled": False, "dorm_trust_enabled": True,

    },
    'Visit': {
        "enable": True
    },
    'Mall':    {
        "enable": True, "shopping": True, "force_shopping_if_credit_full": True,
        "buy_first": [
            "招聘许可", "龙门币", "技巧概要·卷2", "糖", "装置", "酮凝集", "异铁", "聚酸酯", "固源岩",
        ],
        "blacklist": [
            "加急许可", "赤金", "源岩", "酯原料", "异铁碎片", "双酮", "破损装置", "代糖",
            "碳", "家具"
        ]
    },
    'Award': {
        "enable": True
    },
}

PATH = {
    'Maa_core': "C:\\_Paths\\MAA\\Isolate1\\MAA-v4.8.0-beta.2-win-x64",
    'Adb': "C:\\Program Files\\Nox\\bin\\.\\nox_adb.exe",
    'Address': "127.0.0.1:62001",
}

if __name__ == "__main__":
    try:
        Updater(PATH["Maa_core"], Version.Beta).update()
        Asst.load(path=PATH["Maa_core"])
        asst = Asst(callback=my_callback)
        
    except TimeoutError:
        Asst.load(path=PATH["Maa_core"])
        asst = Asst(callback=my_callback)
        
    except KeyboardInterrupt:
        exit()
        
    try:
        asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
        asst.set_instance_option(InstanceOptionType.deployment_with_pause, '1')
        
        retry=0
        while 1:
            if asst.connect(PATH["Adb"], PATH["Address"]):
                print('连接成功')
                del retry
                break
            else:
                retry+=1
                print(f'连接失败，尝试重连{retry:2d}')
                pass

        FIGHT_MODE = fight_task_selector()
        
        asst.append_task('StartUp')
        asst.append_task('Fight', TASKS["Fight"][FIGHT_MODE])
        asst.append_task('Recruit', TASKS['Recruit'])
        asst.append_task('Infrast', TASKS['Infrast'])
        asst.append_task('Visit', TASKS['Visit'])
        asst.append_task('Mall', TASKS['Mall'])
        asst.append_task('Award', TASKS['Award'])
        
        del TASKS, PATH
        asst.start()

        while asst.running():
            time.sleep(0)
            
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
