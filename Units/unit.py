from Units.Regs import *
from Units.memory import *

memory = Memory()
# 内存对象
imm_num = Imm()
# 立即数对象
Lables = {}
# 跳转标签
pc = PC()
# PC对象
regs = Reg()
# 寄存器对象
cc = [0, 0, 0]
# 条件码
stack = Stack()

regs_table = {"r" + str(i): 0 for i in range(31)}

# 计分板大小
instruction_table = []

finished_cmd = []
# 完成的指令

# 在本周期读的不在本周期写，避免冒险
RinClock = []
