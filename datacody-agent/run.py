import pandas as pd
from cody_agent.agent.compiler import compile_workflow
from cody_agent.agent.codegen import generate_code

prompt = input("请输入您的中文数据处理需求（如：加载 input.csv，过滤金额大于1000，按部门聚合求平均年龄并保存）：\n> ")

print("\n正在编译...")
wf = compile_workflow(prompt)
code = generate_code(wf)

print("\n生成代码：")
print(code)

print("\n正在执行...")
exec(code, {"pd": pd})

print("\n任务完成！")
