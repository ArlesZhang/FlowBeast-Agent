# Decision: What FlowBeast Does NOT Do

This document exists to prevent scope creep and architectural drift. Every time Claude (or a human) is tempted to build something new, check this list first.

## Hard Boundaries

### 1. No Video Generation Code

We do NOT build our own video generation models, and we do NOT hand-roll API clients for Runway, Kling, Seedance or HeyGen. We orchestrate the ones that already exist, and we hand over `prompt_package.json` — a structured recipe a human or an existing tool feeds in.

**Why:** Video generation is a commodity. The APIs change every 6 months and someone else maintains them. Our scarce resource is integration + orchestration + commercial delivery, not rendering. Writing a client for an API that has an official SDK is Rule 0 violation.

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

### 4. No Content Publishing Platform

We deliver finished episodes to the customer. We do NOT build:
- A publisher to Douyin/Kuaishou/RedNote
- Post scheduling
- A metrics dashboard

**Why:** Publishing and analytics are solved problems. If a customer needs publishing, we use the platform's own tooling or an existing third-party tool.

**Not a boundary:** collecting the customer's engagement numbers *by hand* and feeding them to `feedback_ingest.py` is part of delivery, and it is how we learn whether the output works.

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

Before building any new abstraction (PromptAtom composition, operator base classes, agent framework):
1. Implement the specific case as a function
2. Prove it works in the pipeline
3. Only then extract the abstraction

**Why:** Premature abstraction is the #1 killer of startup codebases. We prefer 10 working functions over 1 elegant framework.

---

### 7. No Over-Architecture

**This is the #1 risk in the project.** We have layers (FP3, IP2, IP1, OBS) that look impressive on paper but produce zero user-visible output without data.

**Symptoms of over-architecture:**
- Building operators/abstractions when FP3 has < 10 real samples
- Building PromptAtom composition when shot_director already works
- Writing calibration logic when there is no ground truth to calibrate against
- Creating schemas for systems that don't exist yet
- Writing our own version of something an existing library already does (see Rule 0 in CLAUDE.md)

**The rule:** If a module doesn't produce user-visible output in the current Phase, it shouldn't exist. Working code > elegant architecture.

**The only architecture that matters:** Can a customer hand us a topic and receive a finished episode? Everything else is decoration.

## 8. No Infrastructure Work Before Payment Evidence

**This is a hard constraint, not a guideline.**

Before the first real payment:

- ❌ Do NOT redesign the corpus or memory system
- ❌ Do NOT introduce new metadata systems, databases or ingestion frameworks
- ❌ Do NOT introduce new taxonomy layers or optimize the schema
- ❌ Do NOT build automation for a workflow nobody has run twice
- ❌ Do NOT add a scoring/quality layer that has no ground truth to fit to

**Focus exclusively on:**
1. ✅ Making the delivery path work end to end on a real topic, by hand if necessary
2. ✅ Finding one customer and delivering one finished episode
3. ✅ Getting paid

**Why this exists:** Building better infrastructure before you have a customer is the same as
building a factory before you have a product. Every hour spent on the memory system is an hour not
spent finding out whether anyone will pay.

**Lifting the constraint:** After the first real payment, the constraint is replaced by whatever the
paying customer's actual complaints are. Not before.

---

## How to Use This Document

When Claude proposes building something new, ask:
1. Does an existing library, CLI, Skill or MCP already do this? (Rule 0 in CLAUDE.md) If yes, integrate it.
2. Is it blocked by this document's hard boundaries?
3. Does it move us toward a finished episode for a paying customer? If not, don't build it.

When in doubt, the answer is "don't build it."
