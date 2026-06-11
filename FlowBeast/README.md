# FlowBeast Content Factory

**Branch:** `case-pride-prejudice`  
**Single Goal:** Complete the Pride & Prejudice Darcy Rain Confession AI Manju case study, and make it a reusable knowledge base template.

---

## What This Is

This is a **content creation workspace** for producing AI Manju (漫剧) — AI-generated visual storytelling.

**Not a Python project.** Not a framework. Not infrastructure.

Just a focused workspace for one case study that will become the template for all future case studies.

---

## The Mission

### Case Study #001: Pride & Prejudice — Darcy Rain Confession

Transform Jane Austen's iconic rain confession scene (Chapter 34) into a complete AI Manju prompt package.

**Deliverable:** A `prompt_package.json` ready for AI video tools (Seedance, Kling, HeyGen) that produces a 2-minute visual story.

**Success Criteria:**
- [ ] Story analysis captures the emotional core
- [ ] Adaptation preserves Austen's wit while making it visual
- [ ] Character consistency maintained across all shots
- [ ] Style lock prevents visual drift
- [ ] Prompt package exports correctly to target platforms

---

## The Three Layers

### Content Layer (40% of effort)
**决定观众是否愿意看**

- **剧本理解** — Deconstruct the source material
- **情绪提炼** — Map emotional states and conflict structure  
- **编剧改编** — Transform prose into visual script

**Directories:** `01_story_analysis/`, `02_emotion_extraction/`, `03_adaptation/`

### Director Layer (30% of effort)
**决定观众是否留下来看完**

- **场景设计** — Break script into visual scenes
- **镜头设计** — Design every shot: framing, motion, camera
- **角色一致性** — Character bible for AI consistency

**Directories:** `04_scene_design/`, `05_storyboard/`, `06_character_constraints/`

### Prompt Layer (30% of effort)
**AI生成约束与提示词工程**

- **提示词工程** — Compile everything into AI-ready prompts
- **AI生成约束** — Visual style, negative prompts, platform specs

**Directories:** `07_generation_rules/`, `08_prompts/`

---

## Directory Structure

```
lab/
├── _templates/                              # Reusable templates for future cases
│   ├── story_analysis_template.md
│   ├── emotion_map_template.md
│   ├── storyboard_template.md
│   ├── character_bible_template.md
│   ├── style_lock_template.md
│   └── prompt_package_template.md
│
└── pride_prejudice_rain_confession/         # Case Study #001
    ├── 01_story_analysis/                   # Content Layer
    ├── 02_emotion_extraction/               # Content Layer
    ├── 03_adaptation/                       # Content Layer
    ├── 04_scene_design/                     # Director Layer
    ├── 05_storyboard/                       # Director Layer
    ├── 06_character_constraints/            # Director Layer
    ├── 07_generation_rules/                 # Prompt Layer
    └── 08_prompts/                          # Prompt Layer
```

---

## How to Use This Workspace

### For Content Creators

1. Start with `01_story_analysis/story_analysis.md`
2. Work through each directory in order
3. Use templates from `lab/_templates/` for consistency
4. When complete, export `08_prompts/prompt_package.json`

### For Future Case Studies

This case study becomes the template. Future cases:
- 罗密欧与朱丽叶 (Romeo and Juliet)
- 基督山伯爵 (The Count of Monte Cristo)
- 悲惨世界 (Les Misérables)
- 原创短剧 (Original short dramas)

Each will follow the same 8-directory structure.

---

## Philosophy

> **作品即知识库**

Every case study is a knowledge base entry for FlowBeast. The goal is not just to make one video — it's to build a reusable methodology for AI visual storytelling.

**This branch is not about code. It's about content.**

---

## Status

**Current Phase:** Week 1 — Story Analysis

**Next Task:** Write `01_story_analysis/story_analysis.md` answering:
1. Why does Darcy confess?
2. Why does Elizabeth refuse?
3. What is the real conflict?
4. Why is the audience moved?
