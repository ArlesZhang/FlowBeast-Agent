# Task 001: Demo UI — Generation Endpoint + Frontend

## Status: ✅ Complete (v0.5.0-mvp)
## Priority: 🔴 Critical (blocks all other work) — RESOLVED
## Depends on: —
## Related: `.ai/goals/phase_1_mvp.md`

## Shipped (v0.5.0-mvp, 2026-05-31)

- ✅ FastAPI: `POST /api/v1/generate`, `GET /api/v1/tasks/{task_id}`, `GET /api/v1/download/{file_type}/{run_id}` — 3 endpoints
- ✅ Streamlit demo UI (`flowbeast/demo/app.py`) — single-page: input, status, structure, script, audio, downloads
- ✅ 5 successful GRAFT runs with different topics (evidence package)
- ✅ 9 GRAFT operator tests (`tests/test_graft.py`)
- ✅ Total test suite: 67 tests passing (updated to 57 after test audit)

**Note:** This task is complete. The implementation went beyond the original spec by including GRAFT integration, Streamlit UI, and async job handling with BackgroundTasks.

---

## Objective (Original)

Wire the existing pipeline (`run_full_pipeline`) into a FastAPI endpoint and build a minimal web frontend. This is the single most important task — nothing else matters until this works.

## Why This Is Priority #1

Everything else in FlowBeast already works:
- Script generation ✓
- Shot director ✓
- Asset manager ✓
- QualityGate ✓
- Audio engine ✓
- FP3 retrieval ✓

The only missing piece is **exposing it via HTTP**. Without this, FlowBeast is a CLI tool that only the developer can use. With it, FlowBeast is a product.

## Acceptance Criteria

### Backend

- [ ] `POST /v1/generate` accepts `{"topic": "..."}`
- [ ] Calls `run_full_pipeline(topic)` from `drama/pipeline.py`
- [ ] Returns JSON with:
  ```json
  {
    "run_id": "20260530_143022",
    "script": { "title": "...", "core_hook": "...", "scenes": [...] },
    "shot_list": [ { "shot_id": "S01_SH01", "beat_type": "setup", ... } ],
    "prompt_package": { ... },
    "quality": { "score": 0.72, "action": "accept", "reason": "..." },
    "audio_paths": ["audio/episode.mp3"]
  }
  ```
- [ ] Returns 422 for empty/invalid topic
- [ ] Returns 500 with error detail if pipeline fails
- [ ] Logs run_id for each request

### Frontend

- [ ] Single HTML page (`flowbeast/api/static/index.html`)
- [ ] Text input + "Generate" button
- [ ] Loading indicator (generation takes 30-60s)
- [ ] Output sections:
  - Script summary (title, genre, core_hook)
  - Scene-by-scene breakdown with dialogue
  - Shot list table (shot_id, beat_type, shot_type, duration_sec)
  - QualityGate result (score + action badge)
  - Audio player (if episode MP3 exists)
- [ ] "Download prompt_package.json" button

### Testing

- [ ] 5 successful runs with different topics
- [ ] At least 3 runs score >= 0.60 (ACCEPT)

## Key Files

**Modify:**
- `flowbeast/api/main.py` — currently only has `/health`, add `/v1/generate`
- `pyproject.toml` — add `jinja2` if using templates (optional)

**Create:**
- `flowbeast/api/static/index.html` — minimal frontend (plain HTML + vanilla JS)
- `flowbeast/api/routers/generate.py` — endpoint logic (optional, can inline in main.py)

**Reference:**
- `flowbeast/drama/pipeline.py:run_full_pipeline()` — the function to call
- `flowbeast/drama/pipeline.py:_run_output_quality_gate()` — already returns quality dict

## Design Notes

- Use `run_full_pipeline()` as-is. Don't refactor it.
- The pipeline already saves all outputs to `flowbeast/data/outputs/{run_id}/`. The endpoint should read from those files and return them as JSON.
- Frontend: plain HTML + `fetch()` + `innerHTML`. No React, no Vue, no framework. Goal is demo-ability, not production UI.
- CORS is already configured in `api/main.py` (allow all origins).

## Open Questions

- Should the endpoint block until generation completes (synchronous, 30-60s), or return a job ID and poll? **Recommendation: synchronous for Phase 1. Simpler.**
- Should the frontend show intermediate steps (script → shots → quality)? **Recommendation: no, just show final result. Keep it simple.**
