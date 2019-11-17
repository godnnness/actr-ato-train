#!/usr/bin/env python
# encoding: utf-8
"""
@File   : game
@author : yulongsun
@Date   : 3/20/18
@license:
"""
import actr
import time
import math
import numbers
import random
import numpy as np
import matplotlib.pyplot as plt
import time
# from train_model1 import target_v, target_u, train_model

VERSION_NUM = 1
CRASH_LIMIT = 0.3
N_ACTIONS = 5
done = False
# train model绘制速度曲线图用
t_group = []
actual_group = []
target_group = []
targetgroup = []
# act-r 绘制实际运行曲线
timegroup = []
actualgroup = []
speed_target = [""]
speed_actual = ["1"] #初始加速度

class train_model(object):

    def train_model1(self, t, v_t, u_t):
        """
        描述下一个采样时刻和速度以及牵引力的关系，也即动态系统描述
        fitting curve by Train csv data, describe the relationship between the next sample point time with this point
        velocity and traction force. this is called dynamic system description
        :param t: Train sample time point
        :param v_t: t sample point velocity
        :param u_t: t sample point traction force
        :return: t+1 sample point velocity
        """
        if t < 500:
            v_t1 = -0.0002 * (v_t ** 2) + 1.0005 * v_t + 0.0054 * u_t - 0.0035
        elif t < 1000:
            v_t1 = -0.00007 * (v_t ** 2) + 1.0007 * v_t + 0.0050 * u_t - 0.0026
        elif t < 1500:
            v_t1 = 0.00006 * (v_t ** 2) + 0.9987 * v_t + 0.0061 * u_t - 0.0030
        elif t < 2000:
            v_t1 = 0.0002 * (v_t ** 2) + 0.9987 * v_t + 0.0066 * u_t - 0.0041
        else:
            v_t1 = 0.0004 * (v_t ** 2) + 0.9977 * v_t + 0.0061 * u_t - 0.0030
        return v_t1

    def utrain_model(self, t, v_t1, v_t):
        """
        :param t: Train sample time point
        :param v_t1: t+1 sample point velocity
        :param v_t: t sample point velocity
        :return: need traction force according to the Train model
        """
        if t < 500:
            u_t = (v_t1 + 0.0002 * (v_t ** 2) - 1.0005 * v_t + 0.0035) / 0.0054
        elif t < 1000:
            u_t = (-0.00007 * (v_t ** 2) + 1.0007 * v_t - 0.0026 - v_t1) / (- 0.0050)
        elif t < 1500:
            u_t = (0.00006 * (v_t ** 2) + 0.9987 * v_t - 0.0030 - v_t1) / (-0.0061)
        elif t < 2000:
            u_t = (0.0002 * (v_t ** 2) + 0.9987 * v_t - 0.0041 - v_t1) / (-0.0066)
        else:
            u_t = (0.0004 * (v_t ** 2) + 0.9977 * v_t - 0.0030 - v_t1) / (-0.0061)
        return u_t

    # 列车的目标曲线
    def curve(self, t):
        """
        target curve for the Train during the sample fragment
        :param t: time point
        :return: target velocity at t point
        """
        if 100 > t >= 0:
            velocity = (0.8 * (t / 20) ** 2)
        elif 200 > t >= 100:
            velocity = 40 - 0.8 * (t / 20 - 10) ** 2
        elif 400 > t >= 200:
            velocity = 40
        elif 500 > t >= 400:
            velocity = 0.6 * (t / 20 - 20) ** 2 + 40
        elif 600 > t >= 500:
            velocity = 70 - 0.5 * (t / 20 - 30) ** 2
        elif 1800 > t >= 600:
            velocity = 70
        elif 1900 > t >= 1800:
            velocity = 70 - 0.6 * (t / 20 - 90) ** 2
        elif 2000 > t >= 1900:
            velocity = 40 + 0.6 * (t / 20 - 100) ** 2
        elif 2200 > t >= 2000:
            velocity = 40
        elif 2300 > t >= 2200:
            velocity = 40 - 0.8 * (t / 20 - 110) ** 2
        elif 2400 > t >= 2300:
            velocity = 0.8 * (t / 20 - 120) ** 2
        else:
            velocity = 0
        return velocity

    # t时刻左右10的区间内所有速度的平均值
    def target_v(self, t):
        return sum([self.curve(i) for i in range(t-10, t+10)])/20

    def target_u(self,t):
        return self.utrain_model(t, self.target_v(t+1), self.target_v(t))

    # def run_experiment(self, start_point=100, end_point = 10000, time=200, verbose=True, visible=True, trace=True, params=[]):
    #     """Runs an experiment"""
    #     actr.reset()
    #     # current directory
    #     actr.load_act_r_model(r"C:\Users\syl\Desktop\ACTR_ATO\sp_new.lisp")
    #     window = actr.open_exp_window("* Speed trace *", width=800, height=600, visible=visible)
    #     actr.install_device(window)
    #
    #     actr.add_text_to_exp_window(window, text="当前推荐速度：", x=10, y=60, height=40, width=95, color='black', font_size=22)
    #     # actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=20, height=40, width=180, color='black', font_size=22)
    #     actr.add_text_to_exp_window(window, text="当前实际速度：", x=10, y=100, height=40, width=95, color='black', font_size=22)
    #     actr.add_text_to_exp_window(window, text="距离车站位置：", x=10, y=140, height=40, width=95, color='black', font_size=22)
    #     actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=180, height=40, width=95, color='black', font_size=22)
    #     actr.add_button_to_exp_window(window, text="7", x=500, y=60, action=["sp-button-pressed", 0.2, "up"], height=20,width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="6", x=500, y=80, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="5", x=500, y=100, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="4", x=500, y=120, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="3", x=500, y=140, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="2", x=500, y=160, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="1", x=500, y=180, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
    #     actr.add_button_to_exp_window(window, text="up", x=500, y=200, action=["sp-button-pressed-up-keep-down", 2, "up"], height=20, width=100,color='yellow')
    #     actr.add_button_to_exp_window(window, text="keep", x=500, y=220, action=["sp-button-pressed-up-keep-down", 0, "keep"], height=20, width=100, color='gray')
    #     actr.add_button_to_exp_window(window, text="down", x=500, y=240, action=["sp-button-pressed-up-keep-down", 2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-2", x=500, y=260, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-3", x=500, y=280, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-4", x=500, y=300, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-5", x=500, y=320, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-6", x=500, y=340, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="-7", x=500, y=360, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
    #     actr.add_button_to_exp_window(window, text="EB", x=500, y=380, action=["sp-button-stop-pressed", 0.2, "stop"], height=20, width=100, color='red')
    #
    #
    #     for d in range(start_point, end_point):
    #         target_speed = train_model().target_v(d)
    #         actual_speed = 10
    #         delta_speed = actual_speed - target_speed
    #
    #         print(d, str(int(target_speed)))
    #         mubiaosudu = actr.add_text_to_exp_window(window, str(int(target_speed)), x=200, y=60,height=40, width=95, color='red', font_size=22)
    #         shijisudu = actr.add_text_to_exp_window(window, str(int(actual_speed)), x=200, y=100, height=40, width=95,color='red', font_size=22)
    #         deltasudu = actr.add_text_to_exp_window(window, str(int(delta_speed)), x=200, y=20, height=40, width=95,color='red', font_size=22)
    #
    #         actr.remove_items_from_exp_window(window, mubiaosudu)
    #         actr.remove_items_from_exp_window(window, shijisudu)
    #         actr.remove_items_from_exp_window(window, deltasudu)


class Game(train_model):
    """
    game render for Train_model: to transform train sample point state to a 2D picture.
    @ start_point: train_model start point
    @ end_point: train_model last point
    @ input_shape: width and height of render output
    @ actions: input control state list (fuse control model)
    @ pixel_t: reder parameter, time point interval per pixel
    @ pixel_v: render parameter, velocity interval per pixel
    """
    # 设置起始时刻start_point和终止时刻end_point
    start_point = 500
    end_point = 600
    input_shape = [80, 80]
    actions = [-10, -5, 0, 5, 10]
    # actions = [1,2,3,4,5,6,7,0,-1,-2,-3,-4,-5,-6,-7],分别表示七级牵引七级制动以及紧急制动
    pixel_t = 0.05
    pixel_v = 0.05

    def __init__(self, v_range=0.1, u_range=5,setup=False):
        """
        game initial every beginning or after crashed, random choose a start point from [start_point,end_point], set
        initial velocity according to the train_model and needed speed curve(not exactly) with in v_range and u_range
        deviation. reset terminal flag
        游戏初始每个开始或崩溃后，随机选择一个起点[start_point,end_point]，根据train_model和需要的带v_range和u_range偏差速度曲线(不精确的)设置初始速度。重置终止标记
        :param v_range: initial velocity deviation range初速度偏差范围
        :param u_range: initial force deviation range初始力偏差范围
        """
        if setup:
            self.setup()
        # 从t时刻随机开始
        # self.t = random.randrange(self.start_point,
        #                           self.end_point)
        self.t = self.start_point
        self.init = self.t
        # 实际速度由模型操作控制给出
        self.v = self.target_v(self.t) + random.uniform(-1, 1) * v_range
        # 实际牵引力由模型给出，可能有一个牵引级数与牵引力的关系
        self.u = self.target_u(self.t) + random.uniform(-1, 1) * u_range

        self.d_v = self.v - self.target_v(self.t)
        self.dd_v = 0
        self.d_u = self.u - self.target_u(self.t)


        self.reward = 0
        self.terminal = False
        print(self.t, "时刻速度：", self.v, "时刻牵引力：",self.u, "速度差值： ", self.d_v, "牵引力差值： ", self.d_u, "\n",
               " 目标速度：", self.target_v(self.t), "目标牵引力：", self.target_u(self.t))
        t_group.append(self.t)
        actual_group.append(self.v)
        target_group.append(self.target_v(self.t))

    def setup(self, win=None):
        self.window = win
        self.update_window()
        # self.current_trial = Game(self.stimuli[self.index])
        actr.schedule_event_relative(1, "stroop-next")

    def update_window(self):
        print("更新窗口")

    def next(self):
        print("下一个速度变化值、牵引力变化值、距离变化值")

    def accept_response(self):
        print("接受响应")

    def step(self, d_u):
        """
        simulation of train control, to transform train_state from t to t+1 according the train_model with input delta_u
        模拟列车控制，根据输入delta_u的train_model将train_state从t变换为t+1
        also get a reward of this step according to our designed game reward system
        根据我们设计的游戏奖励系统，还可以获得这一步的奖励
        :param d_u: one-hot code form delta_u(delta traction force)
        :return: next sample time point train state(image), this step reward, terminal or not
        """

        d_u = np.sum(d_u * self.actions)
        self.u += d_u
        print(d_u, "转换后的u=u+d_u: ",self.u)

        " calculate next state velocity according to train_model with changed u(force) and now velocity"
        # 根据改变u(力)和现在的速度的train_model计算下一个状态速度
        self.v = self.train_model1(self.t, self.v, self.u)

        self.t += 1
        self.dd_v = abs(self.v - self.target_v(self.t)) - abs(self.d_v)
        self.d_v = self.v - self.target_v(self.t)
        self.d_u = self.u - self.target_u(self.t)
        print(self.t,"时刻速度：",self.v, "时刻牵引力：",self.u,"速度差值： ",self.d_v, "牵引力差值： ",self.d_u,"\n",
            " 目标速度：", self.target_v(self.t), "目标牵引力：", self.target_u(self.t))

        t_group.append(self.t)
        actual_group.append(self.v)
        target_group.append(self.target_v(self.t))

        # , 如果速度差值大于0.3CRASH_LIMIT或者时刻t达到终止时刻end_point就终止，有一个发生就终止
        self.terminal = abs(self.d_v) > CRASH_LIMIT or self.t >= self.end_point

        return self.terminal

    def draw_target_actual_speed(self, t_group, target_group, actual_group):
        x = np.arange(0, 350)
        l1 = plt.plot(t_group, target_group, 'r--', label='targetspeed')
        l2 = plt.plot(t_group, actual_group, 'g--', label='actualspeed')
        plt.plot(t_group, target_group, 'ro-', t_group, actual_group, 'g+-')
        plt.title('Speed ​​tracking')
        plt.xlabel('time')
        plt.ylabel('speed value')
        plt.legend()
        plt.show()



def run_experiment(start_point, end_point, verbose=True, visible=True, trace=True):
        """Runs an experiment"""
        actr.reset()
        # current directory
        actr.load_act_r_model(r"C:\Users\syl\Desktop\ACTR_ATO\sp_new_2.0.lisp")
        window = actr.open_exp_window("* Speed trace *", width=800, height=600, visible=visible)
        actr.install_device(window)


        # actr.add_text_to_exp_window(window, text="当前推荐速度：", x=10, y=60, height=40, width=95, color='black', font_size=22)
        # # actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=20, height=40, width=180, color='black', font_size=22)
        # actr.add_text_to_exp_window(window, text="当前实际速度：", x=10, y=100, height=40, width=95, color='black', font_size=22)
        # actr.add_text_to_exp_window(window, text="距离车站位置：", x=10, y=140, height=40, width=95, color='black', font_size=22)
        # actr.add_text_to_exp_window(window, text="当前速度差值：", x=10, y=180, height=40, width=95, color='black', font_size=22)

        # actr.add_button_to_exp_window(window, text="7", x=500, y=80, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        # actr.add_button_to_exp_window(window, text="6", x=500, y=100, action=["sp-button-pressed", 0.2, "up"],height=20, width=100, color='yellow')
        # actr.add_button_to_exp_window(window, text="5", x=500, y=120, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        # actr.add_button_to_exp_window(window, text="4", x=500, y=140, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        # actr.add_button_to_exp_window(window, text="3", x=500, y=160, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        # actr.add_button_to_exp_window(window, text="2", x=500, y=180, action=["sp-button-pressed", 0.2, "up"], height=20, width=100, color='yellow')
        actr.add_button_to_exp_window(window, text="up", x=500, y=200, action=["sp-button-pressed-up-keep-down", 2, "up"], height=20, width=100,color='yellow')
        actr.add_button_to_exp_window(window, text="keep", x=500, y=220, action=["sp-button-pressed-up-keep-down", 0, "keep"], height=20, width=100, color='gray')
        actr.add_button_to_exp_window(window, text="down", x=500, y=240, action=["sp-button-pressed-up-keep-down", 2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-2", x=500, y=260, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-3", x=500, y=280, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-4", x=500, y=300, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-5", x=500, y=320, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-6", x=500, y=340, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="-7", x=500, y=360, action=["sp-button-pressed", 0.2, "down"], height=20, width=100, color='green')
        # actr.add_button_to_exp_window(window, text="EB", x=500, y=380, action=["sp-button-stop-pressed", 0.2, "stop"], height=20, width=100, color='red')
        actr.add_command("sp-button-pressed-up-keep-down", button_pressed, "sp press button(up\keep\down) task")
        actr.start_hand_at_mouse()



        for i in range(start_point, end_point):

            target_speed = train_model().target_v(i)
            actual_speed = 10
            delta_speed = actual_speed - target_speed
            t_group.append(i)
            target_group.append(target_speed)
            actual_group.append(actual_speed)
            if delta_speed > 0:
                delta_speed_show = "+"
            elif delta_speed < 0:
                delta_speed_show = "-"
            else:
                delta_speed_show = "0"


            print(i, str(int(target_speed)))
            deltasudu = actr.add_text_to_exp_window(window, delta_speed_show, x=550, y=180, height=40, width=95,color='red', font_size=22)
            # mubiaosudu = actr.add_text_to_exp_window(window, str(int(target_speed)), x=200, y=60,height=40, width=95, color='red', font_size=22)
            # shijisudu = actr.add_text_to_exp_window(window, str(int(actual_speed)), x=200, y=100, height=40, width=95,color='red', font_size=22)

            actr.run(100, True)
            actr.print_visicon()
            print("****************************end cmd actr.print_visicon()**********************************")
            actr.all_productions()
            print("****************************end cmd actr.all_productions()**********************************")
            actr.clear_buffer("visual")
            actr.act_r_output(actr.dm())
            actr.buffer_read("manual")
            print("****************************end cmd actr.buffer_read(manual)**********************************")



            # actr.remove_items_from_exp_window(window, mubiaosudu)
            # actr.remove_items_from_exp_window(window, shijisudu)
            actr.remove_items_from_exp_window(window, deltasudu)


        Game().draw_target_actual_speed(t_group, target_group, actual_group)
        actr.remove_command_monitor("output-key", "sp-key-press")


def button_pressed(len, dir):
    global target_speed, actual_speed
    if int(actual_speed) > int(target_speed):
        actual_speed = str(int(actual_speed) - int(len))
    elif int(actual_speed) == int(target_speed):
        actual_speed = actual_speed
    else:
        actual_speed = str(int(actual_speed) + int(len))


if __name__ == "__main__":

    run_experiment(start_point=2191, end_point=2379, verbose=True, visible=True, trace=True)









    game = Game()
    # one-hot code form of input
    du = [[0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0],
          [1, 0, 0, 0, 0]]
    du = np.array(du)

    for i in range(3):
        game.step(d_u=du[i])
    game.draw_target_actual_speed(t_group, target_group, actual_group)


