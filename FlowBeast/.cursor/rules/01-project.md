# FlowBeast Project Rules

> Core project philosophy and guiding principles

## Project Overview

FlowBeast is an AI-native content generation and automation system.

Current focus:
- Viral content pipeline
- AI drama/comic generation
- RAG + retrieval enhancement
- Multi-agent orchestration
- Automated video/content workflow
- Fast iteration MVP

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

1. Working systems over theoretical perfection
2. Fast iteration over premature abstraction
3. Simplicity over enterprise complexity
4. Maintainability over clever code
5. Production pipeline stability over experimentation

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
- AI-assisted development
- Multi-model collaboration
- Long context engineering
- Rapid experimentation
- Local-first workflows
