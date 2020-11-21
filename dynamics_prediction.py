"""
Readme:
循环代码中Tomasulo代码实现，每次跳转都预测为执行。
测试代码为：
.loop: load r0,@0[r10;;]
mulf r4,r0,r2
store @0[r10;;],r4
addf r10,r10,$1
jne r10,r11,.loop

测试代码依据自己实现的指令集进行了修改，功能与作业要求相同：从内存中读取一个数据乘以一个标量后存回。指令集可参考ISA.md文件。
输出执行前后内存中的数据并输出除控制指令外其他指令的发射、执行和写回周期。

代码请在虚拟环境中运行。
"""
from Units.scoreboard_phase import *
from copy import deepcopy

# 导入代码
fp = open('test_code/dynamics_prediction.txt', 'r')
Code_Lines = fp.readlines()

for i in range(len(Code_Lines)):
    label_remove(i, Code_Lines)
# 设置寄存器的值
regs[10] = 0
regs[11] = 1
regs[2] = 2
# 初始化执行周期记录表
for i in range(len(Code_Lines)):
    instruction_table.append([Code_Lines[i], 0, 0, 0])

# 循环的行
loop_lines = deepcopy(instruction_table)
code_lines = deepcopy(Code_Lines)
code_length = len(Code_Lines)
# 执行的指令条数
cnt = 0
# 下一条指令索引
next_cmd = 0
# 时钟
clock = 1
# 本时钟中是否已经使用一个时钟周期
clock_used = []
# 正在运行中的指令
in_exec = set()
# 设定循环的次数
loop_cnt = 5
# 保存循环次数后面使用
LOOP_CNT = loop_cnt

for i in range(loop_cnt + 1):
    memory[i] = i ** 2
print('Memory before loop:')
for i in range(loop_cnt + 1):
    print('Mem[{0:d}]\t{1:d}'.format(i, memory[i]))

print('-' * 37)
jne = 0
# 正在发射的指令是否为跳转指令
while (clock):

    # 指令发射
    if next_cmd < code_length:
        cmd = Code_Lines[next_cmd]
        # 如何是分支指令则跳转
        if cmd.strip().startswith('j'):
            if loop_cnt:
                cmd = assembly_interpreter(cmd)
                begin = Lables[cmd[-1] + ':']
                end = 4
                Code_Lines[next_cmd:next_cmd] = deepcopy(code_lines[begin:end])
                instruction_table[next_cmd:next_cmd] = deepcopy(loop_lines[begin:end])
                jne = 1
                loop_cnt -= 1
                code_length += end - begin
            else:
                jne = 1

        if not jne:
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
            instruction_table[i][-1] = None
            clock_used.append(i)
            instruction_table[i][-2] = clock
            finished_cmd.append(i)
            cnt += 1

    clock += 1
    jne = 0
    clock_used = []
    if cnt >= next_cmd:
        break
# 打印结果
print('|{0:^20s}|{1:^4s}|{2:^4s}|{3:^4s}|'.format('Instruction', 'IS', 'ES', 'WB'))
print('-' * 37)
for i in instruction_table[:-1]:
    print('|{0:<20s}|{1:^4d}|{2:^4d}|{3:^4d}|'.format(i[0].strip(), i[1], i[2], i[3]))
print('-' * 37)

print('Memory after loop:')
for i in range(LOOP_CNT + 1):
    print('Mem[{0:d}]\t{1:d}'.format(i, memory[i]))

print('Clock used:', clock - 1)
