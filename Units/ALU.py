from .interpreter import *


class alu_unit():
    def __init__(self, cal_time):
        # 自己的运行时钟，为正数时为未运行完成，为-1时表示空闲，为0时表示结果可用
        self.cnt = -1
        self.calculate_time = cal_time
        self.result = 0
        self.des = 0

    def setoprand(self, cmd):
        """
        传入汇编指令行并开始计数
        :param cmd: 汇编指令行
        :return:
        """
        self.cnt = self.calculate_time
        cmd = assembly_interpreter(cmd)
        op = cmd[0]
        self.des = addr_mode(cmd[1])
        s1 = addr_mode(cmd[2])
        if op != 'mv':
            s2 = addr_mode(cmd[3])

        if op == 'mv':
            self.result = s1[0][s1[1]]
        elif op == 'addf':
            self.result = s1[0][s1[1]] + s2[0][s2[1]]
        elif op == 'subf':
            self.result = s1[0][s1[1]] - s2[0][s2[1]]
        elif op == 'divf':
            self.result = s1[0][s1[1]] / s2[0][s2[1]]
        elif op == 'mulf':
            self.result = s1[0][s1[1]] * s2[0][s2[1]]

    def get_result(self):
        """
                输出结果，如果未计算完成则返回0
                :return:
                """
        if self.cnt != 0:
            self.cnt -= 1
            return 0
        else:
            # 返回目的地（寄存器，编号和结果值）
            return (self.des, self.result)

    def set_busy(self):
        self.result = -1


integer_unit = alu_unit(1)
add_unit = alu_unit(2)
mul1_unit = alu_unit(10)
mul2_unit = alu_unit(10)
div_unit = alu_unit(60)

# 所有的运算单元，通过操作索引
unit_table = {'mv': integer_unit, 'addf': add_unit, 'mul1': mul1_unit, 'mul2': mul2_unit, 'divf': div_unit}
