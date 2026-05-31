# Audit Report: FlowBeast Pre-Goal-Drive Readiness

**Date:** 2026-05-30
**Scope:** Full project audit — architecture, code, configuration, documentation, tasks, tests
**Assessment:** Independent review from first principles

---

## 1. Executive Summary

### Probability of Achieving Goals via Goal-Driven Claude Code

| Phase | Probability | Estimated Completion | Key Risk |
|-------|-------------|---------------------|----------|
| **Phase 1: Demo System** | **75%** | ~70-80% | FP3 corpus quality, API dependency |
| **Phase 2: VTO Operators (GRAFT/PARASITE)** | **35%** | ~20-30% | Blocked by Phase 0 corpus, not code |
| **Phase 0: Viral Corpus (prerequisite)** | **50%** | ~50% (if humans participate) | Human curation bottleneck, not code |

**Overall assessment: The architecture is sound and well-designed. The code quality is good for Phase 1. But there is a fundamental gap between the code readiness and the knowledge-base readiness.** The system can run end-to-end (3 successful runs exist in `flowbeast/data/outputs/`), but it runs on hand-written seed data, not real reverse-engineered viral content. This is the single biggest risk.

---

## 2. Architecture Review (Strengths)

### ✅ What's Done Well

1. **Clear project positioning**: "Viral Prompt Compiler" is a sharp, defensible positioning. The FP3 moat is clearly articulated.

2. **Layer separation is clean**:
   - `flowbeast/fp3/` — memory (moat)
   - `flowbeast/drama/` — generation (commodity)
   - `flowbeast/observe/` — quality (feedback)
   - `flowbeast/core/` — config/providers (infra)
   - `flowbeast/hooks/` — dev guardrails (devex)

3. **Dual schema design**: `ViralUnit` (legacy, simple) + `ViralScript` (enriched, composable) with `to_viral_unit()` backward compatibility is well thought out.

4. **PromptAtom as first-class citizen**: 40 seed atoms across camera/visual/style/narrative layers — this is the right granularity for a "compiler."

5. **Feedback loop is complete**: `feedback_ingest.py` → `EngagementMetrics` → `compute_virality_score` → `compute_atom_scores` → `get_atom_effectiveness` — the data model exists end-to-end.

6. **QualityGate architecture**: `Scorer → Dedup → Gate → Audit` pipeline with rule-based fallback and reference-anchored mode is correct design.

7. **Anti-scope-creep discipline**: `.ai/decisions/002_what_we_do_not_do.md` is a real document with actual scope boundaries, not lip service.

8. **Multi-provider support**: `openai_compatible`, `anthropic_compatible`, `gemini_provider`, `embedding` — the provider pattern is correct.

9. **3 successful end-to-end runs exist**: `flowbeast/data/outputs/` contains 3 dated runs with full audio, script, shot_list, and prompt_package — the pipeline works.

10. **Test coverage**: 8 test files covering config, drama, fp3 feedback, quality, hooks — the basics are covered.

---

## 3. Critical Gaps (Must-Fix Before Goal-Driving)

### 🔴 CRITICAL — Blocks Progress

#### 3.1 API/Server Has No Generation Endpoint

**File:** `flowbeast/api/main.py`

The only endpoint is `/health`. The core value proposition — `POST /v1/generate {topic}` → `prompt_package.json` — is "pending." Goal-driven work that assumes a web demo will hit this wall.

```python
@app.get("/health")  # This is the ONLY endpoint
async def health():
    return {"status": "healthy", ...}
```

**Fix:** Add a POST `/v1/generate` endpoint that calls `run_full_pipeline()` and returns the `prompt_package.json` path + preview. This is `.ai/tasks/001_demo_ui_endpoint.md` and is marked "not started."

**Impact:** Without this, there is no web demo, which is the Phase 1 goal.

#### 3.2 FP3 Corpus = Hand-Written Seeds Only

**File:** `flowbeast/data/reverse_engineered/` is empty (only `TEMPLATE_viral_analysis.json` exists).

The entire FP3 moat, latent grammar learning, and QualityGate calibration depend on **real reverse-engineered viral content**. Currently:
- `seed_data.py` provides 20 hand-written ViralUnits + 40 PromptAtoms
- `reverse_engineer.py` (477 lines, CLI tool) is ready but has never been used to ingest real data
- QualityGate calibration requires ≥5 real samples for meaningful z-score statistics — currently has 0

**Roadmap admits this:** "Phase 2 (GRAFT/PARASITE) is blocked by corpus quality, not code quality. With 2 demo samples, GRAFT/PARASITE = garbage output."

**Fix:** This requires **human participation** — not code. The user must watch viral dramas, fill out the reverse_engineer CLI, and curate 15-30 samples. Claude Code can't do this.

**Impact:** GRAFT/PARASITE operators will produce meaningless output without a real corpus. QualityGate calibration scores are meaningless with seed data.

#### 3.3 VTO Operators Don't Exist as Code

**Files:** None exist. The roadmap lists `tasks/002_graft_operator.md` and `tasks/003_parasite_operator.md` as future work.

The VTO concept (GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT) is well-documented in README and architecture docs, but **there is zero implementation code**. The generator uses FP3 retrieval + RAG injection, not VTO transformations.

**Impact:** Phase 2 goals cannot be executed. The architecture docs describe what they should do, but no code implements them.

---

### 🟡 IMPORTANT — Quality/Reliability Risks

#### 3.4 `asyncio.run()` Inside Sync Functions

**Files:** `pipeline.py:61`, `generator.py:70`

```python
# pipeline.py
decision = asyncio.run(gate.evaluate(unit))

# generator.py
trend_context = asyncio.run(fetch_trending_context())
```

This is an anti-pattern. Calling `asyncio.run()` inside synchronous code will fail if there's already a running event loop (e.g., inside FastAPI, inside Jupyter, inside some test frameworks). Should be `asyncio.get_event_loop().run_until_complete()` or refactored to be fully async.

#### 3.5 No `.env.example` or Configuration Template

The project depends on `.env` for API keys (LLM provider, embedding) but there is no `.env.example` in the repo. A goal-driven agent will fail immediately without knowing what environment variables are required.

**Required vars** (inferred from `config.py`):
- `MODEL_PROVIDER` — which LLM to use
- `MODEL_NAME` — model identifier
- `API_KEY` / provider-specific keys
- `EMBEDDING_PROVIDER`
- `EMBEDDING_API_KEY`
- Proxy settings if applicable

#### 3.6 Hardcoded Paths in Pipeline

**File:** `pipeline.py:146-149`
```python
base_assets_dir = Path(settings.FLOWBEAST_OUTPUT_DIR).parent.parent.parent / "assets"
character_dir = base_assets_dir / "characters"
scene_dir = base_assets_dir / "scenes"
```

The `parent.parent.parent` chain is fragile and will break if `FLOWBEAST_OUTPUT_DIR` nesting changes. Also, `characters/` and `scenes/` directories are referenced but may not exist.

#### 3.7 Feedback Directory is Empty

**File:** `flowbeast/data/feedback/` is empty.

The entire feedback loop (`feedback_ingest.py` → `get_atom_effectiveness()` → retriever boosting) has never been exercised with real data. `retriever.py` returns neutral score (0.5) when no feedback exists, which is correct behavior but means the feedback boost is a no-op.

#### 3.8 Test Coverage Has Gaps

**Missing test files:**
- `test_drama_pipeline.py` — no test for `run_full_pipeline()` integration
- `test_fp3_retriever.py` — no test for retrieval + feedback boost logic
- `test_fp3_injector.py` — no test for `inject_prompt()`
- `test_drama_audio_assembly.py` — no test for episode audio assembly
- `test_reverse_engineer.py` — no test for the 477-line reverse engineering CLI
- `test_drama_shot_director.py` — no test for shot building
- `test_api.py` — no test for the API endpoints (even the health check)

Existing tests (8 files) are good but cover ~30-40% of the codebase. Critical paths like `generator.py`, `pipeline.py`, and `retriever.py` are not tested directly.

#### 3.9 `langgraph` and `langchain-openai` Are Dependencies But Not Used

**File:** `pyproject.toml`

```toml
"langgraph",
"langchain-openai",
```

These are imported in `pyproject.toml` but I don't see them used anywhere in the codebase. This suggests either:
- They were planned for a future architecture (v0.4+ agents) but not yet used
- They're dead weight that increases install time

If not actively used, remove them to keep dependencies clean.

---

### 🟢 NICE-TO-HAVE — Improvements

#### 3.10 No `.env.example`

Already mentioned in 3.5. Worth reiterating as a blocker for any automated setup.

#### 3.11 Missing `characters/` and `scenes/` Asset Directories

The pipeline references `assets/characters/` and `assets/scenes/` but these directories don't exist in the tree. Only `assets/style/` exists with `color_palette.json`, `negative_prompt.txt`, `render_rules.json`, `visual_style.md`.

#### 3.12 `site/` Build Artifacts in Repo

The `site/` directory (MkDocs build output) is committed to the repo. This should be in `.gitignore` and served from CI/CD.

#### 3.13 Git Branch is Detached HEAD

Current status shows `HEAD` (not on a branch). This may cause issues with git hooks and CI.

#### 3.14 `experiments/` and `reviews/` Directories Are Empty

Both `.ai/experiments/` and `.ai/reviews/` are empty directories. Not critical but signals incomplete setup.

#### 3.15 No GitHub Actions or CI

No `.github/workflows/` for automated testing. The hooks system runs pre-commit/pre-push locally, but there's no CI pipeline for PRs.

---

## 4. Goal-Drive Readiness Scorecard

| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| **Architecture** | 8 | Clean layers, clear boundaries, good separation of concerns |
| **Code Quality** | 7 | Solid FP3/drama modules, some async anti-patterns, minimal tests |
| **Documentation** | 8 | Excellent README, good .ai/ docs, comprehensive cursor rules |
| **Configuration** | 5 | Missing .env.example, some hardcoded paths, langgraph unused |
| **Data/Corpus** | 2 | 0 real samples, hand-written seeds only, empty reverse_engineered/ |
| **Test Coverage** | 4 | 8 test files but gaps in critical paths (pipeline, retriever, API) |
| **API/Demo** | 2 | Only `/health` endpoint, no generation API |
| **VTO Operators** | 1 | Concepts documented, zero implementation |
| **Feedback Loop** | 3 | Code exists, never exercised with real data, empty feedback/ dir |
| **Goal-Drive Config** | 7 | CLAUDE.md goal-driven workflow, .ai/ tasks, goals, status all present |

### Weighted Readiness Score: 4.7/10

The system is architecturally ready but operationally thin. It can run end-to-end (proven by 3 runs), but produces "seed-grade" output, not "viral-grade" output.

---

## 5. Recommendations: What to Fix Before Goal-Driving

### Priority 1 — Immediate (Do Before Goal-Driving)

1. **Create `.env.example`** with all required variables documented
   - Takes 5 minutes, blocks any automated agent from running

2. **Add `POST /v1/generate` endpoint** to `api/main.py`
   - Call `run_full_pipeline()` → return `prompt_package.json` path
   - Task `.ai/tasks/001_demo_ui_endpoint.md` already exists — execute it first

3. **Fix `asyncio.run()` anti-pattern** in `pipeline.py` and `generator.py`
   - Or document the constraint that these must not be called from async contexts

4. **Create `assets/characters/` and `assets/scenes/` directories** (even if empty)
   - Prevents pipeline warnings/errors from missing directories

### Priority 2 — Human-Dependent (Claude Code Can't Do)

5. **Start Sprint 1: Reverse-engineer 15 real viral dramas**
   - Use `uv run python -m flowbeast.reverse.reverse_engineer`
   - Human watches → fills CLI → JSON saved to `flowbeast/data/reverse_engineered/`
   - This is the #1 prerequisite for everything in Phase 2
   - **Timeline estimate:** 7-10 hours of human time (30 min/script × 15)

6. **Define what "demo success" means**
   - Current `.ai/goals/current_goal.md` says "End-to-end web demo"
   - Define acceptance criteria: e.g., "Given topic X, produces prompt_package.json with ≥5 shots, audio, and QualityGate score > 0.5 within 3 minutes"

### Priority 3 — Quality (Goal-Driven Claude Code Can Help)

7. **Add integration test for `run_full_pipeline()`** (mocked LLM)
8. **Add test for API generation endpoint** (after #2)
9. **Add test for `FP3Retriever.retrieve()`** with feedback boost
10. **Remove unused dependencies** (`langgraph`, `langchain-openai`) or document their future use
11. **Add GitHub Actions CI** for automated test runs

---

## 6. Risk Assessment

### What Will Go Well
- **Phase 1 demo system:** Claude Code can implement the API endpoint, wire up the UI, add tests, and deliver a working demo in 1-2 focused sessions
- **Code quality improvements:** Linting, test coverage, async fixes are well within Claude Code's capabilities
- **Documentation:** Already strong, can be enhanced automatically

### What Will Fail Without Human Input
- **FP3 corpus quality:** Claude Code can't watch and judge viral dramas. The entire moat depends on human-curated data
- **GRAFT/PARASITE effectiveness:** Even if code is written, without 30+ real samples, output quality will be garbage
- **QualityGate calibration:** Meaningful z-scores require ≥5 real reverse-engineered samples

### Biggest Single Risk
**The gap between "the pipeline works" and "the output is good" is entirely in the knowledge base, not the code.** The architecture is designed for a data flywheel that hasn't started spinning. Claude Code can build every pipe and valve, but it can't provide the water.

---

## 7. Verdict

**If you goal-drive Claude Code right now on Phase 1 (demo system):**
- **Probability of a working demo:** ~75%
- **Expected completion:** ~70-80% (API endpoint, basic UI, tests)
- **Expected quality of output:** "seed-grade" — functional but not impressive without real FP3 data

**If you goal-drive Claude Code on Phase 2 (VTO operators):**
- **Probability of working operators:** ~35% (code can be written, but quality is garbage without corpus)
- **Expected completion:** ~20-30% (operators coded but producing meaningless output)
- **Root cause:** Blocked by Phase 0, not by code quality

**Recommendation:** Goal-drive Claude Code on **Phase 1 demo tasks first** (API endpoint, UI, tests, async fixes) while **you (the human) work on Sprint 1 corpus building in parallel**. These are the two parallel tracks that unlock everything else.
