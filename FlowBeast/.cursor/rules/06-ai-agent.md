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

## Human-in-the-Loop Workflows

FlowBeast relies on human curation for quality data injection, not autonomous AI self-improvement:

- **Reverse Engineering**: The `reverse_engineer` CLI requires a human to watch and analyze real dramas,
  then provide structured judgments (hook type, conflict pattern, emotional curve, quality label).
  This is intentional — AI cannot reliably self-evaluate content quality without a ground-truth anchor.

- **QualityGate Calibration**: Scores are anchored against a human-curated reference distribution.
  The calibrator computes z-scores from real viral samples, not theoretical ideals.
  When sample count < 5, σ=0 cold-start protection prevents meaningless z-score computation.

- **Negative Samples**: `quality_label` ("viral" / "average" / "failed") allows boundary learning.
  The system must learn what to reject as much as what to accept.

## MCP Integration (Production Pipeline)

The production pipeline (script → audio → video) is solved via MCP/Skills integration with third-party tools (Runway, Kling, HeyGen, etc.).

Principles:
- MCP endpoints should be stable, explicit, and observable
- FlowBeast decides WHAT to produce; MCP tools handle HOW to render it
- Production capacity is horizontally scalable and replaceable
- No need to build custom audio/video generation — integrate, don't reinvent

Avoid:
- Recursive uncontrolled agent loops
- Excessive autonomy in production pipeline
- Autonomous self-calibration without human-curated reference data
- Over-investing in production pipeline sophistication
