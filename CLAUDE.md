# CLAUDE.md

> This project uses Cursor Rules — see [.cursor/rules/](./.cursor/rules/) for detailed development guidelines.
> Positioning, product form and the collaboration rules: `.ai/current/founder_notes.md` (local, not committed).

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
   Claude Skills ecosystem. Say what you found.
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

### Before you build anything

- Adding a dependency? Check whether it is already installed — `uv pip list`.
- Writing a script? Check whether a CLI already on the machine does it.
- Building a sub-agent? Check whether an existing Claude Skill or MCP server covers it.
- Designing a subsystem? Check `.ai/current/capability_map.md` — it maps our capabilities against
  off-the-shelf tools.
- **State your integration choice out loud** ("using X because Y; not writing Z because X covers
  it") so the decision is reviewable.

### What we *do* build ourselves

Only the actual business: the workflow glue that ties tools into one deliverable, and the domain
logic no generic tool can know (drama structure, Chinese short-drama pacing, per-episode delivery
packaging). Everything underneath — infrastructure, plumbing, formats, protocols — is somebody
else's job, already done.

---

## What FlowBeast is

**An AI short-drama production engine.** The deliverable is a finished episode; `prompt_package.json`
is the handoff point where an AI video tool takes over — an artifact, not the product. We do not
build video generation, but "don't build it" does not mean "stop before the episode exists".

```
topic → FP3 viral-memory retrieval → script → shot direction → TTS audio → prompt_package.json → episode
```

| Layer | Path | Role |
|---|---|---|
| **Memory** | `flowbeast/fp3/` | Composable narrative atoms (`ViralUnit`: hook / pattern / emotion) in a FAISS index, retrieved by similarity and injected into the generation prompt. This is what makes output better than a bare LLM call. |
| **Gate** | `flowbeast/observe/quality/` | Rule-based 9-dimension scorer + embedding dedup. **Weak signal, not a judge** — it has never returned ACCEPT and its weights are unfitted. Do not treat its score as a verdict. |
| **Production** | `flowbeast/drama/` | Script → shot list → TTS audio → package. A **replaceable commodity layer**: swap any stage for an off-the-shelf tool the moment a better one exists. |
| **Core** | `flowbeast/core/` | Config + multi-vendor LLM registry (8 vendors, `.env`-switchable). |
| **Interfaces** | `flowbeast/api/`, `flowbeast/demo/` | FastAPI service and Streamlit UI over the same pipeline. |

**Not** a video model builder, **not** a publishing platform, **not** a multi-agent framework.
When the delivery path needs rendering, *integrate* an existing API/SDK — never write our own.
See `.ai/current/decisions/001_project_positioning.md` and `decisions/002_what_we_do_not_do.md`.

---

## Commands

```bash
uv sync                                              # Install dependencies (uv, not pip)
python main.py --topic "your topic"                  # Run the full pipeline (CLI)
uvicorn flowbeast.api.main:app --reload --port 8000  # FastAPI server
uv run streamlit run flowbeast/demo/app.py           # Streamlit UI (port 8501)
uv run python -m flowbeast.fp3.seed_data             # Seed FP3 (ViralUnit)
uv run python -m flowbeast.fp3.feedback_ingest \     # Feedback ingest
  --report production_report.json --views N --likes N
uv run pytest tests/ -q                              # Run all tests (34)
docker-compose up --build                            # Docker
```

Outputs land in `flowbeast/data/outputs/<timestamp>/`.

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

## Tests

Keep tests that catch **real regressions** in the delivery path. Do not write tests that assert
constant shapes, source text, or environment state — those never catch a bug and only add
maintenance cost.

---

## Context Priority

When multiple sources conflict, prioritize:

1. Existing repository architecture
2. CLAUDE.md instructions
3. `.cursor/rules/`
4. Existing code patterns
5. User request
6. General framework conventions

---

## Documentation Map

> `.ai/current/` is **local only** — gitignored on purpose. Business positioning does not belong in
> a public repo. Paths below exist on your machine but not on GitHub.

| Path | Contents |
|---|---|
| `.ai/current/founder_notes.md` | Positioning, Rule 0, collaboration rules (**read first**) |
| `.ai/current/goal.md` | Current phase goal — what to work on now |
| `.ai/current/status.md` | What is wired vs. stubbed |
| `.ai/current/capability_map.md` | Capability → off-the-shelf tool mapping (for Rule 0) |
| `.ai/current/commercialization_playbook.zh.md` | Commercial plan, in Chinese |
| `.ai/current/decisions/` | Positioning and scope-boundary decisions |
| `.ai/skills/` | Task-specific playbooks |

## Working Style

- **Delete before you build.** Removing the wrong thing, or replacing it with an existing tool, is
  usually the correct fix. Do not keep running down a direction that has been falsified.
- **Two failures is the threshold.** If the same command or operation fails twice, stop and report
  to the user (in Chinese) with the error and a suggested manual command. Do not loop.
- **Report in Chinese.** Progress reports to the user are in Chinese; repo artifacts stay English.
