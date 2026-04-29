# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

```bash
# Run tests
uv run pytest tests/ -q

# Run single test file
uv run pytest tests/test_codegen.py -q

# Run config validation (mocked, no LLM calls)
uv run python scripts/test_main_script.py

# Run main entry point
uv run python main.py

# Format code
uv run black flowbeast/
```

## Architecture Overview

### High-Level Flow

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
                                    (LLM call via Qwen)
                                           ↓
                                  script.json + audio → report.json
```

### FP3 System (Burst Content Knowledge Base)

- **WRITE**: `ViralUnit` → `embed_unit()` → `FP3Store.add()` → `save()`
- **READ**: `embed_text()` → `FP3Store.search()` → return similar examples
- **Location**: `flowbeast/data/outputs/vector_store/fp3/`
  - `fp3.index` - FAISS vector index
  - `fp3_meta.json` - Metadata storage

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point: FP3 seeding + run_full_pipeline |
| `flowbeast/drama/pipeline.py` | run_full_pipeline(): script + audio + report |
| `flowbeast/drama/generator.py` | generate_script(): LLM + FP3 RAG |
| `flowbeast/agent/compiler.py` | compile_workflow(): NL → IR |
| `flowbeast/agent/codegen.py` | generate_code(): IR → Python |
| `flowbeast/core/config.py` | settings singleton, path initialization |

### Configuration

- **Model Provider**: `settings.MODEL_PROVIDER` (qwen/openai/gemini)
- **Model Name**: `settings.MODEL_NAME` (default: qwen-turbo)
- **Output Directory**: `settings.FLOWBEAST_OUTPUT_DIR`
- **FP3 Paths**: `settings.FP3_INDEX_PATH`, `settings.FP3_META_PATH`

### Testing Strategy

- **tests/test_codegen.py**: Code generation structure validation
- **tests/test_compiler.py**: IR compilation tests
- **tests/test_main.py**: Entry point logic (mocked, no LLM)
- **scripts/test_main_script.py**: Quick main.py validation
- **tests/full_pipeline_test.py**: Full pipeline integration test (slow, requires LLM)
