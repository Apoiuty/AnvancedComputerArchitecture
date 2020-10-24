from interpreter import *

# 处理标签并生成跳转表
for i in range(len(Code_Lines)):
    label_remove(i, Code_Lines[i])
pc[0] = Lables['.start:']

# 执行指令
while True:
    execute_cmd(Code_Lines[pc[0]])
    if pc[0] == len(Code_Lines):
        break

fp.close()
