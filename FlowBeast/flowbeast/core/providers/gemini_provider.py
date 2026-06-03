"""Google Gemini provider protocol."""

from google import genai
from loguru import logger

from flowbeast.core.config import settings
from .base import build_gemini_drama_prefix, get_model_name


def create_client():
    """Create a Google GenAI client."""
    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not configured for gemini provider")
    return genai.Client(api_key=api_key)


def chat(
    client,
    prompt: str,
    json_mode: bool,
    temperature: float,
) -> str:
    """Generate content via Gemini API."""
    prefix = build_gemini_drama_prefix(json_mode)

    response = client.models.generate_content(
        model=get_model_name(None),
        content=[
            {
                "role": "user",
                "parts": [prefix + prompt],
            },
        ],
        generation_config={
            "temperature": temperature,
            "response_mime_type": "application/json" if json_mode else None,
        },
    )
    content = response.text
    if not content:
        raise ValueError("LLM response is empty")
    return content


def create_embed_client():
    """Create a Gemini embedding client."""
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    return client
