from Units.scoreboard_phase import *

# 导入代码
fp = open('../test_code/tomasulo.txt', 'r')
Code_Lines = fp.readlines()

# 设置一下存储器的值
regs[10] = 0
regs[11] = 0
regs[4] = 2
memory[34] = 7.0
memory[45] = 8.0
# 初始化执行周期记录表
for i in range(len(Code_Lines)):
    instruction_table.append([Code_Lines[i], 0, 0, 0])
# 读取代码
code_length = len(Code_Lines)
cnt = 0
next_cmd = 0
clock = 1
# 本时钟中是否已经使用一个时钟周期
clock_used = []
in_exec = set()
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

    # 执行指令
    for i in range(next_cmd):
        unit = instruction_table[i][-1]
        if i in clock_used or i in finished_cmd:
            continue
        if (unit in in_exec) or read_oprand(unit):
            # 检查操作数是否准备就绪
            # 本周期读取的寄存器
            # if unit.op == 'mv':
            #     RinClock.append(unit.fj)
            # else:
            #     RinClock.append(unit.fj)
            #     RinClock.append(unit.fk)
            in_exec.add(unit)
            i_result = instruction_table[i][-1].get_result()
            if i_result:
                in_exec.remove(unit)
                instruction_table[i][-2] = i_result
                instruction_table[i][-3] = clock
                clock_used.append(i)

    # 写回指令
    for i in range(next_cmd):
        if i in clock_used or i in finished_cmd:
            continue

        unit = instruction_table[i][-2]
        if not isinstance(unit, int):
            unit.write_back()

            # 释放运算单元
            relase_alu(unit)
            del unit
            instruction_table[i][-1] = None
            clock_used.append(i)
            instruction_table[i][-2] = clock
            finished_cmd.append(i)
            cnt += 1

    clock += 1
    clock_used = []
    if cnt == code_length:
        break
# 打印结果
print('|{0:^20s}|{1:^4s}|{2:^4s}|{3:^4s}|'.format('Instruction', 'IS', 'ES', 'WB'))
print('-' * 37)
for i in instruction_table:
    print('|{0:<20s}|{1:^4d}|{2:^4d}|{3:^4d}|'.format(i[0][0:-1], i[1], i[2], i[3]))
print('-' * 37)

print(regs[6])
