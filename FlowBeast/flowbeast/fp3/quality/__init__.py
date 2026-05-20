"""
FP3 Quality Gate Subpackage.

Pipeline: score() -> dedup() -> gate() -> audit()
"""

from .models import GateAction, ScoreResult, DedupResult, GateDecision, CategoryScore
from .config import QualitySettings, quality_settings
from .scorer import BaseScorer, RuleBasedScorer
from .dedup import BaseDeduplicator, EmbeddingDeduplicator
from .gate import QualityGate
from ..store import FP3Store


def create_quality_gate(store: FP3Store = None, audit_dir=None) -> QualityGate:
    """Create a fully wired QualityGate instance from settings."""
    store = store or FP3Store()
    scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
    deduplicator = EmbeddingDeduplicator(
        similarity_threshold=quality_settings.DEDUP_SIMILARITY_THRESHOLD,
        search_k=quality_settings.DEDUP_SEARCH_K,
    )
    return QualityGate(
        scorer=scorer,
        deduplicator=deduplicator,
        store=store,
        accept_threshold=quality_settings.QUALITY_ACCEPT_THRESHOLD,
        review_threshold=quality_settings.QUALITY_REVIEW_THRESHOLD,
        audit_dir=audit_dir,
        enabled=quality_settings.QUALITY_GATE_ENABLED,
    )


__all__ = [
    "GateAction", "ScoreResult", "DedupResult", "GateDecision", "CategoryScore",
    "QualitySettings", "quality_settings",
    "BaseScorer", "RuleBasedScorer",
    "BaseDeduplicator", "EmbeddingDeduplicator",
    "QualityGate", "create_quality_gate",
]
