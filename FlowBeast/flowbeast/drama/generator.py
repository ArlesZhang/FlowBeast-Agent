import os
import json
import re
from datetime import datetime

from loguru import logger
from openai import OpenAI
from google import genai     # Use latest Google GenAI SDK (https://ai.google.dev/tutorials/python_quickstart)

from flowbeast.core.config import settings
from flowbeast.drama.prompt import build_prompt

#region ====================== Client 构建 ======================

# LLM SDK official docs:
# - OpenAI:    https://developers.openai.com/api/docs/quickstart  ( https://github.com/openai/openai-python )
# - Qwen:      https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen  ( https://github.com/dashscope/dashscope-python-sdk )
# - Gemini:    https://ai.google.dev/gemini-api/docs/get-started/python
# call LLM Mode SDK of OpenAI, Qwen, Gemini (refer to official documentation) --> return client instance
#endregion 
def get_client():
    provider = settings.MODEL_PROVIDER.lower()

    if provider == "qwen":
        return OpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    elif provider == "openai":
        return OpenAI(api_key=settings.OPENAI_API_KEY)

    elif provider == "gemini":
        # Ensure the API KEY is configured in settings (FlowBeast config.py)
        if not getattr(settings, "GOOGLE_API_KEY", None):
            raise ValueError("❌ GOOGLE_API_KEY is not configured")

        return genai.Client(api_key=settings.GOOGLE_API_KEY)   # Use the recommended Client class for Gemini (latest SDK)
 
    else:
        raise ValueError(f"❌ 不支持的模型提供商: {provider}")


client = get_client()


# ====================== LLM 调用 ======================
def llm_call(prompt: str, model: str = None) -> str:
#region  Notes  
    """
    # FlowBeast unified LLM call interface
    # Supports providers: qwen / openai / gemini
    # Returns the raw output as a JSON string,which is content under message.content
    """
#endregion 
    provider = settings.MODEL_PROVIDER.lower()
    target_model = model or settings.MODEL_NAME

    logger.info(f"LLM调用 | provider={provider} | model={target_model}")

    # ------------------ Gemini ------------------
    if provider == "gemini":
        response = client.models.generate_content(
            model=target_model,
            content=[
                {
                    "role": "user",
                    "parts": [
                        f"""
You are a top short-drama screenwriter.
You excel at creating conflict, planting hooks, and delivering extreme reversals.
Strictly output JSON including hook, conflict, emotion_curve, etc.
Do not provide any explanations or extra text.

{prompt}  
"""
                    ],
                }
            ],
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json",
            },
        )
        content = response.text

    # ------------------ Qwen / OpenAI ------------------
    else:
        # client must be an OpenAI instance
        kwargs = {
            "model": target_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a top short-drama screenwriter. You excel at creating conflict, "
                        "planting hooks, and delivering extreme reversals. "
                        "You must strictly output in JSON format, including hook, conflict, emotion_curve, etc. "
                        "Do not provide any explanation, only output a JSON object."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }

        # OpenAI special parameter, enable JSON output
        if "gpt" in target_model.lower():
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

    if not content:
        raise ValueError("❌ LLM response is empty")

    return content

# ====================== JSON 提取 ======================
def extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("❌ 未找到JSON结构")


# ====================== 核心生成 (集成 FP3 RAG) ======================
def generate_script(topic: str) -> dict:
    # --- 1. 获取基础 Prompt ---
    base_prompt = build_prompt(topic)

    # --- 2. FP3 爆款基因增强 ---
    try:
        from flowbeast.fp3.retriever import FP3Retriever
        from flowbeast.fp3.injector import inject_prompt
        
        logger.info(f"🔍 正在检索爆款基因: {topic[:15]}...")
        retriever = FP3Retriever()
        viral_examples = retriever.retrieve(topic, k=2)
        
        # 注入逻辑
        prompt = inject_prompt(base_prompt, viral_examples)
        logger.info(f"🚀 FP3 注入完成，检索到 {len(viral_examples)} 条案例")
    except Exception as e:
        logger.warning(f"⚠️ FP3 增强失败，回退到基础生成模式: {e}")
        prompt = base_prompt

    # --- 3. 循环重试生成 ---
    last_error = None
    raw_response = None

    for attempt in range(3):
        try:
            raw_response = llm_call(prompt)

            # ---------- 一级解析 ----------
            try:
                script = json.loads(raw_response)

            # ---------- 二级兜底 ----------
            except json.JSONDecodeError:
                logger.warning("⚠️ JSON解析失败，尝试提取结构")
                cleaned = extract_json(raw_response)
                script = json.loads(cleaned)

            # ---------- 结构校验 ----------
            if "scenes" not in script:
                raise ValueError("❌ JSON缺少 scenes 字段")

            # ---------- 返回结构升级 ----------
            return {
                "script": script,
                "meta": {
                    "topic": topic,
                    "provider": settings.MODEL_PROVIDER,
                    "model": settings.MODEL_NAME,
                    "timestamp": datetime.now().isoformat(),
                    "fp3_enhanced": True
                }
            }

        except Exception as e:
            logger.error(f"⚠️ 第 {attempt + 1} 次生成失败: {e}")

            if attempt == 2:
                logger.error(f"❌ 原始输出:\n{raw_response}")

            last_error = e

    raise ValueError(f"❌ 连续3次生成失败: {last_error}")


# ====================== Test entrance ========================================
if __name__ == "__main__":
    # 注意：运行此测试前请确保已运行 python -m scripts.init_fp3
    topic = "逆袭：开除我的女总裁跪求我回去"
    result = generate_script(topic)

    # 确保输出目录存在
    out_dir = settings.FLOWBEAST_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    # 生成文件名 (带时间戳)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '_')]).rstrip()
    file_path = os.path.join(out_dir, f"script_{timestamp}_{safe_topic}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.success(f"💾 剧本已自动保存至: {file_path}")
    # ---------------------------

    print(json.dumps(result, indent=2, ensure_ascii=False))
