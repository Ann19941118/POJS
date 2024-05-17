import numpy as np

from Job import Job
from Machine import Machine_Time_window
    

class Decode:
    def __init__(self, J, CKS, Machines = [[0],[1,2,3,4],[5,6,7,8]]):
        """
        :param J: 各工件对应的工序数字典
        :param Processing_time: 各工件的加工时间矩阵
        :param M_num: 加工机器数
        """
        self.CK = CKS
        self.M_num = sum([len(s) for s in Machines])
        self.op_optional_machine = Machines
        self.Machines = []  # 存储机器类
        self.fitness = 0  # 适应度，即机器最大加工时长（含休息间隔）
        self.Machine_State = np.zeros(self.M_num, dtype=int)  # 在机器上加工的工件是哪个
        self.Jobs = []  # 存储工件类
        for j in range(self.M_num):
            self.Machines.append(Machine_Time_window(j))
        for k, v in J.items():
            self.Jobs.append(Job(k, v))

    def Earliest_Start(self, Job, O_num, Machine, pt, parall_i):
        if O_num==0:        
            last_O_end = 0  # 上道工序结束时间

            Selected_Machine = Machine
            M_window = self.Machines[Selected_Machine].Empty_time_window()  # 当前机器的空格时间
            M_Tstart = M_window[0]
            M_Tend = M_window[1]
            M_Tlen = M_window[2]
            Machine_end_time = self.Machines[Selected_Machine].End_time
            # print('Machine_end_time:', Machine_end_time)
            ealiest_start = max(last_O_end, Machine_end_time)
            if M_Tlen is not None:  # 此处为全插入时窗
                for le_i in range(len(M_Tlen)):
                # 当前空格时间比加工时间大可插入
                    if M_Tlen[le_i] >= pt:
                    # 当前空格开始时间比该工件上一工序结束时间大可插入该空格，以空格开始时间为这一工序开始
                        if M_Tstart[le_i] >= last_O_end:
                            ealiest_start = M_Tstart[le_i] 
                            break
            M_Ealiest = ealiest_start  # 当前工件当前工序的最早开始时间
            End_work_time = M_Ealiest+pt
                
        if O_num==1:
            last_O_ends = self.Jobs[Job].Last_Processing_end_time[O_num-1]
            # last_O_ends： list [last_o_end1,...]
            last_O_end = last_O_ends[parall_i]
            Selected_Machine = Machine
            M_window = self.Machines[Selected_Machine].Empty_time_window()  # 当前机器的空格时间
            M_Tstart = M_window[0]
            M_Tend = M_window[1]
            M_Tlen = M_window[2]
            Machine_end_time = self.Machines[Selected_Machine].End_time

            ealiest_start = max(last_O_end, Machine_end_time)  # 工序的最早开始时间
            if M_Tlen is not None:  # 此处为全插入时窗
                for le_i in range(len(M_Tlen)):
                
                    if M_Tlen[le_i] >= pt: # 当前机器的空格时间窗比提取工序的加工时间大；
                        if M_Tstart[le_i] >= last_O_end: # 且上一工序的结束时间早于空格的开始时间，则最早开始时间更新为空格开始时间
                            ealiest_start = M_Tstart[le_i] 
                            break

                        # 当前空格开始时间比该工件上一工序结束时间小但空格可满足插入该工序，以该工序的上一工序的结束为开始
                        if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= pt:
                            ealiest_start = last_O_end
                            break
                M_Ealiest = ealiest_start  # 当前工件当前工序的最早开始时间
                End_work_time = M_Ealiest + pt  # 当前工件当前工序的结束时间


        if O_num==2:  #如果是扩增工序

            last_O_ends = self.Jobs[Job].Last_Processing_end_time[O_num-1] # 上道工序结束时间，TODO多个提取工序的结束时间最大值
            # last_O_ends： list [last_o_end1,...]
            last_O_end = max(last_O_ends)
            Selected_Machine = Machine
            M_window = self.Machines[Selected_Machine].Empty_time_window()  # 当前机器的空格时间
            M_Tstart = M_window[0]
            M_Tend = M_window[1]
            M_Tlen = M_window[2]
            Machine_end_time = self.Machines[Selected_Machine].End_time

            ealiest_start = max(last_O_end+7, Machine_end_time)
            if M_Tlen is not None:  # 此处为全插入时窗
                for le_i in range(len(M_Tlen)):
                # 当前空格时间比加工时间大7min（封膜）可插入
                    if M_Tlen[le_i] >= pt:
                    # 当前空格开始时间比该工件上一工序结束时间大可插入该空格，以空格开始时间为这一工序开始
                        if M_Tstart[le_i] >= last_O_end+7:
                            ealiest_start = M_Tstart[le_i] 
                            break
                        # 当前空格开始时间比该工件上一工序结束时间小但空格可满足插入该工序，以该工序的上一工序的结束为开始
                        if M_Tstart[le_i] < last_O_end+7 and M_Tend[le_i] - last_O_end >= pt+7:
                            ealiest_start = last_O_end+7
                            break
            M_Ealiest = ealiest_start  # 当前工件当前工序的最早开始时间
            End_work_time = M_Ealiest+pt
  
        return M_Ealiest, Selected_Machine, pt, O_num, last_O_end, End_work_time

    def decode(self,CHS):
        # 根据生成的试剂排产顺序，解码成工件顺序和机器运行时间窗口，并返回机器最大运行时长
        order = CHS
        for j in order:
            j_ops = self.CK[j] # 第几个工件

            for op in range(3): #只有三个工序 分杯、提取、PCR
                optional_machine = self.op_optional_machine[op] # 根据工序选择功能匹配的机器
                op_nums = j_ops[op]  # 每个工序可能会有多个并行工序[7, 7], [35, 35]等
                if op==0:# 如果是分杯工序
                    Machine = 0  # 只有一台设备 0
                    pt = sum(op_nums)
                    avarage_ = op_nums[0]
                    Para = self.Earliest_Start(j, 0, Machine, pt, 0)  # 根据该设备确定分杯工序最早可加工时间
                    op_starts = [Para[0]+i*avarage_ for i in range(len(op_nums))]
                    op_ends = [Para[0]+(i+1)*avarage_ for i in range(len(op_nums))]
                    Machines = [0 for i in range(len(op_nums))]
                    
                    self.Jobs[j]._Input(op_starts,  # 分杯工序的开始时间
                                        op_ends,  #  分杯工序的结束时间
                                        Machines)     # 分杯工序的使用机器
                    if Para[5] > self.fitness:
                        self.fitness = Para[5]
                    self.Machines[Machine]._Input(j, 
                                                  op_starts[0],   # 分杯工序的开始时间 
                                                  pt, # 分杯工序的持续时间
                                                  0)      # O_num
                elif op==1: # 提取有四台设备可选，哪台可上料时间早就用哪个，有多台可选设备时随机选
                    # 同时提取有多个可并行工序，
                    O_Earliest = []
                    O_end_time = []
                    Mach_selects = []

                    for k in range(len(op_nums)): # 提取1，提取2....
                        
                        para_keep = None
                        input_early_t = None
                        Mach_select = None
                        for Mach in optional_machine:
                            # print('mach:',Mach)
                            Para = self.Earliest_Start(j, 1, Mach, op_nums[k], k )
                            if input_early_t:
                                if Para[0]<input_early_t: # 可插入时间早
                                    input_early_t = Para[0]
                                    para_keep = Para
                                    Mach_select = Mach
                                else:
                                    continue
                            else:
                                input_early_t = Para[0]
                                para_keep = Para
                                Mach_select = Mach
                        self.Machines[Mach_select]._Input(j, para_keep[0], para_keep[2], para_keep[3])
                        O_Earliest.append(input_early_t)
                        O_end_time.append(para_keep[5])
                        Mach_selects.append(Mach_select)
                    # 等可并行的工序都完成后，更新该工件的工序
                    self.Jobs[j]._Input(O_Earliest, O_end_time, Mach_selects)  # 工件完成该工序
                    # 最后一个并行工序的完成时间如果大于现有的机器最大加工时长，则更新（适应度）
                    if para_keep[5] > self.fitness:
                        self.fitness = para_keep[5]   

                elif op==2: # PCR有多台提取设备，哪台可上料就用哪台，有多台可选设备时随机选
                    para_keep = None
                    input_early_t = None
                    Mach_select = None
                    for Mach in optional_machine:
                        Para = self.Earliest_Start(j, 2, Mach, op_nums[0], 0)
                        if input_early_t:
                            if Para[0]<input_early_t: # 最早可加工时间
                                input_early_t = Para[0]
                                para_keep = Para
                                Mach_select = Mach
                            else:
                                continue
                        else:
                            input_early_t = Para[0]
                            para_keep = Para
                            Mach_select = Mach
                    self.Machines[Mach_select]._Input(j, para_keep[0], para_keep[2], para_keep[3])
                    # 等可并行的工序都完成后，更新该工件的工序
                    self.Jobs[j]._Input([para_keep[0]], [para_keep[5]], [para_keep[1]])  # 工件完成该工序
                    # 最后一个并行工序的完成时间如果大于现有的机器最大加工时长，则更新（适应度）
                    if para_keep[5]> self.fitness:
                        self.fitness = para_keep[5]

        return self.fitness # 返回适应度,适应度即最大完工时长






