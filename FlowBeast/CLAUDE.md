# FlowBeast Content Factory

**Branch:** `case-pride-prejudice`  
**Current Milestone:** Case Study #001 Complete (v0.1.0-case-study-001)  
**Next Phase:** Video Generation & Case Study #002 Preparation

---

## Status: Case Study #001 Complete ✅

The Pride & Prejudice Darcy Rain Confession case study has been successfully completed with all 9 skills executed:

- ✅ Story analysis (Chapter 34 deep dive)
- ✅ Emotion extraction (character emotional arcs)
- ✅ Adaptation strategy (literary to visual)
- ✅ Script writing (2-minute dramatic script)
- ✅ Scene design (5-scene breakdown)
- ✅ Storyboard (48 shots with camera directions)
- ✅ Character bibles (Elizabeth & Darcy)
- ✅ Style lock & negative prompts
- ✅ Prompt package (JSON ready for AI tools)

**Deliverable:** `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`

---

## Current Focus

This workspace has transitioned from **content creation** to **content production**:

> Generate video from the completed prompt package, then apply the reusable template to Case Study #002.

**Two parallel tracks:**
1. **Video Generation:** Import `prompt_package.json` into Jimeng AI (即梦) / Seedance / Kling
2. **Template Refinement:** Review Case Study #001, improve templates based on learnings

---

## Reusable Skills Framework (9 Skills)

The 9 skills used to complete Case Study #001 are now **proven templates** for future case studies:

#### Content Layer (内容层)

1. **`01-story-analysis`** — 剧本理解
2. **`02-emotion-extraction`** — 情绪提炼
3. **`03-adaptation-strategy`** — 编剧改编策略
4. **`04-script-writing`** — 写剧本

#### Director Layer (导演层)

5. **`05-scene-design`** — 场景设计
6. **`06-storyboard`** — 分镜设计
7. **`07-character-bible`** — 角色一致性体系

#### Prompt Layer (提示词层)

8. **`08-style-lock`** — 风格锁定与约束
9. **`09-prompt-package`** — 提示词包生成

**For Case Study #002:** Invoke skills by saying "开始故事分析" or "step 1", then proceed through all 9 steps.

---

## Current Phase

**Phase 2: Video Generation & Template Refinement**

### Track 1: Video Generation (User Action)
1. Import `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json` into Jimeng AI (即梦) / Seedance / Kling
2. Generate 48 shots using the prompts
3. Assemble shots into 2-minute video
4. Review visual quality, character consistency, emotional impact

### Track 2: Template Refinement (Claude + User Collaboration)
1. Review Case Study #001 outputs (all 8 directories)
2. Identify what worked well and what could be improved
3. Update templates in `lab/_templates/` based on learnings
4. Document lessons learned in `lab/pride_prejudice_rain_confession/09_retrospective/`

### Track 3: Case Study #002 Preparation (Future)
1. Select next classic scene (e.g., Romeo & Juliet balcony, Monte Cristo revelation)
2. Apply refined templates to new case study
3. Execute 9-skill workflow with improved efficiency

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

### Phase 1 Complete ✅ (v0.1.0-case-study-001)
- [x] All 9 skills completed
- [x] Story analysis captures emotional core of Chapter 34
- [x] Emotion maps track both characters' arcs
- [x] Adaptation strategy makes clear creative decisions
- [x] Script approved (2 minutes, 48 shots)
- [x] Storyboard designs every shot with camera directions
- [x] Character bibles ensure AI consistency
- [x] Prompt package exports to AI video tools
- [x] Templates created for reuse

### Phase 2: In Progress
- [ ] Video generated from prompt package (Jimeng/Seedance/Kling)
- [ ] Visual quality meets cinematic standards
- [ ] Character consistency maintained across 48 shots
- [ ] Emotional impact preserved from script to screen
- [ ] Templates refined based on Case Study #001 learnings
- [ ] Retrospective documented in `09_retrospective/`

### Phase 3: Future
- [ ] Case Study #002 selected and planned
- [ ] Refined templates applied to new case study
- [ ] Workflow efficiency improved (faster execution)
- [ ] Second prompt package ready for generation

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

### For Video Generation (Current Priority):
1. Open `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`
2. Import into Jimeng AI (即梦) / Seedance / Kling
3. Generate shots one by one using the prompts
4. Assemble into 2-minute video
5. Review and iterate

### For Case Study #002 (Future):
1. Say: **"开始故事分析"** or **"使用 01-story-analysis skill"** or **"step 1"**
2. Claude will guide you through the skill
3. When complete, move to next skill: **"情绪提炼"** or **"step 2"**
4. Continue through all 9 steps
5. Final deliverable: `08_prompts/prompt_package.json`

### For Template Refinement:
1. Review outputs in `lab/pride_prejudice_rain_confession/`
2. Discuss what worked and what could improve
3. Update templates in `lab/_templates/`
4. Document learnings in `09_retrospective/`

**Case Study #001 is complete. Ready for production.**
