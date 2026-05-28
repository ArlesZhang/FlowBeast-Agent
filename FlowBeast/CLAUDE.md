# CLAUDE.md

> This project uses Cursor Rules - see [.cursor/rules/](./.cursor/rules/) for detailed development guidelines.

- FlowBeast is a **Viral Prompt Compiler**: input a topic, output a complete prompt package ready for AI video tools. The core moat is the **FP3 Viral Memory System** — decomposing viral content into composable PromptAtom instances, learning their latent grammar, and transforming them via VTO operators to generate structurally novel scripts with proven viral DNA. The production pipeline (script → audio → video) is a replaceable commodity layer.

- The primary goal of this repository is shipping a working AI-native content generation system, not maximizing architectural sophistication.


# Long-Term Vision

FlowBeast is evolving toward an AI-native viral prompt operating system focused on:

- scalable viral content generation via composable PromptAtom instances
- reusable AI workflows (VTO operators)
- feedback-driven optimization systems
- composable narrative atom spaces (FP3)
- MCP-integrated production pipelines

The project prioritizes practical execution, modularity, automation, and iteration speed over theoretical architectural complexity.


## Strategic Architecture

### Core Moat vs. Commodity

**Production pipeline is a commodity.** Script-to-audio, audio-to-video, multi-agent orchestration — all solvable via third-party tools (Runway, Kling, HeyGen) through MCP integration. Capacity scales horizontally; it's easy to replace.

**The real moat is the "Brain"** — deciding *what* to produce, not *how* to render it.

### FP3 is a Viral Memory System — Composable Narrative Atoms

The competitive advantage is **not** "having a vector database of viral scripts." Anyone can embed text and do similarity search.

The moat is FP3 as a **Viral Memory System** — a structured embedding space that stores **composable narrative atoms**, not monolithic scripts.

A `ViralScript` should decompose into individually addressable, pluggable units — both narrative and production atoms:

| Layer | Atom | Role | Property |
|-------|------|------|----------|
| Narrative | **Hook atom** | Opening pattern (first 3s) | Pluggable |
| Narrative | **Conflict kernel** | Core tension engine | Migratable across domains |
| Narrative | **Character slot** | Role archetypes | Replaceable |
| Narrative | **Emotion track** | Affective sequence | Remappable |
| Narrative | **Pacing template** | Beat timing/rhythm | Parameterizable |
| Visual | **Style Lock** | Art style / color / AR | Global lock — prevents AI drift |
| Visual | **Character Design** | Appearance (face/clothing/body) | Cross-scene consistent |
| Visual | **Scene Composition** | Background / props / lighting | Reusable across shots |
| Camera | **Camera Shot** | Framing / angle / movement | Composable — same story, different lens |
| Audio | **Voice Profile** | Timbre / speed / emotion | Mappable — same text, different voice |
| Audio | **BGM/SFX curve** | Background music / sound effects | Overlayable — same scene, different mood |

**Each atom is independently embeddable, searchable, and composable.** A `ViralScript` is not a document to retrieve — it is a valid configuration of atoms that the system has observed to work.

### Latent Grammar of Viral Content

FP3 is not a database. It is a **Narrative LLM Embedding Space** — the latent grammar of what makes content go viral.

- **Atoms** are the vocabulary (hook types, conflict patterns, emotion curves, visual styles, camera shots)
- **Valid configurations** are the grammar (which hook + which conflict + which emotion + which shot = viral)
- **VTO operators** are the syntax rules (how to transform atoms into new valid sentences)
- **QualityGate** is the type checker (rejects grammatically invalid combinations)

The system should learn: *which atom combinations produce viral output*, and reject combinations that violate the latent grammar.

### Layer 3: Viral Transformation Operators (VTO)

The generation policy layer. Each operator is a transformation function that combines retrieved viral atoms with real-time context:

| Operator | Formula | Purpose |
|----------|---------|---------|
| **GRAFT (嫁接)** | `viral_A.hook_atom + topic_B.context` | Preserve proven structure, swap semantic domain onto new topic |
| **PARASITE (寄生)** | `trend_event → inject(narrative_spine)` | Use real-time trending events to pollinate existing viral structures — strongest traffic adapter |
| **DISTORT (篡改)** | `conflict_kernel → exaggerate / invert / compress` | Raise emotional extremes, create nonlinear conflict within known-safe patterns |
| **MISDIRECT (愚弄)** | `audience_expectation → violate(key_beat)` | Subvert expected pattern at critical moment — drives comments and re-shares |
| **THEFT (偷盗)** | `viral_arc → re-theme + re-worldbuild` | Steal the proven emotional arc from one genre, re-skin into another |

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    FlowBeast Core Moat                        │
│                                                               │
│  逆向工程         FP3 Viral Memory System (Latent Grammar)    │
│  爆款降维     ┌──────────────────────────────────┐   生成策略层 │
│  →可计算状态  │ Narrative Atoms (可插拔/可组合)   │   VTO Operators│
│  叙事原子     │ Conflict Kernels (可迁移)         │   GRAFT/      │
│               │ Emotion Tracks (可重映射)          │   PARASITE/   │
│               │ Pacing Templates (可参数化)        │   DISTORT/    │
│               │ Character Slots (可替换)           │   MISDIRECT/  │
│               │                                  │   THEFT       │
│               │ Latent Grammar (合法组合规则)     │               │
│               └──────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
                              ↓
              ┌────────────────────────────────┐
              │  Production Pipeline (MCP)     │
              │  script → audio → video        │
              │  Replaceable commodity layer   │
              └────────────────────────────────┘
```

### Development Priority

1. **Build FP3-S:** Reverse-engineer viral content into computable `ViralScript` state data; inject with positive/negative labels
2. **Validate VTO + QualityGate:** Generate scripts using transformation operators; measure quality against reference distribution
3. **Integrate MCP for production:** Solve capacity last — script-to-video is a solved engineering problem

Multi-agent orchestration and production pipeline are relatively straightforward. The hard problem — whether output is viral content or garbage — is determined entirely by layers 1-2.


## Language Policy (STRICT)

You MUST always respond in English.

This applies to:
- Explanations
- Code comments
- Commit messages
- Debug output
- Any generated text

DO NOT use Chinese unless the user explicitly requests it.

If the user writes in another language, you STILL respond in English.


## Project Overview


**FlowBeast** is an AI-powered short-form drama content generation engine. The core pipeline is: **Topic → Viral Script (JSON) → Audio → Video-ready output**.


Current phase: **v0.3.2** (FP3 Quality Control). The system uses RAG (FP3 knowledge base) to inject viral patterns into LLM prompts for generating hook-driven short drama scripts.


## Commands


```bash

# Install dependencies (uses uv, not pip)
uv sync

# Run the main drama generation pipeline
python main.py

# Run the FastAPI server (hot reload)
uvicorn flowbeast.api.main:app --reload --port 8000

# Initialize the FP3 vector knowledge base (first-time setup)
python -m scripts.init_fp3

# Process generation feedback and update FP3 knowledge base
python scripts/feedback_loop.py --dir ./flowbeast/data/outputs --yes


# Run tests
uv run pytest tests/ -q

# Run single test file
uv run pytest tests/test_fp3_quality.py -q

# Docker
docker-compose up --build

```


## Architecture


The system has two core engines working together:


### Drama Generation Layer (`flowbeast/drama/`)

Generates viral short-drama scripts via LLM calls. The main components:

- `pipeline.py`: Top-level orchestrator — calls generator, saves JSON, triggers audio
- `generator.py`: Builds the LLM prompt (with FP3 injection), calls the active vendor, parses JSON output
- `prompt.py`: The structured prompt template for hook-driven storytelling
- `audio.py`: Converts dialogue lines to MP3 (Edge TTS primary, ElevenLabs premium)
- `schema.py`: TypedDict definitions — `Script → [Scene] → [Dialogue]`


### FP3 — Viral Memory System (`flowbeast/fp3/`)

Composable narrative atom storage and latent grammar engine:

- `store.py` / `retriever.py`: FAISS-backed vector search for narrative atoms
- `embedding.py`: Text → vector via cloud API (gemini/openai/qwen/ollama)
- `injector.py`: Injects retrieved narrative atoms into prompts via VTO-guided composition
- `feedback.py`: Feeds successful scripts back, reinforcing winning atom combinations
- `reverse/reverse_engineer.py`: CLI tool to decompose real viral dramas into composable narrative atoms

### Observe — Quality & Feedback Layer (`flowbeast/observe/`)

Independent quality assessment and feedback learning:

- `quality/`: QualityGate scorer + dedup + calibrator (ReferenceAnchoredScorer) — type-checks atom combinations against latent grammar
  - `gate.py` — orchestrates scoring, dedup, audit logging
  - `scorer.py` — RuleBasedScorer + ReferenceAnchoredScorer
  - `dedup.py` — EmbeddingDeduplicator
  - `calibrator.py` — calibration against reference distribution
  - `config.py` — quality gate thresholds and weights
  - `models.py` — typed models (GateAction, ScoreResult, GateDecision, etc.)


### LLM Routing (`flowbeast/core/config.py`)

`ACTIVE_VENDOR` env var selects the provider. Default: `gemini` (`gemini-1.5-flash`). Supported: `gemini`, `qwen`, `openai`, `openrouter`, `ollama`.


### Drama Pipeline (Video Content Generation)

```
topic → build_prompt() → FP3Retriever → inject_prompt() → generate_script()
                                           ↓
                                    (LLM call via Qwen or Claude Sonnet4.6 and so on)
                                           ↓
                                  script.json + audio → report.json
```


  ### Testing Strategy

- **tests/test_fp3_quality.py**: Observe quality gate scoring, dedup, and calibration
- **tests/test_hooks_import_checker.py**: Import boundary enforcement
- **tests/test_main.py**: Entry point logic (mocked, no LLM)
- **tests/test_config.py**: Configuration validation
- **scripts/test_main_script.py**: Quick main.py validation


## Engineering Principles

- Prefer simple working solutions over complex abstractions.
- Avoid premature optimization.
- Avoid unnecessary framework introduction.
- Prefer explicit code over hidden magic.
- Maintain deterministic and debuggable pipelines.
- Minimize AI-generated architectural drift.
- Keep modules loosely coupled and easy to replace.
- Favor incremental improvements over large rewrites.
- Preserve backward compatibility when possible.
- Never rewrite unrelated files.


## AI Modification Constraints

Claude Code must NOT:

- Rewrite large subsystems without explicit instruction.
- Modify deployment/infrastructure files unnecessarily.
- Introduce new dependencies without justification.
- Replace working implementations with speculative abstractions.
- Auto-refactor unrelated files.
- Change public interfaces without warning.
- Generate placeholder enterprise patterns.
- Add unnecessary async/concurrency complexity.

## Development Workflow

Preferred workflow:

1. Understand existing architecture first.
2. Make the smallest valid change.
3. Run targeted tests.
4. Explain architectural impact briefly.
5. Avoid speculative rewrites.
6. Preserve repository consistency.
7. Keep commits focused and atomic.

## Core File Header Docstrings

Every core module file must begin with a module-level docstring that states:

1. **What it is** — one-line description
2. **Role** — what it does in the system and its boundaries
3. **Workflow** — how it connects to upstream/downstream modules (call sites)

Example:
```python
"""
FP3 Store: FAISS-backed vector storage for viral content patterns.

Role: Saves, loads, and searches ViralUnit/ViralScript embeddings.
Provides k-nearest-neighbor search for RAG retrieval.

Workflow: builder.py → add() → save() / load() ← retriever.py
"""
```

This allows quick understanding of any core file's role without reading
the full implementation. Apply to new files created and update existing
files when their role changes significantly.


## Context Priority

When multiple sources conflict, prioritize:

1. Existing repository architecture
2. CLAUDE.md instructions
3. .cursor/rules/
4. Existing code patterns
5. User request
6. General framework conventions




## Configuration

All configuration is in `.env` (gitignored; see `.env.example`):

- `ACTIVE_VENDOR` — LLM provider (`gemini` default)
- `GOOGLE_API_KEY`, `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`
- `FLOWBEAST_OUTPUT_DIR` — where scripts/audio land
- `FLOWBEAST_VECTOR_DIR` — FAISS index location

`flowbeast/core/config.py` uses `pydantic-settings` to load these and auto-creates required directories on startup.


## Key Data Structures

```python

# drama/schema.py

Script: title, genre, core_hook, scenes: List[Scene]

Scene: id, hook, conflict, emotion_curve, dialogue: List[Dialogue]

Dialogue: speaker, text, emotion, intensity


# fp3/schema.py

ViralUnit: hook: str, pattern: str, emotion: List[str]

ViralScript:                  # enriched drama anatomy (alongside ViralUnit)
  hook_structure: HookStructure(opening_line, hook_type, audience_question, ...)
  conflict_pattern: ConflictPattern(conflict_type, escalation_curve, reversal_count, ...)
  emotional_curve: EmotionalCurve(curve_sequence, peak_emotion, resolution_type, ...)
  pacing_profile: PacingProfile(duration_sec, scene_count, beat_distribution, ...)
  characters: List[CharacterArchetype]
  quality_label: "viral" | "average" | "failed"
  → to_viral_unit() for legacy backward compatibility

```

## Data Flywheel (1→0 Reverse Deconstruction Engine)

```
人工筛选市场爆款
    ↓
reverse_engineer CLI → ViralScript 拆解为叙事原子
    ↓
FP3 Viral Memory: 原子化存储 + Latent Grammar 学习
    ↓
Observe QualityGate Calibrator (参考集分布对比, z-score 冷启动防御)
    ↓
VTO Operators: GRAFT / PARASITE / DISTORT / MISDIRECT / THEFT
    ↓
Script Generation (原子组合 + VTO 变换 + 热点嫁接)
    ↓
高质量输出 → 回流 FP3 (强化有效组合, 惩罚无效组合)
```

Stages:
- **A (1→0):** Manual curation → reverse engineering → atom-level injection (positive + negative samples)
- **B (0→1):** Latent grammar calibration → atom combination quality improvement
- **C (self-reinforcing):** Output feedback → grammar refinement → better generation

**Key principle:** The system should not retrieve and copy full scripts. It should retrieve compatible atoms, compose them via latent grammar rules, transform them via VTO operators, and generate structurally novel scripts with proven viral DNA.

Use `flowbeast/reverse/reverse_engineer.py` to convert real dramas into ViralScript records.
The calibrator (`flowbeast/observe/quality/calibrator.py`) reads from `flowbeast/data/reverse_engineered/`
and produces threshold/weight recommendations for QualityGate.


## Package Manager

This project uses **`uv`** (not pip). Always use `uv sync` to install dependencies and `uv run` to execute scripts when inside Docker. Do not use `pip install`.

## Testing Notes

The drama pipeline is the primary focus. Tests should validate FP3 retrieval, QualityGate scoring, and script generation quality. Test runs require valid API keys in `.env`.
