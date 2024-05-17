'''
Description: your project
Author: Liu Zi Li
Date: 2023-10-10 13:21:57
email: zili.liu@hotmail.com
LastEditTime: 2024-05-17 17:23:25
'''
import random

import matplotlib.pyplot as plt
import numpy as np

from Decode import Decode
from Encode import Encode
from GA import GA
from instance import *


# 绘制甘特图
def Gantt(Machines, fitness):
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin','red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 
         'purple', 'pink', 'Thistle', 'Magenta', 'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 
         'goldenrod', 'mediumslateblue','navajowhite', 'navy', 'sandybrown', 'moccasin']
    plt.figure(figsize=(20,16))
    for i in range(len(Machines)):
        Machine = Machines[i]
        Start_time = Machine.O_start
        End_time = Machine.O_end
        for i_1 in range(len(End_time)):
            plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1],
                     color=M[Machine.assigned_task[i_1][0] - 1], edgecolor='black')
            plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1]) / 2 - 0.5, y=i-0.2,
                     s=Machine.assigned_task[i_1][0])
    plt.yticks(np.arange(len(Machines) + 1), np.arange(1, len(Machines) + 2))
    plt.title('best_schedule_result_%s'%fitness)
    plt.ylabel('Machines')
    plt.xlabel('Time(min)')
    plt.savefig('schedule_result.png')
    plt.show()


if __name__ == '__main__':
    import time
    time_start = time.time()
    Optimal_fit = 999  # 最佳适应度（初始化）
    Optimal_CHS = 0  # 最佳适应度对应的基因个体（初始化）
    g = GA()
    e = Encode(g.Pop_size, J, J_num)
    C = e.initial_()  # 根据生成初始解
    # C s
    Best_fit = []  # 记录适应度在迭代过程中的变化，便于绘图
    for i in range(g.Max_Itertions): 
        print("iter_{} start!".format(i))
        Fit = g.fitness(C, J, Processing_time, Machines) # [time1,time2,time3,.....] 从多个初始解中找到时间花费最小的解
        Best = C[Fit.index(min(Fit))]
        best_fitness = min(Fit)
        if best_fitness < Optimal_fit:
            Optimal_fit = best_fitness
            Optimal_CHS = Best
            d = Decode(J,Processing_time, Machines)

            Best_fit.append(Optimal_fit)
            print('best_fitness', best_fitness)
            Fit.append(d.decode(Optimal_CHS)) # 解码最优的解，更新系统的工件加工进度和机器时间窗
                         
        else:
            Best_fit.append(Optimal_fit)
        for j in range(len(C)):
            Cafter = []
            if random.random() < g.Pm:
                N_i = random.choice(np.arange(len(C)))
                Cafter.append(C[j]) # 原解
                cross = C[N_i]
                variences = g.order_varience(C[j],cross)
              
                Cafter.append(variences[0]) # 变异后产生的新解1
                Cafter.append(variences[1]) # 变异后产生的新解2

            if Cafter != []:# 对比结果，保留花费时间最小的
                Fit = g.fitness(Cafter, J, Processing_time, Machines)
                C[j] = Cafter[Fit.index(min(Fit))]
    print(time.time()-time_start)
    Gantt(d.Machines,min(Best_fit))
    