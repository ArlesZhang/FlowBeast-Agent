# FlowBeast Architecture Rules

> Architecture principles and patterns

## Core Architecture

```
Reverse engineering → FP3 Viral Memory → VTO Operators → Script Generation → Feedback
```

## Layer Definitions

- **FP3** = Viral Memory System (the core moat)
  - Composable narrative atoms (hook, conflict, character, emotion, pacing)
  - Dual schema: `ViralUnit` (3-field legacy) + `ViralScript` (enriched drama anatomy)
  - Reverse engineering CLI converts real dramas into structured ViralScript records
  - VTO operators (GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT) for generation strategy
  - `feedback.py` — output feedback reinforces winning atom combinations
- **Observe** = Quality & feedback layer (`flowbeast/observe/`)
  - `quality/` — QualityGate scorer, dedup, calibrator (independent of FP3 internals)
  - Future: metrics, tracing, monitoring
- **Drama** = Script generation pipeline (`flowbeast/drama/`)
  - `pipeline.py` → `generator.py` → `prompt.py` → `audio.py`
  - FP3 injection occurs inside `generate_script()` before LLM call
- **Core** = Configuration, routing (`flowbeast/core/`)
- **Production** = Script → audio → video (commodity, MCP-integrated)

## Data Flywheel Pattern (1→0 Reverse Deconstruction Engine)

FlowBeast uses a human-in-the-loop data flywheel for quality improvement:

```
Manual curation (market viral dramas)
    → reverse_engineer CLI → ViralScript anatomy (composable narrative atoms)
    → FP3 Viral Memory (atom-level injection, positive/negative labels)
    → Observe QualityGate calibrator (reference-distribution scoring, z-score cold-start defense)
    → VTO Operators (GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT)
    → Script generation (atom composition + VTO transformation)
    → High-quality output → feedback loops back to FP3
```

Key rules:
- FP3 quality depends on real viral content injection, not hand-written seeds
- Calibration requires >= 5 reverse-engineered samples for meaningful z-score statistics
- QualityGate falls back to rule-based scoring when no calibration report exists
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
