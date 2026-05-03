# FlowBeast Hooks System v2

**Adaptive Guardrail for FlowBeast**

A Python-based git hooks system that enforces architectural integrity and protects the FP3/IP2 core system during development.

## Overview

This is **NOT** a generic linting system. This is an **ADAPTIVE GUARDRAIL** layer that prevents accidental architectural degradation during rapid development.

### v2 UPGRADES

- **Configurable Policies**: Rules are now configurable via whitelist system
- **Structural Abstraction**: Checks for structural patterns, NOT exact pipeline steps
- **Evolvable**: Easy to extend with new checks without breaking existing rules
- **Backward Compatible**: All existing functionality preserved

### Architecture Rules Enforced

1. **No Legacy Contamination**: Core modules (fp3, drama) must never import from `flowbeast.legacy_workflows.*`
   - Note: `agent` module is allowed via whitelist for workflow compilation

2. **Config Centralization**: All modules should use `flowbeast.core.config`

3. **FP3 Integrity**: FP3 structural abstraction (evaluation entry points, scoring interface, retrieval abstraction) must be intact

## Components

```
flowbeast/hooks/
├── __init__.py              # Package initialization
├── import_checker.py        # RULE 1: Check illegal imports (v2 with whitelist)
├── fp3_guard.py             # RULE 3: Protect FP3 integrity (v2 structural checks)
├── hook_runner.py           # Main hook orchestration
└── README.md                # This file
```

Tests are in `tests/`:
- `tests/test_hooks_import_checker.py` (v2 whitelist tests)
- `tests/test_hooks_fp3_guard.py` (v2 structural tests)

## Usage

### Pre-Commit Hook

Automatically runs on every commit:

```bash
git commit -m "Your message"
```

Checks performed:
- Illegal imports (core → legacy) - **enforced**
- FP3 structural abstraction check - **enforced**
- Missing bypass patterns - **enforced**
- Type hints - **skipped** (soft check)

### Pre-Push Hook

Automatically runs before push:

```bash
git push origin main
```

Runs:
- FP3 tests
- Key pipeline tests

Fails if any FP3-related test fails.

## Installation

The hooks are installed in `.git/hooks/`:

```bash
# Hooks are automatically placed in .git/hooks/
ls -la .git/hooks/pre-commit
ls -la .git/hooks/pre-push
```

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

### Bypassing Hooks (Not Recommended)

```bash
# Bypass pre-commit hook
git commit --no-verify -m "Your message"

# Bypass pre-push hook
git push --no-verify
```

**Warning**: Use `--no-verify` only when you know what you're doing. These hooks protect the architectural integrity of the codebase.

## Whitelist System (v2)

The import checker uses a configurable whitelist system:

```python
ALLOWED_IMPORTS = {
    "flowbeast.agent": [
        "flowbeast.legacy_workflows.ir.models",
        "flowbeast.legacy_workflows.ir.*",
        "flowbeast.legacy_workflows.*",
    ],
}
```

To add a new allowed import:

1. Add to `ALLOWED_IMPORTS` in `flowbeast/hooks/import_checker.py`
2. Use wildcard patterns (`.*`) for module-level access

### FP3 Structural Checks (v2)

The FP3 guard now checks for **structural abstraction**, NOT exact pipeline steps:

**What it checks:**
1. `store.py` exists with VectorStore/QdrantStore/etc. class
2. `retriever.py` exists with retrieve/search method
3. `embedding.py` exists with embed/encode function
4. No bypass patterns in code (e.g., `# quality check disabled`)

**What it does NOT check:**
- Exact pipeline sequence
- Specific function names
- Implementation details

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Git Hook                              │
│                  (pre-commit / pre-push)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Hook Runner                              │
│               Orchestrates all checkers                     │
└──────────┬───────────────┬──────────────────────────────────┘
           │               │
           ▼               ▼
┌─────────────────┐  ┌─────────────────┐
│ Import Checker  │  │   FP3 Guard     │
│ (v2 Whitelist)  │  │  (v2 Structural)│
└─────────────────┘  └─────────────────┘
           │               │
           ▼               ▼
┌────────────────────────────────────────┐
│           Violation Reporting          │
└────────────────────────────────────────┘
```

## Extending

Add new checks by:

1. Creating a new checker module in `flowbeast/hooks/`
2. Implementing the check logic
3. Adding the checker to `hook_runner.py`

Example:

```python
# flowbeast/hooks/my_checker.py
class MyChecker:
    def check(self, files: List[str]) -> List[Violation]:
        # Your check logic
        pass

# In hook_runner.py
def _run_my_checker(self, files: List[str]) -> int:
    from flowbeast.hooks.my_checker import MyChecker
    checker = MyChecker()
    violations = checker.check(files)
    return 0 if not violations else 1
```

## Troubleshooting

### Hook fails with "Module not found"

```bash
# Ensure dependencies are installed
uv sync

# Run the hook manually to see detailed error
uv run python -m flowbeast.hooks.hook_runner pre-commit
```

### Hook is too slow

The hooks only check staged/modified files for pre-commit. For full checks, run:

```bash
uv run pytest tests/ -q
```

before pushing.

## Behavior Notes

### Warning vs Error

- **Warning**: Informational checks - do not block commits/pushes
- **Error**: Actual violations - block commits/pushes

### v1 vs v2 Comparison

| Feature | v1 | v2 |
|---------|----|----|
| Import Rules | Hard-coded | Whitelist-based |
| FP3 Checks | Exact pipeline steps | Structural abstraction |
| Configurability | Low | High |
| Brittle | Yes | No |
| Extendable | Medium | High |
