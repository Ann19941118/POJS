'''
Description: your project
Author: Liu Zi Li
Date: 2023-10-10 13:21:57
email: zili.liu@hotmail.com
LastEditTime: 2024-05-17 17:31:40
'''
import itertools
import random

import numpy as np

from Decode import Decode
from instance import *


class GA():
    def __init__(self):
        self.Pop_size = 100  # 种群数量
        self.Pm = 0.5  # 交叉概率
        self.Max_Itertions = 50  # 最大迭代次数

    # 适应度
    def fitness(self, CHS, J, Processing_time, Machines):
        Fit = []
        for i in range(len(CHS)):
            d = Decode(J, Processing_time, Machines)

            Fit.append(d.decode(CHS[i]))
            # break
        return Fit


    # 订单交叉嘛
    def order_varience(self, CHS1, CHS2):
        """
        :param CHS: 工件选择部分的基因1
        :param CHS2: 工件选择部分的基因2
        :return: 变异的工件选择部分的基因
        """
        # print('T0:',T0)
        random.shuffle(CHS1)
        random.shuffle(CHS2)
        return CHS1, CHS2





