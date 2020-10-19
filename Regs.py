"""
寄存器类
"""
import numpy as np


def check_reg(s):
    """
    检查字符串s是否合法
    :param s: r1,r2,...
    :return: 合法返回寄存器号，不合法返回-1
    """
    if isinstance(s, str):
        num = int(s[1:])
    elif isinstance(s, int):
        num = s
    else:
        return -1

    if 0 < num < 33:
        return num
    else:
        return -1


class Reg:
    """
    寄存器类
    """

    def __init__(self):
        self.__regs = np.zeros((32, 1), dtype=np.uint32)

    def __getitem__(self, item):
        reg_num = check_reg(item)
        if reg_num != -1:
            return self.__regs[reg_num][0]
        else:
            print("Access nonexistent reg.\n")
            raise Exception

    def __setitem__(self, key, value):
        reg_num = check_reg(key)
        if reg_num != -1:
            self.__regs[reg_num][0] = value
        else:
            print("Access nonexistent reg.\n")
            raise Exception


# 程序计数器
PC = 0
# 创建寄存器对象
regs = Reg()
