# FlowBeast Hooks System

**Adaptive Guardrail for FlowBeast**

A Python-based hooks system that enforces architectural integrity during development.

## Overview

This is **NOT** a generic linting system. This is an **ADAPTIVE GUARDRAIL** layer that prevents accidental architectural degradation during rapid development.

### Architecture Rules Enforced

1. **Config Centralization**: All core modules should use `flowbeast.core.config`

2. **FP3 Integrity**: FP3 structural abstraction (store, retriever, embedding interfaces) must be intact

## Components

```
flowbeast/hooks/
├── __init__.py              # Package initialization
├── import_checker.py        # Check config usage and FP3 integrity
├── fp3_guard.py             # Protect FP3 structural abstraction
├── hook_runner.py           # Main hook orchestration
└── README.md                # This file
```

Tests are in `tests/`:
- `tests/test_hooks_import_checker.py`
- `tests/test_hooks_fp3_guard.py`

## Usage

### Pre-Commit Hook

Automatically runs on every commit:

```bash
git commit -m "Your message"
```

### Pre-Push Hook

Automatically runs before push:

```bash
git push origin main
```

## Installation

The hooks are automatically placed in `.git/hooks/`.

Both hooks are executable and ready to use.

## Development

### Running Checks Manually

```bash
# Run pre-commit checks
uv run python -m flowbeast.hooks.hook_runner pre-commit

# Run pre-push checks
uv run python -m flowbeast.hooks.hook_runner pre-push
```

### Running Tests

```bash
# Run all hook tests
uv run pytest tests/test_hooks_import_checker.py
uv run pytest tests/test_hooks_fp3_guard.py

# Run all tests
uv run pytest tests/ -v
```

## Architecture

```
┌─────────────────────────────────┐
│       Git Hook                  │
│  (pre-commit / pre-push)        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│       Hook Runner               │
│  Orchestrates all checkers      │
└──────┬──────────────┬───────────┘
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│ImportChecker│  │  FP3 Guard  │
└─────────────┘  └─────────────┘
       │              │
       ▼              ▼
┌───────────────────────────┐
│    Violation Reporting    │
└───────────────────────────┘
```

## Extending

Add new checks by:

1. Creating a new checker module in `flowbeast/hooks/`
2. Implementing the check logic
3. Adding the checker to `hook_runner.py`

## Troubleshooting

### Hook fails with "Module not found"

```bash
# Ensure dependencies are installed
uv sync

# Run the hook manually to see detailed error
uv run python -m flowbeast.hooks.hook_runner pre-commit
```
