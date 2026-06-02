# Content Strategy: The Real Phase 2 Blocker

## The Problem

Phase 2 (GRAFT/PARASITE) success depends **entirely on data quality**, not code quality.

**Current state:** FP3 has ~20 demo ViralUnit hooks (hand-written, not reverse-engineered). GRAFT/PARASITE with demo data = garbage output.

**Required state:** High-quality, reverse-engineered, labeled viral scripts across multiple genres and hook types.

**Critical insight:** The number "30 scripts" is a **validation threshold**, not a destination. For the Chinese short-drama market, 30 scripts is "did the pipeline even work?" — not a knowledge base.

## 🔴 Hard Constraint: Phase 0 Optimization Freeze

**Before reaching 30 real reverse-engineered samples:**

- ❌ Do NOT redesign the corpus system
- ❌ Do NOT introduce new metadata systems
- ❌ Do NOT introduce new databases
- ❌ Do NOT introduce new ingestion frameworks
- ❌ Do NOT introduce new taxonomy layers
- ❌ Do NOT optimize the schema
- ❌ Do NOT build automation

**Focus exclusively on:**
1. ✅ Acquiring samples (watch, judge, curate)
2. ✅ Reverse engineering samples (run CLI, verify output)
3. ✅ Building the first 30 ViralScript assets

**Why this exists:** Building better infrastructure when you have 2 samples is the same as building a factory when you have 2 customers. The most dangerous form of over-architecture is optimizing a system that has no data yet.

**Lifting the constraint:** After 30 real samples are collected and validated, you may optimize the corpus system. Not before.

## Explicit Corpus Tiers

| Tier | Scripts | What It Means | Phase Readiness | Time to Reach |
|------|---------|-------------|-----------------|---------------|
| **Validation** | 30 | "Can we even run GRAFT?" | Phase 2 entry gate | 4 weeks (sprint) |
| **MVP** | 100 | "GRAFT produces reliably good output" | Phase 2 MVP | 8-10 weeks |
| **Defensible** | 300 | "Cross-genre, statistically significant" | Phase 2 complete | 6 months |
| **Moat** | 1000+ | "Competitors can't replicate quickly" | Phase 3 ready | 12+ months |

**The dangerous number is 30.** It creates a false sense of security. "We have 30 scripts, let's ship Phase 2" when the reality is: 30 scripts proves the operator runs, not that it works.

## Sprint Model: Fast Path to Phase 2 Validation

**Problem:** At 1-2 scripts/week, 30 scripts takes 15-30 weeks (too slow).

**Solution:** Sprint-based acquisition (2-3 scripts/day × 2 weeks = 30 scripts).

### Sprint 1: Weeks 1-2 (15 scripts)
- **Goal:** Pipeline validation + initial diversity
- **Target:** 1-2 scripts per day
- **Focus:** 5+ genres represented
- **Effort:** ~8-10 hours total

### Sprint 2: Weeks 3-4 (15 scripts)
- **Goal:** Reach 30 scripts (Phase 2 entry gate)
- **Target:** 1-2 scripts per day
- **Focus:** Quality distribution (60% viral, 20% average, 20% failed)
- **Effort:** ~8-10 hours total

**By the time Phase 1 demo is done (2-3 weeks), you'll have 15-30 scripts in FP3 — ready for Phase 2.**

## Phase 2 Entry Requirements (30 scripts)

To validate that GRAFT/PARASITE can run, you need:

- **20 viral scripts** (quality_label: "viral")
  - 5+ genres represented (CEO, school, rebirth, revenge, xianxia, system, etc.)
  - 3+ hook types per genre (suspense, conflict, identity, reversal, curiosity)
  - Each fully decomposed via `reverse_engineer.py` CLI
  
- **10 average/failed scripts** (quality_label: "average" | "failed")
  - Negative samples for boundary learning
  - "What NOT to do" examples

- **Total: 30 scripts minimum** for Phase 2 validation

## Phase 2 MVP Requirements (100 scripts)

For GRAFT to produce output a human rates as "consistently good":

- **100 scripts across 10+ genres**
  - 5-10 scripts per genre
  - Hook type diversity within each genre
  - Emotional arc diversity (escalation patterns, payoffs, cliffhangers)
  - Quality distribution: ~60% viral, ~20% average, ~20% failed

## Phase 2 Complete Requirements (300 scripts)

- **300+ scripts** across 15+ genres
- Cross-platform (Douyin, Kuaishou, YouTube Shorts, TikTok)
- Temporal diversity (trends from last 12 months)
- Statistically significant patterns (z-score calibration meaningful on all dimensions)

## The Real Timeline

| Phase | Scripts Needed | Human Effort (est.) | Time | Sprint Model |
|-------|---------------|---------------------|------|--------------|
| Phase 2 validation | 30 | 16 hours | 4 weeks | Sprint 1+2 (2 scripts/day) |
| Phase 2 MVP | 100 | 60 hours | 8-10 weeks | Maintenance (1-2/week) |
| Phase 2 complete | 300 | 180 hours | 6 months | Ongoing |
| Defensible moat | 1000+ | 600+ hours | 12+ months | Ongoing |

**This is a content operations problem, not an engineering problem.**

## Provenance Pipeline

```
flowbeast/data/raw/                    # Human-curated raw samples
├── 001_ceos_secret_wife/
│   ├── source_url.txt                 # https://douyin.com/...
│   ├── notes.md                       # Human judgment + quality_label
│   ├── screenshot.png                 # (Optional) Key visual
│   └── transcript.txt                 # (Optional) Dialogue
│
├── 002_reborn_as_daughter/
│   └── ...
│
└── ... (one directory per raw sample)

          ↓ reverse_engineer.py --dir raw/

flowbeast/data/reverse_engineered/     # Agent-produced ViralScripts
├── 001_ceos_secret_wife.json
├── 002_reborn_as_daughter.json
└── ... (one JSON per sample)

          ↓ inject into FP3

flowbeast/data/vector_store/fp3/       # FP3 index + metadata
```

**Why provenance matters:**
- Trace bad output back to source
- Analyze which platforms/genres are over/under-represented
- Evaluate corpus quality over time
- Reproduce analysis if schema changes

## Data Sources

| Source | Pros | Cons | Priority |
|--------|------|------|----------|
| **Manual curation** | High quality, cultural context | Slow (35 min/script) | Primary (Sprint 1+2) |
| **User submissions** | Scalable, bootstraps flywheel | Needs Phase 1 demo first | Phase 2+ |
| **Scraping** | Fast | Legal risk, quality varies | TBD |
| **Third-party APIs** | Structured data | Cost, data rights | TBD |

**Recommendation:** Start with manual curation NOW (parallel with Phase 1). Sprint model: 1-2 scripts per day for 4 weeks = 30 scripts (Phase 2 validation).

## Content Operations Workflow

```
Human (judge + curator):
  1. Watch viral short drama on Douyin/TikTok/Kuaishou
  2. Judge: is this worth preserving? (viral metrics, hook strength, replay value)
  3. Create raw/NNN_title/ directory
  4. Fill in: source_url.txt, notes.md, (optional) screenshot.png, transcript.txt

Agent (extractor + structurer):
  5. Run reverse_engineer.py --dir raw/ → batch process all samples
  6. Extract: hook_structure, conflict_pattern, emotional_curve, pacing_profile
  7. Validate: all fields filled, logical consistency
  8. Inject into FP3 → QualityGate calibrates
  9. Track progress in .ai/tasks/000_viral_corpus_building.md

Repeat 30 → 100 → 300 → 1000+ times
```

**Time per script:**
- Human curation: ~30 min (watch + judge + fill raw/ directory)
- Agent extraction: ~5 min (run CLI, verify output)
- Total: ~35 min per script

## Success Metric: When Is Phase 2 Ready?

### Phase 2 Entry (30 scripts)
- [ ] 30 scripts decomposed and stored in FP3
- [ ] 5+ genres represented
- [ ] Quality distribution: ~60% viral, ~20% average, ~20% failed
- [ ] QualityGate calibration shows σ > 0.01 on ≥ 5 dimensions
- [ ] GRAFT on a NEW topic produces output rated "better than random" by human

### Phase 2 MVP (100 scripts)
- [ ] 100 scripts across 10+ genres
- [ ] GRAFT produces output a human rates as "consistently good"
- [ ] PARASITE matches trends to compatible spines reliably
- [ ] Corpus analysis shows no major gaps (genre, platform, time)

### Phase 2 Complete (300 scripts)
- [ ] 300+ scripts with statistical significance
- [ ] Cross-platform diversity (Douyin, TikTok, Kuaishou, YouTube)
- [ ] Temporal diversity (trends from last 12 months)
- [ ] Corpus is defensible (competitors can't replicate quickly)

## The Moat

**Code is not the moat. Viral Knowledge Base is the moat.**

Anyone can build a script generator with an LLM. But a curated, decomposed, labeled database of 300+ viral scripts with latent grammar? That's defensible.

**Prioritize content collection over architectural sophistication.**

## Parallel Execution Strategy

**Phase 1 (Demo System) and Phase 0 (Corpus Building) run in parallel.**

- Phase 1 needs engineering focus (HTTP, frontend, async handling)
- Phase 0 needs human focus (watch, judge, curate)
- They don't block each other
- Sprint 1+2 (4 weeks): 30 scripts → Phase 2 entry gate
- Phase 2 starts when BOTH Phase 1 (done) AND Phase 0 (30 scripts) are ready

**By the time Phase 1 demo is polished (2-3 weeks), Phase 0 will have produced 15-30 scripts — ready for Phase 2.**
