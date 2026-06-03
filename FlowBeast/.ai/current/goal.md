# Current Goal: v0.6.0 — 30 Real Reverse-Engineered Scripts

**Phase:** 0 (Corpus Building)  
**Sprint 1:** June 1-14 (15 scripts)  
**Sprint 2:** June 15-28 (15 scripts)  
**Target:** 30 real scripts → Phase 2 entry gate

---

## Mission

Validate that the Corpus Factory process works by reverse-engineering 30 real viral short dramas into GOLD-quality ViralScript artifacts.

**Success Metric:** Can a new topic inherit proven viral mechanics and outperform baseline generation?

---

## Why This Matters

- GRAFT works with seed data but produces generic output (all 5 runs use same hook: 冲突爆发)
- With 30 real scripts, GRAFT will have diverse viral structures to transfer
- QualityGate calibration requires real data for meaningful z-score statistics
- This is the single highest-leverage thing to do next — everything else is blocked by it

---

## What You Do NOT Do

- ❌ Do NOT redesign the corpus system (see `.ai/decisions/002_what_we_do_not_do.md` #8)
- ❌ Do NOT introduce new metadata systems, databases, ingestion frameworks
- ❌ Do NOT optimize the schema
- ❌ Do NOT build automation
- ❌ Do NOT build PARASITE/DISTORT/MISDIRECT/THEFT
- ❌ Do NOT redesign test infrastructure
- ❌ Do NOT work on video generation, publishing, analytics

**Focus exclusively on:** acquiring samples, reverse engineering them, building 30 ViralScripts.

---

## How to Do It

1. Watch 1-2 viral short dramas per day
2. Follow the checklist in `.ai/reports/003_human_annotation_checklist.md`
3. Run `uv run python -m flowbeast.reverse.reverse_engineer`
4. Verify output: all GRAFT-critical fields populated, QualityGate ACCEPT/REVIEW
5. Track progress in `.ai/milestones/v0.6.0-corpus-30.md`

---

## Controlled Vocabularies

Use the vocabularies in `.ai/reports/002_gold_standard_vocab.md`:

- **7 hook types:** 冲突爆发, 身份错位, 悬念开场, 好奇驱动, 情感暴击, 权力反转, 超自然介入
- **8 conflict types:** 权力碾压, 身份揭露, 逻辑反杀, 情感背叛, 资源争夺, 尊严捍卫, 规则博弈, 立场对立
- **17 genres:** 逆袭, 身份反转, 重生, 霸总, 家庭伦理, 职场, 玄幻, 系统, 悬疑, 喜剧, 悲剧, 甜宠, 复仇, 穿越, 末日, 校园, 其他

---

## Acceptance Criteria

### Phase 2 Entry (30 scripts)

- [ ] 30 scripts decomposed and stored in FP3
- [ ] 5+ genres represented (minimum 3 per genre)
- [ ] Quality distribution: ~60% viral, ~20% average, ~20% failed
- [ ] QualityGate calibration shows σ > 0.01 on ≥ 5 dimensions
- [ ] GRAFT on a NEW topic produces output rated "better than random" by human
- [ ] At least 3 different hook types used in corpus
- [ ] At least 3 different conflict types used in corpus

---

## Reference Documents

- `.ai/milestones/v0.6.0-corpus-30.md` — Detailed sprint tracker
- `.ai/reports/001_corpus_factory.md` — Full audit + schema analysis
- `.ai/reports/002_gold_standard_vocab.md` — Controlled vocabularies
- `.ai/reports/003_human_annotation_checklist.md` — Step-by-step annotation guide
- `.ai/reports/004_corpus_quality_criteria.md` — GOLD/SILVER/BRONZE/REJECT scoring
- `.ai/content_strategy.md` — Corpus strategy + tiers
- `.ai/decisions/002_what_we_do_not_do.md` — Hard boundaries
