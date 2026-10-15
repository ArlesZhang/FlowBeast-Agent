# Decision: What FlowBeast Is

## ⚠️ Update 2026-10-15 — Commercial positioning has changed

> 市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。
>
> *Four early-stage playbooks — a static-corpus moat, cheap extraction services, a distinctive
> brand name, and prompt packs — have been empirically falsified by the market. Light-asset models
> no longer work in the AI 2.0 era; the way forward is deeper system-level workflow integration and
> delivery of business outcomes.*

**FlowBeast is not sold as a compiler, and not sold as prompt packs.** The productized form is
**done-with-you AI short-drama production for small Chinese teams, priced per finished episode** —
a service, not a SaaS. The free public scorer is the top of funnel, not the product.

**The one acceptance test for everything below: 有真实付费证据 (there is real payment evidence).**
No positioning claim counts until a customer has paid for a delivered episode.

**Why the sections below still stand:** they describe what the *code* is and is not. They are
architectural boundaries and remain correct. What changed is who pays and for what.

Full reasoning, evidence, and the 30-day plan: [commercialization_playbook.md](../commercialization_playbook.md).

---

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
