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
1. **Build character assets** — Generate Elizabeth & Darcy reference images (front, side, 3/4, full body, expressions) using GPT Image / Grok / Jimeng AI
2. **Build scene assets** — Generate sitting room reference images (wide angle, window area, door area, lighting, rain) using AI tools
3. **Lock assets** — Place all approved assets in `09_assets/` with completed checklists
4. **Generate 48 shots** — Import prompt_package.json + reference assets into Jimeng AI / Seedance / Kling
5. **Assemble video** — Edit shots into 2-minute video
6. **Review** — Check visual quality, character consistency, scene consistency, emotional impact

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
- **Call image generation APIs** (no DALL-E, Stable Diffusion, Midjourney API calls)
- **Build automated asset generation pipelines** (assets are created manually by the human creator)
- **Suggest batch automation** before the manual workflow is proven with a published, audience-validated work
- **Skip asset locking** — never suggest going straight to shot generation without locked character and scene assets

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
- [ ] Character assets created (Elizabeth: front, side, 3/4, full body, expressions)
- [ ] Character assets created (Darcy: front, side, 3/4, full body, wet coat, expressions)
- [ ] Scene assets created (sitting room: wide, window, door, fireplace, lighting)
- [ ] Weather assets created (gentle rain, heavy rain, storm, soft rain)
- [ ] Character interaction assets created (together neutral, together conflict)
- [ ] All assets locked in `09_assets/` with completed checklists
- [ ] Scene consistency lock created (`07_generation_rules/scene_lock.md`)
- [ ] Video generated from prompt package (Jimeng/Seedance/Kling)
- [ ] Visual quality meets cinematic standards
- [ ] Character consistency maintained across 48 shots
- [ ] Scene consistency maintained across 48 shots
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

## Production Layers & Time Allocation

The full AI Manju workflow has four layers with clear responsibilities:

### Content Layer (40% of total time) — Claude Code
> Decides whether the audience wants to watch at all

- **剧本理解** (Script understanding) — Claude Code
- **情绪提炼** (Emotion extraction) — Claude Code

### Director Layer (30% of total time) — Claude Code
> Decides whether the audience stays until the end

- **场景设计** (Scene design) — Claude Code
- **镜头设计** (Shot design / storyboard) — Claude Code
- **角色&场景一致性体系** (Character & scene consistency system) — Claude Code
- **提示词工程** (Prompt engineering) — Claude Code
- **AI生成约束体系** (AI generation constraints) — Claude Code

### Asset Layer (20% of total time) — Human + AI Tools
> All shots reference a unified asset system. **The second biggest failure point in AI Manju.**

- **角色资产库** (Character asset library) — GPT Image (human-operated)
- **场景资产库** (Scene asset library) — Claude Code (specs) + Jimeng AI (human-operated generation)

### Generation Layer (10% of total time) — Human + AI Video Tools
> Final shot generation and assembly

- **镜头生成** (Shot generation) — Jimeng AI / Seedance / Kling (human-operated)
- **视频组装** (Video assembly) — Human editing

---

## Core Production Principles (Phase 2+)

### Principle 1: Asset-First, Not Prompt-First

**Before generating ANY shot, lock the visual assets.**

The two biggest failure points in AI visual storytelling:
1. **Character inconsistency** — faces, costumes, expressions drift between shots
2. **Scene inconsistency** — rooms, furniture, lighting, weather drift between shots

Text-based consistency rules (prompts, checklists, negative prompts) are **necessary but insufficient**. You must have **visual reference assets** — fixed images that every shot is measured against.

**The correct production order:**
```
Content Layer (40%): Script understanding → Emotion extraction
    ↓
Director Layer (30%): Scene design → Storyboard → Consistency system → Prompts
    ↓
Asset Layer (20%): Character assets (GPT Image) + Scene assets (Jimeng AI)
    ↓
Generation Layer (10%): Shot generation → Assembly
```

Skipping the Asset Layer and going straight to shot generation is the #1 mistake. Without locked assets, "consistency" is just wishful thinking.

### Principle 2: Manual-First Asset Creation (No API Automation)

**The human creator builds character and scene assets by manually operating AI tools. Do NOT automate this with API calls.**

**Tool responsibilities per asset type:**

| Asset Type | Primary Tool | Claude Code Role | Human Role |
|-----------|-------------|-----------------|------------|
| **Character assets** | GPT Image | None (human does it alone) | Generate, curate, approve |
| **Scene assets** | Jimeng AI (即梦) | Design specs, prompts, checklists | Generate, curate, approve |

**Why manual-first matters:**
1. **Learning the tools** — Operating GPT Image, Jimeng AI, Grok manually builds intuition about what each tool can and cannot do. This knowledge is irreplaceable.
2. **Embedding artistic vision** — Characters carry the creator's interpretation of the story. Darcy's intensity, Elizabeth's wit — these are felt, not specified. Manual creation ensures the creator's vision is embedded in every asset.
3. **Quality judgment** — Only a human can look at a generated image and say "yes, this IS my Darcy" or "no, this doesn't feel right." This judgment cannot be automated.
4. **Automation is premature** — API-based generation workflows should only be considered AFTER:
   - At least one complete case study has been published
   - The video has received meaningful audience validation (100+ views)
   - The workflow has been proven to produce consistent, high-quality results
   - The creator has a clear understanding of what to automate and what to keep manual

**What Claude Code should do for assets:**
- Design asset specifications (what angles, what expressions, what scenes)
- Create scene consistency constraints and templates (`scene_lock.md`)
- Organize and catalog assets (directory structure, naming, checklists)
- Evaluate asset quality (check against character bibles, scene requirements)
- Write Jimeng AI prompts for scene asset generation
- **Never** call image generation APIs on behalf of the user
- **Never** propose building automated asset generation pipelines

**What Claude Code should NOT do:**
- Generate images via API keys (no DALL-E, no Stable Diffusion, no Midjourney API)
- Build automated pipelines that bypass human creative judgment
- Suggest "batch generation" or "automated workflows" for asset creation
- Assume the user wants automation before they have proven the manual workflow

### Principle 3: Two Pillars of Visual Consistency

Both pillars are equally important. Neither can be skipped.

| Pillar | Constraints (Claude Code) | Assets (Human + AI Tools) |
|--------|--------------------------|--------------------------|
| **Character Consistency** | `06_character_constraints/` (bibles, rules, checklists) | `09_assets/characters/` (GPT Image) |
| **Scene Consistency** | `07_generation_rules/scene_lock.md` (lock, rules, checklists) | `09_assets/scenes/` (Jimeng AI) |

**Character consistency** answers: "Do Elizabeth and Darcy look the same in every shot?"
**Scene consistency** answers: "Does the room, lighting, weather, and furniture look the same in every shot?"

Both must be answered YES before shot generation begins.

### Principle 4: Asset Directory Structure

```
09_assets/
├── characters/
│   ├── elizabeth_bennet/
│   │   ├── front_view.png          -- Face-on reference
│   │   ├── side_view.png           -- Profile reference
│   │   ├── three_quarter.png       -- 3/4 angle reference
│   │   ├── full_body.png           -- Full costume reference
│   │   ├── expressions/            -- One per emotional beat
│   │   └── README.md               -- Asset checklist
│   ├── mr_darcy/
│   │   ├── front_view.png
│   │   ├── side_view.png
│   │   ├── three_quarter.png
│   │   ├── full_body.png
│   │   ├── wet_coat_detail.png     -- Wet coat reference (CRITICAL)
│   │   ├── expressions/
│   │   └── README.md
│   └── character_interaction/
│       ├── together_neutral.png    -- Both characters, same style
│       ├── together_conflict.png
│       └── README.md
├── scenes/
│   ├── sitting_room/
│   │   ├── wide_angle.png          -- Full room establishing shot
│   │   ├── window_area.png         -- Elizabeth's starting position
│   │   ├── door_area.png           -- Darcy's entrance
│   │   ├── fireplace_area.png      -- Background detail
│   │   ├── lighting_reference.png  -- Overcast gray lighting
│   │   ├── rain_on_window.png      -- Rain streaks on glass
│   │   └── README.md               -- Scene asset checklist
│   └── weather/
│       ├── gentle_rain.png         -- Beat 1 rain intensity
│       ├── heavy_rain.png          -- Beat 2-3 rain intensity
│       ├── storm_rain.png          -- Beat 4 rain intensity
│       └── soft_rain.png           -- Beat 5 rain intensity
└── README.md                       -- Asset collection status
```

---

## Quick Start

### For Video Generation (Current Priority):
1. **Build character assets** — Use GPT Image / Grok / Jimeng AI to generate Elizabeth & Darcy reference images (see `09_assets/characters/` for checklist)
2. **Build scene assets** — Generate sitting room & weather reference images (see `09_assets/scenes/` for checklist)
3. **Lock assets** — Verify all assets match character bibles and scene lock, place in `09_assets/`
4. **Open prompt package** — `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`
5. **Generate shots** — Import into Jimeng AI / Seedance / Kling with reference assets
6. **Assemble & review** — Edit into 2-minute video, check consistency

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
