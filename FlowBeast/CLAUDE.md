# CLAUDE.md

> This project uses Cursor Rules - see [.cursor/rules/](./.cursor/rules/) for detailed development guidelines.

FlowBeast is a **Viral Prompt Compiler**: input a topic, output a complete prompt package (`prompt_package.json`) ready for AI video tools (Seedance, Kling, HeyGen). The core moat is the **FP3 Viral Memory System** — composable narrative atoms + VTO operators + QualityGate. The production pipeline (script → audio → video) is a replaceable commodity layer.

For current status, goals, and task breakdowns, see `.ai/`.


## Language Policy (STRICT)

You MUST always respond in English. This applies to: explanations, code comments, commit messages, debug output, any generated text. DO NOT use Chinese unless the user explicitly requests it. If the user writes in another language, you STILL respond in English.


## Commands

```bash
uv sync                                              # Install dependencies (uv, not pip)
python main.py                                       # Run drama generation pipeline
uvicorn flowbeast.api.main:app --reload --port 8000  # FastAPI server
uv run python -m flowbeast.fp3.seed_data             # Seed FP3 (ViralUnit + PromptAtom)
uv run python -m flowbeast.fp3.feedback_ingest \     # Feedback ingest
  --report production_report.json --views N --likes N
uv run pytest tests/ -q                              # Run all tests
uv run pytest tests/test_fp3_quality.py -q           # Run single test file
docker-compose up --build                           # Docker
```


## Package Manager

This project uses **`uv`** (not pip). Always use `uv sync` to install dependencies and `uv run` to execute scripts. Do not use `pip install`.


## Core File Header Docstrings

Every core module file must begin with a module-level docstring:

```python
"""
FP3 Store: FAISS-backed vector storage for viral content patterns.

Role: Saves, loads, and searches ViralUnit/ViralScript embeddings.
Provides k-nearest-neighbor search for RAG retrieval.

Workflow: builder.py → add() → save() / load() ← retriever.py
"""
```

State: (1) what it is, (2) role + boundaries, (3) upstream/downstream connections.


## Context Priority

When multiple sources conflict, prioritize:

1. Existing repository architecture
2. CLAUDE.md instructions
3. `.cursor/rules/`
4. Existing code patterns
5. User request
6. General framework conventions


## Goal-Driven Workflow

When working on a specific task:

1. Read `.ai/goals/current_goal.md` to understand the current phase
2. Read `.ai/status/current_status.md` to see what's wired vs stub
3. Read `.ai/decisions/002_what_we_do_not_do.md` to avoid scope creep
4. Pick the next task from `.ai/tasks/` (ordered by priority)
5. Execute. Do not propose work outside the current phase.
