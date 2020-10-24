"""
寄存器类
"""
from memory import *


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


class PC:
    """
    PC寄存器
    """

    def __init__(self):
        self.esp = 0

    def __getitem__(self, item):
        return self.esp

    def __setitem__(self, key, value):
        self.esp = value


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


class Stack:
    """
    栈
    """

    def __init__(self):
        self.esp = -1
        # 栈顶元素
        self.ebp = -1
        # 栈底
        self.__stack = [0] * 1000

    def push(self, data):
        self.esp += 1
        self.__stack[self.esp] = data

    def pop(self):
        if self.esp != -1:
            self.esp -= 1
            return self.__stack[self.esp + 1]
        else:
            print("Empty stack.")
