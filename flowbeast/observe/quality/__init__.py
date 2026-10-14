"""
Observe Quality Gate Subpackage.

Pipeline: score() -> dedup() -> gate() -> audit()
"""

from loguru import logger

from .models import GateAction, ScoreResult, DedupResult, GateDecision, CategoryScore
from .config import QualitySettings, quality_settings
from .scorer import BaseScorer, RuleBasedScorer, ReferenceAnchoredScorer
from .dedup import BaseDeduplicator, EmbeddingDeduplicator
from .gate import QualityGate
from flowbeast.fp3.store import FP3Store


def create_quality_gate(
    store: FP3Store = None,
    audit_dir=None,
    calibrated: bool = False,
) -> QualityGate:
    """
    Create a fully wired QualityGate instance from settings.

    Args:
        store: FP3 store for dedup checks
        audit_dir: Optional audit log directory
        calibrated: If True, try to load calibration data and use
            ReferenceAnchoredScorer. Falls back to RuleBasedScorer
            if no calibration report exists.
    """
    store = store or FP3Store()
    deduplicator = EmbeddingDeduplicator(
        similarity_threshold=quality_settings.DEDUP_SIMILARITY_THRESHOLD,
        search_k=quality_settings.DEDUP_SEARCH_K,
    )

    # --- Scorer selection ---
    if calibrated:
        from .calibrator import load_calibration_report
        report = load_calibration_report()
        if report:
            logger.info(
                f"QualityGate: using ReferenceAnchoredScorer "
                f"(calibrated, {report['reference_count']} samples)"
            )
            # Apply recommended thresholds if available
            accept = report.get("recommended_thresholds", {}).get(
                "accept", quality_settings.QUALITY_ACCEPT_THRESHOLD
            )
            review = report.get("recommended_thresholds", {}).get(
                "review", quality_settings.QUALITY_REVIEW_THRESHOLD
            )
            weights = report.get("recommended_weights", quality_settings.weights_dict)
            reference_stats = report.get("dimension_stats", {})
            scorer = ReferenceAnchoredScorer(
                weights=weights,
                reference_stats=reference_stats,
            )
        else:
            logger.info("QualityGate: no calibration data, using RuleBasedScorer")
            scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
            accept = quality_settings.QUALITY_ACCEPT_THRESHOLD
            review = quality_settings.QUALITY_REVIEW_THRESHOLD
    else:
        scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
        accept = quality_settings.QUALITY_ACCEPT_THRESHOLD
        review = quality_settings.QUALITY_REVIEW_THRESHOLD

    return QualityGate(
        scorer=scorer,
        deduplicator=deduplicator,
        store=store,
        accept_threshold=accept,
        review_threshold=review,
        audit_dir=audit_dir,
        enabled=quality_settings.QUALITY_GATE_ENABLED,
    )


__all__ = [
    "GateAction", "ScoreResult", "DedupResult", "GateDecision", "CategoryScore",
    "QualitySettings", "quality_settings",
    "BaseScorer", "RuleBasedScorer", "ReferenceAnchoredScorer",
    "BaseDeduplicator", "EmbeddingDeduplicator",
    "QualityGate", "create_quality_gate",
]
