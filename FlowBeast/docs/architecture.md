# Architecture

FlowBeast consists of two core engines working together:

## IP2 — Drama Generation Layer (`flowbeast/drama/`)

Generates viral short-drama scripts via LLM calls.

### Components

- **`pipeline.py`**: Top-level orchestrator
- **`generator.py`**: Builds LLM prompts, calls vendor API
- **`prompt.py`**: Structured prompt templates
- **`audio.py`**: Converts dialogue to MP3
- **`schema.py`**: TypedDict definitions

```
topic → build_prompt() → FP3Retriever() → inject_prompt() → generate_script()
                                          ↓
                                   (LLM call)
                                          ↓
                                 script.json + audio → report.json
```

## FP3 — Viral Gene Knowledge Base (`flowbeast/fp3/`)

RAG layer that enriches prompts with retrieved viral patterns.

### Components

- **`store.py`**: FAISS-backed vector search
- **`retriever.py`**: Topic → vector → search
- **`embedding.py`**: Text → vector via Qwen
- **`injector.py`**: Inject ViralUnit examples into prompt
- **`builder.py`**: Build knowledge base from seed data
- **`feedback.py`**: Feed successful scripts back into KB

## LLM Routing (`flowbeast/core/config.py`)

`ACTIVE_VENDOR` env var selects the provider:

| Provider | Model | API Key |
|----------|-------|---------|
| Gemini | gemini-1.5-flash | `GOOGLE_API_KEY` |
| Qwen | qwen-plus | `DASHSCOPE_API_KEY` |
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| OpenRouter | auto | `OPENROUTER_API_KEY` |
| Ollama | local | - |

## Data Flow

```
Natural Language Prompt
         ↓
  compile_workflow()     [flowbeast/agent/compiler.py]
         ↓
    DataWorkflow (IR)    [flowbeast/ir/models.py]
         ↓
  generate_code()        [flowbeast/agent/codegen.py]
         ↓
   Python Code Output
```

## Key Data Structures

### drama/schema.py

```python
Script: title, genre, core_hook, scenes: List[Scene]
Scene: id, hook, conflict, emotion_curve, dialogue: List[Dialogue]
Dialogue: speaker, text, emotion, intensity
```

### fp3/schema.py

```python
ViralUnit: hook: str, pattern: str, emotion: List[str]
```
