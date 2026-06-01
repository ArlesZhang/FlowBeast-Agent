# Hard Boundaries — What FlowBeast Does NOT Do

**Source:** `.ai/decisions/002_what_we_do_not_do.md`

**Every time tempted to build something new, check this list first.**

## Success Metric

**Can a new topic inherit proven viral mechanics and outperform baseline generation?**

Use this as the decision filter. If a proposed change doesn't help answer "yes" to this question, don't build it.

## 1. No Video Generation Code
- Do NOT call video APIs (Runway, Kling, Seedance, HeyGen)
- Output: `prompt_package.json` only
- Video generation is a commodity; APIs change frequently
- Exception: MCP integration in Phase 4 if trivial (< 1 day)

## 2. No PromptAtom Composition Engine
- `PromptAtom` is a Pydantic schema, NOT used in retrieval/composition
- Composition is done by `shot_director.py` + `asset_manager.py` (working code)
- Do NOT build a composition engine to replace them
- Only change if PromptAtom gets integrated into retriever AND proves better output

## 3. No Multi-Agent Orchestration
- Pipeline is linear: topic → script → shots → prompt_package → audio
- No agents, no tool use, no orchestration needed
- Adding agents increases complexity, makes debugging harder

## 4. No Content Publishing or Analytics
- Stop at `prompt_package.json`
- Do NOT: publish, schedule posts, collect metrics, build dashboards
- `feedback_ingest.py` accepts engagement data as input, but we don't collect it

## 5. No General-Purpose LLM Wrapping
- LLMs used for exactly one thing: script generation from topic + FP3 context
- Do NOT: chatbots, "ask FlowBeast anything", summarization, translation

## 6. No New Abstractions Without Working Code First
1. Implement as a function
2. Prove it works in the pipeline
3. Only then extract the abstraction
- Premature abstraction is the #1 killer of startup codebases

## 7. No Over-Architecture (#1 risk)
- If a module doesn't produce user-visible output in the current Phase, it shouldn't exist
- Working code > elegant architecture
- Symptoms: designing VTO operators when FP3 has < 10 samples, writing calibrator logic when reference distribution has < 5 samples

## 8. No Phase 0 Optimization (Until 30 Real Samples) — HARD CONSTRAINT
Before 30 real reverse-engineered viral scripts:
- ❌ No corpus system redesign
- ❌ No new metadata systems, databases, ingestion frameworks, taxonomy layers
- ❌ No schema optimization, no automation
- ✅ Focus: acquiring samples, reverse engineering them, building first 30 ViralScript assets

## How to Use
When proposing something new:
1. Is it on this list? → Don't build it.
2. Is it blocked by this document? → Don't build it.
3. When in doubt, the answer is "don't build it."
