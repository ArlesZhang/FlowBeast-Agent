# Video Production Guide: Darcy's Rain Confession

**Purpose:** Step-by-step instructions for generating video from the completed prompt package  
**Target Platform:** Jimeng AI (即梦) / Seedance / Kling  
**Total Shots:** 48  
**Total Duration:** ~2 minutes

---

## Pre-Production Checklist

Before you start, ensure you have:

- [ ] Access to Jimeng AI (即梦) / Seedance / Kling
- [ ] `08_prompts/prompt_package.json` file ready
- [ ] `08_prompts/per_shot_prompts.md` for reference
- [ ] `06_character_constraints/elizabeth_bennet.md` and `mr_darcy.md` for consistency checks
- [ ] `07_generation_rules/style_lock.md` for visual reference
- [ ] `07_generation_rules/negative_prompts.md` for quality control

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

**Visual Quality:**
- [ ] Lighting is overcast/gray (no sunlight)
- [ ] Rain is visible (intensity matches the beat)
- [ ] Composition is cinematic (rule of thirds, leading lines)
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

## Phase 2: Verify Character Consistency

### Critical Consistency Checks

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

4. **Style lock adherence:**
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
- Use rain reference image
- Regenerate affected shots

### Issue: Lighting too bright or too dark
**Solution:**
- Add "overcast, gray, diffused light" to prompts
- Add "sunlight, bright" to negative prompts
- Adjust lighting in post-production
- Regenerate affected shots

---

## Quick Reference

**Prompt Package:** `08_prompts/prompt_package.json`  
**Per-Shot Prompts:** `08_prompts/per_shot_prompts.md`  
**Character Bibles:** `06_character_constraints/elizabeth_bennet.md`, `mr_darcy.md`  
**Style Lock:** `07_generation_rules/style_lock.md`  
**Negative Prompts:** `07_generation_rules/negative_prompts.md`  
**Shot List:** `05_storyboard/shot_list.md`  
**Script:** `03_adaptation/script.md`

---

## Success Metrics

**Video generation succeeds if:**
- [ ] All 48 shots generated
- [ ] Character consistency maintained (Elizabeth & Darcy look the same)
- [ ] Style lock adhered to (semi-realistic anime, period-accurate)
- [ ] Emotional beats land correctly
- [ ] 2-minute video assembled
- [ ] Video published on at least 2 platforms
- [ ] Viewer feedback gathered (100+ views minimum)
- [ ] Retrospective documented in `09_retrospective/`

---

**Ready to generate. Let's make this real. 🎬**
