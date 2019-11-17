#!/usr/bin/env python
# encoding: utf-8
"""
@File   : game
@author : wuziheng
@Date   : 3/20/18
@license:
"""
import random
import numpy as np
import matplotlib.pyplot as plt
# from train_model1 import target_v, target_u, train_model

VERSION_NUM = 1
CRASH_LIMIT = 0.3
N_ACTIONS = 5

def train_model(t, v_t, u_t):
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

def utrain_model(t, v_t1, v_t):
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
def curve(t):
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
def target_v(t):
    return sum([curve(i) for i in range(t-10, t+10)])/20

def target_u(t):
    return utrain_model(t,target_v(t+1),target_v(t))

class Game(object):
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

    def __init__(self, v_range=0.1, u_range=5):
        """
        game initial every beginning or after crashed, random choose a start point from [start_point,end_point], set
        initial velocity according to the train_model and needed speed curve(not exactly) with in v_range and u_range
        deviation. reset terminal flag
        游戏初始每个开始或崩溃后，随机选择一个起点[start_point,end_point]，根据train_model和需要的带v_range和u_range偏差速度曲线(不精确的)设置初始速度。重置终止标记
        :param v_range: initial velocity deviation range初速度偏差范围
        :param u_range: initial force deviation range初始力偏差范围
        """
        # 从t时刻随机开始
        # self.t = random.randrange(self.start_point,
        #                           self.end_point)
        self.t = self.start_point
        self.init = self.t
        # 实际速度由模型操作控制给出
        self.v = target_v(self.t) + random.uniform(-1, 1) * v_range
        # 实际牵引力由模型给出，可能有一个牵引级数与牵引力的关系
        self.u = target_u(self.t) + random.uniform(-1, 1) * u_range

        self.d_v = self.v - target_v(self.t)
        self.dd_v = 0
        self.d_u = self.u - target_u(self.t)


        self.reward = 0
        self.terminal = False
        print(self.t, "时刻速度：", self.v, "时刻牵引力：",self.u, "速度差值： ", self.d_v, "牵引力差值： ", self.d_u, "\n",
               " 目标速度：", target_v(self.t), "目标牵引力：", target_u(self.t))
        t_group.append(self.t)
        actual_group.append(self.v)
        target_group.append(target_v(self.t))

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
        self.v = train_model(self.t, self.v, self.u)

        self.t += 1
        self.dd_v = abs(self.v - target_v(self.t)) - abs(self.d_v)
        self.d_v = self.v - target_v(self.t)
        self.d_u = self.u - target_u(self.t)
        print(self.t,"时刻速度：",self.v, "时刻牵引力：",self.u,"速度差值： ",self.d_v, "牵引力差值： ",self.d_u,"\n",
            " 目标速度：", target_v(self.t), "目标牵引力：", target_u(self.t))

        t_group.append(self.t)
        actual_group.append(self.v)
        target_group.append(target_v(self.t))

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

if __name__ == "__main__":


    t_group = []
    actual_group = []
    target_group = []

    game = Game()
    # one-hot code form of input
    du = [[0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0],
          [1, 0, 0, 0, 0]]
    du = np.array(du)

    for i in range(3):
        game.step(d_u=du[i])
    game.draw_target_actual_speed(t_group, target_group, actual_group)


