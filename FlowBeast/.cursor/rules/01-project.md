# FlowBeast Project Rules

> Core project philosophy and guiding principles

## Project Overview

FlowBeast is an AI-powered viral short-drama engine. The core moat is the **FP2 Viral Memory System** — decomposing viral content into composable narrative atoms, learning their latent grammar, and transforming them via VTO operators to generate structurally novel scripts. The production pipeline (script → audio → video) is a replaceable commodity layer.

Current focus:
- FP3 narrative atom extraction and injection
- Latent grammar learning for viral content
- VTO-guided script generation (GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT)
- QualityGate calibration
- MCP integration for audio/video production

## Core Principles

The assistant must:
- Preserve existing architecture unless explicitly instructed
- Avoid unnecessary abstractions
- Avoid introducing frameworks unless required
- Avoid rewriting unrelated modules
- Prefer incremental refactors
- Keep functions and modules understandable
- Preserve backward compatibility when possible

## Project Priorities

1. The "Brain" (what to produce) over the pipeline (how to render it)
2. Working systems over theoretical perfection
3. Fast iteration over premature abstraction
4. Simplicity over enterprise complexity
5. Maintainability over clever code

## Understanding the Project

The assistant should understand:
- This is a long-term evolving monorepo
- Architecture consistency is critical
- Token/context efficiency matters
- Docker/devcontainer environment is important
- Local development workflow must remain stable

## Code Generation Guidelines

When generating code:
- Prefer explicit code over magic
- Prefer readability over extreme DRY
- Prefer predictable behavior over hidden automation
- Prefer modular design without fragmentation

## Prohibitions

Never:
- Silently rename public APIs
- Change project structure without reason
- Introduce heavy dependencies casually
- Generate fake implementations pretending to work
- Over-engineer abstractions for future possibilities
- Replace existing stable implementations unnecessarily

## Optimization Targets

The project is optimized for:
- AI-assisted development (Claude Code as primary collaborator)
- Multi-model collaboration (Qwen / Openai / Gemini / Claude)
- Rapid experimentation with narrative atoms and VTO operators
- Local-first workflows with cloud API fallback for LLM/embedding
