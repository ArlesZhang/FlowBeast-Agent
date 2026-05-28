"""Anthropic-compatible provider protocol (Claude via Anthropic SDK).

Used for:
- Direct Anthropic API (api.anthropic.com)
- Proxy gateways that expose Anthropic-compatible endpoints
  (e.g., Token Plan, SiliconFlow Claude proxy, etc.)
"""

from anthropic import Anthropic
from loguru import logger

from flowbeast.core.config import settings
from .base import build_drama_system_prompt, extract_anthropic_text, get_model_name


def create_client() -> Anthropic:
    """Create an Anthropic-compatible client."""
    api_key = getattr(settings, "ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured for anthropic provider")

    kwargs: dict = {"api_key": api_key}
    base_url = getattr(settings, "ANTHROPIC_BASE_URL", None)
    if base_url:
        kwargs["base_url"] = base_url
    return Anthropic(**kwargs)


def chat(
    client: Anthropic,
    prompt: str,
    json_mode: bool,
    temperature: float,
) -> str:
    """Execute a message via Anthropic-compatible API."""
    system_msg = build_drama_system_prompt(json_mode)

    response = client.messages.create(
        model=get_model_name(None),
        system=system_msg,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=8192,
        thinking={"type": "disabled"},
    )

    content = extract_anthropic_text(response.content)
    if not content:
        raise ValueError("LLM response is empty")
    return content
