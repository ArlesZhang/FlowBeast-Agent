"""Text embedding implementations."""

from flowbeast.core.config import settings


def embed_text(text: str) -> list:
    """Convert text to a dense embedding vector.

    Routing:
    - gemini:  models/embedding-001  (1536-d)
    - openai:  text-embedding-3-small (1536-d)
    - qwen:    text-embedding-v3      (1024-d)
    - ollama:  nomic-embed-text       (768-d, local, no API key)
    """
    provider = settings.EMBED_PROVIDER.lower()
    target_model = settings.EMBED_MODEL

    if provider == "ollama":
        import httpx
        from openai import OpenAI

        # OLLAMA_BASE_URL is the Docker address; on host use localhost directly
        base = settings.OLLAMA_BASE_URL
        if "host.docker.internal" in base:
            base = "http://localhost:11434"
        client = OpenAI(
            api_key="ollama",
            base_url=base + "/v1",
            http_client=httpx.Client(transport=httpx.HTTPTransport(retries=1)),
        )
        resp = client.embeddings.create(model=target_model, input=text)
        return resp.data[0].embedding

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
