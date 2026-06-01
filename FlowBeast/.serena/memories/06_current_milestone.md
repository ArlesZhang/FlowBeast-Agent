# Current Milestone

**Phase:** 0 (Corpus Building)
**Last updated:** 2026-06-01

## Completed
- [x] v0.5.0-mvp: Demo Validation MVP (2026-05-31)
  - CLI pipeline with --topic flag
  - FastAPI with 4 endpoints
  - Streamlit demo UI
  - GRAFT v0 operator (231 lines, 9 tests, 5 evidence runs)
  - FP3 retrieval (seed data)
  - QualityGate (9-dim scorer + dedup)
  - Edge TTS audio validation
  - 57 tests passing
- [x] v0.6.0 Corpus Factory validation (2026-06-01)
  - Full audit of reverse_engineer.py, ViralScript schema, FP3 storage
  - Controlled vocabularies (7 hook types, 8 conflict types, 17 genres)
  - Human annotation checklist (20-30 min/script)
  - GOLD/SILVER/BRONZE/REJECT quality criteria
  - 3 gold examples validated (职场逆袭, 重生, 家庭伦理)

## Current Goal: 30 Real Reverse-Engineered Scripts
- Sprint 1: June 1-14 (15 scripts)
- Sprint 2: June 15-28 (15 scripts)
- Phase 2 entry gate after 30 scripts

## What's Missing (Critical Blockers)
- 🔴 0 real reverse-engineered scripts in FP3 (only ~20 seed data)
- 🔴 PARASITE operator (no code)
- 🔴 QualityGate calibration (needs real data)
- 🔴 Feedback flywheel (never exercised)

## Hard Constraint
**Before 30 real samples: NO corpus system redesign, NO new databases, NO schema optimization, NO automation, NO new VTO operators.** Focus on acquiring and reverse-engineering scripts only.

## Key Files
- `.ai/goals/current_goal.md` — current milestone goal
- `.ai/milestones/v0.6.0-corpus-30.md` — sprint tracker
- `.ai/reports/001_corpus_factory.md` — full audit
- `.ai/reports/002_gold_standard_vocab.md` — controlled vocabularies
- `.ai/reports/003_human_annotation_checklist.md` — annotation guide
- `.ai/reports/004_corpus_quality_criteria.md` — quality scoring
