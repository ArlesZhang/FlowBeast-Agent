# FlowBeast Architecture Rules

> Architecture principles and patterns

## Core Architecture

```
FP2 -> FP3 -> IP1 -> IP2 -> Product -> Observe -> FP2
```

## Layer Definitions

- **FP2** = Data processing layer
- **FP3** = Viral knowledge base + retrieval
- **IP1** = Generation enhancement / RAG
- **IP2** = Multi-agent automation
- **Product** = Video/content pipeline MVP
- **Observe** = Observation and Feedback Center

## Module Boundaries

Each module should:
- Have a clear responsibility
- Minimize cross-dependencies
- Expose stable interfaces
- Avoid circular imports

## Preferred Design Patterns

Prefer:
- Service layer
- Adapters
- Config-driven systems
- Explicit pipelines
- Typed models
- Stateless processing

Avoid:
- Deep inheritance trees
- Hidden side effects
- God objects
- Overuse of decorators
- Meta-programming unless necessary

## Configuration Requirements

Configuration must:
- Use centralized config (see `flowbeast/core/config.py`)
- Support .env loading
- Work inside Docker/devcontainers
- Avoid hardcoded paths
- Support proxy/network configuration

## AI Pipeline Requirements

AI pipeline code should:
- Be traceable
- Be debuggable
- Preserve intermediate outputs
- Support retries
- Support caching when useful
- Preserve prompts for observability

## Long-term Maintainability

The assistant must think about:
- Future agent expansion
- Long context workflows
- Retrieval scaling
- Async task orchestration
- Content generation reliability

**But should NOT prematurely build infrastructure for them.**

## File Organization

Prefer:
- Small focused modules
- Clear naming
- Predictable directory structure

Avoid:
- 2000-line files
- Utility dumping grounds
- Random helper modules
