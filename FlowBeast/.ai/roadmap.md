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

**Status:** 🟡 Sprint 1 not started

---

## Phase 1: Demo System (Current Focus)

**Goal:** End-to-end web demo (topic → script → shots → audio → browser)

**Why this matters:** No one can see the product working. Demo is the fastest path to user validation.

**Scope:**
- FastAPI endpoint (`POST /v1/generate`)
- Async job handling (don't block for 30-60s)
- Polling endpoint (`GET /v1/jobs/{job_id}`)
- Frontend (HTML + JS, no framework)
- Error handling (LLM failures, JSON parse errors)
- File serving (audio, downloads)
- Loading UX

**Effort:** 10-16 hours of focused work

**Key files:**
- `flowbeast/api/main.py` — Add endpoints
- `flowbeast/static/index.html` — Frontend (new)
- `.ai/tasks/001_demo_system.md` — Detailed requirements

**Status:** 🟡 Not started

---

## Phase 2: VTO Operators (Blocked by Phase 0 + Phase 1)

**Goal:** GRAFT/PARASITE operators produce structurally novel scripts with proven viral DNA.

**Why this matters:** This is the "magic" that makes FlowBeast different from a generic script generator.

**Entry gate:**
- ✅ Phase 1 demo complete
- ✅ Phase 0 corpus: 30 real reverse-engineered scripts
- ✅ QualityGate calibration: σ > 0.01 on ≥ 5 dimensions

**MVP gate:**
- ✅ 100 scripts in corpus
- ✅ GRAFT produces output rated "consistently good" by human
- ✅ PARASITE matches trends to compatible spines reliably

**Complete gate:**
- ✅ 300 scripts in corpus
- ✅ Cross-genre GRAFT works
- ✅ Corpus is defensible (competitors can't replicate quickly)

**Key files:**
- `flowbeast/fp3/injector.py` — Add VTO transformation logic
- `flowbeast/fp3/retriever.py` — Add operator-aware retrieval
- `flowbeast/fp3/vto/` — Operator implementations (new)

**Status:** 🔴 Blocked (Phase 0: 0/30 scripts, Phase 1: not started)

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

## Execution Strategy

**Parallel execution:**
- Phase 0 (corpus) runs in parallel with Phase 1 (demo)
- Sprint 1+2 (4 weeks): 30 scripts → Phase 2 entry gate
- Phase 2 starts when BOTH Phase 0 and Phase 1 are ready

**Timeline:**
- **Weeks 1-2:** Phase 1 engineering + Phase 0 Sprint 1 (15 scripts)
- **Weeks 3-4:** Phase 1 polish + Phase 0 Sprint 2 (15 scripts)
- **Week 5+:** Phase 2 entry (if both gates met)

**Key insight:** Phase 2 is NOT blocked by Phase 1 alone. It's blocked by BOTH Phase 1 (demo) AND Phase 0 (corpus). Start both now.

---

## Success Criteria

**Phase 0 (corpus) success:**
- 30 real reverse-engineered scripts (not demo hooks)
- 5+ genres represented
- Quality distribution: 60% viral, 20% average, 20% failed
- QualityGate calibration meaningful (σ > 0.01)

**Phase 1 (demo) success:**
- User can type topic → see script + shots + audio in browser
- 5 successful end-to-end runs with different topics
- Error handling works (LLM failures, parse errors)

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
