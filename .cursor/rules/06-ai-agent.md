# FlowBeast AI Agent Rules

> AI agent design and implementation guidelines
> NOTE: Rules below apply to the current phase. Revisit when the commercial phase changes.

## Phase Context

**Current — Delivery validation:** Land the first paying customer for a delivered episode.
Human judgment decides what ships; AI assists. No autonomous self-improvement.

**Later — Automation:** Only after there is real payment evidence. Topic discovery,
automated feedback loops, trend sensing. Rules in this file get updated then.

**Note:** the earlier "reverse-engineer viral dramas into a corpus" phase was falsified and its
tooling removed. The *principle* below still holds — AI still cannot self-evaluate content quality
without a ground-truth anchor; the anchor is now customer feedback, not a scraped corpus.

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

> These rules apply while the knowledge base is small and calibration is manual.
> Revisit when automated data pipelines are actually online.

FlowBeast relies on human judgment for quality, not autonomous AI self-improvement:

- **Ground truth comes from delivery.** A human (the operator, then the customer) decides whether
  an episode is good. AI cannot reliably self-evaluate content quality without an external anchor —
  and the only anchors that count are **a human's judgment** and **real engagement data**.

- **QualityGate is uncalibrated.** Its 9 dimensions have never produced an ACCEPT, and the weights
  were never fitted to outcomes. Treat the score as a weak signal. The deleted calibrator was
  circular (weights derived from scores derived from the same weights) — do not rebuild that shape.

- **Negative Samples**: knowing what to reject matters as much as what to accept. Record rejected
  and failed deliveries, not just successful ones.

## MCP Integration (Production Pipeline)

> This section is Rule 0 applied to production. It does not expire.

The production pipeline (script → audio → video) is solved via MCP/Skills integration with third-party tools (Runway, Kling, HeyGen, Seedance, etc.).

Principles:
- MCP endpoints should be stable, explicit, and observable
- FlowBeast decides WHAT to produce; MCP tools handle HOW to render it
- Production capacity is horizontally scalable and replaceable
- No need to build custom audio/video generation — integrate, don't reinvent
- **Before writing any module, search for an existing tool first** (see CLAUDE.md Rule 0)

Avoid:
- Recursive uncontrolled agent loops
- Excessive autonomy in the production pipeline
- Self-calibration against your own scores (circular — this was already tried and deleted)
- Over-investing in production pipeline sophistication
- Writing our own version of something a library already does
