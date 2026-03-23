import os
import json
import re
from openai import OpenAI
from flowbeast.drama.prompt import build_prompt


def get_client(provider="openai"):
    if provider == "qwen":
        return OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        ), "qwen-max"

    return OpenAI(api_key=os.getenv("OPENAI_API_KEY")), "gpt-4o-mini"


client, DEFAULT_MODEL = get_client(provider="qwen")


def llm_call(prompt: str, model: str = None) -> str:
    target_model = model or DEFAULT_MODEL

    kwargs = {
        "model": target_model,
        "messages": [
            {
                "role": "system",
                "content": "你是短视频爽剧编剧。必须只输出JSON对象，不要任何解释或额外文本。"
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    # 仅 OpenAI 启用 JSON mode
    if "gpt" in target_model:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("未找到JSON结构")


def generate_script(topic: str) -> dict:
    prompt = build_prompt(topic)

    last_error = None
    raw_response = None

    for attempt in range(3):
        try:
            raw_response = llm_call(prompt)

            try:
                return json.loads(raw_response)
            except json.JSONDecodeError:
                cleaned = extract_json(raw_response)
                return json.loads(cleaned)

        except Exception as e:
            print(f"⚠️ 第 {attempt + 1} 次失败: {e}")
            if attempt == 2:
                print("原始输出：\n", raw_response)
            last_error = e

    raise ValueError(f"连续3次生成失败: {last_error}")


if __name__ == "__main__":
    res = generate_script("逆袭：开除我的女总裁跪求我回去")
    print(json.dumps(res, indent=2, ensure_ascii=False))
