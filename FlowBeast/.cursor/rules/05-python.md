# FlowBeast Python Rules

> Python-specific conventions and requirements

## Preferred Stack

- Python 3.11+
- FastAPI
- Pydantic
- pytest
- uv (package manager)

## Async

Use async only when:
- IO-bound
- External API heavy
- Parallel workflows are beneficial

**Avoid unnecessary async complexity.**

## Pydantic

Prefer Pydantic for:
- Config models
- Request schemas
- Structured outputs
- Pipeline contracts

## File Paths

Never hardcode absolute paths.

Use:
- `pathlib.Path`
- Config-driven paths

## Environment

Code must work in:
- Local Linux
- Docker
- Dev Containers
- CI environments

## External APIs

External API integrations must:
- Support retries
- Handle timeouts
- Handle rate limits
- Preserve observability

## AI API Calls

AI model calls should:
- Preserve prompts
- Preserve responses
- Support provider swapping
- Avoid provider lock-in

## Package Management

Always use `uv` for package management:
```bash
uv sync          # Install dependencies
uv add <package> # Add new dependency
uv run pytest    # Run tests
```
