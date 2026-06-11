# Quick Start: Generate Video Now

**Goal:** Turn the prompt package into a real video in the next 24-48 hours

---

## 5-Step Action Plan

### Step 1: Open Jimeng AI (即梦) (5 minutes)
- Go to [jimeng.jianying.com](https://jimeng.jianying.com)
- Log in or create account
- Navigate to "AI Video Generation" or similar feature

### Step 2: Import Prompt Package (10 minutes)
- Open `08_prompts/prompt_package.json`
- Look for "Batch Import" or "JSON Import" in Jimeng AI
- Upload the file
- Verify 48 shots are loaded

**If no import feature:**
- Open `08_prompts/per_shot_prompts.md`
- Manually create first shot (S01) by copying the prompt
- Add negative prompts from `07_generation_rules/negative_prompts.md`

### Step 3: Generate First Batch (30 minutes)
- Generate shots S01-S06 (Beat 1: The Unexpected Arrival)
- Review each shot immediately
- Check character consistency (Elizabeth & Darcy)
- Check style (semi-realistic anime, period-accurate)
- Regenerate any poor-quality shots

**Quality check:**
- Do Elizabeth and Darcy look consistent?
- Is the lighting overcast/gray?
- Is rain visible?
- Are costumes correct (blue-gray dress, dark wet coat)?

### Step 4: Create 30-Second Test Clip (20 minutes)
- Select 10-12 key shots (see `PRODUCTION_GUIDE.md` Phase 3)
- Sequence them in order
- Add rain sound effect (gentle → heavy → storm)
- Review the test clip

**Decision point:**
- If test clip looks good → Continue to full assembly
- If test clip has issues → Fix problems first

### Step 5: Assemble Full Video (1-2 hours)
- Generate remaining shots (S07-S48)
- Sequence all 48 shots
- Add transitions (cuts)
- Add sound design (rain, thunder, score)
- Export as 1080p or 4K, 24 fps, 16:9

---

## Critical Files (Open These Now)

1. **`08_prompts/prompt_package.json`** — Import this into Jimeng AI
2. **`08_prompts/per_shot_prompts.md`** — Reference for each shot
3. **`06_character_constraints/elizabeth_bennet.md`** — Character reference
4. **`06_character_constraints/mr_darcy.md`** — Character reference
5. **`07_generation_rules/negative_prompts.md`** — Quality control

---

## Quality Checklist (Per Shot)

After generating each shot, ask:

- [ ] Does Elizabeth look the same as in previous shots?
- [ ] Does Darcy look the same as in previous shots?
- [ ] Is Darcy's coat still wet? (critical!)
- [ ] Is the lighting overcast/gray? (no sunlight)
- [ ] Is rain visible?
- [ ] Does the expression match the emotion?
- [ ] Is the style semi-realistic anime? (not cartoon, not photorealistic)

**If any answer is NO → Regenerate the shot**

---

## Troubleshooting

**Problem: Character faces change**
- Solution: Use same reference image for all shots
- Solution: Increase face description in prompts
- Solution: Use "face lock" feature if available

**Problem: Darcy's coat dries**
- Solution: Add "wet coat, dripping water" to every prompt
- Solution: Add "dry coat" to negative prompts

**Problem: Style drift**
- Solution: Add style description to every prompt
- Solution: Use style reference image

---

## Time Estimate

| Phase | Time |
|-------|------|
| Import & setup | 15 minutes |
| Generate 48 shots | 2-4 hours |
| Quality review | 1 hour |
| Assemble video | 1-2 hours |
| **Total** | **4-7 hours** |

**Can be done in one day** if you focus.

---

## Next Actions

**Right now:**
1. Open Jimeng AI (即梦)
2. Import `prompt_package.json`
3. Generate S01-S06 (first batch)
4. Review quality
5. Continue or fix issues

**Today:**
- Generate all 48 shots
- Create 30-second test clip
- Assemble full 2-minute video

**Tomorrow:**
- Add sound design
- Color grading
- Export final video
- Publish to Douyin/Bilibili

**This week:**
- Gather viewer feedback
- Document learnings in `09_retrospective/`
- Plan Case Study #002

---

## Need Help?

**For detailed instructions:** Read `PRODUCTION_GUIDE.md`  
**For character reference:** Read `06_character_constraints/*.md`  
**For style reference:** Read `07_generation_rules/style_lock.md`  
**For shot sequence:** Read `05_storyboard/shot_list.md`

---

**Stop planning. Start generating. 🎬**
