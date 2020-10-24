from Regs import *
from memory import *

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
fp = open('code2.txt', 'r')
Code_Lines = fp.readlines()
