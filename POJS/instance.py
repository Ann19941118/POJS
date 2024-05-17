'''
Description: your project
Author: Liu Zi Li
Date: 2024-04-23 10:49:38
email: zili.liu@hotmail.com
LastEditTime: 2024-05-17 17:21:38
'''
"""
Processing_time：工件各工序对应各机器加工时间矩阵
J：各工件对应的工序数字典
M_num：加工机器数
J_num：工件个数
"""

Processing_time = [
    [[7,7], [35,35], [80]],        
    [[11,11], [35,35], [60]],      
    [[7], [22], [120]],            
    [[11,11], [22,22], [75]],     
    [[11,11,11],[22,22,22], [120]],
    [[11], [35], [120]]            
    ]           

Machines = [[0],[1,2,3,4],[5,6,7,8]]

J_num = len(Processing_time)

# 按工件顺序对应的工序数
J = {i: 3 for i in range(1, J_num+1)}
