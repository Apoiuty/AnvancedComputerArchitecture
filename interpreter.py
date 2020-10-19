from Regs import *
from memory import *


def load(reg, addr):
    """
    读操作
    :param reg: 'r1'寄存器字符
    :param addr: 地址
    :return:
    """
    addr = addr_mode(addr)
    regs[reg] = memory[addr]


def store(reg, addr):
    """
    读操作
    :param reg: 'r1'寄存器字符
    :param addr: 地址
    :return:
    """
    addr = addr_mode(addr)
    memory[addr] = regs[reg]


def add(reg1, reg2, reg3):
    """
    reg1=reg2+reg3
    :param reg1:
    :param reg2:
    :param reg3:
    :return:
    """
    regs[reg1] = regs[reg2] + regs[reg3]


JUMP_TABLE = {
    'Load': load,
    'Add': add,
    'Store': store
}


def assembly_interpreter(line):
    """
    汇编语言解释器
    :param line: 一行汇编语言字符串
    :return: 包含操作码和操作数的列表
    """
    line = line.replace(',', ' ').replace('\n', ' ')
    return line.split()


def execute_cmd(cmd):
    """执行指令"""
    JUMP_TABLE[cmd[0]](*cmd[1:])
