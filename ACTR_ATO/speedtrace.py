"""
@File   : ACTR_ATO
@author : yulosun
@Date   : 10/11/19
@license:
"""

import actr
import time
import math
import numpy as np
import numbers
import matplotlib.pyplot as plt
import SYL_spt2

import datetime

actr.load_act_r_model(r"C:\Users\syl\Desktop\ACTR_ATO\sp_new.lisp")
response = False


t = 0
choice = None
done = False

def button_pressed(len, dir):
    global choice, speed_actual, speed_target
    if not (choice):
        choice = dir
    if not (done):
        if int(speed_actual[0]) > int(speed_target[0]):
            speed_actual[0] = str(int(speed_actual[0]) - int(len))
        elif int(speed_actual[0]) == int(speed_target[0]):
            speed_actual[0] = speed_actual[0]
        else:
            speed_actual[0] = str(int(speed_actual[0]) + int(len))

def button_stop_pressed(dir):
    speed_actual[0] = str(0)

def number_sims(a, b):
    if isinstance(b, numbers.Number) and isinstance(a, numbers.Number):
        return abs(a - b) / -300
    else:
        return False

def compute_difference():
    c = actr.buffer_read('imaginal')
    n = actr.copy_chunk(c)
    actr.mod_chunk(n,'difference',abs(actr.chunk_slot_value(c,'length') - actr.chunk_slot_value(c,'goal-length')))
    return n

def experiment(human=False):
    global response
    response = False
    if human == True:
        while response == False:
            actr.process_events()
    else:
        actr.install_device(window)
        actr.start_hand_at_mouse()
        actr.run(10, True)
    actr.remove_command_monitor("output-key", "sp-key-press")
    actr.remove_command("sp-key-press")
    print(actr.get_time(model_time=True))
    actr.run_n_events(2, real_time=False)
    return response

if __name__ == '__main__':

    # 绘制目标曲线
    targetgroup = []
    # 绘制实际运行曲线
    actualgroup = []
    window = actr.open_exp_window("速度曲线追踪", visible=True, width=600, height=600, x=100, y=100)
    actr.install_device(window)
    actr.add_text_to_exp_window(window, text="当前推荐速度：", x=10, y=60, height=40, width=95, color='black', font_size=22)
    # actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=20, height=40, width=180, color='black', font_size=22)
    actr.add_text_to_exp_window(window, text="当前实际速度：", x=10, y=100, height=40, width=95, color='black', font_size=22)
    actr.add_text_to_exp_window(window, text="距离车站位置：", x=10, y=140, height=40, width=95, color='black', font_size=22)
    actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=180, height=40, width=95, color='black', font_size=22)
    speed_target = [""]
    speed_actual = ["40"]
    timegroup = []


    # actr.add_image_to_exp_window(window, "background", "ref-brain.gif", x=0, y=0, width=390, height=390)
    # actr.add_items_to_exp_window(window,actr.create_image_for_exp_window(window, "brain", "ref-brain.gif", x=10, y=160, width=128,
    #                                                               height=128, action="click-brain-py"))



    start_time = datetime.datetime.now()

    for i in range(2191,2379):
        t += 1
        # t = time.time()
        # speed_target[0] = math.log2(t+1)
        speed_target[0] = SYL_spt2.train_model().target_v(i)
        print("目标速度：", speed_target[0])

        recomed_speed = speed_target[0]  # 推荐速度
        text2 = speed_actual[0]  # 实际速度
        text3 = str(int(recomed_speed) - int(text2))  # 速度差值
        if int(text3) == 0:
            text3 = "0"
        elif int(text3) > 0:
            text3 = "+"
        else:
            text3 = "-"
        text4 = "3"  # 距离目标车站的距离
        text5 = "前方将出现斜坡！"
        x1_target_speed = actr.add_text_to_exp_window(window, str(speed_target), x=200, y=60, color='black', height=50, width=100, font_size=22)
        x2_actual_speed = actr.add_text_to_exp_window(window, text2, x=200, y=100, color='black', height=50, width=100, font_size=22)
        x3_delta_speed = actr.add_text_to_exp_window(window, text3, x=200, y=20, color='black', height=50, width=100, font_size=22)
        x4_delta_distance = actr.add_text_to_exp_window(window, text4, x=200, y=140, color='black', height=50, width=100, font_size=22)
        x5 = actr.add_text_to_exp_window(window, str(int(recomed_speed) - int(text2)), x=200, y=180, color='black', height=50, width=100, font_size=22)
        x6 = actr.add_text_to_exp_window(window, text5, x=10, y=240, color='red', height=50, width=100, font_size=22)
        # actr.start_hand_at_mouse()
        actr.add_command("sp-button-pressed-up-keep-down", button_pressed,"sp press button(up\keep\down) task")
        actr.add_command("sp-number-sims", number_sims, "Similarity hook function for building sticks task.")
        actr.add_command("sp-button-stop-pressed", button_stop_pressed, "sp task output-key monitor")
        actr.add_command("sp-compute-difference", compute_difference,"Imaginal action function to compute the difference between sticks.")

        actr.monitor_command("output-key", "sp-key-press")
        experiment(human=False)
        actr.reset()
        actr.remove_items_from_exp_window(window, x1_target_speed)
        actr.remove_items_from_exp_window(window, x2_actual_speed)
        actr.remove_items_from_exp_window(window, x3_delta_speed)
        actr.remove_items_from_exp_window(window, x4_delta_distance)
        actr.remove_items_from_exp_window(window, x5)
        targetgroup.append(speed_target[0])
        actualgroup.append(speed_actual[0])

        actr.add_button_to_exp_window(window, text="7", x=500, y=60, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="6", x=500, y=80, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="5", x=500, y=100, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="4", x=500, y=120, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="3", x=500, y=140, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="2", x=500, y=160, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="1", x=500, y=180, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="up", x=500, y=200, action=["sp-button-pressed-up-keep-down", 2, "up"], height=20, width=100,color='yellow')
        actr.add_button_to_exp_window(window, text="keep", x=500, y=220, action=["sp-button-pressed-up-keep-down", 0, "keep"], height=20, width=100, color='gray')
        actr.add_button_to_exp_window(window, text="down", x=500, y=240, action=["sp-button-pressed-up-keep-down", 2, "down"], height=20, width=100,color='green')
        actr.add_button_to_exp_window(window, text="-2", x=500, y=260, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="-3", x=500, y=280, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="-4", x=500, y=300, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="-5", x=500, y=320, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="-6", x=500, y=340, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="-7", x=500, y=360, action=["sp-button-pressed", 0.2, "down"],height=20, width=100, color='green')
        actr.add_button_to_exp_window(window, text="EB", x=500, y=380, action=["sp-button-stop-pressed",0.2, "stop"],height=20, width=100,color='red')
        # actr.start_hand_at_mouse()
        timegroup.append(t)
        actr.print_visicon()

    x = np.arange(0, 350)
    l1 = plt.plot(timegroup, targetgroup, 'r--',label='targetspeed')
    l2 = plt.plot(timegroup, actualgroup, 'g--', label='actualspeed')
    plt.plot(timegroup, targetgroup, 'ro-',timegroup, actualgroup, 'g+-')
    plt.title('Speed ​​tracking')
    plt.xlabel('time')
    plt.ylabel('speed value')
    plt.legend()

    end_time = datetime.datetime.now()
    interval = (end_time - start_time).seconds
    print("程序共执行了：",interval)


    my_y_ticks = np.arange(0, 100, 0.3)


    plt.yticks(my_y_ticks)

    plt.show()











