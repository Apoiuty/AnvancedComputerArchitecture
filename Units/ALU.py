from .interpreter import *


class alu_unit:
    # 功能单元个数
    load = 2
    mul = 2
    add = 3
    store = 2
    cal_time = {
        'subf': 2,
        'addf': 2,
        'mulf': 10,
        'divf': 40,
        'load': 2,
        'store': 2
    }

    def __init__(self, operation):
        # 自己的运行时钟，为正数时为未运行完成，为-1时表示空闲，为0时表示结果可用
        self.calculate_time = self.cal_time[operation]
        self.vj = 0
        self.vk = 0
        self.fi = 0
        self.op = operation
        self.result = 0
        self.des = 0
        self.cnt = -1
        self.sendto = []
        self.op_set = 0
        self.addr = 0

    def setoprand(self):
        """
        传入汇编指令行并开始计数
        :return:
        """
        # 已经设置了oprand
        self.op_set = 1
        self.cnt = self.calculate_time
        self.des = addr_mode(self.fi)

        if self.op == 'store':
            self.des = (memory, self.addr + self.vk)

        if self.op == 'load':
            self.result = memory[self.vj + self.addr]
        elif self.op == 'store':
            self.result = self.vj
        elif self.op == 'addf':
            self.result = self.vj + self.vk
        elif self.op == 'subf':
            self.result = self.vj - self.vk
        elif self.op == 'divf':
            self.result = self.vj / self.vk
        elif self.op == 'mulf':
            self.result = self.vj * self.vk

        # print(self.op, self.result)

    def get_result(self):
        """
                输出结果，如果未计算完成则返回0
                :return:
                """
        self.cnt -= 1
        if self.cnt != 0 or self.cnt == -1:
            return 0
        else:
            # 返回目的地（寄存器，编号和结果值）
            # 写入其他需要的值的指令

            return self

    def write_back(self):
        if self.op != 'store':
            if regs_table[self.fi] == self:
                regs_table[self.fi] = 0
                self.des[0][self.des[1]] = self.result
        else:
            self.des[0][self.des[1]] = self.result

        # 写入其他单元
        for unit in self.sendto:
            if unit[1] == 0:
                unit[0].vj = self.result
            else:
                unit[0].vk = self.result


load_store = []
