import pytest
from cody_agent.agent.compiler import compile_workflow
from cody_agent.agent.codegen import generate_code

TEST_PROMPT = (
    "加载 ./data/input.csv，"
    "过滤 age > 30，"
    "选择 name, department，"
    "保存为 ./data/output.parquet"
)

def test_full_pipeline(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake")
    # 模拟 LLM 成功返回
    from unittest.mock import patch
    mock_resp = {
        "description": "test",
        "steps": [
            {"id": "s1", "step_type": "load_data", "params": {"path": "./data/input.csv", "format": "csv"}, "input_df_id": "df", "output_df_id": "df1"},
            {"id": "s2", "step_type": "filter_rows", "params": {"condition": "age > 30"}, "input_df_id": "df1", "output_df_id": "df2"},
            {"id": "s3", "step_type": "select_columns", "params": {"columns": ["name", "department"]}, "input_df_id": "df2", "output_df_id": "df3"},
            {"id": "s4", "step_type": "save_data", "params": {"path": "./data/output.parquet", "format": "parquet"}, "input_df_id": "df3", "output_df_id": "df4"}
        ]
    }
    with patch("cody_agent.agent.compiler._call_llm", return_value=mock_resp):
        wf = compile_workflow(TEST_PROMPT)
        code = generate_code(wf)
        assert "pd.read_csv" in code
        assert "to_parquet" in code
