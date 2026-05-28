# FlowBeast AI Agent Rules

> AI agent design and implementation guidelines
> NOTE: Rules below apply to Phase 1 (current). Phase 2+ goals override these when reached.

## Phase Context

**Phase 1 (v0.3.x — NOW):** Human-curated data injection. All quality data comes from real viral dramas analyzed by a human via `reverse_engineer` CLI. No autonomous self-improvement.

**Phase 2 (v0.6+ — FUTURE):** Topic Discovery Engine, real-time streams (Kafka/Qdrant), automated feedback loops. Rules in this file will be updated at that time.

**Phase 3 (Endgame):** Fully autonomous pipeline: trend sensing → viral modeling → content generation → video production → auto-distribution. This is the goal, not a constraint.

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

## Human-in-the-Loop Workflows (Phase 1)

> These rules apply while the knowledge base is small and calibration is manual.
> Revisit when Phase 2 automated data pipelines are online.

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

> Current phase: integrate commodity tools, don't reinvent. Phase 2+ may change this.

The production pipeline (script → audio → video) is solved via MCP/Skills integration with third-party tools (Runway, Kling, HeyGen, etc.).

Principles:
- MCP endpoints should be stable, explicit, and observable
- FlowBeast decides WHAT to produce; MCP tools handle HOW to render it
- Production capacity is horizontally scalable and replaceable
- No need to build custom audio/video generation — integrate, don't reinvent

Avoid (Phase 1):
- Recursive uncontrolled agent loops
- Excessive autonomy in production pipeline
- Autonomous self-calibration without human-curated reference data
- Over-investing in production pipeline sophistication

> When Phase 2 is reached, revisit: automated calibration and autonomous feedback
> loops become goals, not anti-patterns.
