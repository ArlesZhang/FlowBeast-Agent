# Quick Start: From Assets to Video

**Goal:** Build locked visual assets, then turn the prompt package into a real video

---

## Step 0: Build Visual Assets (DO THIS FIRST — 2-4 hours)

**Do NOT skip this step. Without locked assets, shot consistency is impossible.**

### Character Assets (GPT Image — ~1-2 hours)
1. Open ChatGPT with GPT Image
2. Use `06_character_constraints/elizabeth_bennet.md` and `mr_darcy.md` as references
3. Generate and save to `09_assets/characters/`:
   - Elizabeth: front, side, 3/4, full body, 5 expressions (9 images)
   - Darcy: front, side, 3/4, full body, wet coat detail, 5 expressions (10 images)
   - Interaction: together neutral, together conflict (2 images)
4. Verify all share the same art style (semi-realistic anime)

### Scene Assets (Jimeng AI — ~1-2 hours)
1. Open Jimeng AI (即梦)
2. Use `07_generation_rules/scene_lock.md` as reference
3. Generate and save to `09_assets/scenes/`:
   - Room: wide angle, window, door, fireplace, lighting, rain-on-window (6 images)
   - Weather: gentle, heavy, storm, soft rain (4 images)
4. Verify all room shots show the same layout and lighting

### Lock Check
- [ ] All 21 character assets created and approved
- [ ] All 10 scene assets created and approved
- [ ] Placed in correct `09_assets/` directories
- [ ] **You are satisfied with how characters and room look**

**Detailed instructions:** See `PRODUCTION_GUIDE.md` Phase 0

---

## Step 1: Open Jimeng AI (即梦) (5 minutes)
- Go to [jimeng.jianying.com](https://jimeng.jianying.com)
- Log in or create account
- Navigate to "AI Video Generation" or similar feature

## Step 2: Import Prompt Package (10 minutes)
- Open `08_prompts/prompt_package.json`
- Look for "Batch Import" or "JSON Import" in Jimeng AI
- Upload the file
- Verify 48 shots are loaded

**If no import feature:**
- Open `08_prompts/per_shot_prompts.md`
- Manually create first shot (S01) by copying the prompt
- Add negative prompts from `07_generation_rules/negative_prompts.md`
- Attach character and scene reference images from `09_assets/`

## Step 3: Generate First Batch (30 minutes)
- Generate shots S01-S06 (Beat 1: The Unexpected Arrival)
- Review each shot immediately
- Check character consistency (Elizabeth & Darcy)
- Check scene consistency (room, lighting, rain)
- Check style (semi-realistic anime, period-accurate)
- Regenerate any poor-quality shots

**Quality check:**
- Do Elizabeth and Darcy look consistent?
- Does the room look the same across shots?
- Is the lighting overcast/gray?
- Is rain visible?
- Are costumes correct (blue-gray dress, dark wet coat)?

## Step 4: Create 30-Second Test Clip (20 minutes)
- Select 10-12 key shots (see `PRODUCTION_GUIDE.md` Phase 3)
- Sequence them in order
- Add rain sound effect (gentle → heavy → storm)
- Review the test clip

**Decision point:**
- If test clip looks good → Continue to full assembly
- If test clip has issues → Fix problems first

## Step 5: Assemble Full Video (1-2 hours)
- Generate remaining shots (S07-S48)
- Sequence all 48 shots
- Add transitions (cuts)
- Add sound design (rain, thunder, score)
- Export as 1080p or 4K, 24 fps, 16:9

---

## Critical Files (Open These Now)

1. **`09_assets/characters/`** — Character reference images (build first)
2. **`09_assets/scenes/`** — Scene reference images (build first)
3. **`08_prompts/prompt_package.json`** — Import this into Jimeng AI
4. **`08_prompts/per_shot_prompts.md`** — Reference for each shot
5. **`07_generation_rules/scene_lock.md`** — Scene consistency reference
6. **`06_character_constraints/elizabeth_bennet.md`** — Character reference
7. **`06_character_constraints/mr_darcy.md`** — Character reference
8. **`07_generation_rules/negative_prompts.md`** — Quality control

---

## Quality Checklist (Per Shot)

After generating each shot, ask:

**Character:**
- [ ] Does Elizabeth look the same as in previous shots?
- [ ] Does Darcy look the same as in previous shots?
- [ ] Is Darcy's coat still wet? (critical!)
- [ ] Does the expression match the emotion?

**Scene:**
- [ ] Does the room look the same as in previous shots?
- [ ] Is the lighting overcast/gray? (no sunlight)
- [ ] Is rain visible? Does intensity match the beat?
- [ ] Are props correct (book, gloves)?

**Style:**
- [ ] Is the style semi-realistic anime? (not cartoon, not photorealistic)
- [ ] Is it period-accurate? (no modern elements)

**If any answer is NO → Regenerate the shot**

---

## Time Estimate

| Phase | Time |
|-------|------|
| Build character assets (GPT Image) | 1-2 hours |
| Build scene assets (Jimeng AI) | 1-2 hours |
| Generate 48 shots | 2-4 hours |
| Quality review | 1 hour |
| Assemble video | 1-2 hours |
| **Total** | **6-11 hours** |

**Can be done in two days** — Day 1: Assets, Day 2: Shots + Assembly.

---

## Next Actions

**Right now:**
1. Open ChatGPT with GPT Image
2. Start generating Elizabeth's front view
3. Then side, 3/4, full body, expressions
4. Then Darcy
5. Then scene assets in Jimeng AI

**After assets are locked:**
1. Open Jimeng AI (即梦)
2. Import `prompt_package.json`
3. Generate S01-S06 (first batch)
4. Review quality
5. Continue or fix issues

**This week:**
- Generate all 48 shots
- Create 30-second test clip
- Assemble full 2-minute video
- Add sound design
- Export final video
- Publish to Douyin/Bilibili

**Next week:**
- Gather viewer feedback
- Document learnings in `09_retrospective/`
- Plan Case Study #002

---

## Need Help?

**For detailed instructions:** Read `PRODUCTION_GUIDE.md`  
**For character reference:** Read `06_character_constraints/*.md`  
**For scene consistency:** Read `07_generation_rules/scene_lock.md`  
**For style reference:** Read `07_generation_rules/style_lock.md`  
**For shot sequence:** Read `05_storyboard/shot_list.md`

---

**Build assets first. Then generate shots. 🎬**
