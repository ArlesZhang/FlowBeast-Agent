# Reusable Templates for Case Studies

**Status:** Proven in Case Study #001 (Pride & Prejudice — Darcy Rain Confession)  
**Purpose:** Initialize new case study directories with battle-tested templates

---

## Template Files

| Template | Skill | Purpose | Proven In |
|----------|-------|---------|-----------|
| `story_analysis_template.md` | 01-story-analysis | Deconstruct source material | Case Study #001 ✅ |
| `emotion_map_template.md` | 02-emotion-extraction | Map emotional states | Case Study #001 ✅ |
| `storyboard_template.md` | 06-storyboard | Shot-by-shot design | Case Study #001 ✅ |
| `character_bible_template.md` | 07-character-bible | Character consistency | Case Study #001 ✅ |
| `style_lock_template.md` | 08-style-lock | Visual style constraints | Case Study #001 ✅ |
| `prompt_package_template.md` | 09-prompt-package | Final prompt export | Case Study #001 ✅ |

**Note:** Skills 03-05 (adaptation, scene design) use custom outputs based on the specific case, so they don't have separate template files. Their structure is documented in the case study itself.

---

## The 9-Skill Workflow

These templates support a proven 9-skill workflow for transforming classic literature into AI Manju:

### Content Layer (40%)
1. **01-story-analysis** — Deconstruct source material (use `story_analysis_template.md`)
2. **02-emotion-extraction** — Map emotional arcs (use `emotion_map_template.md`)
3. **03-adaptation-strategy** — Define adaptation approach (custom output)
4. **04-script-writing** — Write the script (custom output)

### Director Layer (30%)
5. **05-scene-design** — Design visual scenes (custom output)
6. **06-storyboard** — Create shot list (use `storyboard_template.md`)
7. **07-character-bible** — Define characters (use `character_bible_template.md`)

### Prompt Layer (30%)
8. **08-style-lock** — Lock visual style (use `style_lock_template.md`)
9. **09-prompt-package** — Export prompts (use `prompt_package_template.md`)

**Total time:** ~1-2 weeks per case study (depending on complexity)

---

## Usage

### Starting a New Case Study

```bash
# 1. Create new case study directory
mkdir -p lab/new_case_study/{01_story_analysis,02_emotion_extraction,03_adaptation,04_scene_design,05_storyboard,06_character_constraints,07_generation_rules,08_prompts,09_retrospective}

# 2. Copy templates
cp lab/_templates/story_analysis_template.md lab/new_case_study/01_story_analysis/
cp lab/_templates/emotion_map_template.md lab/new_case_study/02_emotion_extraction/
cp lab/_templates/storyboard_template.md lab/new_case_study/05_storyboard/
cp lab/_templates/character_bible_template.md lab/new_case_study/06_character_constraints/
cp lab/_templates/style_lock_template.md lab/new_case_study/07_generation_rules/
cp lab/_templates/prompt_package_template.md lab/new_case_study/08_prompts/

# 3. Invoke skills sequentially
# Say: "开始故事分析" or "step 1"
# Then: "情绪提炼" or "step 2"
# Continue through all 9 steps
```

### Adapting Templates

These templates are **starting points**, not rigid constraints. Adapt them based on:
- The specific source material (novel, play, film, etc.)
- The target platform (Jimeng AI, Seedance, Kling, etc.)
- The visual style (anime, realistic, painterly, etc.)
- The emotional tone (romantic, tragic, comedic, etc.)

**Example adaptations:**
- For Romeo & Juliet: Add "balcony setting" to scene design template
- For Monte Cristo: Add "revelation moment" to emotion map template
- For contemporary drama: Update costume descriptions in character bible

---

## Philosophy

Every case study is a **knowledge base entry** for FlowBeast. Templates ensure:

1. **Consistency** — Same structure across all case studies
2. **Efficiency** — Don't reinvent the wheel for each case
3. **Comparability** — Easy to compare across case studies
4. **Scalability** — Can produce multiple case studies in parallel
5. **Learning** — Each case study improves the templates

---

## Template Evolution

### Version 1.0 (Case Study #001)
- Initial templates created
- Proven in Pride & Prejudice case study
- 48 shots, 2 minutes, ready for video generation

### Version 1.1 (After Case Study #001 video)
- Updates based on video generation learnings
- Character consistency improvements
- Style lock refinements
- Prompt package optimizations

### Version 2.0 (After Case Study #002)
- Major improvements based on second case study
- Workflow efficiency gains
- Template simplifications
- New best practices documented

---

## Quality Standards

A good template should:
- ✅ Be clear and actionable (no ambiguity)
- ✅ Be comprehensive (cover all necessary aspects)
- ✅ Be flexible (adapt to different cases)
- ✅ Be efficient (don't waste time on unnecessary details)
- ✅ Be proven (tested in real case studies)

A bad template:
- ❌ Is too rigid (can't adapt to different cases)
- ❌ Is too vague (doesn't provide enough guidance)
- ❌ Is too complex (takes longer to use than to do manually)
- ❌ Is untested (never been used in a real case study)

---

## Contributing Improvements

If you improve a template during a case study:

1. Document the improvement in `09_retrospective/`
2. Explain why the improvement matters
3. Update the template in `lab/_templates/`
4. Commit with message: `refactor: improve [template_name] based on Case Study #[N]`

**Example:**
```
refactor: improve character_bible_template based on Case Study #001

- Added "wetness continuity" section (critical for rain scenes)
- Simplified expression range (too detailed before)
- Added reference image suggestions (helps AI generation)
```

---

## Quick Links

- **Case Study #001:** `lab/pride_prejudice_rain_confession/`
- **Prompt Package:** `lab/pride_prejudice_rain_confession/08_prompts/prompt_package.json`
- **Video Generation:** Import into Jimeng AI (即梦) / Seedance / Kling
- **Next Case Study:** Choose Romeo & Juliet / Monte Cristo / Les Misérables

---

**Templates are living documents. Improve them with every case study. 📚**
