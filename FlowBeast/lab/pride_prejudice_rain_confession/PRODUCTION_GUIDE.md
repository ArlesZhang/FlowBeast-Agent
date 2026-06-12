# Video Production Guide: Darcy's Rain Confession

**Purpose:** Step-by-step instructions for generating video from the completed prompt package  
**Target Platform:** Jimeng AI (即梦) / Seedance / Kling  
**Total Shots:** 48  
**Total Duration:** ~2 minutes

---

## Pre-Production Checklist

Before you start, ensure you have:

- [ ] Access to GPT Image (for character assets)
- [ ] Access to Jimeng AI (即梦) / Seedance / Kling (for scene assets + shot generation)
- [ ] `08_prompts/prompt_package.json` file ready
- [ ] `08_prompts/per_shot_prompts.md` for reference
- [ ] `06_character_constraints/elizabeth_bennet.md` and `mr_darcy.md` for consistency checks
- [ ] `07_generation_rules/style_lock.md` for visual reference
- [ ] `07_generation_rules/scene_lock.md` for scene consistency
- [ ] `07_generation_rules/negative_prompts.md` for quality control

---

## Phase 0: Build and Lock Visual Assets (DO THIS FIRST)

**This phase is mandatory. Do NOT skip to Phase 1 without locked assets.**

Without visual reference assets, text-based consistency rules are insufficient. The two biggest failure points in AI Manju are character inconsistency and scene inconsistency. Both are solved by locking visual assets BEFORE shot generation.

### Step 1: Build Character Assets (GPT Image)

**Tool:** GPT Image (ChatGPT) — best for consistent character faces  
**Reference:** `06_character_constraints/elizabeth_bennet.md`, `mr_darcy.md`  
**Output directory:** `09_assets/characters/`

#### Elizabeth Bennet (9 images)

| Asset | Description | File |
|-------|-------------|------|
| Front view | Face-on portrait, clear features, neutral expression | `elizabeth_bennet/front_view.png` |
| Side view | Profile, showing hair and jawline | `elizabeth_bennet/side_view.png` |
| 3/4 view | Most common shot angle | `elizabeth_bennet/three_quarter.png` |
| Full body | Full costume: blue-gray gown, shawl | `elizabeth_bennet/full_body.png` |
| Beat 1: Surprise | Eyes widening, curious | `elizabeth_bennet/expressions/beat1_surprise.png` |
| Beat 2: Shock | Disbelieving, mouth slightly open | `elizabeth_bennet/expressions/beat2_shock.png` |
| Beat 3: Anger | Jaw tightening, defensive | `elizabeth_bennet/expressions/beat3_anger.png` |
| Beat 4: Fury | Eyes blazing, accusatory | `elizabeth_bennet/expressions/beat4_fury.png` |
| Beat 5: Exhaustion | Eyes down, drained | `elizabeth_bennet/expressions/beat5_exhaustion.png` |

#### Mr. Darcy (10 images)

| Asset | Description | File |
|-------|-------------|------|
| Front view | Strong jawline, intense eyes | `mr_darcy/front_view.png` |
| Side view | Profile view | `mr_darcy/side_view.png` |
| 3/4 view | Most common shot angle | `mr_darcy/three_quarter.png` |
| Full body | Full costume: wet tailcoat, waistcoat, boots | `mr_darcy/full_body.png` |
| Wet coat detail | Close-up of wet coat texture (CRITICAL) | `mr_darcy/wet_coat_detail.png` |
| Beat 1: Intense | Rigid posture, barely contained | `mr_darcy/expressions/beat1_intense.png` |
| Beat 2: Vulnerable | Eyes pleading, desperate | `mr_darcy/expressions/beat2_vulnerable.png` |
| Beat 3: Proud | Chin raised, defensive | `mr_darcy/expressions/beat3_proud.png` |
| Beat 4: Humiliated | Face pale, shocked | `mr_darcy/expressions/beat4_humiliated.png` |
| Beat 5: Devastated | Rigid bow, dignified | `mr_darcy/expressions/beat5_devastated.png` |

#### Character Interactions (2 images)

| Asset | Description | File |
|-------|-------------|------|
| Together neutral | Both in room, maximum distance (Beat 1) | `character_interaction/together_neutral.png` |
| Together conflict | Close confrontation (Beat 4) | `character_interaction/together_conflict.png` |

**How to create character assets:**
1. Open ChatGPT with GPT Image
2. Use character bible descriptions as prompt references
3. Generate multiple options per asset (3-5 variations)
4. Select the one that best matches your vision of the character
5. Ensure ALL selected assets share the same art style (semi-realistic anime)
6. Save to `09_assets/characters/` directories
7. Update checklist in each directory's README.md

### Step 2: Build Scene Assets (Jimeng AI)

**Tool:** Jimeng AI (即梦) — good for cinematic scene generation  
**Reference:** `07_generation_rules/scene_lock.md`, `04_scene_design/scene_breakdown.md`  
**Output directory:** `09_assets/scenes/`

#### Sitting Room (6 images)

| Asset | Description | File |
|-------|-------------|------|
| Wide angle | Full room establishing shot, ALL furniture visible | `sitting_room/wide_angle.png` |
| Window area | Elizabeth's position: chair, desk, rain on glass | `sitting_room/window_area.png` |
| Door area | Darcy's entrance: wooden door, nearby chair | `sitting_room/door_area.png` |
| Fireplace area | Unlit fireplace, mantel, tools | `sitting_room/fireplace_area.png` |
| Lighting | Overcast gray diffused lighting quality | `sitting_room/lighting_reference.png` |
| Rain on window | Close-up rain streaks on glass | `sitting_room/rain_on_window.png` |

#### Weather (4 images)

| Asset | Description | File |
|-------|-------------|------|
| Gentle rain | Beat 1 intensity: steady, gentle drops | `weather/gentle_rain.png` |
| Heavy rain | Beats 2-3 intensity: wind-driven, darker | `weather/heavy_rain.png` |
| Storm rain | Beat 4 intensity: torrential, lightning | `weather/storm_rain.png` |
| Soft rain | Beat 5 intensity: lighter, aftermath | `weather/soft_rain.png` |

**How to create scene assets:**
1. Open Jimeng AI (即梦)
2. Use `scene_lock.md` descriptions as prompt references
3. Generate multiple options per asset
4. Ensure all room assets share the same layout, furniture, and lighting
5. Ensure all weather assets show rain (no sun, no fog, no snow)
6. Save to `09_assets/scenes/` directories
7. Update checklist in each directory's README.md

### Step 3: Lock Assets (Verify & Approve)

Before proceeding to Phase 1, verify:

**Character Lock:**
- [ ] Elizabeth: ALL 9 assets created, same style, same face
- [ ] Darcy: ALL 10 assets created, same style, same face, wet coat visible
- [ ] Interactions: 2 assets, both characters in same style together
- [ ] ALL character assets are in `09_assets/characters/`
- [ ] ALL checklists in README.md files are updated

**Scene Lock:**
- [ ] Room: ALL 6 assets created, same layout, same lighting
- [ ] Weather: ALL 4 assets created, rain intensity progression visible
- [ ] ALL scene assets are in `09_assets/scenes/`
- [ ] ALL checklists in README.md files are updated

**Final Check:**
- [ ] Open ALL assets side-by-side
- [ ] Character faces are consistent across all views
- [ ] Room looks identical in all angles
- [ ] Lighting is consistently overcast/gray
- [ ] Style is consistently semi-realistic anime
- [ ] **You are satisfied with how the characters and room look**

**If any check fails:** Go back and regenerate that asset. Do NOT proceed with substandard assets.

### Why This Phase Matters

```
Without locked assets:
  Prompt says "dark brown wavy hair" → AI generates different hair every time
  Prompt says "small modest room" → AI generates different rooms every time
  Result: Inconsistent, unwatchable

With locked assets:
  Reference image shows Elizabeth's exact face → AI matches it every time
  Reference image shows the exact room → AI matches it every time
  Result: Consistent, professional
```

**Assets are the foundation. Everything else is built on top of them.**

---

## Phase 1: Generate 48 Shots

### Step 1: Import Prompt Package

1. Open Jimeng AI (即梦) / Seedance / Kling
2. Look for "Import" or "Batch Generation" feature
3. Upload `08_prompts/prompt_package.json`
4. Verify all 48 shots are loaded

**If platform doesn't support JSON import:**
- Use `08_prompts/per_shot_prompts.md` to manually create each shot
- Copy/paste the prompt for each shot
- Add negative prompts from `07_generation_rules/negative_prompts.md`

### Step 2: Configure Global Settings

Set these parameters for all shots:

| Parameter | Value |
|-----------|-------|
| Aspect Ratio | 16:9 |
| Resolution | 1080p (or 4K if supported) |
| Frame Rate | 24 fps |
| Style | Semi-realistic anime |
| Duration | Per shot (2-4 seconds each) |

### Step 3: Generate Shots One by One

For each shot (S01 to S48):

1. **Copy the prompt** from `per_shot_prompts.md`
2. **Paste into platform**
3. **Add negative prompts** (copy from `negative_prompts.md`)
4. **Generate the shot**
5. **Review immediately** (see Quality Checklist below)
6. **Regenerate if needed** (don't accept poor quality)

**Pro Tips:**
- Generate in batches of 5-10 shots (easier to manage)
- Start with Beat 1 (S01-S06) as a test batch
- If first batch looks good, continue with confidence
- If first batch has issues, adjust prompts before continuing

### Step 4: Quality Checklist (Per Shot)

After generating each shot, check:

**Character Consistency:**
- [ ] Elizabeth's face matches character bible
- [ ] Darcy's face matches character bible
- [ ] Costumes are correct (blue-gray dress, dark wet coat)
- [ ] Hair is correct (Elizabeth: dark brown wavy; Darcy: dark damp)
- [ ] No face morphing or costume drift

**Scene Consistency:**
- [ ] Room looks the same as previous shot (same layout, furniture, wallpaper)
- [ ] Lighting is overcast/gray (no sunlight, no warm light, no candles)
- [ ] Rain is visible (intensity matches the beat)
- [ ] Props are correct (book on chair, Darcy's gloves in hand)
- [ ] Furniture hasn't changed style or position
- [ ] No modern elements in the room

**Visual Quality:**
- [ ] Composition is cinematic (rule of thirds, leading lines)
- [ ] Style is semi-realistic anime (not cartoon, not photorealistic)
- [ ] No artifacts, blurriness, or low-quality issues

**Emotional Accuracy:**
- [ ] Expression matches the emotion tag in the prompt
- [ ] Body language is appropriate for the beat
- [ ] Eye contact is correct (intense, avoidance, etc.)

**Style Adherence:**
- [ ] Semi-realistic anime style (not cartoon, not photorealistic)
- [ ] Period-accurate (Regency era, early 1810s)
- [ ] No modern elements (phones, modern clothing, etc.)

**If any check fails:**
- Regenerate the shot with stronger negative prompts
- Adjust prompt weights (increase character description, decrease background)
- Use character reference images if platform supports
- Don't accept poor quality — regenerate until it's right

---

## Phase 2: Verify Character & Scene Consistency

### Critical Character Checks

**Elizabeth Bennet:**
- Compare S02 (reading by window) with S48 (collapse into chair)
- Check: Same face? Same hair? Same dress?
- If different, regenerate problematic shots

**Mr. Darcy:**
- Compare S04 (doorway) with S46 (departure)
- Check: Same face? Same coat (wet)? Same hair (damp)?
- If different, regenerate problematic shots

**Costume Consistency:**
- Elizabeth: Blue-gray empire-waist gown throughout
- Darcy: Dark wet tailcoat throughout (never dries)
- If costumes change, regenerate

**Wetness Continuity (CRITICAL):**
- Darcy's coat must stay wet throughout (S04 to S46)
- His hair must stay damp throughout
- If coat dries, regenerate

### Critical Scene Checks

**Room Layout:**
- Compare S01 (wide establishing) with S24 (mid-scene) with S48 (final wide)
- Check: Same room? Same furniture? Same wallpaper? Same size?
- If different, regenerate problematic shots

**Lighting Consistency:**
- Check all shots: Overcast, gray, cool light throughout
- No shot should have warm/sunlight/candle light
- If lighting drifts, regenerate

**Weather Progression:**
- Beat 1 (S01-S06): Gentle rain visible
- Beat 2 (S07-S17): Heavy rain visible
- Beat 3 (S18-S27): Heavy gusting rain visible
- Beat 4 (S28-S39): Storm rain visible, lightning at S28 and S38
- Beat 5 (S40-S48): Softer rain visible
- If rain disappears or intensity doesn't match, regenerate

**Prop Tracking:**
- Elizabeth's book: On chair from S05 onward
- Darcy's gloves: In hand from S07 onward
- Darcy's coat: Wet from S04 to S46
- If props disappear or appear incorrectly, regenerate

### Consistency Troubleshooting

**Problem: Face changes between shots**
- Solution: Use same face reference image for all shots
- Solution: Increase face description weight in prompts
- Solution: Use platform's "face lock" feature if available

**Problem: Costume changes**
- Solution: Include detailed costume description in every prompt
- Solution: Use costume reference image
- Solution: Regenerate with stronger negative prompts ("different outfit")

**Problem: Darcy's coat dries**
- Solution: Add "wet coat, dripping water" to every Darcy prompt
- Solution: Add "dry coat" to negative prompts
- Solution: Regenerate affected shots

**Problem: Style drift**
- Solution: Include style description in every prompt
- Solution: Use style reference image
- Solution: Regenerate with stronger style prompts

---

## Phase 3: Create 30-Second Test Clip

### Purpose
Test the workflow before committing to full 48-shot assembly.

### Shot Selection (10-12 shots)

**Opening Tension (4 shots):**
- S01: Establishing room (3s)
- S04: Darcy in doorway (3s)
- S06: Darcy enters (3s)
- S07: Both characters (3s)

**Confession Vulnerability (3 shots):**
- S10: Darcy's confession (3s)
- S11: Elizabeth's shock (2s)
- S15: Darcy's eyes (2s)

**Explosive Refusal (3 shots):**
- S28: Elizabeth points (3s)
- S32: "You broke her heart!" (3s)
- S38: "Last man in the world" (4s)

**Devastated Departure (2 shots):**
- S44: Darcy bows (3s)
- S48: Elizabeth collapses (3s)

**Total:** 12 shots, ~33 seconds

### Assembly Steps

1. **Sequence shots** in order
2. **Add transitions** (cuts, as specified in shot list)
3. **Add sound design:**
   - Rain (gentle → heavy → storm → softer)
   - Thunder (S09, S18, S28, S38)
   - Dialogue (if voice generation available)
4. **Review the test clip:**
   - Does it tell the story clearly?
   - Are characters consistent?
   - Does the emotional arc work?
   - Is the pacing right?

**If test clip looks good:** Proceed to full assembly  
**If test clip has issues:** Fix problems before full assembly

---

## Phase 4: Assemble Full 2-Minute Video

### Step 1: Sequence All 48 Shots

Follow the shot list in `05_storyboard/shot_list.md`:

- Beat 1: S01-S06 (15 seconds)
- Beat 2: S07-S17 (30 seconds)
- Beat 3: S18-S27 (30 seconds)
- Beat 4: S28-S39 (30 seconds)
- Beat 5: S40-S48 (15 seconds)

**Total:** 120 seconds (2 minutes)

### Step 2: Add Transitions

- **Cut:** Most transitions (as specified in shot list)
- **Dissolve:** Optional for S47→S48 (wide to medium)
- **Fade to black:** S48→End

### Step 3: Add Sound Design

**Rain:**
- Beat 1: Gentle, steady
- Beat 2: Heavy, increasing
- Beat 3: Heavy, gusting
- Beat 4: Storm, intense
- Beat 5: Steady, softer

**Thunder:**
- S09: Distant rumble
- S18: Closer rumble
- S28: Thunder crash
- S38: Thunder crash
- S47: Fading thunder

**Dialogue (if available):**
- Use voice generation for key lines:
  - "In vain have I struggled" (S10)
  - "You are the last man in the world" (S38)
  - "I wish you happiness" (S45)

**Score:**
- Melancholic piano (opening)
- Building tension (middle)
- Emotional peak (refusal)
- Quiet resolution (departure)

### Step 4: Color Grading

**Overall look:**
- Cool, desaturated
- Blue-gray tones
- Cinematic, not cheerful
- Consistent across all shots

**Tools:**
- Use platform's color grading if available
- Or export and grade in DaVinci Resolve / Premiere Pro

### Step 5: Export

**Settings:**
- Resolution: 1080p or 4K
- Frame rate: 24 fps
- Codec: H.264 or H.265
- Format: MP4
- Aspect ratio: 16:9

---

## Phase 5: Publish and Gather Feedback

### Platform Strategy

**Primary platforms:**
- Douyin (抖音) — Chinese short video
- Bilibili (B站) — Chinese anime/entertainment
- Xiaohongshu (小红书) — Chinese lifestyle/culture

**Secondary platforms:**
- YouTube Shorts — International audience
- Instagram Reels — Visual storytelling
- TikTok — Global reach

### Posting Strategy

**Title options:**
- "傲慢与偏见：达西雨中表白 | AI漫剧" (Pride & Prejudice: Darcy's Rain Confession | AI Manju)
- "经典文学 × AI视觉叙事 | 达西的告白" (Classic Literature × AI Visual Storytelling | Darcy's Confession)
- "用AI重现经典：傲慢与偏见雨中表白" (Recreating Classics with AI: Pride & Prejudice Rain Confession)

**Tags:**
- #AI漫剧 #傲慢与偏见 #达西 #经典文学 #视觉叙事 #AI生成

**Description:**
- Brief intro to the scene (Chapter 34)
- Mention it's AI-generated (transparency)
- Ask for feedback (engagement)

### Feedback to Gather

**Quantitative:**
- Views
- Likes
- Shares
- Comments
- Completion rate (how many watch to the end)

**Qualitative:**
- Does it capture the emotional core?
- Is it "not cheesy/melodramatic" (不狗血烂俗)?
- Would viewers watch to the end?
- Would viewers share it?
- What's the most memorable moment?

**Questions to ask in comments:**
- "哪个镜头最打动你？" (Which shot moves you most?)
- "角色一致性如何？有没有出戏的地方？" (How's character consistency? Any moments that break immersion?)
- "你希望看到下一个经典场景是什么？" (What classic scene would you like to see next?)

---

## Phase 6: Document Learnings

### Create Retrospective Document

**File:** `09_retrospective/retrospective.md`

**Sections:**

1. **What worked well:**
   - Which skills were most effective?
   - Which shots required no regeneration?
   - What surprised you (in a good way)?

2. **What could be improved:**
   - Which skills need refinement?
   - Which shots required multiple regenerations? Why?
   - What was the biggest challenge?

3. **Character consistency:**
   - How consistent were Elizabeth and Darcy across shots?
   - What caused inconsistencies?
   - How to prevent in future?

4. **Scene consistency:**
   - How consistent was the room across shots?
   - Did lighting drift? Did weather match beat progression?
   - Did props track correctly?
   - How effective were scene reference assets?

5. **Style lock adherence:**
   - How well did the style lock work?
   - Were there style drifts?
   - How to improve style consistency?

5. **Workflow efficiency:**
   - How long did video generation take?
   - What was the most time-consuming part?
   - How to speed up next time?

6. **Viewer feedback:**
   - What did viewers like most?
   - What did viewers criticize?
   - What surprised you about the feedback?

7. **Recommendations for Case Study #002:**
   - What to do differently?
   - What to keep the same?
   - What new techniques to try?

### Update Templates

Based on learnings:

1. **Identify template improvements**
   - What was missing from the templates?
   - What was unnecessary?
   - What could be clearer?

2. **Update template files**
   - Edit `lab/_templates/*.md`
   - Add new sections if needed
   - Remove outdated sections

3. **Document changes**
   - Commit message: `refactor: improve [template_name] based on Case Study #001`
   - Explain why the improvement matters
   - Show before/after examples

---

## Troubleshooting Common Issues

### Issue: Platform doesn't support JSON import
**Solution:** Use `per_shot_prompts.md` to manually create each shot

### Issue: Character faces change between shots
**Solution:** 
- Use same face reference image for all shots
- Increase face description weight in prompts
- Use platform's "face lock" feature
- Regenerate problematic shots

### Issue: Darcy's coat dries
**Solution:**
- Add "wet coat, dripping water" to every Darcy prompt
- Add "dry coat" to negative prompts
- Regenerate affected shots

### Issue: Style drift (too cartoon or too photorealistic)
**Solution:**
- Include style description in every prompt
- Use style reference image
- Adjust prompt weights
- Regenerate with stronger style prompts

### Issue: Rain not visible
**Solution:**
- Add "rain visible, rain streaks" to prompts
- Increase rain intensity in prompts
- Use rain reference image from `09_assets/scenes/weather/`
- Regenerate affected shots

### Issue: Lighting too bright or too dark
**Solution:**
- Add "overcast, gray, diffused light" to prompts
- Add "sunlight, bright" to negative prompts
- Use lighting reference image from `09_assets/scenes/sitting_room/`
- Regenerate affected shots

### Issue: Room looks different between shots
**Solution:**
- Use wide-angle room reference image in every prompt
- Include detailed room description ("small modest sitting room, faded floral wallpaper, wooden floorboards")
- Increase background consistency weight
- Regenerate affected shots

### Issue: Furniture changes style
**Solution:**
- Include specific furniture descriptions in prompts ("Regency style armchair, dark wood writing desk")
- Use room reference image
- Add "modern furniture" to negative prompts
- Regenerate affected shots

### Issue: Props disappear or appear incorrectly
**Solution:**
- Track prop states per beat (book, gloves, coat wetness)
- Include prop descriptions in relevant shot prompts
- Check prop checklist after each generation

---

## Quick Reference

**Character Assets:** `09_assets/characters/` (GPT Image — build first)  
**Scene Assets:** `09_assets/scenes/` (Jimeng AI — build first)  
**Prompt Package:** `08_prompts/prompt_package.json`  
**Per-Shot Prompts:** `08_prompts/per_shot_prompts.md`  
**Character Bibles:** `06_character_constraints/elizabeth_bennet.md`, `mr_darcy.md`  
**Scene Lock:** `07_generation_rules/scene_lock.md`  
**Style Lock:** `07_generation_rules/style_lock.md`  
**Negative Prompts:** `07_generation_rules/negative_prompts.md`  
**Shot List:** `05_storyboard/shot_list.md`  
**Script:** `03_adaptation/script.md`

---

## Success Metrics

**Video generation succeeds if:**
- [ ] Character assets built and locked (21 images minimum)
- [ ] Scene assets built and locked (10 images minimum)
- [ ] All 48 shots generated
- [ ] Character consistency maintained (Elizabeth & Darcy look the same across all shots)
- [ ] Scene consistency maintained (room, lighting, weather, furniture consistent across all shots)
- [ ] Style lock adhered to (semi-realistic anime, period-accurate)
- [ ] Emotional beats land correctly
- [ ] 2-minute video assembled
- [ ] Video published on at least 2 platforms
- [ ] Viewer feedback gathered (100+ views minimum)
- [ ] Retrospective documented in `09_retrospective/`

---

**Ready to generate. Let's make this real. 🎬**
