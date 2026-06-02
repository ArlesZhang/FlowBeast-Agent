# Decision: What FlowBeast Does NOT Do

This document exists to prevent scope creep and architectural drift. Every time Claude (or a human) is tempted to build something new, check this list first.

## Hard Boundaries

### 1. No Video Generation Code

We do NOT call video APIs (Runway, Kling, Seedance, HeyGen). We output `prompt_package.json` — a structured recipe that a human (or future MCP layer) feeds to those tools.

**Why:** Video generation is a commodity. The APIs change every 6 months. Our moat is the prompt structure, not the rendering pipeline. Building video generation code is a distraction from the core product.

**Exception:** If MCP integration becomes trivial (< 1 day of work) and a specific tool's API is stable, we might add it in Phase 4. Not before.

---

### 2. No PromptAtom Composition Engine

`PromptAtom` is a Pydantic schema in `fp3/prompt_atom.py`. It is NOT used in retrieval, composition, or the generation pipeline.

The actual composition is done by:
- `shot_director.py` — beat_type-driven shot list (504 lines, working)
- `asset_manager.py` — character/scene/style lock injection (402 lines, working)

**Why building a composition engine would be wrong:**
- shot_director + asset_manager already solve the problem differently
- PromptAtom has no integration with FAISS search (retriever.py searches ViralUnit/ViralScript, not PromptAtom)
- Building composition would mean rewriting working code to fit an unproven abstraction

**When this might change:** If PromptAtom gets integrated into the retriever and pipeline, and proves it produces better output than the current system. Not before.

---

### 3. No Multi-Agent Orchestration

The pipeline is linear:
```
topic → script → shots → prompt_package → audio
```

There is no need for agents, tool use, or orchestration. Adding agents would:
- Increase complexity without improving output quality
- Make debugging harder
- Violate the "simple working solutions" principle

**Exception:** If we add MCP integration in Phase 4, it might use agent-like patterns for tool calling. But that's infrastructure, not core product.

---

### 4. No Content Publishing or Analytics

We stop at `prompt_package.json`. We do NOT:
- Publish to Douyin/Kuaishou/RedNote
- Schedule posts
- Collect engagement metrics (views/likes/shares)
- Build dashboards

**Why:** Publishing and analytics are solved problems (use platform APIs or third-party tools). Our product is the prompt compiler, not the distribution layer.

**Exception:** `feedback_ingest.py` accepts engagement data as input (for Phase 3 flywheel), but we don't collect it ourselves.

---

### 5. No General-Purpose LLM Wrapping

We use LLMs for exactly one thing: generating script JSON from a topic + FP3 context.

We do NOT:
- Build chatbots
- Offer "ask FlowBeast anything" interfaces
- Use LLMs for summarization, translation, or other generic tasks

**Why:** Every LLM call costs money and adds latency. We optimize for the one task that matters: script generation.

---

### 6. No New Abstractions Without Working Code First

Before building any new abstraction (PromptAtom composition, VTO operator base class, agent framework):
1. Implement the specific case as a function
2. Prove it works in the pipeline
3. Only then extract the abstraction

**Why:** Premature abstraction is the #1 killer of startup codebases. We prefer 10 working functions over 1 elegant framework.

---

### 7. No Over-Architecture

**This is the #1 risk in the project.** We have layers (FP3, IP2, IP1, OBS) that look impressive on paper but produce zero user-visible output without data.

**Symptoms of over-architecture:**
- Designing VTO operators when FP3 has < 10 samples
- Building PromptAtom composition when shot_director already works
- Writing calibrator logic when reference distribution has < 5 samples
- Creating schemas for systems that don't exist yet

**The rule:** If a module doesn't produce user-visible output in the current Phase, it shouldn't exist. Working code > elegant architecture.

**The only architecture that matters:** Can a user type a topic and get a prompt package? Everything else is decoration.

## 8. No Phase 0 Optimization (Until 30 Real Samples)

**This is a hard constraint, not a guideline.**

Before reaching 30 real reverse-engineered viral scripts:

- ❌ Do NOT redesign the corpus system
- ❌ Do NOT introduce new metadata systems
- ❌ Do NOT introduce new databases
- ❌ Do NOT introduce new ingestion frameworks
- ❌ Do NOT introduce new taxonomy layers
- ❌ Do NOT optimize the schema
- ❌ Do NOT build automation

**Focus exclusively on:**
1. ✅ Acquiring samples (watch, judge, curate)
2. ✅ Reverse engineering samples (run CLI, verify output)
3. ✅ Building the first 30 ViralScript assets

**Why this exists:** Building better infrastructure when you have 2 samples is the same as building a factory when you have 2 customers. The most dangerous form of over-architecture is optimizing a system that has no data yet.

**Lifting the constraint:** After 30 real samples are collected and validated, you may optimize the corpus system. Not before.

---

## How to Use This Document

When Claude proposes building something new, ask:
1. Is it on the "Not Built" list in `status/current_status.md`?
2. Is it blocked by this document's hard boundaries?
3. If yes to either, don't build it.

When in doubt, the answer is "don't build it."
