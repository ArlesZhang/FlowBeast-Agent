# Corpus Quality Criteria

**Version:** 1.0  
**Date:** 2026-06-01

---

## Quality Tiers

| Tier | Criteria | GRAFT Output Quality | Use In |
|------|----------|---------------------|--------|
| **GOLD** | All structural fields accurate + human confidence >= 0.8 + QualityGate ACCEPT | Structurally differentiated, proven viral DNA | GRAFT retrieval pool, corpus training |
| **SILVER** | All required fields populated + some uncertainty on 1-2 fields + QualityGate ACCEPT/REVIEW | Adequate but may be generic | GRAFT retrieval pool (lower priority) |
| **BRONZE** | Required fields populated but some are weak + QualityGate REVIEW | May produce generic output | Review queue for upgrade to SILVER |
| **REJECT** | Any required field missing or wrong + QualityGate REJECT | N/A | Fix and resubmit |

---

## Scoring Rubric

### GOLD (Score: 4)

- `hook_type` matches controlled vocabulary AND accurately describes the hook
- `conflict_type` matches controlled vocabulary AND accurately describes the conflict
- `escalation_curve` has 3-5 steps AND matches the actual progression
- `opening_line` is the actual first line/visual
- `audience_question` is a specific, compelling question
- `emotional_payload` is a specific emotion (not generic)
- `highest_stakes` matches controlled vocabulary AND accurately describes stakes
- `curve_sequence` has 3+ emotions AND matches actual progression
- `semantic_summary` explains WHY it went viral (not just plot summary)
- `source_url` works and points to the correct video
- `genre` is specific and accurate
- `quality_label` is justified by actual engagement data

**Minimum 12/12 criteria met.**

### SILVER (Score: 3)

- All GOLD criteria EXCEPT:
  - 1-2 fields have minor inaccuracies (e.g., `escalation_curve` has wrong order but correct steps)
  - `audience_question` is specific but may not capture the exact viewer psychology
  - `semantic_summary` is good but could be sharper
  - Human confidence is 0.6-0.8

**Minimum 9/12 criteria met, no REJECT violations.**

### BRONZE (Score: 2)

- Required fields populated but:
  - `opening_line` is a paraphrase, not the actual first line
  - `hook_type` is correct but `conflict_type` is uncertain
  - `escalation_curve` is incomplete (2 steps) or order is wrong
  - `semantic_summary` is a plot summary, not a viral reason
  - Human confidence is 0.4-0.6

**Minimum 6/12 criteria met, no REJECT violations.**

### REJECT (Score: 1)

Any of the following:

- `opening_line` is empty or a placeholder
- `hook_type` doesn't match any controlled vocabulary value AND isn't "其他"
- `conflict_type` doesn't match any controlled vocabulary value AND isn't "其他"
- `escalation_curve` has 0-1 steps
- `curve_sequence` has 0-1 emotions
- `quality_label` is not one of viral/average/failed
- `source_url` is a placeholder ("https://") or missing
- `genre` is empty or generic ("短剧")
- The JSON doesn't parse as a valid ViralScript

---

## Quality Gate Integration

The QualityGate (`observe/quality/gate.py`) evaluates ViralUnit (3 fields), not ViralScript (full anatomy). This means:

1. **QualityGate catches gross duplicates** — two entries with the same hook + pattern + emotion
2. **QualityGate does NOT catch subtle errors** — wrong hook_type classification, incorrect escalation curve, empty audience_question
3. **Human review is the primary quality control** — the checklist in 003_human_annotation_checklist.md is more important than the automated gate

**Recommendation:** Keep QualityGate as a duplicate detector and gross error filter. Rely on human review for nuanced accuracy.

---

## Progression Rules

| From | To | How |
|------|----|-----|
| BRONZE → SILVER | Re-annotate with the checklist, fix weak fields | Re-run reverse_engineer.py with corrections |
| SILVER → GOLD | Re-watch source video, verify all 12 criteria | Requires second human review or re-watch |
| Any → REJECT | Auto-detected by QualityGate or manual review | Fix and resubmit |
| REJECT → BRONZE+ | Fix the violations, resubmit | Re-run reverse_engineer.py |

---

## Corpus-Level Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **GOLD ratio** | >= 60% of corpus | Count GOLD / total entries |
| **Genre diversity** | >= 5 genres with >= 3 entries each | Group by genre |
| **Hook type diversity** | >= 5 hook types represented | Group by hook_type |
| **Conflict type diversity** | >= 5 conflict types represented | Group by conflict_type |
| **Platform diversity** | >= 2 platforms represented | Group by source_platform |
| **Quality label distribution** | ~60% viral, ~20% average, ~20% failed | Group by quality_label |
| **Annotation confidence avg** | >= 0.7 | Average confidence_score |
