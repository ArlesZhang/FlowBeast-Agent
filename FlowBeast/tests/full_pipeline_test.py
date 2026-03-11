import os
import pandas as pd
import structlog
import time 
import sys
import importlib.util # 用于导入动态生成的文件

# 确保能找到 flowbeast 模块
sys.path.append(os.getcwd()) 

try:
    from flowbeast.agent.compiler import compile_workflow
    from flowbeast.agent.codegen import generate_code
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保 flowbeast/agent/compiler.py 和 codegen.py 存在且语法正确。")
    sys.exit(1)

# 配置 structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
        structlog.processors.JSONRenderer(indent=2)
    ]
)
log = structlog.get_logger()

# 1. 准备数据
os.makedirs('flowbeast/data', exist_ok=True)
csv_content = '''name,age,department,amount
Alice,28,Engineering,900
Bob,35,Sales,1500
Charlie,42,Engineering,2200
David,25,Sales,1200
Eve,50,HR,800
'''
with open('flowbeast/data/input.csv', 'w') as f:
    f.write(csv_content)
print('✅ 数据已创建。')

# 2. 编译 (Qwen Turbo)
prompt = '加载 flowbeast/data/input.csv，过滤 amount>1000，按 department 聚合求 age 的平均值 (rename 为 avg_age) 和 amount 的总和 (rename 为 total_sales)，最后保存到 flowbeast/data/top_sales.parquet'
print('-------------------- 编译 (Qwen Turbo) --------------------')
try:
    wf = compile_workflow(prompt, model='qwen-turbo')
    code = generate_code(wf)
    print('\n✅ 生成成功！')
    print('-------------------- Pandas 代码 --------------------')
    print(code)
    
    # 3. 保存
    workflow_file = 'generated_workflow.py'
    with open(workflow_file, 'w') as f:
        f.write(code)
    print(f'\n✅ 已保存到 {workflow_file}')
    
    # 4. 终极修复：不再使用 exec()，而是导入并运行
    print('-------------------- 执行验证 --------------------')
    try:
        # 动态导入刚刚生成的 .py 文件
        spec = importlib.util.spec_from_file_location("generated_workflow", workflow_file)
        workflow_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(workflow_module)
        
        # 调用函数
        workflow_module.run_workflow() 
        print('✅ 执行成功！')
        
    except Exception as e:
        print(f'❌ 执行异常: {e}')
    
    # 5. 验证输出 (现在不再需要 time.sleep)
    output_path = 'flowbeast/data/top_sales.parquet'
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f'\n🎉🎉🎉 项目闭环成功！{output_path} 已生成。')
        df = pd.read_parquet(output_path)
        print(f'输出预览:\n{df.head()}')
    else:
        print(f'❌ 未找到 {output_path} 或文件为空。')
        
except Exception as e:
    log.error('Compile failed', error=str(e))
    print(f'\n❌ 失败: {e}')
