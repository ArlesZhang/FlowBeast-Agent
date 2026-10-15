# CLAUDE.md

> This project uses Cursor Rules — see [.cursor/rules/](./.cursor/rules/) for detailed development guidelines.

## ⚠️ Read this first

> 市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。
> AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。

**FlowBeast is not sold as a compiler, and not sold as prompt packs.** The productized form is
**done-with-you AI short-drama production for small Chinese teams, priced per finished episode** —
a service, not a SaaS. The free public scorer is the top of funnel, not the product.

**The one acceptance test for everything: 有真实付费证据 (there is real payment evidence).**
No feature, refactor, or document counts until a customer has paid for a delivered episode.

**Optimize for: usable · landable · integrable · deliverable · profitable.** Not for completeness,
not for elegance, not for architectural purity. A working integration beats a better invention.

Full reasoning and the 30-day plan: [.ai/current/commercialization_playbook.zh.md](.ai/current/commercialization_playbook.zh.md)
(English: [commercialization_playbook.md](.ai/current/commercialization_playbook.md)).

---

## Rule 0 — Never reinvent the wheel

**Assume the market has already solved it, and solved it better.** Frameworks, packages, modules,
open-source projects, Claude Skills, MCP servers, plugins, SaaS APIs — the overwhelming majority of
what this project needs already exists, is maintained by someone else, and is more mature than
anything we would write in a day.

The scarce resource is **not code**. It is **integration + orchestration + commercial delivery**.
Writing our own version of something that already exists spends the one resource we cannot get back.

### The default order of operations

1. **Search first.** Before writing a module, search GitHub / PyPI / npm / the MCP registry / the
   Claude Skills ecosystem for an existing solution. Say what you found.
2. **Integrate** — use it as a dependency (best outcome: zero lines of our own code).
3. **Borrow** — port the proven design or algorithm, with attribution and a license check.
4. **Write our own** — only if 1–3 genuinely failed, and only after stating *why* they failed.

### Hard rules

- **Never write from scratch what a library does.** No hand-rolled tokenizers, retry logic, TTS
  alignment, subtitle formatting, auth, queueing, scheduling, or vector search.
- **Prefer the boring, popular, maintained option** over a bespoke one, even when ours would be
  marginally better tuned. Maintenance cost outlives the tuning benefit.
- **Check the license before adopting.** MIT / Apache-2.0 / BSD: fine. GPL/AGPL in a commercial
  path: flag it to the user before depending on it.
- **Vendored copies go stale.** Prefer a real dependency over copying a file into the repo.
- **When a tool almost fits, extend it** (plugin, config, wrapper, upstream PR) rather than forking
  the concept into our own parallel implementation.

### In practice

- Before adding a dependency, check whether it is already installed — `uv pip list`.
- Before writing a script, check whether a CLI already on the machine does it.
- Before building a sub-agent, check whether an existing Claude Skill or MCP server covers it.
- Before designing a subsystem, check `[.ai/current/capability_map.md](.ai/current/capability_map.md)`
  — it already maps our capabilities against off-the-shelf tools.
- **State your integration choice out loud** ("using X because Y; not writing Z because X covers
  it") so the decision is reviewable.

### What we *do* build ourselves

Only the parts that are the actual business: the workflow glue that ties tools into one deliverable,
and the domain logic that no generic tool can know (drama structure, Chinese short-drama pacing,
per-episode delivery packaging). Everything under those — infrastructure, plumbing, formats,
protocols — is somebody else's job, already done.

---

## What FlowBeast Is (code-level)

A pipeline that turns a topic into a delivered short-drama episode:

```
topic → FP3 viral-memory retrieval → script → shot direction → TTS audio → prompt_package.json
```

- **FP3 Viral Memory System** — composable narrative atoms (ViralUnit: hook / pattern / emotion)
  stored in a FAISS index, retrieved by similarity and injected into the generation prompt.
  This is the piece that makes output better than a bare LLM call.
- **QualityGate** — rule-based scorer + dedup, gating generated scripts.
- The production pipeline (script → audio → shots → package) is a **replaceable commodity layer**;
  swap any stage for an off-the-shelf tool whenever a better one exists.

**Not** a video generator, **not** a publishing platform, **not** a multi-agent framework.
We stop at `prompt_package.json` and the delivered episode. See
[decisions/001_project_positioning.md](.ai/current/decisions/001_project_positioning.md).

---

## Commands

```bash
uv sync                                              # Install dependencies (uv, not pip)
python main.py                                       # Run drama generation pipeline
python main.py --topic "your topic"                  # Run with custom topic
uvicorn flowbeast.api.main:app --reload --port 8000  # FastAPI server
uv run streamlit run flowbeast/demo/app.py           # Streamlit demo UI (port 8501)
uv run python -m flowbeast.fp3.seed_data             # Seed FP3 (ViralUnit)
uv run python -m flowbeast.fp3.feedback_ingest \     # Feedback ingest
  --report production_report.json --views N --likes N
uv run pytest tests/ -q                              # Run all tests
docker-compose up --build                            # Docker
```

## Package Manager

This project uses **`uv`** (not pip). Always use `uv sync` to install dependencies and `uv run` to
execute scripts. Do not use `pip install`.


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


## Documentation Map

- `.ai/current/` — current phase, status, roadmap, positioning decisions
- `.ai/current/commercialization_playbook.zh.md` — the commercial plan, in Chinese (**read first**)
- `.ai/current/capability_map.md` — capability → off-the-shelf tool mapping (for Rule 0)
- `.ai/skills/` — task-specific playbooks


## Working Style

- **Delete before you build.** Removing the wrong thing, or replacing it with an existing tool, is
  usually the correct fix. Do not keep running down a direction that has been falsified.
- **Two failures is the threshold.** If the same command or operation fails twice, stop and report
  to the user (in Chinese) with the error and a suggested manual command. Do not loop.
- **Report in Chinese.** Progress reports to the user are in Chinese; repo artifacts stay English.
