# Reusable Templates for Case Studies

This directory contains templates for initializing new case study directories.

## Template Files

| Template | Purpose |
|----------|---------|
| `story_analysis_template.md` | Template for deconstructing source material |
| `emotion_map_template.md` | Template for mapping emotional states |
| `storyboard_template.md` | Template for shot-by-shot design |
| `character_bible_template.md` | Template for character consistency |
| `style_lock_template.md` | Template for visual style constraints |
| `prompt_package_template.md` | Template for final prompt export |

## Usage

When starting a new case study:

```bash
# Create new case study directory
mkdir -p lab/new_case_study/{01_story_analysis,02_emotion_extraction,03_adaptation,04_scene_design,05_storyboard,06_character_bible,07_style_lock,08_prompts,09_assets,10_retrospective}

# Copy templates
cp lab/_templates/story_analysis_template.md lab/new_case_study/01_story_analysis/
cp lab/_templates/emotion_map_template.md lab/new_case_study/02_emotion_extraction/
# ... etc
```

## Philosophy

Every case study is a **knowledge base entry** for FlowBeast. Templates ensure consistency and make it easy to:
- Compare across case studies
- Extract patterns
- Build the FlowBeast Knowledge Base
