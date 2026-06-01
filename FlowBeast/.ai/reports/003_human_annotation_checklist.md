# Human Annotation Checklist — Reverse Engineering a Viral Script

**Time budget:** 20-30 minutes per script  
**Tool:** `uv run python -m flowbeast.reverse.reverse_engineer`

Print this checklist or keep it open while annotating.

---

## Step 0: Preparation

- [ ] Open the viral short drama on Douyin/Kuaishou/RedNote
- [ ] Have the interactive reverse_engineer.py CLI ready
- [ ] Have a notes app or paper ready for jotting key moments

---

## Step 1: Watch and Note (5 minutes)

- [ ] Watch the full script (3-5 minutes)
- [ ] Note the **first line or opening visual** (this is `opening_line`)
- [ ] Note what **question** you had after the first 3 seconds (this is `audience_question`)
- [ ] Note the **core conflict** — who vs who, what's at stake
- [ ] Note the **emotional journey** — how did you feel at each point?
- [ ] Note the **ending** — catharsis, cliffhanger, or bittersweet?
- [ ] Note any **special techniques** — silence before reveal, micro-expressions, etc.

---

## Step 2: Fill Interactive Form (10 minutes)

Run: `uv run python -m flowbeast.reverse.reverse_engineer`

### Section 1: Source Info

- [ ] `source_title` — Exact title of the short drama
- [ ] `source_platform` — From controlled vocab: 红果短剧 / 抖音 / 快手 / YouTube Shorts / TikTok / 其他
- [ ] `source_url` — Direct link to the video

### Section 2: Viral Metrics

- [ ] `viral_metrics.views` — Approximate view count (e.g., "500万")
- [ ] `viral_metrics.likes` — Approximate like count (e.g., "50万")
- [ ] `quality_label` — viral (high engagement, replay value) / average (decent but not standout) / failed (should have worked but didn't)

### Section 3: Hook Structure ⚠️ Critical for GRAFT

- [ ] `opening_line` — The actual first line/visual text (NOT a summary)
- [ ] `hook_type` — From controlled vocabulary: 冲突爆发 / 身份错位 / 悬念开场 / 好奇驱动 / 情感暴击 / 权力反转 / 超自然介入
- [ ] `time_to_hook` — immediate / within_3s / delayed
- [ ] `audience_question` — What a viewer naturally asks after the hook (e.g., "为什么他要这样做?", "她是谁?")
- [ ] `emotional_payload` — The core emotion (压抑 / 震惊 / 愤怒 / 甜蜜 / 恐惧 / 好奇 / 紧张)

### Section 4: Conflict Pattern ⚠️ Critical for GRAFT

- [ ] `conflict_type` — From controlled vocabulary: 权力碾压 / 身份揭露 / 逻辑反杀 / 情感背叛 / 资源争夺 / 尊严捍卫 / 规则博弈 / 立场对立
- [ ] `escalation_curve` — Sequence of 3-5 steps from: 压抑 / 铺垫 / 升级 / 爆发 / 反转 / 悬念 / 高潮 / 余韵
- [ ] `reversal_count` — Integer 0-5 (how many times the outcome flips)
- [ ] `highest_stakes` — From controlled vocabulary: 尊严 / 生存 / 情感 / 权力 / 真相 / 自由

### Section 5: Emotional Curve

- [ ] `curve_sequence` — List of emotions in order (at least 3): 压抑 / 震惊 / 愤怒 / 爽点 / 甜蜜 / 悲伤 / 恐惧 / 紧张 / 绝望 / 希望
- [ ] `peak_emotion` — The strongest emotion
- [ ] `peak_position` — early / middle / late
- [ ] `resolution_type` — From controlled vocabulary: 爽点收尾 / 悬念留白 / 情感余韵 / 循环闭合 / 开放式结局

### Section 6: Pacing Profile

- [ ] `duration_sec` — Approximate total duration in seconds
- [ ] `scene_count` — Number of distinct scenes
- [ ] `beat_distribution` — How many scenes of each beat type (tension, payoff, reveal, setup, cliffhanger)

### Section 7: Production Notes

- [ ] `genre` — From controlled vocabulary (see 002_gold_standard_vocab.md)
- [ ] `tags` — From consistent tag list
- [ ] `characters` — At least protagonist (name, role, archetype, transformation arc)
- [ ] `special_techniques` — Notable production techniques (e.g., "沉默停顿3秒", "身份揭示前静默")
- [ ] `semantic_summary` — One line: "这部剧为什么火？"

---

## Step 3: Review (5 minutes)

- [ ] Re-read the saved JSON file
- [ ] Verify all 10 GRAFT-critical fields are non-empty and accurate
- [ ] Check that controlled vocabulary values match the actual content
- [ ] Verify `audience_question` is a real question a viewer would ask
- [ ] Verify `opening_line` is the actual first line, not a summary
- [ ] Check `escalation_curve` shows actual progression

---

## Step 4: Validate (2 minutes)

```bash
# Verify the JSON parses correctly
uv run python -m flowbeast.reverse.reverse_engineer --input flowbeast/data/reverse_engineered/YOUR_FILE.json --no-inject
```

- [ ] No Pydantic errors
- [ ] QualityGate result: ACCEPT or REVIEW (if REJECT, review and fix)

---

## Step 5: Accept

- [ ] If QualityGate passed, accept the entry into FP3
- [ ] Update the progress tracker in `.ai/tasks/000_viral_corpus_building.md`
- [ ] File the raw source material in `flowbeast/data/raw/NNN_title/`

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | How to Fix |
|---------|-------------|------------|
| `opening_line` is a summary, not the actual first line | GRAFT needs the structural pattern of the actual hook | Re-watch the first 3 seconds and transcribe exactly |
| `audience_question` is empty or generic ("发生了什么?") | GRAFT can't transfer audience psychology | Think: "What made ME keep watching after the hook?" |
| `hook_type` doesn't match the actual hook | GRAFT transfers the wrong structure | Compare against the controlled vocabulary definitions |
| `escalation_curve` is too short (1-2 steps) | GRAFT can't transfer the escalation pattern | Watch the conflict progression scene by scene |
| `semantic_summary` is a plot summary, not a viral reason | Can't learn WHY scripts go viral | Ask: "What emotional need did this fulfill?" |
