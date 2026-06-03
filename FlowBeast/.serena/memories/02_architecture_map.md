# Architecture Map — Module Structure & Data Flow

## Layer 1: Core (`flowbeast/core/`)
- `config.py` — Central settings via pydantic-settings. All config goes through `settings` singleton. Key paths: `FP3_INDEX_PATH`, `FP3_META_PATH`, `OUTPUTS_DIR`, `VECTOR_STORE_PATH`.
- `providers/` — LLM provider abstractions (OpenAI-compatible, Anthropic-compatible, Gemini, embedding). Use `base.py` interface.

## Layer 2: FP3 (`flowbeast/fp3/`)
- `schema.py` — ViralUnit, ViralScript, HookStructure, ConflictPattern, EmotionalCurve, PacingProfile, CharacterArchetype
- `prompt_atom.py` — PromptAtom (Pydantic schema, NOT used in composition — see 03_hard_boundaries)
- `store.py` — FAISS vector storage for ViralUnit/ViralScript
- `retriever.py` — k-nearest-neighbor search against FP3
- `builder.py` — Constructs FP3 from data
- `injector.py` — Injects retrieved context into prompt
- `seed_data.py` — Seeds FP3 with ViralUnit + PromptAtom
- `feedback.py` — Extracts ViralUnit from generated script JSON
- `feedback_ingest.py` — Engagement metrics → virality score → atom weight boosting

## Layer 3: Drama (`flowbeast/drama/`)
- `pipeline.py` — Orchestrates: topic → script → shots → prompt_package → audio
- `generator.py` — LLM script generation with FP3 context injection, `extract_json()`, `validate_script_structure()`
- `prompt.py` — `build_prompt()` with 爽文 rules, NARRATIVE_STRUCTURES
- `schema.py` — Drama-related Pydantic models
- `shot_director.py` — Beat_type-driven shot list generation (504 lines)
- `asset_manager.py` — StyleLock, character/scene asset loading, `build_visual_prompt()`, `export_prompt_package()`
- `audio.py`, `audio_assembly.py` — Edge TTS audio generation (quality check layer)
- `trending.py` — Trending topic detection

## Layer 4: VTO (`flowbeast/vto/`)
- `graft.py` — GRAFT operator: extract hook/conflict from ViralScript, structural transfer to new topic

## Layer 5: Quality (`flowbeast/observe/quality/`)
- `scorer.py` — 9-dim RuleBasedScorer
- `dedup.py` — EmbeddingDeduplicator
- `gate.py` — Gate decision (ACCEPT/REVIEW/REJECT)
- `config.py`, `models.py`, `calibrator.py` — Quality configuration and models

## Layer 6: Reverse (`flowbeast/reverse/`)
- `reverse_engineer.py` — Analyze generated script back into ViralScript anatomy

## Layer 7: Hooks (`flowbeast/hooks/`)
- `hook_runner.py` — Pre-commit hook execution
- `fp3_guard.py` — FP3 integrity checks
- `import_checker.py` — Architecture enforcement (config centralization)

## Layer 8: API & Demo
- `api/main.py` — FastAPI: health check, generation endpoint (pending)
- `demo/app.py` — Streamlit single-page UI

## Entry Points
- `main.py` — CLI: `python main.py [--topic "..."]`
- `uvicorn flowbeast.api.main:app --reload --port 8000`
- `uv run streamlit run flowbeast/demo/app.py --server.port 8501`

## Data Flow
```
user topic
  → trending.py (optional: enrich with trending context)
  → fp3/retriever.py (retrieve viral structures from FP3)
  → fp3/injector.py (inject into prompt)
  → drama/prompt.py (build final prompt with 爽文 rules)
  → drama/generator.py (LLM call → script JSON)
  → observe/quality/ (score → dedup → gate)
  → drama/pipeline.py (orchestrate)
  → drama/shot_director.py (script → shots)
  → drama/asset_manager.py (inject StyleLock → prompt_package.json)
  → drama/audio.py (Edge TTS validation)
```
