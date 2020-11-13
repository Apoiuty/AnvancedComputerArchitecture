from .ALU import *


def try_issue(cmd):
    """
    检验执行单元是否可以执行并设置功能单元状态
    :param cmd:指令
    :return:
    """
    op = cmd[0]

    if op == 'addf':
        if add_unit.cnt == -1:
            set_func_units(cmd, 'addf')
            return 'addf'
    if op == 'subf':
        if add_unit.cnt == -1:
            set_func_units(cmd, 'subf')
            return 'subf'
    elif op == 'mulf':
        if mul1_unit.cnt == -1 or mul2_unit.cnt == -1:
            if mul1_unit.cnt == -1:
                set_func_units(cmd, 'mul1')
                return 'mul1'
            else:
                set_func_units(cmd, 'mul2')
                return 'mul2'

    elif op == 'mv':
        if integer_unit.cnt == -1:
            set_func_units(cmd, 'mv')
            return 'mv'
    elif op == 'divf':
        if div_unit.cnt == -1:
            set_func_units(cmd, 'divf')
            return 'divf'
    return 0


def set_func_units(cmd, op):
    """
    设置功能状态单元和寄存器单元
    :param cmd:
    :param op:
    :return:
    """
    global func_unit
    global regs_table
    global instruction_table
    func_unit[op]['busy'] = 1
    func_unit[op]['op'] = unit_table[op]
    func_unit[op]['fi'] = cmd[1]
    func_unit[op]['fj'] = cmd[2]
    func_unit[op]['qj'] = regs_table.get(cmd[2], 0)
    regs_table[cmd[1]] = unit_table[op]
    func_unit[op]['rj'] = not regs_table.get(cmd[2], 0)
    if op != 'mv':
        func_unit[op]['fk'] = cmd[3]
        func_unit[op]['qk'] = regs_table.get(cmd[3], 0)
        func_unit[op]['rk'] = not regs_table.get(cmd[3], 0)


def issue(cmd):
    """
    是否可以发射命令
    :param cmd_num:当前尝试发射指令在指令状态表中的序号
    :return:
    """
    global instruction_table
    cmd = assembly_interpreter(cmd)
    if not regs_table[cmd[1]]:
        return try_issue(cmd)


def read_oprand(cmd_num):
    """
    获取指令操作数
    :param cmd:
    :return:
    """
    cmd = instruction_table[cmd_num][0]
    unit = instruction_table[cmd_num][-1]
    # 设置功能单元状态
    if func_unit[unit]['rj'] and func_unit[unit]['rk']:
        func_unit[unit]['rj'] = func_unit[unit]['rk'] = 0
        func_unit[unit]['qj'] = func_unit[unit]['qk'] = 0
        # 设置操作数
        unit_table[unit].setoprand(cmd)
        return 1
    return 0
