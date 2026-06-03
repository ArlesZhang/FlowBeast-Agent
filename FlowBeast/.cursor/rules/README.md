# FlowBeast Cursor Rules

Welcome to FlowBeast's AI-assisted development rules.

```
.cursor/
└── rules/
    ├── 01-project.md
    ├── 02-architecture.md
    ├── 03-coding-style.md
    ├── 04-testing.md
    ├── 05-python.md
    ├── 06-ai-agent.md
    ├── 07-docker-devcontainer.md
    └── 08-git-workflow.md
```

## Purpose

These rules are designed to:
- Maintain stable AI output
- Reduce architecture drift
- Enhance long-term consistency
- Prevent AI over-engineering
- Support multi-model collaboration (Claude / DeepSeek / Qwen)

## Current Focus

- FP3 Viral Memory System (narrative atom extraction + injection)
- Latent grammar learning for viral content generation
- VTO-guided script generation (GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT)
- QualityGate calibration against reference distribution
- MCP integration for audio/video production (commodity layer)

## Project Priorities

1. The "Brain" (what to produce) over the pipeline (how to render it)
2. Working systems over theoretical perfection
3. Fast iteration over premature abstraction
4. Simplicity over enterprise complexity
5. Maintainability over clever code

## Philosophy

This is NOT about "restricting AI". It's about stabilizing AI's long-term output style.

For FlowBeast's stage, the most important thing is:
- Prevent AI over-engineering (pipeline sophistication is not the moat)
- Prevent architecture drift (FP3 is the core, everything else is commodity)
- Maintain long-term consistency
- Improve multi-model collaboration stability
- Reduce context pollution

## Usage

These rules are loaded by Cursor IDE to guide AI behavior. The rules are organized into:

- `01-project.md` - Project overview and philosophy
- `02-architecture.md` - Architecture rules and patterns
- `03-coding-style.md` - Coding style guidelines
- `04-testing.md` - Testing strategy and rules
- `05-python.md` - Python-specific conventions
- `06-ai-agent.md` - AI agent design rules
- `07-docker-devcontainer.md` - Container environment rules
- `08-git-workflow.md` - Git workflow conventions
