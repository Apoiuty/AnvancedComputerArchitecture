from .ALU import *


def try_issue(cmd):
    """
    检验执行单元是否可以执行并设置功能单元状态
    :param cmd:指令
    :return:
    """
    op = cmd[0]

    if op == 'addf':
        if add_unit.busy == 0:
            set_func_units(cmd, 'addf', add_unit)
            return add_unit
    if op == 'subf':
        if add_unit.busy == 0:
            set_func_units(cmd, 'subf', add_unit)
            return add_unit
    elif op == 'mulf':
        if mul1_unit.busy == 0:
            set_func_units(cmd, 'mul1', mul1_unit)
            return mul1_unit
        elif mul2_unit.busy == 0:
            set_func_units(cmd, 'mul2', mul2_unit)
            return mul2_unit

    elif op == 'mv':
        if integer_unit.busy == 0:
            set_func_units(cmd, 'mv', integer_unit)
            return integer_unit
    elif op == 'divf':
        if div_unit.busy == 0:
            set_func_units(cmd, 'divf', div_unit)
            return div_unit
    return 0


def set_func_units(cmd, op, unit):
    """
    设置功能状态单元和寄存器单元
    :param unit:
    :param cmd:
    :param op:
    :return:
    """
    global regs_table
    unit.busy = 1
    unit.op = op
    unit.fi = cmd[1]
    unit.fj = cmd[2]
    unit.qj = regs_table[cmd[2]]
    regs_table[cmd[1]] = unit
    unit.rj = not regs_table[cmd[2]]
    if op != 'mv':
        unit.fk = cmd[3]
        unit.qk = regs_table[cmd[3]]
        unit.rk = not regs_table[cmd[3]]
    else:
        unit.fk = 0
        unit.qk = 0
        unit.rk = 1


def issue(cmd):
    """
    是否可以发射命令
    :param cmd_num:当前尝试发射指令在指令状态表中的序号
    :return:
    """
    global instruction_table
    cmd = assembly_interpreter(cmd)
    # cmd1是des
    if not regs_table[cmd[1]]:
        return try_issue(cmd)


def read_oprand(cmd_num):
    """
    获取指令操作数
    :param cmd:
    :return:
    """
    unit = instruction_table[cmd_num][-1]
    # 设置功能单元状态
    # 设置操作数
    if unit.rj and unit.rk:
        unit.rj = unit.rk = unit.qj = unit.qk = 0
        unit.setoprand()
        return 1
    return 0


def check_hazard(i, write_back):
    """
    检查i指令前的冒险
    :param i:要写回指令所在位置
    :param write_back:写回的项目及值，（（对象，索引），数据）
    :return:
    """
    global instruction_table
    write_back_reg = write_back[0][1]
    for j in range(i):
        # 处理前面的冒险
        # write_back01 为寄存器索引
        if j in finished_cmd:
            continue
        before_unit = instruction_table[j][-1]
        if before_unit.busy and (before_unit.fj != write_back_reg or before_unit.rj == 0) and \
                (before_unit.fk != write_back_reg or before_unit.rk == 0):
            continue
        return 0
    return 1


def write_Back(write_back, next_cmd, i):
    """
    将结果写回寄存器并设置相应的标志位
    :param write_back: 写回的项目
    :param next_cmd: 下一条指令位置
    :param i: 写回指令所在的位置
    :return:
    """
    write_back_unit = instruction_table[i][-1]
    for j in range(i + 1, next_cmd):
        after_unit = instruction_table[j][-1]
        if after_unit.busy:
            if after_unit.qj == write_back_unit:
                after_unit.rj = 1
            if after_unit.qk == write_back_unit:
                after_unit.rk = 1
    write_back[0][0][write_back[0][1]] = write_back[1]
    #     设置功能单元状态和寄存器结果状态
    regs_table[write_back_unit.fi] = 0
    write_back_unit.busy = 0
