# FlowBeast AI Agent Rules

> AI agent design and implementation guidelines

## Agent Philosophy

- Agents are tools, not magic
- Deterministic pipelines are preferred when possible
- Observability is mandatory

## Agent Design

Agents should:
- Have clear responsibilities
- Have explicit inputs/outputs
- Be composable
- Be debuggable

Avoid:
- Monolithic autonomous agents
- Hidden prompt chains
- Untraceable tool calls

## Prompt Engineering

Prompts should:
- Be versioned
- Be modular
- Be reusable
- Be observable

## Tool Usage

Tool interfaces should:
- Be stable
- Be explicit
- Return structured data

## Multi-Agent Systems

Prefer:
- Coordinator patterns
- Explicit orchestration
- Shared memory abstractions

Avoid:
- Recursive uncontrolled agent loops
- Excessive autonomy
