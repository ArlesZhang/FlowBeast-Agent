# FlowBeast Coding Style Rules

> General coding guidelines and patterns

## Prohibited Patterns

Never use:
- One-letter variables (except in short loops)
- Clever hacks
- Deep nesting (more than 3 levels)
- Massive functions
- Unnecessary async

## Comments

Comments should explain:
- Why (not what)
- Architectural intent
- Non-obvious decisions

**Do NOT comment obvious code.**

## Logging

Prefer structured logging.

Log:
- Pipeline stages
- Errors
- Retries
- Important state transitions
- AI request metadata

**Avoid noisy logs.**

## Error Handling

Never silently swallow exceptions.

Prefer:
- Explicit exception handling
- Meaningful error messages
- Retry-safe operations

## Imports

Prefer:
- Absolute imports
- Stable import paths (e.g., `from flowbeast.drama.generator import ...`)
- Grouped imports (stdlib, third-party, local)

Avoid:
- Wildcard imports (`from xxx import *`)
- Circular dependencies

## Refactoring

Refactors should:
- Preserve behavior
- Be incremental
- Avoid unnecessary rewrites
- Minimize architectural drift

## AI-Generated Code

AI-generated code must:
- Be production-readable
- Avoid placeholder implementations
- Avoid fake mocks unless requested
- Avoid TODO-heavy output
- Prefer working minimal solutions
