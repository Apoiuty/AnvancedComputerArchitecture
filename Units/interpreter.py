from sys import exit
from Units.operation import *
from Units.unit import *


def label_remove(line_num, Code_Lines):
    """
    将命令中的标签加入命令跳转表中
    :param line_num:行数
    :param Code_Lines: 汇编命令行数组
    :return:
    """
    line = Code_Lines[line_num]
    line = line.strip()
    if line.startswith('.'):
        white = line.index(' ')
        label_index(line_num, line[:white])
        Code_Lines[line_num] = line[white:].strip()


def label_index(line_num, label):
    """
    添加子函数的跳转表
    :param line_num: 汇编语言行号
    :param label: str
    :return:
    """
    Lables[label] = line_num


def assembly_interpreter(line):
    """
    汇编语言解释器(ID段)
    :param line_num: 行号
    :param line: 一行汇编语言字符串
    :return: 包含操作码和操作数的列表
    """
    line = line.strip()
    if line.startswith('#'):
        return None
    if set(line) <= {'\n', ' '}:
        # 可以用空行了
        return
    if line == 'ret':
        return [line]
    if line == 'exit':
        exit()
    # 查看是否是ret语句

    white_index = line.index(' ')
    op = line[:white_index]
    operand = line[white_index:].strip()
    operand = operand.split(',')
    for i in range(len(operand)):
        operand[i] = operand[i].strip(' ')
    operand.insert(0, op)
    return operand


def execute_cmd(cmd):
    """
    执行命令（EX）cmd[0]为操作码，cmd[1:]为操作数
    :param cmd:
    :return:
    """
    pc[0] += 1
    # PC++
    cmd = assembly_interpreter(cmd)
    if cmd == None:
        # 跳过注释行
        return
    op = cmd[0]
    operand = []
    for i in cmd[1:]:
        operand.append(addr_mode(i))

    if op.startswith('j'):
        FUNC_TAB[op](op, *operand)
    elif op == 'ret':
        FUNC_TAB[op]()
    else:
        FUNC_TAB[op](*operand)


def addr_mode(addr):
    """
    寻址方式确定，并返回操作对象和操作地址
    :param addr: 地址字符串,是经汇编语言处理后前后无空格的字符
    :return: 操作对象和操作地址的元组
    """

    if addr.startswith('$'):
        # 立即数寻址
        if addr[1:].find('.') == -1:
            return imm_num, int(addr[1:])
        else:
            return imm_num, float(addr[1:])
    elif addr.startswith('#'):
        # 直接寻址
        return memory, int(addr[1:])
    elif addr.startswith('.'):
        # 标签寻址
        return Lables, addr
    elif addr.startswith('['):
        # 寄存起器间接寻址
        return memory, regs[addr[1:-1].strip()]
    elif addr.startswith('r'):
        return regs, addr
    elif addr.startswith('@'):
        # 变址寻址
        addr = addr[1:]
        left = addr.index('[')
        right = addr.index(']')
        imm = addr[:left]
        imm = int(imm)
        addr = addr[left + 1:right]
        addr = addr.replace(';', ' ')
        addr = addr.split()
        if len(addr) == 0:
            print("Invalid indexed addressing.")
            raise Exception
        elif len(addr) == 1:
            return memory, imm + regs[addr[0]]
        elif len(addr) == 2:
            return memory, imm + regs[addr[0]] * int(addr[1])
        elif len(addr) == 3:
            return memory, imm + regs[addr[0]] + regs[addr[1]] * int(addr[2])


def tomasulo_addr(addr):
    """
    tomasulo算法中寻址方式确定
    :param addr:
    :return:寄存器和立即数
    """
    addr = addr[1:]
    left = addr.index('[')
    right = addr.index(']')
    imm = addr[:left]
    imm = int(imm)
    addr = addr[left + 1:right]
    addr = addr.replace(';', ' ')
    addr = addr.split()
    reg = addr[0]
    return (reg, imm)
