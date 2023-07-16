# encoding=utf-8
'''
Filename :小鸟五小时计算.py
Datatime :2022/12/02
Author :KJH-x
'''
from time import strftime
from time import gmtime
from datetime import datetime, timedelta
# print(datetime.strftime("",datetime.localtime()))


def finishTime(timeString1: str) -> list:
    in_time = []
    if timeString1.find(":") == -1:
        if len(timeString1) == 5:
            in_time.append(timeString1[0:1])
            in_time.append(timeString1[1:3])
            in_time.append(timeString1[3:5])
        elif len(timeString1) == 6:
            in_time.append(timeString1[0:2])
            in_time.append(timeString1[2:4])
            in_time.append(timeString1[4:6])
    return in_time

msg="\
    >>　　　　倒计时参考此时间　　　　<<\n\
    >>设短一些（如十分钟）留足时间换人<<\n\
"

date_suffix = datetime.strftime(datetime.now(), "%Y-%m-%d ")
"""'2022-11-30'"""
# time1 = "9:12:34"
# time2 = "4:14:37"

print("\n作者KJH-x，保留解释权利，脚本给出时间仅供测试，不承担后果\n")
print("\n  [注意] 输入时间时可以不输入冒号 \n")
time1 = ":".join(finishTime(input("[输入] 输入其中一个倒计时: ")))
print(f"[验算] 记录到的第一个时间: {time1}")

time2 = ":".join(finishTime(input("\n[输入] 输入另一个倒计时: ")))
print(f"[验算] 记录到的第二个时间: {time2}\n")


five_hours = datetime.strptime(date_suffix+"5:00:00", "%Y-%m-%d %H:%M:%S")
zero_o_clock = datetime.strptime(date_suffix+"0:00:00", "%Y-%m-%d %H:%M:%S")
skill_time_1 = datetime.strptime(date_suffix+time1, "%Y-%m-%d %H:%M:%S")
skill_time_2 = datetime.strptime(date_suffix+time2, "%Y-%m-%d %H:%M:%S")


if (skill_time_1-skill_time_2).total_seconds() >= 0:
    slower_duration = (skill_time_1-zero_o_clock).total_seconds()
    faster_duration = (skill_time_2-zero_o_clock).total_seconds()
else:
    slower_duration = (skill_time_2-zero_o_clock).total_seconds()
    faster_duration = (skill_time_1-zero_o_clock).total_seconds()

targettime = (five_hours-zero_o_clock).total_seconds()

acc_duration_slow = slower_duration - targettime
acc_duration_fast = (faster_duration / slower_duration) * acc_duration_slow
acc_duration_diff = acc_duration_slow-acc_duration_fast

a = strftime("%H:%M:%S", gmtime(targettime))
b = strftime("%H:%M:%S", gmtime(slower_duration))
c = strftime("%H:%M:%S", gmtime(acc_duration_slow))
d = strftime("%H:%M:%S", gmtime(faster_duration))
e = strftime("%H:%M:%S", gmtime(acc_duration_fast))
r = faster_duration / slower_duration

print(f"[验算] 需要加速时长: {b} - {a} = {c}")
print(f"[验算] 技能加速比例: {d} / {b} = {r:.3f}\n")
del a,b,c,d,e,r

print(58*"-")
print(f"[结果]:{strftime('%H:%M:%S', gmtime(acc_duration_fast))}")
print(msg)
print(
    f"[提示] 用此加速策略将为你节省 {strftime('%H:%M:%S', gmtime(acc_duration_diff))}")
print(58*"-")
input("回车键退出")
