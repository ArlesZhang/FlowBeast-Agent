import pytest
import json
from flowbeast.legacy_workflows.ir.models import DataWorkflow
from flowbeast.legacy_workflows.codegen.pandas_generator import PandasCodeGenerator

# 模拟一个经过验证的 DataWorkflow IR
mock_workflow_data = {
    "description": "加载、过滤、聚合、保存",
    "steps": [
        {"id": "s1", "step_type": "load_data", "params": {"path": "./data/in.csv", "format": "csv"}, "input_df_id": "df", "output_df_id": "df1"},
        {"id": "s2", "step_type": "filter_rows", "params": {"column": "age", "condition": "> 30"}, "input_df_id": "df1", "output_df_id": "df2"},
        {"id": "s3", "step_type": "group_aggregate", "params": {"group_by": ["department"], "aggregations": {"avg_age": ["age", "mean"], "total_count": ["name", "count"]}}, "input_df_id": "df2", "output_df_id": "df3"},
        {"id": "s4", "step_type": "save_data", "params": {"path": "./data/out.parquet", "format": "parquet"}, "input_df_id": "df3", "output_df_id": "df_final"}
    ]
}

def test_codegen_structure():
    """测试 PandasCodeGenerator 是否生成正确的代码结构。"""
    workflow = DataWorkflow(**mock_workflow_data)
    generator = PandasCodeGenerator()
    generated_code = generator.generate_script(workflow)

    # 检查关键模块和函数是否存在
    assert "import pandas as pd" in generated_code
    assert "def execute_pipeline():" in generated_code

    # 检查依赖追踪和修复后的 save_data
    assert 'df = pd.read_csv' in generated_code
    assert 'df = df' in generated_code  # Filter step
    assert 'df.groupby' in generated_code  # Group by step

    # 检查 save_data 步骤
    assert 'df.to_parquet' in generated_code

def test_codegen_agg_params():
    """测试聚合函数参数是否正确渲染。"""
    workflow = DataWorkflow(**mock_workflow_data)
    generator = PandasCodeGenerator()
    generated_code = generator.generate_script(workflow)

    # 检查聚合部分存在
    assert '.agg(' in generated_code
