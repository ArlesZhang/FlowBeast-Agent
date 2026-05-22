from abc import ABC, abstractmethod
from typing import Optional
from loguru import logger

from .models import DedupResult
from ..schema import ViralUnit
from ..store import FP3Store
from ..embedding import embed_unit


class BaseDeduplicator(ABC):
    """Abstract deduplication engine. Swap in Qdrant/Weaviate/Pgvector implementations."""

    @abstractmethod
    async def check_duplicate(self, unit: ViralUnit, store: FP3Store) -> DedupResult:
        """Check if a candidate ViralUnit is semantically duplicate in the store."""
        ...


class EmbeddingDeduplicator(BaseDeduplicator):
    """
    Dedup using existing FP3 embedding infrastructure + FAISS search.

    Converts L2 distance to cosine similarity proxy via:
        cos_sim = 1 - (L2_distance^2) / 2
    """

    def __init__(self, similarity_threshold: float = 0.95, search_k: int = 5):
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError(f"similarity_threshold must be in [0,1], got {similarity_threshold}")
        self.threshold = similarity_threshold
        self.search_k = search_k

    async def check_duplicate(self, unit: ViralUnit, store: FP3Store) -> DedupResult:
        logger.debug(f"Dedup: embedding candidate [hook={unit.hook[:30]}...]")
        candidate_vec = embed_unit(unit)

        if store.index.ntotal == 0:
            logger.debug("Dedup: store is empty, no duplicates possible")
            return DedupResult(
                is_duplicate=False, similarity_score=0.0, threshold_used=self.threshold,
                duplicate_checks_performed=0,
            )

        results = store.search_with_scores(candidate_vec, k=self.search_k)

        if not results:
            return DedupResult(
                is_duplicate=False, similarity_score=0.0, threshold_used=self.threshold,
                duplicate_checks_performed=min(self.search_k, store.index.ntotal),
            )

        best_distance, best_match = min(results, key=lambda x: x[0])
        similarity = self._l2_to_cosine(best_distance)
        is_dup = similarity >= self.threshold

        # Soft warning for high domain similarity (not rejection-worthy)
        if 0.85 <= similarity < self.threshold:
            logger.debug(
                f"Dedup: high domain similarity ({similarity:.4f}) but below reject threshold. "
                f"Closest: {best_match.get('hook', 'N/A')[:40]}..."
            )

        logger.info(
            f"Dedup: is_dup={is_dup}, sim={similarity:.4f}, "
            f"threshold={self.threshold}, closest={best_match.get('hook', 'N/A')[:30]}..."
        )

        return DedupResult(
            is_duplicate=is_dup,
            similarity_score=round(similarity, 4),
            closest_match=best_match,
            closest_distance=round(float(best_distance), 4),
            threshold_used=self.threshold,
            duplicate_checks_performed=min(self.search_k, store.index.ntotal),
        )

    @staticmethod
    def _l2_to_cosine(l2_distance: float) -> float:
        cos = 1.0 - (l2_distance ** 2) / 2.0
        return max(0.0, min(1.0, cos))
