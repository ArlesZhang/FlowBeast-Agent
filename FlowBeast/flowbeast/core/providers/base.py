"""Shared utilities for all provider implementations."""

from flowbeast.core.config import settings


def build_drama_system_prompt(json_mode: bool) -> str:
    """Build the short-drama screenwriter system prompt."""
    if json_mode:
        return (
            "You are a top short-drama screenwriter. You excel at creating conflict, "
            "planting hooks, and delivering extreme reversals. "
            "You MUST strictly output ONLY valid JSON, with no explanation, no markdown fences, "
            "and no extra text. The entire response must be a single JSON object."
        )
    return "You are a helpful assistant."


def build_gemini_drama_prefix(json_mode: bool) -> str:
    """Build the Gemini-specific instruction prefix (injected into user content)."""
    if json_mode:
        return (
            "You are a top short-drama screenwriter. "
            "You excel at creating conflict, planting hooks, and delivering extreme reversals. "
            "Strictly output JSON including hook, conflict, emotion_curve, etc. "
            "Do not provide any explanations or extra text.\n\n"
        )
    return ""


def extract_anthropic_text(content) -> str:
    """Extract text from Anthropic response, skipping ThinkingBlock entries."""
    return "\n".join(
        block.text for block in content if hasattr(block, "text")
    )


def get_model_name(override: str | None) -> str:
    """Resolve the active model name."""
    return override or settings.MODEL_NAME
