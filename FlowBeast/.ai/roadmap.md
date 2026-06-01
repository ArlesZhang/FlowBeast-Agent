# FlowBeast Roadmap

## Phase 0: Viral Knowledge Base (Content Operations)

**Goal:** Build the Viral Knowledge Base — the real moat of FlowBeast.

**Why this matters:** Phase 2 (GRAFT/PARASITE) is blocked by corpus quality, not code quality. With 2 demo samples, GRAFT/PARASITE = garbage output. With 30+ real samples, the operators work.

**Current state:** 0 real reverse-engineered scripts. ~20 hand-written demo hooks.

**Sprint model:**
- **Sprint 1 (Weeks 1-2):** 15 scripts, pipeline validation + initial diversity
- **Sprint 2 (Weeks 3-4):** 15 scripts, reach Phase 2 entry gate (30 total)
- **Maintenance (Weeks 5+):** 1-2 scripts/week, grow to 100+ for Phase 2 MVP

**Corpus tiers:**
- **30 scripts:** Phase 2 validation ("can we even run GRAFT?")
- **100 scripts:** Phase 2 MVP ("GRAFT produces reliably good output")
- **300 scripts:** Phase 2 complete ("cross-genre, statistically significant")

**🔴 Hard constraint:** No Phase 0 optimization before 30 real samples. See `.ai/decisions/002_what_we_do_not_do.md` #8.

**Key files:**
- `.ai/tasks/000_viral_corpus_building.md` — Sprint tracker
- `.ai/content_strategy.md` — Full strategy
- `flowbeast/reverse/reverse_engineer.py` — CLI tool (477 lines, ready to use)
- `flowbeast/data/raw/` — Human-curated samples
- `flowbeast/data/reverse_engineered/` — Agent-produced ViralScripts

**Division of labor:**
- Human: watch, judge, curate (30 min/script)
- Agent: extract, structure, validate, inject (5 min/script)

**Status:** 🟡 Sprint 1 not started — **CORPUS IS STILL 0 REAL SCRIPTS**

---

## Phase 1: Demo System ✅ COMPLETE (v0.5.0-mvp)

**Goal:** End-to-end web demo (topic → script → shots → audio → browser)

**Status:** ✅ Shipped 2026-05-31

**What was delivered:**
- ✅ FastAPI: 4 endpoints (`/health`, `POST /api/v1/generate`, `GET /api/v1/tasks/{task_id}`, `GET /api/v1/download/{file_type}/{run_id}`)
- ✅ Async job handling via `BackgroundTasks` + in-memory state + JSON persistence
- ✅ Streamlit demo UI (`flowbeast/demo/app.py`) — topic input, status polling, GRAFT structure visualization, script display, audio player, downloads
- ✅ 5 successful GRAFT runs with different topics (evidence package)
- ✅ 67 tests passing (includes 9 GRAFT tests)
- ✅ 17 production runs total

**Key files:**
- `flowbeast/api/main.py` — 4 endpoints
- `flowbeast/demo/app.py` — Streamlit single-page UI
- `flowbeast/vto/graft.py` — GRAFT v0 operator
- `tests/test_graft.py` — 9 GRAFT tests

---

## Phase 2: VTO Operators 🟡 GRAFT v0 Complete, PARASITE Pending

**Goal:** GRAFT/PARASITE operators produce structurally novel scripts with proven viral DNA.

**Status:** 🟡 GRAFT v0 shipped (seed data). PARASITE not started. Blocked by corpus quality.

**What exists:**
- ✅ `flowbeast/vto/graft.py` — GRAFT v0 (231 lines, working)
- ✅ Extracts hook_structure + conflict_pattern from FP3 ViralScripts
- ✅ Builds structural transfer prompt with 5 migration instructions
- ✅ 5 evidence runs prove the operator works end-to-end
- ✅ 9 tests passing

**What's missing:**
- 🔴 Real reverse-engineered scripts in FP3 (0 real, ~20 seed)
- 🔴 All 5 evidence runs use same hook_type (冲突爆发) + conflict_type (权力碾压)
- 🔴 PARASITE operator: no code
- 🔴 DISTORT/MISDIRECT/THEFT: no code

**Entry gate:**
- ✅ Phase 1 demo complete
- ❌ Phase 0 corpus: 0/30 real reverse-engineered scripts
- ❌ QualityGate calibration: meaningless with seed data

**Key files:**
- `flowbeast/vto/graft.py` — GRAFT v0 (complete)
- `flowbeast/fp3/injector.py` — RAG injection (working)
- `flowbeast/fp3/retriever.py` — k-NN retrieval (working)

---

## Phase 3: Feedback Flywheel (Blocked by Phase 1 + Phase 2)

**Goal:** Real users + real engagement data → FP3 atom weights → better generations.

**Why this matters:** This is the self-reinforcing loop that makes the system improve over time.

**Entry gate:**
- ✅ Phase 1 demo live (real users generating scripts)
- ✅ Phase 2 operators working (quality output)
- ✅ Real engagement data (views/likes/shares from published content)

**Status:** 🔴 Blocked (Phase 1: not started, Phase 2: not started)

---

## Execution Strategy (Updated 2026-06-01)

**Phase 1 is complete.** The only remaining blocker is Phase 0 (corpus).

**Current focus:**
- Phase 0 (corpus): Sprint 1 → 15 scripts in 2 weeks → Phase 2 entry gate
- Phase 1 (demo): Maintenance only — bug fixes, not new features
- Phase 2 (VTO): Blocked until 30 real scripts. PARASITE design can start but implementation waits.

**Timeline:**
- **Weeks 1-2 (June 1-14):** Phase 0 Sprint 1 — 15 real reverse-engineered scripts
- **Weeks 3-4 (June 15-28):** Phase 0 Sprint 2 — reach 30 scripts → Phase 2 entry gate
- **Week 5+:** Phase 2 GRAFT with real corpus + PARASITE v0

**Key insight:** Phase 1 was the easy part. Phase 0 is the hard part — it requires human curation, not code. Every day of watching and reverse-engineering viral scripts is more valuable than a week of building infrastructure.

---

## Success Criteria

**Phase 0 (corpus) success:**
- 30 real reverse-engineered scripts (not demo hooks)
- 5+ genres represented
- Quality distribution: 60% viral, 20% average, 20% failed
- QualityGate calibration meaningful (σ > 0.01)

**Phase 1 (demo) success:** ✅ COMPLETE
- ✅ User can type topic → see script + shots + audio in Streamlit UI
- ✅ 5 successful GRAFT runs with different topics
- ✅ Error handling works (LLM failures, parse errors)
- ✅ 67 tests passing
- ✅ FastAPI server with 4 endpoints

**Phase 2 (VTO) success:**
- GRAFT on NEW topic produces output rated "better than random"
- PARASITE on TRENDING topic references trend naturally
- Cross-genre GRAFT works (CEO hook → xianxia topic)

---

## Key Documents

- `.ai/tasks/000_viral_corpus_building.md` — Phase 0 sprint tracker
- `.ai/tasks/001_demo_system.md` — Phase 1 requirements
- `.ai/content_strategy.md` — Corpus strategy + tiers
- `.ai/decisions/002_what_we_do_not_do.md` — Hard constraints (including Phase 0 freeze)
- `.ai/status/current_status.md` — Current state + blockers
