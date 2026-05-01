# CLAUDE.md

 @README.md 

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

  

## Project Overview

  

**FlowBeast** is an AI-powered short-form drama content generation engine. The core pipeline is: **Topic → Viral Script (JSON) → Audio → Video-ready output**.

  

Current phase: **v0.3.2** (FP3 Quality Control). The system uses RAG (FP3 knowledge base) to inject viral patterns into LLM prompts for generating hook-driven short drama scripts.

  

## Commands

  

```bash

# Install dependencies (uses uv, not pip)
uv sync

# Run the main drama generation pipeline
python main.py
  
# Run the FastAPI server (hot reload)
uvicorn flowbeast.api.main:app --reload --port 8000

# Initialize the FP3 vector knowledge base (first-time setup)
python -m scripts.init_fp3

# Process generation feedback and update FP3 knowledge base
python scripts/feedback_loop.py --dir ./flowbeast/data/outputs --yes


# Run a single test file
pytest tests/full_pipeline_test.py

# Run tests
uv run pytest tests/ -q

# Run single test file
uv run pytest tests/test_codegen.py -q

# Run config validation (mocked, no LLM calls)
uv run python scripts/test_main_script.py

# Docker
docker-compose up --build

```

  

## Architecture

  

The system has two core engines working together:

  

### IP2 — Drama Generation Layer (`flowbeast/drama/`)

Generates viral short-drama scripts via LLM calls. The main components:

- `pipeline.py`: Top-level orchestrator — calls generator, saves JSON, triggers audio

- `generator.py`: Builds the LLM prompt (with FP3 injection), calls the active vendor, parses JSON output

- `prompt.py`: The structured prompt template for hook-driven storytelling

- `audio.py`: Converts dialogue lines to MP3 (Edge TTS primary, ElevenLabs premium)

- `schema.py`: TypedDict definitions — `Script → [Scene] → [Dialogue]`

  

### FP3 — Viral Gene Knowledge Base (`flowbeast/fp3/`)

RAG layer that enriches prompts with retrieved viral patterns:

- `store.py` / `retriever.py`: FAISS-backed vector search

- `embedding.py`: Text → vector via sentence-transformers

- `injector.py`: Injects retrieved `ViralUnit` examples into the prompt

- `feedback.py`: Feeds successful scripts back into the knowledge base


### LLM Routing (`flowbeast/core/config.py`)

`ACTIVE_VENDOR` env var selects the provider. Default: `gemini` (`gemini-1.5-flash`). Supported: `gemini`, `qwen`, `openai`, `openrouter`, `ollama`.

  

### Data Flow

```
Natural Language Prompt
         ↓
  compile_workflow()      [flowbeast/agent/compiler.py]
         ↓
    DataWorkflow (IR)     [flowbeast/ir/models.py]
         ↓
  generate_code()         [flowbeast/agent/codegen.py]
         ↓
   Python Code Output
```

### Drama Pipeline (Video Content Generation)

```
topic → build_prompt() → FP3Retriever → inject_prompt() → generate_script()
                                           ↓
                                    (LLM call via Qwen or Claude Sonnet4.6 and so on)
                                           ↓
                                  script.json + audio → report.json
```


  ### Testing Strategy

- **tests/test_codegen.py**: Code generation structure validation
- **tests/test_compiler.py**: IR compilation tests
- **tests/test_main.py**: Entry point logic (mocked, no LLM)
- **scripts/test_main_script.py**: Quick main.py validation
- **tests/full_pipeline_test.py**: Full pipeline integration test (slow, requires LLM)

## Configuration

  

All configuration is in `.env` (gitignored; see `.env.example`):

- `ACTIVE_VENDOR` — LLM provider (`gemini` default)

- `GOOGLE_API_KEY`, `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`

- `FLOWBEAST_OUTPUT_DIR` — where scripts/audio land

- `FLOWBEAST_VECTOR_DIR` — FAISS index location

  

`flowbeast/core/config.py` uses `pydantic-settings` to load these and auto-creates required directories on startup.

  

## Key Data Structures

```python

# drama/schema.py

Script: title, genre, core_hook, scenes: List[Scene]

Scene: id, hook, conflict, emotion_curve, dialogue: List[Dialogue]

Dialogue: speaker, text, emotion, intensity


# fp3/schema.py

ViralUnit: hook: str, pattern: str, emotion: List[str]

```
  

## Package Manager
  
This project uses **`uv`** (not pip). Always use `uv sync` to install dependencies and `uv run` to execute scripts when inside Docker. Do not use `pip install`.

## Agent/Compiler Layer (`flowbeast/agent/`, `flowbeast/compiler/`)

These modules (`compiler.py`, `codegen.py`) are a separate sub-system for NL → IR → Python (Pandas) workflow compilation. They are not part of the drama generation pipeline — they power the `/v1/execute` API endpoint for data transformation use cases.


## Testing Notes

Tests in `tests/` cover the agent/compiler layer (NL→IR→Pandas codegen) rather than the drama pipeline. The drama pipeline is tested via `tests/full_pipeline_test.py` as an E2E flow. Test runs require valid API keys in `.env`.