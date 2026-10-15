# Skill: QualityGate — Accept/Review/Reject Pipeline

## Purpose
QualityGate is the type checker of the FP3 Latent Grammar. It rejects atom combinations that violate the learned viral grammar — ensuring only structurally sound, non-duplicate, high-signal content enters FP3 or reaches generation output.

## Decision Pipeline
```
ViralUnit candidate
    → Stage 1: Score (RuleBasedScorer)
    → Stage 2: Dedup (EmbeddingDeduplicator against FP3 store)
    → Stage 3: Gate rules → GateDecision {ACCEPT | REVIEW | REJECT}
    → Stage 4: Audit log (JSON file per decision)
```

## Thresholds
| Action | Condition |
|--------|-----------|
| **ACCEPT** | `weighted_total >= 0.60` AND not a duplicate |
| **REVIEW** | `0.40 <= weighted_total < 0.60` AND not a duplicate |
| **REJECT** | `weighted_total < 0.40` OR is a duplicate |

## Scoring Dimensions (9 total, weighted sum)
`hook_strength` · `emotional_intensity` · `novelty` · `retention_potential` · `virality_signals` · `pacing` · `engagement_density` · `conflict_density` · `replay_potential`

### RuleBasedScorer
Heuristic regex-based scoring. Each dimension scans for keyword markers (e.g., shock/twist/secret for hook_strength, cliffhanger phrases for retention_potential).

> The former `ReferenceAnchoredScorer` and its calibrator were deleted — the reference distribution
> they scored against was never fitted to real outcomes, so the percentile mapping was circular.

## Data Models
```python
GateAction    # Enum: ACCEPT | REJECT | REVIEW
ScoreResult   # category_scores: Dict[str,float], weighted_total, explanations
DedupResult   # is_duplicate, similarity_score, closest_match, threshold_used
GateDecision  # candidate_hook, action, score_result, dedup_result, reason, audit_trail
```

## Key Files
- `flowbeast/observe/quality/gate.py` — orchestrator (evaluate, evaluate_and_store)
- `flowbeast/observe/quality/scorer.py` — RuleBasedScorer
- `flowbeast/observe/quality/dedup.py` — EmbeddingDeduplicator
- `flowbeast/observe/quality/config.py` — thresholds and weights
- `flowbeast/observe/quality/models.py` — typed Pydantic models

## Call Sites
- `flowbeast/drama/pipeline.py` → `_run_output_quality_gate()` — gates generated output
- `flowbeast/fp3/feedback.py` — gates incoming feedback-fed scripts
