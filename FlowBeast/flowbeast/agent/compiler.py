import os
import json
import httpx
import structlog
from openai import OpenAI, APIError, RateLimitError
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from flowbeast.ir.models import DataWorkflow # 确保 models.py 存在

load_dotenv()
log = structlog.get_logger()

# --- Qwen 客户端初始化 ---
try:
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        timeout=50.0
    )
except Exception as e:
    log.error("Qwen Client 初始化失败", error=str(e))
    client = None

# 修复：使用 Pydantic 错误日志要求的小写格式
# (Pydantic 错误日志显示它需要 'load_data', 'filter_rows', 'group_aggregate')
NAME_TO_STEP_TYPE_MAP = {
    "load_data": "load_data",
    "load_csv": "load_data",
    "filter": "filter_rows",
    "filter_rows": "filter_rows",
    "filter_data": "filter_rows",
    "group_by": "group_aggregate",
    "agg": "group_aggregate",
    "aggregate": "group_aggregate",
    "aggregate_data": "group_aggregate",
    "save_data": "save_data",
    "save_parquet": "save_data"
}

# 修复：我们必须强制 Qwen 输出 JSON
SYSTEM_PROMPT = """
你是一个专业的 DataWorkflow 编译器。
- 严格输出 JSON 格式。
- 你的输出必须是一个 JSON 对象，包含一个名为 'steps' 的数组。
- 每个步骤必须包含 'name' 和 'params' 字段。
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def _call_llm(user_prompt: str, model: str = "qwen-turbo") -> str:
    if client is None:
        raise ValueError("LLM client 未初始化")
        
    # 修复：使用三引号 f"""...""" 避免 SyntaxError
    full_prompt = f"""请严格按 JSON 格式输出，包含 steps 数组：
{user_prompt}"""
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]
    
    resp = client.chat.completions.create(
        model=model,
        temperature=0.0,
        messages=messages,
        response_format={"type": "json_object"} 
    )
    return resp.choices[0].message.content


def compile_workflow(user_prompt: str, model: str = "qwen-turbo") -> DataWorkflow:
    """核心入口：自然语言 → 验证通过的 IR"""
    try:
        raw_json = _call_llm(user_prompt, model)
        log.info("LLM raw output", raw_json=raw_json)
        
        if isinstance(raw_json, (str, bytes, bytearray)):
            parsed = json.loads(raw_json)
        else:
            parsed = raw_json

        # --- 核心修复：手动添加 Pydantic 需要的字段 ---

        # 修复：添加 'description' 字段 (Pydantic 需要)
        if 'description' not in parsed:
            parsed['description'] = f"Workflow for: {user_prompt[:30]}..."

        if 'steps' in parsed and isinstance(parsed['steps'], list):
            for i, step in enumerate(parsed['steps']):
                
                # 修复：添加 'id' 字段 (Pydantic 需要)
                if 'id' not in step:
                    step['id'] = f"step_{i+1}"
                
                # 修复：使用小写映射
                if 'name' in step:
                    step_name_lower = step['name'].lower()
                    
                    mapped_type = NAME_TO_STEP_TYPE_MAP.get(
                        step_name_lower, 
                        "filter_rows" # 默认或未知的类型
                    )
                    step['step_type'] = mapped_type

                # 修复：暴力修复聚合格式
                if step["step_type"] == "group_aggregate":
                    if "params" not in step: step["params"] = {}
                    p = step["params"]
                    if "aggregations" in p:
                        raw_agg = p["aggregations"]
                        rename = p.get("renames") or p.get("rename", {})
                        new_agg = {}
                        
                        if isinstance(raw_agg, dict):
                            for col, func in raw_agg.items():
                                new_name = rename.get(col, col)
                                new_agg[new_name] = (col, func)
                        elif isinstance(raw_agg, list):
                            for item in raw_agg:
                                col = item.get("column") or item.get("col")
                                func = item.get("function") or item.get("func") or "sum"
                                new = item.get("rename") or item.get("new_name") or col
                                if col:
                                    new_agg[new] = (col, func)
                                    
                        p["aggregations"] = new_agg # 覆盖为统一格式
                        p["group_by"] = p.get("group_by") or p.get("columns") or p.get("by") or ["department"]

        # 4. 验证与赋值
        workflow = DataWorkflow.model_validate(parsed)
        
        log.info("Compile success", steps=len(workflow.steps))
        
        return workflow
    
    except Exception as e:
        log.error("Compile failed", exc_info=e)
        raise
