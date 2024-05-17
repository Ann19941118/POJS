'''
Description: your projectGS_num
Author: Liu Zi Li
Date: 2024-05-15 15:47:53
email: zili.liu@hotmail.com
LastEditTime: 2024-05-16 14:54:58
'''
import random

import numpy as np


class Encode:
    def __init__(self, Pop_size, J, J_num):
        """
        :param Matrix: 机器加工时间矩阵  ?
        :param Pop_size: 种群数量
        :param J: 各工件对应的工序数 {0:4,1:4,...}
        :param J_num: 工件数 6
        """

        self.J = J
        self.J_num = J_num
        self.CHS = []
        self.GS_num = int(0.6 * Pop_size)  # 全局选择初始化
        self.Len_Chromo = J_num

    # 生成初始化矩阵
    def CHS_Matrix(self, C_num):
        return np.zeros([C_num, self.Len_Chromo], dtype=int)

    
    def initial_(self):
        OS = self.CHS_Matrix(self.GS_num)
        OL = [j for j in range(self.J_num)]
        for i in range(self.GS_num):
            
            random.shuffle(OL)
            OS[i] = OL

        return OS
