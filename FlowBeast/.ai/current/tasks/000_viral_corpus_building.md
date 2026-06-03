# Task 000: Viral Corpus Building (Long-Running)

## Status: 🟡 Sprint 1 Active (parallel with Phase 1)
## Priority: 🔴 Critical (blocks Phase 2)
## Depends on: —
## Blocks: Phase 2 (GRAFT/PARASITE)
## Related: `.ai/content_strategy.md`

## Objective

Build the Viral Knowledge Base — the real moat of FlowBeast. Reverse-engineer high-quality viral short dramas into FP3-compatible ViralScript artifacts.

**This is a content operations task, not a coding task.** It runs in parallel with Phase 1 engineering.

## Why This Matters

- GRAFT/PARASITE with 2 demo samples = garbage output
- GRAFT/PARASITE with 30 curated samples = works
- GRAFT/PARASITE with 100+ curated samples = defensible

**The number "30" is a validation threshold, not a destination.** See `.ai/content_strategy.md` for corpus size analysis.

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

**Why:** This is the most dangerous form of over-architecture. Building better infrastructure when you have 2 samples is the same as building a factory when you have 2 customers. Get to 30 first, then optimize.

## Sprint Model (Parallel with Phase 1)

### Sprint 1: Weeks 1-2 (15 scripts)

**Goal:** Pipeline validation + initial diversity
- Target: 1-2 scripts per day
- Focus: 5+ genres represented
- Effort: ~8-10 hours total

### Sprint 2: Weeks 3-4 (15 scripts)

**Goal:** Reach 30 scripts (Phase 2 entry gate)
- Target: 1-2 scripts per day
- Focus: Quality distribution (60% viral, 20% average, 20% failed)
- Effort: ~8-10 hours total

### Maintenance: Weeks 5+ (ongoing)

**Goal:** Grow to 100 scripts (Phase 2 MVP)
- Target: 1-2 scripts per week
- Focus: Genre depth + trend diversity
- Effort: ~35 min per script

**By the time Phase 1 demo is done (2-3 weeks), you'll have 15-30 scripts in FP3 — ready for Phase 2.**

## Division of Responsibility

### Human (Curator + Judge)

- **Discover:** Watch viral content on Douyin, TikTok, Kuaishou, YouTube Shorts
- **Select:** Choose scripts worth preserving (based on viral metrics, hook strength, replay value)
- **Judge:** Rate quality (viral / average / failed) and explain WHY
- **Provide raw source:** Create `flowbeast/data/raw/NNN_title/` directory with:
  - `source_url.txt` — URL to the original video
  - `notes.md` — Human curator notes + quality judgment
  - `screenshot.png` — (Optional) Key visual or thumbnail
  - `transcript.txt` — (Optional) Dialogue transcript

### Agent (Extractor + Structurer)

- **Batch process:** Run `reverse_engineer.py --dir raw/` on human-provided raw material
- **Extract:** hook_structure, conflict_pattern, emotional_curve, pacing_profile, characters
- **Normalize:** Convert to FP3-compatible ViralScript format
- **Validate:** Verify output quality (all fields filled, logical consistency)
- **Store:** Inject into FP3, update QualityGate calibration
- **Track progress:** Update this task file with running count

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

## Explicit Corpus Tiers

| Tier | Scripts | What It Means | Phase Readiness |
|------|---------|-------------|-----------------|
| **Validation** | 30 | "Can we even run GRAFT?" | Phase 2 entry gate |
| **MVP** | 100 | "GRAFT produces reliably good output" | Phase 2 MVP |
| **Defensible** | 300 | "Cross-genre, statistically significant" | Phase 2 complete |

**The number "30" is NOT the finish line.** It's the minimum to validate that GRAFT/PARASITE can run. Meaningful quality requires 100+. Defensibility requires 300+.

## Progress Tracker

| # | Date | Title | Genre | Hook Type | Quality | Raw Dir |
|---|------|-------|-------|-----------|---------|---------|
| 1 | | | | | | `raw/001_.../` |
| 2 | | | | | | `raw/002_.../` |
| 3 | | | | | | `raw/003_.../` |
| ... | | | | | | |

**Current count:** 0 scripts (Sprint 1 not started)

## Acceptance Criteria

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

## Estimated Effort

- **Sprint 1 (15 scripts):** ~8 hours (2 weeks × 1-2/day)
- **Sprint 2 (15 scripts):** ~8 hours (2 weeks × 1-2/day)
- **Phase 2 validation total:** ~16 hours over 4 weeks
- **Phase 2 MVP (100 scripts):** ~60 hours over 8-10 weeks
- **Phase 2 complete (300 scripts):** ~180 hours over 6 months

## Key Commands

```bash
# Reverse-engineer a single raw sample
uv run python -m flowbeast.reverse.reverse_engineer --input raw/001_title/

# Batch import all raw samples
uv run python -m flowbeast.reverse.reverse_engineer --dir raw/

# Check FP3 corpus size
uv run python -c "from flowbeast.fp3.store import FP3Store; s=FP3Store(); print(f'FP3 has {len(s.meta)} entries')"

# Run QualityGate calibration
uv run python -c "from flowbeast.fp3.quality.calibrator import run_calibration; import asyncio; asyncio.run(run_calibration())"
```

## Data Storage

- **Raw samples:** `flowbeast/data/raw/` (human-curated, one dir per sample)
- **Processed scripts:** `flowbeast/data/reverse_engineered/` (agent-produced)
- **FP3 index:** `flowbeast/data/vector_store/fp3/` (agent-managed)

## Open Questions

- What is the primary source of viral scripts? (Douyin? TikTok? Kuaishou?)
- Should we track platform-specific trends (e.g., Douyin vs TikTok)?
- How long is a script's "shelf life" before trends change?
- Should failed scripts be from our own generation (negative samples) or real market failures?
