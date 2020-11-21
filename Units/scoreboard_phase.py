from .ALU import *


def try_issue(cmd):
    """
    检验执行单元是否可以执行并设置功能单元状态
    :param cmd:指令
    :return:
    """
    op = cmd[0]
    global load_store

    if op == 'load' and alu_unit.load:
        alu_unit.load -= 1
        tmp_unit = alu_unit(op)
        set_func_units(cmd, op, tmp_unit)
        load_store.append(tmp_unit)
        return tmp_unit
    if op == 'store' and alu_unit.store:
        alu_unit.store -= 1
        tmp_unit = alu_unit(op)
        set_func_units(cmd, op, tmp_unit)
        load_store.append(tmp_unit)
        return tmp_unit
    if (op == 'addf' or op == 'subf') and alu_unit.add:
        alu_unit.add -= 1
        tmp_unit = alu_unit(op)
        set_func_units(cmd, op, tmp_unit)
        return tmp_unit
    if (op == 'mulf' or op == 'divf') and alu_unit.mul:
        alu_unit.mul -= 1
        tmp_unit = alu_unit(op)
        set_func_units(cmd, op, tmp_unit)
        return tmp_unit
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

    if op not in {'load', 'store'}:
        # vj
        if regs_table.get(cmd[2], 0):
            unit.vj = regs_table[cmd[2]]
            regs_table[cmd[2]].sendto.append([unit, 0])
        else:
            s2 = addr_mode(cmd[2])
            unit.vj = s2[0][s2[1]]

        # vk
        if regs_table.get(cmd[3], 0):
            unit.vk = regs_table[cmd[3]]
            regs_table[cmd[3]].sendto.append([unit, 1])
        else:
            s3 = addr_mode(cmd[3])
            unit.vk = s3[0][s3[1]]
    else:
        if op == 'load':
            reg, imm = tomasulo_addr(cmd[2])
            unit.addr = imm
            # load的vj
            if regs_table[reg]:
                unit.vj = regs_table[reg]
                regs_table[reg].sendto.append([unit, 0])
            else:
                s2 = addr_mode(reg)
                unit.vj = s2[0][s2[1]]

        else:
            # 用vk来表示des的需要的寄存器
            reg, imm = tomasulo_addr(cmd[1])
            unit.addr = imm
            if regs_table[reg]:
                unit.vk = regs_table[reg]
                regs_table[reg].sendto.append([unit, 1])
            else:
                s2 = addr_mode(reg)
                unit.vk = s2[0][s2[1]]

            # vj表示要存储的值
            if regs_table[cmd[2]]:
                unit.vj = regs_table[cmd[2]]
                regs_table[cmd[2]].sendto.append([unit, 0])
            else:
                s2 = addr_mode(reg)
                unit.vj = s2[0][s2[1]]

    # 写入的位置
    unit.fi = cmd[1]

    # 设置qi
    if op != 'store':
        regs_table[cmd[1]] = unit


def issue(cmd):
    """
    是否可以发射命令
    :param cmd_num:当前尝试发射指令在指令状态表中的序号
    :return:
    """
    global instruction_table
    cmd = assembly_interpreter(cmd)
    # cmd1是des
    return try_issue(cmd)


def read_oprand(unit):
    """
    获取指令操作数
    :param cmd:
    :return:
    """
    # 设置功能单元状态
    # 设置操作数
    global load_store
    if (isinstance(unit.vj, alu_unit) or isinstance(unit.vk, alu_unit)) or \
            ((unit.op in {"load", "store"} and load_store and not unit == load_store[0]) or \
             (unit.op in {"load", "store"} and not load_store)) or unit.op_set:
        # 如果还有操作数未生成则继续等待
        return 0
    else:
        if unit.op in {"load", "store"}:
            if load_store:
                load_store.pop(0)
        unit.setoprand()
        return 1


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


def relase_alu(unit):
    """
    释放单元
    :param unit:
    :return:
    """
    if unit.op in {'load'}:
        alu_unit.load += 1
    elif unit.op == 'store':
        alu_unit.store += 1
    elif unit.op in {'mulf', 'divf'}:
        alu_unit.mul += 1
    else:
        alu_unit.add += 1
