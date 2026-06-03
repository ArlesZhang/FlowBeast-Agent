# Decision: What FlowBeast Is

## Positioning

**FlowBeast is a Viral Prompt Compiler.**

Input: a topic. Output: a complete prompt package (`prompt_package.json`) ready for AI video tools (Seedance, Kling, HeyGen).

The moat is not video rendering. The moat is knowing **what prompt structure produces viral content** — learned from decomposing real viral scripts into composable atoms (FP3) and transforming them via VTO operators.

## Core Differentiation

- Not a generic RAG system — FP3 stores structured viral DNA (hook_type, conflict_pattern, emotion_curve), not raw text
- Not a generic script generator — output is a prompt package (shots + style lock + camera + audio), not a screenplay
- Not an agent framework — single pipeline, deterministic flow, no multi-agent orchestration
- Not a video production tool — we output the recipe, not the meal

## What We Are NOT (hard boundaries)

- **Not a video generator.** We don't call Runway/Kling/Seedance APIs. We output prompt_package.json and the human (or future MCP layer) feeds it to those tools.
- **Not a multi-agent system.** The pipeline is linear: topic → script → shots → prompt package → audio. No agent orchestration needed.
- **Not a content publishing platform.** We stop at prompt_package.json. Publishing, scheduling, analytics collection — all out of scope.
- **Not a general-purpose LLM wrapper.** We use LLMs for one thing: generating script JSON from a topic + FP3 context. That's it.
- **Not a PromptAtom composition engine (yet).** PromptAtom is a schema. The actual composition is done by shot_director.py + asset_manager.py. Don't build what already works differently.

## Target User

Solo content creator or small team producing short-form drama (1-5 min episodes) for Douyin/Kuaishou/RedNote. They need:
- Fast iteration: topic → prompt package in < 60 seconds
- Consistent quality: Style Lock prevents AI drift across shots
- Proven structure: FP3 injects viral DNA, not random creativity
