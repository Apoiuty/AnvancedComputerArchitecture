from interpreter import *

# 设置内存单元
from unit import memory, regs

print("Before operation.")
memory[0] = 25
memory[1] = 2
memory[3] = 4
for i in [0, 1, 3]:
    print('addr ' + hex(i) + ':', memory[i])

for i in range(1, 4):
    print('r' + str(i) + ':', regs[i])

# 解释命令并执行
with open('code2.txt', 'r') as fp:
    for line in fp:
        cmd = assembly_interpreter(line)
        execute_cmd(cmd)

print("After operation.")
for i in range(1, 4):
    print('r' + str(i) + ':', regs[i])
for i in [0, 1, 3]:
    print('addr ' + hex(i) + ':', memory[i])
