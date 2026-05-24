"""
Drama Generator: produces viral short-drama scripts via LLM calls.

Role: Builds prompt (with FP3 RAG injection), calls the active LLM vendor
(gemini/qwen/openai/openrouter/ollama), parses JSON output into Script
schema. The ONLY connection point between FP3 knowledge base and drama
generation — FP3 examples are retrieved and injected here.

Workflow: topic → build_prompt() → FP3Retriever.retrieve() → inject_prompt() → llm_call() → parse
"""

import os
import json
import re
import asyncio
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


# ====================== 结构校验 ======================
def validate_script_structure(script: dict) -> list[str]:
    """Validate generated script has all required fields. Returns list of issues."""
    issues = []
    if not script.get("title"):
        issues.append("missing title")
    if not script.get("core_hook"):
        issues.append("missing core_hook")
    if not isinstance(script.get("scenes"), list):
        issues.append("scenes is not a list")
    elif len(script["scenes"]) < 3:
        issues.append(f"too few scenes: {len(script['scenes'])} (need >= 3)")
    else:
        for i, scene in enumerate(script["scenes"]):
            if not isinstance(scene.get("dialogue"), list):
                issues.append(f"scene {i}: missing dialogue list")
            elif len(scene.get("dialogue", [])) == 0:
                issues.append(f"scene {i}: empty dialogue")
            for j, line in enumerate(scene.get("dialogue", [])):
                if not line.get("text"):
                    issues.append(f"scene {i}, line {j}: empty text")
    return issues


# ====================== 核心生成 (集成 FP3 RAG + 实时热点) ======================
def generate_script(
    topic: str,
    auto_trend: bool = True,
) -> dict:
    # --- 1. 获取基础 Prompt (含实时热点注入) ---
    trend_context = None
    if auto_trend:
        try:
            from flowbeast.drama.trending import fetch_trending_context

            logger.info("🔥 正在抓取实时热搜...")
            trend_context = asyncio.run(fetch_trending_context())
            if trend_context.topics:
                logger.info(f"🔥 获取到 {len(trend_context.topics)} 条热搜话题")
            else:
                logger.warning("⚠️ 实时热搜为空，使用纯话题生成")
                trend_context = None
        except Exception as e:
            logger.warning(f"⚠️ 实时热搜抓取失败，使用纯话题生成: {e}")
            trend_context = None

    base_prompt = build_prompt(
        topic=topic,
        trend_context=trend_context.creative_brief() if trend_context else None,
    )

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
            logger.info("FP3 检索结果为空，使用增强 prompt")
    except Exception as e:
        logger.warning(f"⚠️ FP3 增强失败，使用增强 prompt: {e}")
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
            issues = validate_script_structure(script)
            if issues:
                raise ValueError(f"结构校验失败: {', '.join(issues)}")

            # ---------- 返回结构升级 ----------
            return {
                "script": script,
                "meta": {
                    "topic": topic,
                    "provider": settings.MODEL_PROVIDER,
                    "model": settings.MODEL_NAME,
                    "timestamp": datetime.now().isoformat(),
                    "fp3_enhanced": fp3_used,
                    "trend_enhanced": bool(trend_context and trend_context.topics),
                },
            }

        except Exception as e:
            logger.error(f"⚠️ 第 {attempt + 1} 次生成失败: {e}")
            last_error = e

    logger.error(f"❌ 原始输出:\n{raw_response}")
    raise ValueError(f"连续3次生成失败: {last_error}")


# ====================== Test entrance ========================================
if __name__ == "__main__":
    topic = "逆袭：开除我的女总裁跪求我回去"
    result = generate_script(topic, auto_trend=True)

    out_dir = settings.FLOWBEAST_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '_')]).rstrip()
    file_path = os.path.join(out_dir, f"script_{timestamp}_{safe_topic}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.success(f"💾 剧本已自动保存至: {file_path}")

    print(json.dumps(result, indent=2, ensure_ascii=False))
