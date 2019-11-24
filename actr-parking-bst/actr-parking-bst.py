#!/usr/bin/env python
#
# # -*- coding: utf-8 -*-
# # @Time : 2019/11/22 11:11
# # @Author : Yulong Sun
# # @Site :
# # @File : actr-parking-bst.py
# # @Software: PyCharm

"""
假定：优秀驾驶员看到速度和不同制动级位就能判断出大概距离
初始条件：初始距离，初始速度
这个程序的思路使让actr看到距离停车标的初始距离和实际到达精度30m，让actr从不同的制动级位的长度下进行选择，不断缩小距离最后达到实际精度
"""

import actr
import random
import  time

actr.load_act_r_model(r"C:\Users\syl\Desktop\ACTR_ATO\actr-parking-bst\actr-parking.lisp")

target = None
current_stick = None
current_line = None
done = False
choice = None
window = None
visible = False

exp_data = [20, 67, 20, 47, 87, 20, 80, 93, 83, 13, 29, 27, 80, 73, 53]
exp_stims = [[15, 250, 55, 125], [10, 155, 22, 101], [14, 200, 37, 112],
             [22, 200, 32, 114], [10, 243, 37, 159], [22, 175, 40, 73],
             [15, 250, 49, 137], [10, 179, 32, 105], [20, 213, 42, 104],
             [14, 237, 51, 116], [12, 149, 30, 72], [14, 237, 51, 121],
             [22, 200, 32, 114], [14, 200, 37, 112], [15, 250, 55, 125]]

no_learn_stims = [[15, 200, 41, 103], [10, 200, 29, 132]]
test_stim = [[40,300,80,30,15,5,30]]



def build_display(a, b, c, d, e, f, goal):
    global window, target, current_stick, done, current_line, choice

    target = goal
    current_stick = 0
    done = False
    choice = None
    current_line = None
    window = actr.open_exp_window("停车对标", visible=visible, width=600, height=400)

    actr.add_button_to_exp_window(window, text="A", x=5, y=23, action=["bst-button-pressed", a, "under"], height=24,width=40)
    actr.add_button_to_exp_window(window, text="B", x=5, y=48, action=["bst-button-pressed", b, "over"], height=24, width=40)
    actr.add_button_to_exp_window(window, text="C", x=5, y=73, action=["bst-button-pressed", c, "under"], height=24,width=40)
    actr.add_button_to_exp_window(window, text="D", x=5, y=98, action=["bst-button-pressed", d, "under"], height=24,width=40)
    actr.add_button_to_exp_window(window, text="E", x=5, y=120, action=["bst-button-pressed", e, "under"], height=24,width=40)
    actr.add_button_to_exp_window(window, text="F", x=5, y=140, action=["bst-button-pressed", f, "under"], height=24, width=40)

    # actr.add_text_to_exp_window(window, text="实际距离： ", x=5, y=123, height=24, width=65)
    actr.add_button_to_exp_window(window, text="Reset", x=5, y=340, action="bst-reset-button-pressed", height=24, width=65)
    actr.add_line_to_exp_window(window, [75, 35], [a + 75, 35], "black")
    actr.add_line_to_exp_window(window, [75, 60], [b + 75, 60], "black")
    actr.add_line_to_exp_window(window, [75, 85], [c + 75, 85], "black")
    actr.add_line_to_exp_window(window, [75, 110], [d + 75, 110], "black")
    actr.add_line_to_exp_window(window, [75, 135], [e + 75, 135], "black")
    actr.add_line_to_exp_window(window, [75, 160], [f + 75, 160], "black")
    actr.add_line_to_exp_window(window, [75, 310], [goal + 75, 310], "green")
    # actr.add_line_to_exp_window(window, [75, 320], [current_stick + 75, 215], "blue")
    actr.add_text_to_exp_window(window, "注意！\nB表示目标距离；模型先注视ABCDEF四条线，之后将目标线与C对比，求其差值，依次比较A,D,E,F,直至出现Done,结束对标。\nA表示四级制动，制动距离较长；"
                                        "\nC表示一级制动，制动距离最长;", x=400, y=310, color='blue', height=200, width=150, font_size=12)



# 对应的按键
def button_pressed(len, dir):
    global choice, current_stick

    if not (choice):
        choice = dir

    if not (done):
        if current_stick > target:
            current_stick -= len
        else:
            current_stick += len

        update_current_line()

# 如果停车超标则重置显示
def reset_display():
    global current_stick

    if not (done):
        current_stick = 0
        update_current_line()
        overparking=actr.add_text_to_exp_window(window,"停车超标！", x=300, y=200, color='red',height=20,width=75,font_size=24)
        time.sleep(1)
        actr.remove_items_from_exp_window(window,overparking)



actr.add_command("bst-button-pressed", button_pressed,
                 "Choice button action for the Building Sticks Task.  Do not call directly")
actr.add_command("bst-reset-button-pressed", reset_display,
                 "Reset button action for the Building Sticks Task.  Do not call directly")


# current_stick指的是当前的ABC三个之一，current_line指的是蓝色的长度
# 如果实际距离等于目标距离，说明对标成功；
# 如果实际距离等于0。移除实际距离
# 如果存在当前距离
def update_current_line():
    global current_line, done

    if current_stick == target:
        done = True
        actr.modify_line_for_exp_window(current_line, [75, 330], [target + 75, 330])
        actr.add_text_to_exp_window(window, "Done", x=5, y=200)
        actr.add_text_to_exp_window(window, "对标成功！", x=300, y=200, color='red', height=20, width=75,font_size=24)
    elif current_stick == 0:
        if current_line:
            actr.remove_items_from_exp_window(window, current_line)
            current_line = None
    elif current_line:
        actr.modify_line_for_exp_window(current_line, [75, 330], [current_stick + 75, 330])
    else:
        current_line = actr.add_line_to_exp_window(window, [75, 330], [current_stick + 75, 330], "blue")


def do_experiment(sticks, human=False):
    build_display(*sticks)

    if human:
        wait_for_human()
    else:
        actr.install_device(window)
        actr.start_hand_at_mouse()
        actr.run(100, visible)

# 等待真人做实验
def wait_for_human():
    while not (done):
        actr.process_events()

    start = actr.get_time(False)
    while (actr.get_time(False) - start) < 1000:
        actr.process_events()

def bst_set(human, vis, stims, learn=True):
    global visible

    result = []

    visible = vis

    for stim in stims:
        if not (learn) and not (human):
            actr.reset()
        do_experiment(stim, human)
        result.append(choice)

    return result
# 测试数据采用的是no_learn_stims，应该修改
def test(n=1, human=False):
        l = len(test_stim)

        result = [0] * l

        if human or (n <= 3):
            v = True
        else:
            v = False

        for i in range(n):

            d = bst_set(human, v, test_stim, False)

            for j in range(l):
                if d[j] == "over":
                    result[j] += 1

        return result


def experiment(n, human=False):
    l = len(test_stim)

    result = [0] * l
    p_values = [["decide-over", 0], ["decide-under", 0], ["force-over", 0], ["force-under", 0]]
    for i in range(n):
        actr.reset()
        d = bst_set(human, vis=True, stims=test_stim)
        for j in range(l):
            if d[j] == "over":
                result[j] += 1

        actr.hide_output()

        # for p in p_values:
        #     p[1] += production_u_value(p[0])

        actr.unhide_output()

    result = list(map(lambda x: 100 * x / n, result))

    if len(result) == len(exp_data):
        actr.correlation(result, exp_data)
        actr.mean_deviation(result, exp_data)

    print()
    print("Trial ", end="")
    for i in range(l):
        print("%-8d" % (i + 1), end="")
    print()

    print("  ", end="")
    for i in range(l):
        print("%8.2f" % result[i], end="")

    print()
    print()

    for p in p_values:
        print("%-12s: %6.4f" % (p[0], p[1] / n))


def production_u_value(prod):
    return actr.spp(prod, ":u")[0][0]


if __name__ == "__main__":
    test(2, human=False)
    # experiment(1, human=False)
