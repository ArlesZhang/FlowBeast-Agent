import pytest
import json
from flowbeast.ir.models import DataWorkflow
from flowbeast.agent.codegen import generate_code

# 模拟一个经过验证的 DataWorkflow IR
mock_workflow_data = {
    "description": "加载、过滤、聚合、保存",
    "steps": [
        {"id": "s1", "step_type": "load_data", "params": {"path": "./data/in.csv", "format": "csv"}, "input_df_id": "df", "output_df_id": "df1"},
        {"id": "s2", "step_type": "filter_rows", "params": {"condition": "age > 30"}, "input_df_id": "df1", "output_df_id": "df2"},
        {"id": "s3", "step_type": "group_aggregate", "params": {"group_by": ["department"], "aggregations": {"avg_age": ("age", "mean"), "total_count": ("name", "count")}}, "input_df_id": "df2", "output_df_id": "df3"}, # 增加一个聚合确保 tojson 逻辑正确
        {"id": "s4", "step_type": "save_data", "params": {"path": "./data/out.parquet", "format": "parquet"}, "input_df_id": "df3", "output_df_id": "df_final"}
    ]
}

def test_codegen_structure():
    """测试 generate_code 是否生成正确的代码结构和依赖追踪。"""
    workflow = DataWorkflow(**mock_workflow_data)
    generated_code = generate_code(workflow)
    
    # 检查关键模块和函数是否存在
    assert "import pandas as pd" in generated_code
    assert "def run_workflow():" in generated_code
    
    # 检查依赖追踪和修复后的 save_data
    assert 'df1 = pd.read_csv(r"./data/in.csv")' in generated_code
    assert 'df2 = df1.query("age > 30")' in generated_code
    assert 'df3 = (' in generated_code
    
    # 断言现在应该检查的是 `.agg(` 而不是 `.agg(**{`
    assert '.agg(' in generated_code
    
    # 检查 save_data 步骤是否使用了正确的 input_df_id (df3)
    assert 'df3.to_parquet' in generated_code
    
def test_codegen_agg_params():
    """测试聚合函数参数是否正确渲染（使用 tojson）。"""
    workflow = DataWorkflow(**mock_workflow_data)
    generated_code = generate_code(workflow)
    
    # 由于使用了 |tojson，我们预期看到一个合法的 JSON 字符串
    # 注意：Python 的 |tojson 在字典中使用双引号
    expected_agg = json.dumps(mock_workflow_data['steps'][2]['params']['aggregations'])
    
    # 检查 Jinja2 是否正确渲染了 .agg(JSON_STRING) 部分
    # 字符串包含完整的 JSON 且周围没有 **{}
    expected_assert = f".agg({expected_agg})"
    
    # 移除空格进行严格检查
    assert expected_assert.replace(" ", "") in generated_code.replace(" ", "")

    # 确保没有旧的 **{ 出现
    assert '.agg(**{' not in generated_code
