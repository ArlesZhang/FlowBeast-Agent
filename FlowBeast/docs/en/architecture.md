# Architecture

FlowBeast consists of two core engines working together:

## IP2 — Drama Generation Layer (`flowbeast/drama/`)

Generates viral short-drama scripts via LLM calls.

## FP3 — Viral Gene Knowledge Base (`flowbeast/fp3/`)

RAG layer that enriches prompts with retrieved viral patterns.

## LLM Routing (`flowbeast/core/config.py`)

| Provider | Model | API Key |
|----------|-------|---------|
| Gemini | gemini-1.5-flash | `GOOGLE_API_KEY` |
| Qwen | qwen-plus | `DASHSCOPE_API_KEY` |
| OpenAI | gpt-4o | `OPENAI_API_KEY` |

## Key Data Structures

```python
# drama/schema.py
Script: title, genre, core_hook, scenes: List[Scene]
Scene: id, hook, conflict, emotion_curve, dialogue: List[Dialogue]

# fp3/schema.py
ViralUnit: hook: str, pattern: str, emotion: List[str]
```
