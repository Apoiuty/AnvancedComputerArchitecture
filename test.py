# test file
from interpreter import *

pc[0] = 25
stack.ebp = 1
stack.esp = 45
print(stack.ebp, stack.esp)
execute_cmd('')
print(pc[0])
print(stack.ebp, stack.esp)
execute_cmd('ret')
print(stack.ebp, stack.esp)
