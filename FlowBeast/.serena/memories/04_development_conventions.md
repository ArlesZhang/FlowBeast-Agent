# Development Conventions

## Package Manager
- Use **`uv`** exclusively. `uv sync` to install, `uv run` to execute.
- Do NOT use `pip install`.

## Language Policy (STRICT)
- ALWAYS respond in English: explanations, code comments, commit messages, debug output.
- DO NOT use Chinese unless explicitly requested.

## Module Docstrings
Every core module must begin with a module-level docstring:
```python
"""
Module Name: One-line description.

Role: What it does + boundaries.
Provides: Key capabilities.

Workflow: upstream.py → this_module() → downstream.py
"""
```

## File Organization
- Core modules go in `flowbeast/` package
- Entry point: `main.py` (project root)
- Tests: `tests/` (pytest, run via `uv run pytest tests/ -q`)
- Dev configs: `.devcontainer/`, `.cursor/rules/`, `CLAUDE.md`
- Project goals/status: `.ai/current/` (goal.md, status.md, decisions/, tasks/)

## Git Workflow
- Branch: `develop` (main working branch)
- Pre-commit hooks run automatically (import check, type hints, FP3 integrity)
- Commit messages: prefix with type (`feat:`, `chore:`, `docs:`, `fix:`)
- End commit messages with: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Code Style
- Simple functions over abstractions
- Wrap instead of rewrite (don't refactor working code)
- JSON over infrastructure (prefer config files over databases)
- Match existing code's naming conventions, comment density, and idiom

## Configuration
- All config through `flowbeast/core/config.py` — single source of truth
- Use `pydantic-settings` for environment-variable-backed configuration
- pytest config in `pyproject.toml`: `[tool.pytest.ini_options] pythonpath = ["."]`

## Assets
- `assets/style/` — Style Lock files (visual_style.md, negative_prompt.txt, color_palette.json, render_rules.json)
- These are read by `asset_manager.py` to prevent AI style drift
