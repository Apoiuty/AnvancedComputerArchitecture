"""
寄存器类
"""
import numpy as np
from memory import Word


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

    if 0 <= num < 32:
        return num
    else:
        return -1


class Reg:
    """
    寄存器类
    """

    def __init__(self):
        self.__regs = [Word() for i in range(32)]
        # 初始化寄存器
        for i in range(32):
            self.__regs[i][0] = 0

    def __getitem__(self, item):
        reg_num = check_reg(item)
        if reg_num != -1:
            return self.__regs[reg_num][0]
        else:
            print("Access nonexistent reg.")
            raise Exception

    def __setitem__(self, key, value):
        reg_num = check_reg(key)
        if reg_num != -1:
            self.__regs[reg_num][0] = value
        else:
            print("Access nonexistent reg.")
            raise Exception


# 程序计数器
PC = 0
# 创建寄存器对象
regs = Reg()
