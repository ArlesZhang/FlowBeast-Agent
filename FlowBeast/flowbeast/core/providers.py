"""
FlowBeast Provider Abstraction Layer.

Single source of truth for LLM client creation, LLM calls, and embedding.
Supports: qwen, openai, gemini, deepseek, openrouter, ollama, glm.

Usage:
    from flowbeast.core.providers import get_llm_client, llm_call, embed_text

    # Get raw client for advanced use
    client = get_llm_client()

    # Unified LLM call
    text = llm_call("Your prompt here", temperature=0.7)

    # Unified embedding
    vec = embed_text("some text")
"""

from typing import Optional
from loguru import logger

from flowbeast.core.config import settings


# ====================== OpenAI-compatible providers ======================
# qwen, openai, deepseek, openrouter, ollama, glm all support the OpenAI chat API.

_OPENAI_COMPATIBLE = {
    "qwen": {
        "api_key": lambda: settings.DASHSCOPE_API_KEY,
        "base_url": lambda: settings.DASHSCOPE_BASE_URL,
    },
    "openai": {
        "api_key": lambda: settings.OPENAI_API_KEY,
        "base_url": lambda: None,
    },
    "deepseek": {
        "api_key": lambda: settings.DEEPSEEK_API_KEY,
        "base_url": lambda: "https://api.deepseek.com/v1",
    },
    "openrouter": {
        "api_key": lambda: settings.OPENROUTER_API_KEY,
        "base_url": lambda: settings.OPENROUTER_BASE_URL,
    },
    "ollama": {
        "api_key": lambda: "ollama",  # dummy key
        "base_url": lambda: settings.OLLAMA_BASE_URL,
    },
    "glm": {
        "api_key": lambda: settings.GLM_API_KEY,
        "base_url": lambda: "https://open.bigmodel.cn/api/paas/v4",
    },
}


def get_llm_client():
    """
    Return a configured LLM client for the active provider.

    - OpenAI-compatible providers (qwen, openai, deepseek, openrouter, ollama, glm):
      returns an `openai.OpenAI` instance.
    - gemini: returns a `google.genai.Client` instance.
    """
    provider = settings.MODEL_PROVIDER.lower()

    if provider == "gemini":
        from google import genai
        if not getattr(settings, "GOOGLE_API_KEY", None):
            raise ValueError("GOOGLE_API_KEY is not configured for gemini provider")
        return genai.Client(api_key=settings.GOOGLE_API_KEY)

    if provider in _OPENAI_COMPATIBLE:
        from openai import OpenAI
        cfg = _OPENAI_COMPATIBLE[provider]
        api_key = cfg["api_key"]()
        base_url = cfg["base_url"]()
        if not api_key:
            raise ValueError(
                f"API key not configured for provider '{provider}'. "
                f"Set the appropriate *_API_KEY in .env."
            )
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        return OpenAI(**kwargs)

    raise ValueError(f"Unsupported LLM provider: {provider}")


def llm_call(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    json_mode: bool = False,
) -> str:
    """
    Unified LLM call across all providers.

    Args:
        prompt: User prompt content.
        model: Override model name (default: settings.MODEL_NAME).
        temperature: Sampling temperature.
        json_mode: If True, request JSON-only output.

    Returns:
        Raw response text string.
    """
    provider = settings.MODEL_PROVIDER.lower()
    target_model = model or settings.MODEL_NAME
    client = get_llm_client()

    logger.info(f"LLM调用 | provider={provider} | model={target_model}")

    if provider == "gemini":
        response = client.models.generate_content(
            model=target_model,
            content=[
                {
                    "role": "user",
                    "parts": [
                        "You are a top short-drama screenwriter. "
                        "You excel at creating conflict, planting hooks, and delivering extreme reversals. "
                        "Strictly output JSON including hook, conflict, emotion_curve, etc. "
                        "Do not provide any explanations or extra text.\n\n" + prompt,
                    ],
                },
            ],
            generation_config={
                "temperature": temperature,
                "response_mime_type": "application/json" if json_mode else None,
            },
        )
        content = response.text

    else:
        # OpenAI-compatible
        system_msg = (
            "You are a top short-drama screenwriter. You excel at creating conflict, "
            "planting hooks, and delivering extreme reversals. "
            "You must strictly output in JSON format, including hook, conflict, emotion_curve, etc. "
            "Do not provide any explanation, only output a JSON object."
            if json_mode
            else "You are a helpful assistant."
        )

        kwargs = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

    if not content:
        raise ValueError("LLM response is empty")

    return content


# ====================== Embedding ======================

def embed_text(text: str) -> list:
    """
    Convert text to a dense embedding vector.

    Routing:
    - gemini:  models/embedding-001  (1536-d)
    - openai:  text-embedding-3-small (1536-d)
    - qwen:    text-embedding-v3      (1024-d)
    - fallback: None (raises)
    """
    provider = settings.EMBED_PROVIDER.lower()
    target_model = settings.EMBED_MODEL

    if provider == "gemini":
        from google import genai
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        result = client.models.embed_content(
            model=target_model,
            contents=text,
            config={"task_type": "retrieval_query"},
        )
        return result["embeddings"][0]["values"]

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        resp = client.embeddings.create(model=target_model, input=text)
        return resp.data[0].embedding

    if provider == "qwen":
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.DASHSCOPE_BASE_URL,
        )
        resp = client.embeddings.create(model=target_model, input=text)
        return resp.data[0].embedding

    raise ValueError(f"Unsupported embedding provider: {provider}")
