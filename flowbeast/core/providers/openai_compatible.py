"""OpenAI-compatible provider protocol (qwen, openai, deepseek, openrouter, ollama, glm)."""

from openai import OpenAI
from loguru import logger

from flowbeast.core.config import settings
from .base import build_drama_system_prompt, get_model_name


# Registry: vendor_name -> config
_OPENAI_VENDORS = {
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
        "api_key": lambda: "ollama",
        "base_url": lambda: settings.OLLAMA_BASE_URL,
    },
    "glm": {
        "api_key": lambda: settings.GLM_API_KEY,
        "base_url": lambda: "https://open.bigmodel.cn/api/paas/v4",
    },
}


def create_client(vendor: str) -> OpenAI:
    """Create an OpenAI-compatible client for the given vendor."""
    if vendor not in _OPENAI_VENDORS:
        raise ValueError(f"Unknown OpenAI-compatible vendor: {vendor}")

    cfg = _OPENAI_VENDORS[vendor]
    api_key = cfg["api_key"]()
    base_url = cfg["base_url"]()

    if not api_key:
        raise ValueError(
            f"API key not configured for vendor '{vendor}'. "
            f"Set the appropriate *_API_KEY in .env."
        )

    kwargs: dict = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def chat(
    client: OpenAI,
    prompt: str,
    json_mode: bool,
    temperature: float,
) -> str:
    """Execute a chat completion via OpenAI-compatible API."""
    system_msg = build_drama_system_prompt(json_mode)

    kwargs: dict = {
        "model": get_model_name(None),
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


def supports_embed(vendor: str) -> bool:
    """Check if this vendor supports embeddings."""
    return vendor in ("openai", "qwen")


def create_embed_client(vendor: str) -> OpenAI:
    """Create an OpenAI client configured for embeddings."""
    if vendor == "qwen":
        return OpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.DASHSCOPE_BASE_URL,
        )
    if vendor == "openai":
        return OpenAI(api_key=settings.OPENAI_API_KEY)
    raise ValueError(f"Vendor '{vendor}' does not support OpenAI embeddings")
