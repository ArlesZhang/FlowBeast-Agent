import os
import json
import re
from datetime import datetime

from loguru import logger

from flowbeast.core.config import settings
from flowbeast.core.providers import llm_call
from flowbeast.drama.prompt import build_prompt


# ====================== JSON 提取 ======================
def extract_json(text: str) -> str:
    """从 LLM 原始输出中提取 JSON 块（容错 markdown 包裹等）。"""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("未找到JSON结构")


# ====================== 核心生成 (集成 FP3 RAG) ======================
def generate_script(topic: str) -> dict:
    # --- 1. 获取基础 Prompt ---
    base_prompt = build_prompt(topic)

    # --- 2. FP3 爆款基因增强 ---
    fp3_used = False
    try:
        from flowbeast.fp3.retriever import FP3Retriever
        from flowbeast.fp3.injector import inject_prompt

        logger.info(f"🔍 正在检索爆款基因: {topic[:15]}...")
        retriever = FP3Retriever()
        viral_examples = retriever.retrieve(topic, k=2)

        if viral_examples:
            prompt = inject_prompt(base_prompt, viral_examples)
            fp3_used = True
            logger.info(f"🚀 FP3 注入完成，检索到 {len(viral_examples)} 条案例")
        else:
            prompt = base_prompt
            logger.info("FP3 检索结果为空，使用基础 prompt")
    except Exception as e:
        logger.warning(f"⚠️ FP3 增强失败，回退到基础生成模式: {e}")
        prompt = base_prompt

    # --- 3. 循环重试生成 ---
    last_error = None
    raw_response = None

    for attempt in range(3):
        try:
            raw_response = llm_call(prompt, json_mode=True)

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
                raise ValueError("JSON缺少 scenes 字段")

            # ---------- 返回结构升级 ----------
            return {
                "script": script,
                "meta": {
                    "topic": topic,
                    "provider": settings.MODEL_PROVIDER,
                    "model": settings.MODEL_NAME,
                    "timestamp": datetime.now().isoformat(),
                    "fp3_enhanced": fp3_used,
                },
            }

        except Exception as e:
            logger.error(f"⚠️ 第 {attempt + 1} 次生成失败: {e}")

            if attempt == 2:
                logger.error(f"❌ 原始输出:\n{raw_response}")

            last_error = e

    raise ValueError(f"连续3次生成失败: {last_error}")


# ====================== Test entrance ========================================
if __name__ == "__main__":
    topic = "逆袭：开除我的女总裁跪求我回去"
    result = generate_script(topic)

    out_dir = settings.FLOWBEAST_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '_')]).rstrip()
    file_path = os.path.join(out_dir, f"script_{timestamp}_{safe_topic}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.success(f"💾 剧本已自动保存至: {file_path}")

    print(json.dumps(result, indent=2, ensure_ascii=False))
