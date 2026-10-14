# FlowBeast Testing Rules

> Testing strategy and conventions

## Testing Philosophy

- Reliability over coverage vanity
- Test critical pipelines first
- Preserve iteration speed

## Priority Testing Areas

**Highest priority:**
- FP3 retrieval logic
- Observe QualityGate scoring and calibration
- Narrative atom composition and VTO transformations
- Prompt pipelines (build_prompt → inject → generate)
- Config loading
- Docker/devcontainer behavior
- API boundaries

**Lower priority:**
- Thin wrappers
- Simple DTOs
- Trivial utility functions

## Preferred Test Style

Prefer:
- pytest
- Clear test naming
- Small focused tests
- Integration tests for pipelines
- Realistic test data

Avoid:
- Over-mocking
- Brittle snapshot tests
- Artificial enterprise test patterns

## Test Naming

Use:
- `test_<behavior>`
- `test_<condition>_<result>`

Examples:
- `test_load_config_from_env`
- `test_retriever_returns_ranked_results`
- `test_pipeline_handles_timeout`

## AI Pipeline Testing

AI-related tests should:
- Validate structure
- Validate schema
- Validate retries/fallbacks
- Avoid depending on exact wording

## Regression Prevention

Important bug fixes should include tests.

## Performance

Tests should:
- Run locally
- Work inside devcontainers
- Avoid external dependency requirements when possible
