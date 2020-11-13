from Units.scoreboard_phase import *

# 导入代码
fp = open('test_code/code3.txt', 'r')
Code_Lines = fp.readlines()

# 初始化记分牌
for i in range(6):
    instruction_table.append([Code_Lines[i], 0, 0, 0, 0])

# 读取代码
code_length = len(Code_Lines)
cnt = 0
next_cmd = 0
clock = 1
# 本时钟中是否已经使用一个时钟周期
clock_cnt = []
while (clock):
    # 指令发射
    cmd = Code_Lines[next_cmd]
    # issue result是使用的运算单元
    issue_result = issue(cmd)
    if issue_result:
        # 设置指令已发射
        instruction_table[next_cmd].append(issue_result)
        instruction_table[next_cmd][1] = clock
        clock_cnt.append(next_cmd)
        next_cmd += 1

    # 读取操作数,多个指令可以同一个周期读
    for i in range(next_cmd):
        if i in clock_cnt:
            continue
        if read_oprand(i):
            instruction_table[i][2] = clock
            clock_cnt.append(i)

    # 执行指令
    for i in range(next_cmd):
        if i in clock_cnt:
            continue
        i_result = unit_table[instruction_table[i][-1]].get_result()
        if i_result:
            instruction_table[i][-2] = i_result
            instruction_table[i][-3] = clock
            clock_cnt.append(i)

    # 写回指令
    for i in range(next_cmd):
        if i in clock_cnt:
            continue
        if not isinstance(instruction_table[i][-2], int):
            write_back = instruction_table[i][-2]
            for j in range(i):
                # write_back01 为寄存器索引
                before_unit = instruction_table[j][-1]
                if func_unit[before_unit]['busy'] and \
                        (func_unit[before_unit]["fj"] != write_back[0][1]
                         or func_unit[before_unit]["rj"] == 0) and (
                        func_unit[before_unit]["fk"] != write_back[0][1]
                        or func_unit[before_unit]["rk"] == 0):
                    # write_back1是结果
                    write_back[0][write_back[1]] = write_back[1]
                    instruction_table[i][-2] = clock
                    write_unit = instruction_table[i][-1]
                    func_unit[write_unit]["busy"] = 0
                    # 找出qj和qk以该寄存器为依赖的指令并设为ok
                    if j < next_cmd:
                        for k in range(j, next_cmd):
                            unitK = instruction_table[k][-1]
                            if func_unit[unitK]["busy"]:
                                if func_unit[unitK]["qj"] == unit_table[instruction_table[i][-1]]:
                                    func_unit[unitK]["rj"] = 1
                                if func_unit[unitK]["qk"] == unit_table[instruction_table[i][-1]]:
                                    func_unit[unitK]["rk"] = 1
            regs_table[func_unit[instruction_table[i][-1]]["fi"]] = 0
            unit_table[instruction_table[i][-1]].set_busy()
            func_unit[instruction_table[i][-1]]["busy"] = 0
            cnt += 1

    clock += 1
    clock_cnt = []
    if cnt == code_length:
        break
