# 三元运算符
from Units.unit import *


def add(des, op1, op2):
    """
    des=op1+op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] + op2[0][op2[1]]


def sub(des, op1, op2):
    """
    des=op1-op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] - op2[0][op2[1]]


def mul(des, op1, op2):
    """
    des=op1*op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] * op2[0][op2[1]]


def div(des, op1, op2):
    """
    des=op1+op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] // op2[0][op2[1]]


def divf(des, op1, op2):
    """
    des=op1+op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] / op2[0][op2[1]]


def AND(des, op1, op2):
    """
    des=op1&op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] & op2[0][op2[1]]


def OR(des, op1, op2):
    """
    des=op1|op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] | op2[0][op2[1]]


def XOR(des, op1, op2):
    """
    des=op1^op2
    :param op1:
    :param op2:
    """
    (des[0])[des[1]] = op1[0][op1[1]] ^ op2[0][op2[1]]


# 二元运算符
def mv(des, op):
    """
    des=op
    :param des:
    :param op:
    :return:
    """
    (des[0])[des[1]] = op[0][op[1]]


def cmp(op1, op2):
    """
    cmp two op and set cc
    :param a:
    :param b:
    :return:
    """
    a = op1[0][op1[1]]
    b = op2[0][op2[1]]
    if type(a) != type(b):
        print("Cannot compare two different type value")
        raise Exception
    else:
        if a > b:
            cc[2] = 1
            cc[0] = cc[1] = 0
        elif a < b:
            cc[0] = 1
            cc[1] = cc[2] = 0
        else:
            cc[1] = 1
            cc[0] = cc[2] = 0


# 一元指令
def NOR(op):
    op[0][op[1]] = ~op[0][op[1]]


def inc(op):
    op[0][op[1]] += 1


def dec(op):
    op[0][op[1]] -= 1


def jmp(op, oprand):
    if op == 'jmp' or op == 'je' and cc == [0, 1, 0] or op == 'ja' and \
            cc == [0, 0, 1] or op == 'jge' and (cc == [0, 1, 0] or cc == [0, 0, 1]) or op == 'jb' \
            and cc == [1, 0, 0] or op == 'jle' and (cc == [1, 0, 0] or cc == [0, 1, 0]) or \
            op == 'jne' and (not cc == [0, 1, 0]):
        setPC(oprand)


def pop(op):
    op[0][op[1]] = stack.pop()


def push(op):
    stack.push(op[0][op[1]])


def call(op):
    """
    子函数调用指令
    :param op:
    :return:
    """

    stack.push(stack.ebp)
    stack.ebp = stack.esp
    stack.push(pc[0])
    setPC(op)


def ret():
    """
    子程序返回
    :return:
    """
    stack.esp = stack.ebp + 1
    setPC((imm_num, stack.pop()))
    stack.ebp = stack.pop()


def out(op):
    """输出寄存器或内容内容"""
    print(op[0][op[1]])


FUNC_TAB = {
    'add': add,
    'addf': add,
    'sub': sub,
    'subf': sub,
    'mul': mul,
    'mulf': mul,
    'div': div,
    'divf': divf,
    'and': AND,
    'or': OR,
    'xor': XOR,
    'mv': mv,
    'cmp': cmp,
    'nor': NOR,
    'inc': inc,
    'dec': dec,
    'jmp': jmp,
    'ja': jmp,
    'jge': jmp,
    'jb': jmp,
    'jle': jmp,
    'je': jmp,
    'jne': jmp,
    'pop': pop,
    'push': push,
    'call': call,
    'ret': ret,
    'out': out
}


def setPC(pos):
    """
    设置PC寄存器
    :return:
    """
    a = pos[0]
    if a == imm_num:
        pc[0] = a[pos[1]]
    elif a == Lables:
        pc[0] = a[pos[1] + ':']
    elif a == regs:
        pc[0] += a[pos[1]]
