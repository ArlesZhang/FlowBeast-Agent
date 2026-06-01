# Current Status

**Last updated:** 2026-06-01 (Post-v0.5.0-mvp — Corpus Factory Complete)

## Completed Milestones

| Milestone | Status | Date |
|-----------|--------|------|
| v0.5.0-mvp: Demo Validation MVP | ✅ Complete | 2026-05-31 |
| v0.6.0: Corpus Factory (validation) | ✅ Complete | 2026-06-01 |

## What Exists (Code)

| Component | Status | Notes |
|-----------|--------|-------|
| CLI pipeline (`python main.py --topic "..."`) | ✅ | 17 production runs |
| FastAPI (4 endpoints) | ✅ | `/health`, `POST /api/v1/generate`, `GET /api/v1/tasks/{task_id}`, `GET /api/v1/download/{file_type}/{run_id}` |
| Streamlit demo UI | ✅ | `flowbeast/demo/app.py` |
| GRAFT v0 operator | ✅ | 231 lines, 9 tests, 5 evidence runs (seed data) |
| FP3 retrieval (seed data) | ✅ | ~20 hand-written ViralUnit entries |
| QualityGate (9-dim scorer) | ✅ | Rule-based + dedup |
| Edge TTS audio | ✅ | Quality validation layer |
| Tests | ✅ | 57 tests passing |
| Corpus Factory Report | ✅ | Audit + vocabularies + checklist + 3 gold examples |

## What's Missing

| Component | Status | Blocker |
|-----------|--------|---------|
| Real reverse-engineered corpus | 🔴 0 scripts | **Human curation required** |
| PARASITE operator | 🔴 No code | Blocked by corpus |
| Feedback flywheel | 🔴 Never exercised | Blocked by Phase 0 + Phase 1 users |
| QualityGate calibration | 🔴 Meaningless | Needs ≥5 real reverse-engineered scripts |
| `.env.example` | ✅ | Just created |
| Corpus Factory Report | ✅ | Just created |

## Current Priority

**Phase 0: Corpus Building — Sprint 1 (15 scripts by June 14)**

1. Watch 1-2 viral short dramas per day
2. Follow checklist in `.ai/reports/003_human_annotation_checklist.md`
3. Run `uv run python -m flowbeast.reverse.reverse_engineer`
4. Verify output → FP3
5. Repeat 30 times

**Success Metric:** Can a new topic inherit proven viral mechanics and outperform baseline generation?

## How to Run

```bash
# CLI pipeline
python main.py --topic "your topic"

# API server
uvicorn flowbeast.api.main:app --reload --port 8000

# Streamlit demo
uv run streamlit run flowbeast/demo/app.py --server.port 8501

# Tests
uv run pytest tests/ -q

# Reverse engineer a viral script
uv run python -m flowbeast.reverse.reverse_engineer
```
