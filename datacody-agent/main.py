from cody_agent.agent.compiler import CompilerAgent
from cody_agent.codegen.pandas_generator import PandasCodeGenerator
from cody_agent.execution.runner import PipelineRunner

def test_full_pipeline():
    print("=== DataCody Agent 端到端测试 ===\n")
    
    # 1. 用户请求
    user_request = "从CSV文件加载数据，过滤出年龄大于30的员工，保存为Parquet格式"
    print(f"用户请求: {user_request}")
    
    # 2. 编译为IR
    compiler = CompilerAgent()
    workflow = compiler.compile_to_ir(user_request)
    print(f"\n生成工作流: {workflow.description}")
    for step in workflow.steps:
        print(f"  - {step.step_type}: {step.params}")
    
    # 3. 生成代码
    codegen = PandasCodeGenerator()
    script = codegen.generate_script(workflow)
    print(f"\n生成的代码:\n```python\n{script}\n```")
    
    # 4. 执行管道
    runner = PipelineRunner()
    result = runner.execute_pandas_script(script)
    
    print(f"\n执行结果: {'成功' if result['success'] else '失败'}")
    if result['stdout']:
        print(f"输出: {result['stdout']}")
    if result['stderr']:
        print(f"错误: {result['stderr']}")

if __name__ == "__main__":
    test_full_pipeline()
