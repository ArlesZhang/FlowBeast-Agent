# Current Goal: Demo Validation MVP (14 days / 250 turns)

## Mission

Prove that FlowBeast can:
1. Retrieve proven viral structures from FP3
2. Apply GRAFT transformation to a new Topic
3. Generate a structurally differentiated script
4. Produce a complete content asset package
5. Demonstrate the full workflow through a minimal local UI

**Validation sprint — evidence over completeness.**

## Core Hypothesis

FlowBeast's unique value: Viral Structure Retrieval → Structure Transfer (GRAFT) → New Topic Generation.

A human observer must clearly distinguish Original vs GRAFT-enhanced generation.

## Deliverables

- [x] **D1. Baseline Pipeline Verification** — `python main.py --topic "test"` works, all artifacts produced, 58 tests green
- [ ] **D2. FastAPI Wrapper** — POST /api/v1/generate + GET /api/v1/tasks/{id} (BackgroundTasks, in-memory state)
- [ ] **D3. GRAFT v0** — Hook + Conflict extraction from ViralScript, structure transfer to new topic
- [ ] **D4. FP3 Retrieval** — Use existing FP3 assets, expose in output and UI
- [ ] **D5. Minimal Streamlit UI** — Single page: input, status, retrieved structure, script, audio, download
- [ ] **D6. Evidence Package** — 5 successful runs with prompt packages, production reports, audio
- [ ] **D7. Demo Recording** — 1-3 min recording showing full workflow

## Constraints

- Wrap instead of rewrite
- Simple functions over abstractions
- JSON over infrastructure
- No new databases, agent frameworks, orchestration systems, RAG systems
- No refactoring working pipeline code

## Day 1 Gate: ✅ PASSED

- Baseline pipeline runs with `--topic` flag
- Script, audio, production_report.json, prompt_package.json all produced
- 58 tests pass
- FP3 retrieval works (2 cases from seed data)
