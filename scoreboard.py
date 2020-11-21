"""
记分牌算法
"""
from Units.scoreboard_phase import *

# 导入代码
fp = open('test_code/code3.txt', 'r')
Code_Lines = fp.readlines()

regs[4] = 25
regs[10] = 25
regs[11] = 25
# 初始化记分牌
for i in range(6):
    instruction_table.append([Code_Lines[i], 0, 0, 0])

# 读取代码
code_length = len(Code_Lines)
cnt = 0
next_cmd = 0
clock = 1
# 本时钟中是否已经使用一个时钟周期
clock_used = []
while (clock):
    # 指令发射
    if next_cmd < code_length:
        cmd = Code_Lines[next_cmd]
        # issue result是使用的运算单元
        issue_result = issue(cmd)
        if issue_result:
            # 设置指令已发射
            # 将最后的一个元素设置为积分表项
            instruction_table[next_cmd].append(issue_result)
            instruction_table[next_cmd][1] = clock
            clock_used.append(next_cmd)
            next_cmd += 1

    # 读取操作数,多个指令可以同一个周期读
    for i in range(next_cmd):
        unit = instruction_table[i][-1]
        if i in clock_used or i in finished_cmd:
            continue
        if read_oprand(i):
            # 本周期读取的寄存器
            if unit.op == 'mv':
                RinClock.append(unit.fj)
            else:
                RinClock.append(unit.fj)
                RinClock.append(unit.fk)
            instruction_table[i][2] = clock
            clock_used.append(i)

    # 执行指令
    for i in range(next_cmd):
        if i in clock_used or i in finished_cmd:
            continue
        i_result = instruction_table[i][-1].get_result()
        if i_result:
            instruction_table[i][-2] = i_result
            instruction_table[i][-3] = clock
            clock_used.append(i)

    # 写回指令
    for i in range(next_cmd):
        if i in clock_used or i in finished_cmd:
            continue
        write_back = instruction_table[i][-2]
        if not isinstance(write_back, int):
            if check_hazard(i, write_back) and write_back[0][1] not in RinClock:
                write_Back(write_back, next_cmd, i)
                clock_used.append(i)
                instruction_table[i][-2] = clock
                finished_cmd.append(i)
                cnt += 1
    clock += 1
    clock_used = []
    RinClock = []
    if cnt == code_length:
        break

# 打印结果
for i in instruction_table:
    print(i[0:-1])
