# Visual Assets: Darcy's Rain Confession

**Status:** Collecting assets before shot generation  
**Priority:** HIGHEST — No shot generation until assets are locked  
**Creator:** Human (manual creation using GPT Image, Grok, Jimeng AI)

---

## Purpose

This directory holds **locked visual reference assets** for character and scene consistency.

Every shot generated in Phase 2 must reference these assets. Without them, text-based consistency rules are insufficient.

**The rule is simple: No locked assets = No shot generation.**

---

## Asset Directories

### `characters/` — Character Reference Images

Visual references that define how Elizabeth and Darcy look throughout all 48 shots.

| Directory | Contents | Required Assets |
|-----------|----------|----------------|
| `elizabeth_bennet/` | Elizabeth reference images | Front, side, 3/4, full body, 5 expressions |
| `mr_darcy/` | Darcy reference images | Front, side, 3/4, full body, wet coat, 5 expressions |
| `character_interaction/` | Both characters together | Neutral, conflict |

**Total character assets required: ~16 images**

### `scenes/` — Scene Reference Images

Visual references that define how the sitting room and weather look throughout all 48 shots.

| Directory | Contents | Required Assets |
|-----------|----------|----------------|
| `sitting_room/` | Room reference images | Wide, window, door, fireplace, lighting, rain-on-window |
| `weather/` | Weather intensity references | Gentle, heavy, storm, soft |

**Total scene assets required: ~11 images**

---

## Asset Creation Process

### Who Creates Assets
**The human creator** — using AI image tools manually. NOT automated via API.

### Which Tools to Use
- **GPT Image (ChatGPT)** — Best for character portraits with consistent faces
- **Grok** — Good for alternative styles and expressions
- **Jimeng AI (即梦)** — Good for cinematic quality and Chinese-market aesthetic
- **Any other tool** that produces the right result

### How to Create Assets
1. Use character bible files (`06_character_constraints/`) as prompt references
2. Use scene lock file (`07_generation_rules/scene_lock.md`) as scene references
3. Generate multiple options per asset
4. Select the one that best matches your vision
5. Save to the appropriate directory
6. Update the checklist in each subdirectory's README.md

### Quality Standards
Each asset must:
- Match the character bible / scene lock description
- Be in the correct visual style (semi-realistic anime)
- Be high resolution (1080p minimum)
- Be 16:9 aspect ratio (or square for face close-ups)
- Feel right to YOU (the creator's judgment is final)

---

## Asset Lock Checklist

### Characters (Complete ALL before shot generation)
- [ ] Elizabeth: Front view approved
- [ ] Elizabeth: Side view approved
- [ ] Elizabeth: 3/4 view approved
- [ ] Elizabeth: Full body approved
- [ ] Elizabeth: Beat 1 expression (Surprise)
- [ ] Elizabeth: Beat 2 expression (Shock)
- [ ] Elizabeth: Beat 3 expression (Anger)
- [ ] Elizabeth: Beat 4 expression (Fury)
- [ ] Elizabeth: Beat 5 expression (Exhaustion)
- [ ] Darcy: Front view approved
- [ ] Darcy: Side view approved
- [ ] Darcy: 3/4 view approved
- [ ] Darcy: Full body approved
- [ ] Darcy: Wet coat detail approved
- [ ] Darcy: Beat 1 expression (Intense)
- [ ] Darcy: Beat 2 expression (Vulnerable)
- [ ] Darcy: Beat 3 expression (Proud)
- [ ] Darcy: Beat 4 expression (Humiliated)
- [ ] Darcy: Beat 5 expression (Devastated)
- [ ] Interaction: Together neutral
- [ ] Interaction: Together conflict

### Scenes (Complete ALL before shot generation)
- [ ] Room: Wide angle establishing shot
- [ ] Room: Window area
- [ ] Room: Door area
- [ ] Room: Fireplace area
- [ ] Room: Lighting reference (overcast)
- [ ] Room: Rain on window
- [ ] Weather: Gentle rain (Beat 1)
- [ ] Weather: Heavy rain (Beats 2-3)
- [ ] Weather: Storm rain (Beat 4)
- [ ] Weather: Soft rain (Beat 5)

### Final Lock
- [ ] ALL character assets complete and approved
- [ ] ALL scene assets complete and approved
- [ ] Assets placed in correct directories
- [ ] README checklists updated in each subdirectory
- [ ] **Ready for shot generation**

---

## Philosophy

> Assets are created by the human, not by the machine.

The process of manually creating these assets IS the creative process. It's how you:
- Learn the tools
- Embed your vision into the characters
- Develop intuition about what works
- Build judgment about quality

**Do NOT automate this. Do NOT rush this. This is the foundation.**
