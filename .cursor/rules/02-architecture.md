# FlowBeast Architecture Rules

> Architecture principles and patterns

## Core Architecture

```
Reverse engineering → FP3 Viral Memory → VTO Operators → Script Generation → Feedback
```

## Layer Definitions

- **FP3** = Viral Memory System (the core moat)
  - Composable narrative atoms (hook, pattern, emotion)
  - `ViralUnit` — 3 fields, deliberately minimal
  - `feedback.py` — output feedback reinforces winning atom combinations
- **Observe** = Quality & feedback layer (`flowbeast/observe/`)
  - `quality/` — QualityGate scorer + dedup + audit (independent of FP3 internals)
  - Future: metrics, tracing, monitoring
- **Drama** = Script generation pipeline (`flowbeast/drama/`)
  - `pipeline.py` → `generator.py` → `prompt.py` → `audio.py`
  - FP3 injection occurs inside `generate_script()` before LLM call
- **Core** = Configuration, routing (`flowbeast/core/`)
- **Production** = Script → audio → video (commodity, MCP-integrated)

## Delivery Flow (current)

```
Topic → FP3 Viral Memory retrieval (atom injection)
    → Script generation
    → QualityGate (rule-based scorer + dedup)
    → Shot direction → TTS audio
    → prompt_package.json + episode_audio.mp3  ← delivered to the customer
    → Real engagement data → feedback_ingest → atom weights
```

Key rules:
- **Rule 0: never reinvent the wheel.** Integrate or borrow before writing (see CLAUDE.md).
- FP3 quality improves from **real delivery data**, not from reverse-engineering other people's hits
- QualityGate is currently uncalibrated — treat its score as a signal, not a verdict
- The only acceptance test is **有真实付费证据** (real payment evidence)
- ViralScript backward-compatible with ViralUnit via `to_viral_unit()`

## Module Boundaries

Each module should:
- Have a clear responsibility
- Minimize cross-dependencies
- Expose stable interfaces
- Avoid circular imports

## Preferred Design Patterns

Prefer:
- Service layer
- Adapters
- Config-driven systems
- Explicit pipelines
- Typed models
- Stateless processing

Avoid:
- Deep inheritance trees
- Hidden side effects
- God objects
- Overuse of decorators
- Meta-programming unless necessary

## Configuration Requirements

Configuration must:
- Use centralized config (see `flowbeast/core/config.py`)
- Support .env loading
- Work inside Docker/devcontainers
- Avoid hardcoded paths
- Support proxy/network configuration

## AI Pipeline Requirements

AI pipeline code should:
- Be traceable
- Be debuggable
- Preserve intermediate outputs
- Support retries
- Support caching when useful
- Preserve prompts for observability

## Long-term Maintainability

The assistant must think about:
- FP3 knowledge base quality (garbage in = garbage out)
- VTO operator effectiveness (which transformations produce viral output)
- QualityGate calibration accuracy
- Narrative atom composability and searchability
- MCP integration for production pipeline

**But should NOT prematurely build infrastructure for theoretical possibilities.**

## File Organization

Prefer:
- Small focused modules
- Clear naming
- Predictable directory structure

Avoid:
- 2000-line files
- Utility dumping grounds
- Random helper modules
