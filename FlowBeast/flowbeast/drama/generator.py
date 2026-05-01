import json
import re
from datetime import datetime

from loguru import logger
from openai import OpenAI
import google.generativeai as genai

from flowbeast.core.config import settings
from flowbeast.drama.prompt import build_prompt

# ====================== Client 构建 ======================
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
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        return genai

    else:
        raise ValueError(f"❌ 不支持的模型提供商: {provider}")


client = get_client()


# ====================== LLM 调用 ======================
def llm_call(prompt: str, model: str = None) -> str:
    """
    FlowBeast 统一 LLM 调用接口
    支持 provider：qwen / openai / gemini
    返回 JSON 字符串（原始输出）
    """
    provider = settings.MODEL_PROVIDER.lower()
    target_model = model or settings.MODEL_NAME

    logger.info(f"🧠 LLM调用 | provider={provider} | model={target_model}")

    # ------------------ Gemini ------------------
    if provider == "gemini":
        # 避免全局污染，直接在这里 import
        import google.generativeai as genai

        # 确保已经用 API KEY 配置过
        if not getattr(settings, "GOOGLE_API_KEY", None):
            raise ValueError("❌ 未配置 GOOGLE_API_KEY")

        genai.configure(api_key=settings.GOOGLE_API_KEY)

        model_obj = genai.GenerativeModel(target_model)

        response = model_obj.generate_content(
            f"""
你是顶级短视频爽剧编剧。
你擅长制造冲突、埋设钩子(Hook)和极致反转。
必须严格输出 JSON，包含 hook, conflict, emotion_curve 等字段。
不要任何解释或额外文本。

{prompt}
""",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json",  # 确保输出 JSON
            ),
        )
        content = response.text

    # ------------------ Qwen / OpenAI ------------------
    else:
        # client 必须是 OpenAI 实例
        kwargs = {
            "model": target_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是顶级短视频爽剧编剧。你擅长制造冲突、埋设钩子(Hook)和极致反转。"
                        "必须严格按照 JSON 格式输出，包含 hook, conflict, emotion_curve 等字段。"
                        "不要任何解释，只输出符合格式 of JSON 对象。"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }

        # OpenAI 特殊参数，启用 JSON 输出
        if "gpt" in target_model.lower():
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

    if not content:
        raise ValueError("❌ LLM 返回为空")

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


# ====================== 测试入口 ======================
if __name__ == "__main__":
    # 注意：运行此测试前请确保已运行 python -m scripts.init_fp3
    topic = "逆袭：开除我的女总裁跪求我回去"
    result = generate_script(topic)

    # --- 新增：自动保存 logic ---
    import os
    from flowbeast.core.config import settings

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
