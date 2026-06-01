# FlowBeast — Project Overview

**Identity:** Viral Prompt Compiler. Input: topic. Output: `prompt_package.json` (structured recipe for AI video tools: Seedance, Kling, HeyGen).

**Core moat:** FP3 (Viral Memory System) — composable narrative atoms + VTO operators + QualityGate. The production pipeline (script → audio → video) is a replaceable commodity layer.

**Core hypothesis:** Viral structure retrieval + structure transfer (GRAFT) → structurally differentiated script generation. A human observer must clearly distinguish Original vs GRAFT-enhanced generation.

**Pipeline:**
```
topic → FP3 retrieval → LLM script → QualityGate → shots → prompt_package.json → (audio validation)
```

**Key files:**
- `main.py` — CLI entry point, `run_full_pipeline()`
- `flowbeast/drama/pipeline.py` — orchestrates the pipeline
- `flowbeast/drama/generator.py` — LLM script generation with FP3 context
- `flowbeast/fp3/` — FP3 memory system (store, retriever, schema, seed_data, feedback)
- `flowbeast/vto/graft.py` — GRAFT operator (hook + conflict extraction + structural transfer)
- `flowbeast/observe/quality/` — QualityGate (scorer, dedup, gate decision)
- `flowbeast/api/main.py` — FastAPI wrapper (POST /api/v1/generate)
- `flowbeast/demo/app.py` — Streamlit demo UI
- `assets/style/` — Style Lock assets (visual style, negative prompt, color palette, render rules)

**Package manager:** `uv` (not pip). `uv sync`, `uv run pytest`, `uv run ...`

**Test command:** `uv run pytest tests/ -q` (57 tests, all passing)
