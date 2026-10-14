"""
FlowBeast Provider Abstraction Layer — Protocol-based.

Each sub-module implements one API protocol:
  openai_compatible  — OpenAI chat format (qwen, openai, deepseek, openrouter, ollama, glm)
  anthropic_compatible — Anthropic messages format (Claude, Token Plan, etc.)
  gemini_provider    — Google GenAI format
  embedding          — Dense vector embeddings

Public API (stable):
  get_llm_client()  -> raw client instance
  llm_call(prompt)  -> unified LLM call
  embed_text(text)  -> unified embedding
"""

from typing import Optional
from loguru import logger

from flowbeast.core.config import settings
from . import openai_compatible, anthropic_compatible, gemini_provider, embedding


def get_llm_client():
    """Return a configured LLM client for the active provider.

    Returns openai.OpenAI, anthropic.Anthropic, or google.genai.Client
    depending on the active provider.
    """
    provider = settings.MODEL_PROVIDER.lower()

    if provider == "anthropic":
        return anthropic_compatible.create_client()
    if provider == "gemini":
        return gemini_provider.create_client()
    # All others are OpenAI-compatible
    return openai_compatible.create_client(provider)


def llm_call(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    json_mode: bool = False,
) -> str:
    """Unified LLM call across all providers.

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

    logger.info(f"LLM call | provider={provider} | model={target_model}")

    if provider == "anthropic":
        client = anthropic_compatible.create_client()
        return anthropic_compatible.chat(client, prompt, json_mode, temperature)

    if provider == "gemini":
        client = gemini_provider.create_client()
        return gemini_provider.chat(client, prompt, json_mode, temperature)

    # OpenAI-compatible
    client = openai_compatible.create_client(provider)
    return openai_compatible.chat(client, prompt, json_mode, temperature)


def embed_text(text: str) -> list:
    """Convert text to a dense embedding vector."""
    return embedding.embed_text(text)
