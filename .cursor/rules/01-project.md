# FlowBeast Project Rules

> Core project philosophy and guiding principles

## Project Overview

FlowBeast is an **AI short-drama production engine**: input a topic, output a complete production package (`prompt_package.json` + episode audio) ready for an AI video tool to render into a finished episode.

**The package is an artifact, not the product.** The product is an episode that can be published as-is. Positioning and product form are deliberately **not** specified here — see [CLAUDE.md](../../CLAUDE.md), which defers them to `.ai/current/founder_notes.md` (local, not committed).

The core asset is the **FP3 Viral Memory System** — real viral scripts decomposed into composable narrative atoms (`ViralUnit`: hook / pattern / emotion), retrieved by similarity and injected into the generation prompt. Audio generation (Edge TTS) doubles as a quality-validation layer. Video rendering is a replaceable commodity layer.

Current focus:
- A **fixed format** — same characters, same sets, one vertical niche, one repeatable structure
- Marginal cost per episode low enough to publish daily
- Production package export (script JSON + shot prompts + style lock + audio)
- End-to-end delivery path: topic → episode that ships
- **Rule 0: never reinvent the wheel** — integrate/borrow before writing

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
- Rapid experimentation with narrative atoms and shot composition
- Local-first workflows with cloud API fallback for LLM/embedding
