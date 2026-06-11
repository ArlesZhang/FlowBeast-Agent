# FlowBeast Content Factory — Case Study #001

**Branch:** `case-pride-prejudice`  
**Single Goal:** 完成《傲慢与偏见》达西雨中表白的 AI 漫剧案例，沉淀为可复用的知识库模板。

---

## Absolute Focus

This workspace exists for **one purpose only**:

> Complete the Pride & Prejudice Darcy Rain Confession AI Manju case study.

**Not a Python project. Not a framework. Not infrastructure.**

If a task doesn't directly advance this case study, **don't do it.**

---

## Goal-Driven Workflow with Skills

This project uses **9 sequential skills** to complete the case study. Each skill corresponds to a phase of work and produces specific deliverables.

### How to Use

Invoke skills by saying:
- "使用 story-analysis skill" or "开始故事分析" or "step 1"
- "使用 emotion-extraction skill" or "情绪提炼" or "step 2"
- Continue through all 9 steps

Or invoke any skill directly by name at any time.

### The 9 Skills

#### Content Layer (内容层)

1. **`story-analysis`** — 剧本理解
   - Output: `01_story_analysis/story_analysis.md`
   - User role: Read source, provide interpretation
   - Claude role: Structure analysis, supplement perspectives

2. **`emotion-extraction`** — 情绪提炼
   - Output: `02_emotion_extraction/emotion_map.md`, `conflict_structure.md`
   - User role: Describe emotional beats
   - Claude role: Generate documents, visualize curves

3. **`adaptation-strategy`** — 编剧改编策略
   - Output: `03_adaptation/adaptation_strategy.md`
   - User role: Make creative decisions (keep/cut/amplify)
   - Claude role: Present options, analyze tradeoffs

4. **`script-writing`** — 写剧本
   - Output: `03_adaptation/script.md`
   - User role: Review and approve
   - Claude role: Write script based on strategy

#### Director Layer (导演层)

5. **`scene-design`** — 场景设计
   - Output: `04_scene_design/scene_breakdown.md`
   - User role: Visualize scenes, make decisions
   - Claude role: Structure scenes, provide references

6. **`storyboard`** — 分镜设计
   - Output: `05_storyboard/shot_list.md`, `camera_directions.md`
   - User role: Make directorial decisions
   - Claude role: Generate shot list, suggest camera work

7. **`character-bible`** — 角色一致性体系
   - Output: `06_character_constraints/*.md` (4 files)
   - User role: Define character vision
   - Claude role: Structure character sheets, provide era references

#### Prompt Layer (提示词层)

8. **`style-lock`** — 风格锁定与约束
   - Output: `07_generation_rules/style_lock.md`, `negative_prompts.md`
   - User role: Define visual style preferences
   - Claude role: Structure constraints, generate negative prompts

9. **`prompt-package`** — 提示词包生成
   - Output: `08_prompts/prompt_package.json`, `per_shot_prompts.md`
   - User role: Review and approve
   - Claude role: Compile all work into final prompt package

### Workflow Sequence

```
story-analysis → emotion-extraction → adaptation-strategy → script-writing
    ↓                                                              ↓
scene-design ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
    ↓
storyboard → character-bible → style-lock → prompt-package
```

Each skill builds on previous outputs. Complete them in order for best results.

---

## Current Phase

**Week 1: Story Analysis**

You are helping the user deconstruct Jane Austen's rain confession scene (Chapter 34) and prepare it for AI visual storytelling.

**Immediate task:** Invoke `story-analysis` skill to create `01_story_analysis/story_analysis.md`

This file must answer:
1. 达西为什么要表白？
2. 伊丽莎白为什么拒绝？
3. 这场戏真正的冲突是什么？
4. 观众为什么会被打动？

---

## The Three Layers

### Content Layer (40%) — 决定观众是否愿意看
- `01_story_analysis/` — 剧本理解
- `02_emotion_extraction/` — 情绪提炼
- `03_adaptation/` — 编剧改编

### Director Layer (30%) — 决定观众是否留下来看完
- `04_scene_design/` — 场景设计
- `05_storyboard/` — 镜头设计
- `06_character_constraints/` — 角色一致性体系

### Prompt Layer (30%) — AI生成约束
- `07_generation_rules/` — AI生成约束体系
- `08_prompts/` — 提示词工程

---

## Rules

### DO
- Focus on content creation: story analysis, emotion mapping, adaptation, shot design
- Use templates from `lab/_templates/` for consistency
- Invoke skills to guide workflow
- Write in English (code comments, commit messages, generated text)
- Ask clarifying questions when the user's intent is unclear
- Help the user think through creative decisions

### DON'T
- Write Python code (this is not a Python project)
- Modify infrastructure (there is no infrastructure)
- Propose building frameworks or abstractions
- Suggest adding dependencies or tools
- Distract from the single goal

---

## Language Policy

**STRICT:** Always respond in English.

This applies to: explanations, code comments, commit messages, debug output, any generated text.

DO NOT use Chinese unless the user explicitly requests it. If the user writes in another language, you STILL respond in English.

---

## Context Priority

When multiple sources conflict, prioritize:

1. **The case study goal** (complete the Darcy rain confession)
2. This CLAUDE.md file
3. `.claude/skills/` skill definitions
4. `lab/pride_prejudice_rain_confession/` contents
5. User's immediate request
6. Templates in `lab/_templates/`

---

## Success Metrics

This branch succeeds when:

- [ ] All 9 skills completed
- [ ] `01_story_analysis/story_analysis.md` is complete and insightful
- [ ] `02_emotion_extraction/emotion_map.md` captures the emotional arc
- [ ] `03_adaptation/adaptation_strategy.md` makes clear creative decisions
- [ ] `03_adaptation/script.md` is approved by user
- [ ] `05_storyboard/shot_list.md` designs every shot
- [ ] `06_character_constraints/` ensures AI consistency
- [ ] `08_prompts/prompt_package.json` exports to AI video tools
- [ ] The case study can be reused as a template for future works

**Nothing else matters.**

---

## Philosophy

> **作品即知识库**

This case study is not just a video — it's a knowledge base entry for FlowBeast.

Every decision, every template, every file is designed to be **reused** for:
- 罗密欧与朱丽叶
- 基督山伯爵
- 悲惨世界
- 原创短剧

**This branch is not about code. It's about content.**

---

## Quick Start

To begin the case study:

1. Say: **"开始故事分析"** or **"使用 story-analysis skill"** or **"step 1"**
2. Claude will guide you through the skill
3. When complete, move to next skill: **"情绪提炼"** or **"step 2"**
4. Continue through all 9 steps
5. Final deliverable: `08_prompts/prompt_package.json`

**You are now ready to create.**
