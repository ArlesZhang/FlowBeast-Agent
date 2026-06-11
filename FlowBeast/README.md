# FlowBeast Content Factory

**Branch:** `case-pride-prejudice`  
**Current Milestone:** Case Study #001 Complete (v0.1.0-case-study-001)  
**Status:** Ready for Video Generation

---

## What This Is

This is a **content production workspace** for AI Manju (漫剧) — AI-generated visual storytelling.

**Not a Python project.** Not a framework. Not infrastructure.

A focused workspace that transforms classic literature into AI-ready visual narratives through a proven 9-skill workflow.

---

## Case Study #001: Complete ✅

### Pride & Prejudice — Darcy Rain Confession

Jane Austen's iconic rain confession scene (Chapter 34) has been successfully transformed into a complete AI Manju prompt package.

**Deliverables:**
- ✅ 48-shot storyboard with camera directions
- ✅ 2-minute dramatic script
- ✅ Character bibles for Elizabeth & Darcy
- ✅ Style lock & negative prompts
- ✅ `prompt_package.json` ready for AI video tools

**Target Platforms:** Jimeng AI (即梦), Seedance, Kling, HeyGen

**Tag:** `v0.1.0-case-study-001`

---

## The Three Layers

### Content Layer (40% of effort) — 决定观众是否愿意看

- **剧本理解** — Deconstruct the source material
- **情绪提炼** — Map emotional states and conflict structure  
- **编剧改编** — Transform prose into visual script

**Directories:** `01_story_analysis/`, `02_emotion_extraction/`, `03_adaptation/`

**Status:** ✅ Complete

### Director Layer (30% of effort) — 决定观众是否留下来看完

- **场景设计** — Break script into visual scenes
- **镜头设计** — Design every shot: framing, motion, camera
- **角色一致性** — Character bible for AI consistency

**Directories:** `04_scene_design/`, `05_storyboard/`, `06_character_constraints/`

**Status:** ✅ Complete

### Prompt Layer (30% of effort) — AI生成约束与提示词工程

- **提示词工程** — Compile everything into AI-ready prompts
- **AI生成约束** — Visual style, negative prompts, platform specs

**Directories:** `07_generation_rules/`, `08_prompts/`

**Status:** ✅ Complete

---

## Directory Structure

```
lab/
├── _templates/                              # Reusable templates for future cases
│   ├── 01-story-analysis.md
│   ├── 02-emotion-extraction.md
│   ├── 03-adaptation-strategy.md
│   ├── 04-script-writing.md
│   ├── 05-scene-design.md
│   ├── 06-storyboard.md
│   ├── 07-character-bible.md
│   ├── 08-style-lock.md
│   └── 09-prompt-package.md
│
└── pride_prejudice_rain_confession/         # Case Study #001 (Complete)
    ├── 01_story_analysis/                   # ✅ Story analysis complete
    ├── 02_emotion_extraction/               # ✅ Emotional arcs mapped
    ├── 03_adaptation/                       # ✅ Script & strategy complete
    ├── 04_scene_design/                     # ✅ 5 scenes designed
    ├── 05_storyboard/                       # ✅ 48 shots designed
    ├── 06_character_constraints/            # ✅ Character bibles complete
    ├── 07_generation_rules/                 # ✅ Style lock & negatives ready
    ├── 08_prompts/                          # ✅ Prompt package exported
    └── 09_retrospective/                    # ⏳ Pending (post-generation)
```

---

## Current Phase: Video Generation

### Next Steps

1. **Import prompt package** into Jimeng AI (即梦) / Seedance / Kling
   - File: `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`
   
2. **Generate 48 shots** using the prompts
   - Review character consistency across shots
   - Check visual style matches style lock
   - Verify emotional beats land correctly

3. **Assemble into 2-minute video**
   - Sequence shots according to storyboard
   - Add transitions and sound design
   - Final color grading

4. **Review and iterate**
   - Does it capture the emotional core?
   - Is character consistency maintained?
   - Does it work as AI Manju (not cheesy/melodramatic)?

5. **Document learnings** in `09_retrospective/`
   - What worked well?
   - What could be improved?
   - How to apply to Case Study #002?

---

## Reusable Skills Framework

The 9 skills used to complete Case Study #001 are now **proven templates** for future case studies:

| Skill | Phase | Output |
|-------|-------|--------|
| `01-story-analysis` | Content | Story analysis document |
| `02-emotion-extraction` | Content | Emotional arc maps |
| `03-adaptation-strategy` | Content | Adaptation decisions |
| `04-script-writing` | Content | 2-minute script |
| `05-scene-design` | Director | Scene breakdown |
| `06-storyboard` | Director | Shot list & camera directions |
| `07-character-bible` | Director | Character sheets |
| `08-style-lock` | Prompt | Visual style & negatives |
| `09-prompt-package` | Prompt | AI-ready prompt package |

**For Case Study #002:** Invoke skills sequentially using the same workflow.

---

## Future Case Studies

This case study becomes the template. Future cases:
- 罗密欧与朱丽叶 (Romeo and Juliet) — Balcony scene
- 基督山伯爵 (The Count of Monte Cristo) — Revelation scene
- 悲惨世界 (Les Misérables) — Jean Valjean's redemption
- 原创短剧 (Original short dramas) — Contemporary stories

Each will follow the same 9-skill workflow, building on refined templates.

---

## Philosophy

> **作品即知识库**

Every case study is a knowledge base entry for FlowBeast. The goal is not just to make one video — it's to build a reusable methodology for AI visual storytelling.

**This branch is not about code. It's about content.**

---

## Technical Details

**Branch:** `case-pride-prejudice`  
**Base Commit:** `0ab8a37` (same as `develop` and `main`)  
**Current Commit:** `7e54ced`  
**Current Tag:** `v0.1.0-case-study-001`

**Archived Infrastructure:** All Python code, tests, and infrastructure remain in `main` and `develop` branches for future use.

**Git Strategy:** This branch focuses on content creation. When ready to merge back to `main`, only merge the `lab/` directory and updated documentation.

---

## Quick Links

- **Prompt Package:** `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`
- **Script:** `lab/pride_prejudice_rain_confession/03_adaptation/script.md`
- **Storyboard:** `lab/pride_prejudice_rain_confession/05_storyboard/shot_list.md`
- **Character Bibles:** `lab/pride_prejudice_rain_confession/06_character_constraints/`
- **Templates:** `lab/_templates/`

---

**Case Study #001 is complete. Ready for production. 🎬**
