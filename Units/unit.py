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

"""
记分牌"""
func_unit = {"mv": {"busy": 0, "op": 0, "fi": 0, "fj": 0, "fk": 0, "qj": 0, "qk": 0, "rj": 0, "rk": 0},
             "mul1": {"busy": 0, "op": 0, "fi": 0, "fj": 0, "fk": 0, "qj": 0, "qk": 0, "rj": 0, "rk": 0},
             "mul2": {"busy": 0, "op": 0, "fi": 0, "fj": 0, "fk": 0, "qj": 0, "qk": 0, "rj": 0, "rk": 0},
             "addf": {"busy": 0, "op": 0, "fi": 0, "fj": 0, "fk": 0, "qj": 0, "qk": 0, "rj": 0, "rk": 0},
             "divf": {"busy": 0, "op": 0, "fi": 0, "fj": 0, "fk": 0, "qj": 0, "qk": 0, "rj": 0, "rk": 0}}

regs_table = {"r" + str(i): 0 for i in range(31)}

# 计分板大小
instruction_table = []
