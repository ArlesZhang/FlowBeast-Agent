"""
FP3 Retriever: RAG retrieval interface for the drama generation pipeline.

Role: Embeds a query topic, searches the FAISS index, returns top-k ranked
ViralUnit/ViralScript examples as dicts. Boosts atoms with proven real-world
performance via feedback data. Called inside generator.py before the LLM
prompt is assembled.

This is the read path of the FP3 knowledge base.
"""

from .embedding import embed_text
from .store import FP3Store


class FP3Retriever:
    def __init__(self):
        self.store = FP3Store()

    def retrieve(self, query: str, k=2, use_feedback_boost: bool = True):
        vec = embed_text(query)
        # Get more candidates than needed so we can re-rank
        candidates = self.store.search_with_scores(vec, k=min(k * 3, 10))

        if not candidates:
            return []

        results = []
        for dist, meta in candidates:
            hook = meta.get("hook", "")
            feedback_boost = self._get_feedback_score(hook) if use_feedback_boost else 0

            # Combined score: similarity (higher dist = worse) + feedback
            # Normalize: L2 distance 0-2 -> 0-1 similarity; feedback 0-100 -> 0-1
            sim_score = max(0, 1 - dist / 2)
            combined = sim_score * 0.7 + feedback_boost * 0.3

            results.append({
                **meta,
                "_similarity": round(sim_score, 4),
                "_feedback_score": round(feedback_boost, 4),
                "_combined_score": round(combined, 4),
            })

        # Sort by combined score, return top-k
        results.sort(key=lambda x: x["_combined_score"], reverse=True)
        return results[:k]

    @staticmethod
    def _get_feedback_score(hook: str) -> float:
        """
        Look up the mean virality score for a hook from feedback data.
        Returns 0.0-1.0 normalized score.
        """
        from .feedback_ingest import get_atom_effectiveness

        effectiveness = get_atom_effectiveness(hook)
        run_count = effectiveness.get("run_count", 0)

        if run_count == 0:
            return 0.5  # neutral — no data, don't penalize

        # Normalize virality (0-100) to 0-1
        mean_virality = effectiveness.get("mean_virality", 0)
        return min(mean_virality / 100, 1.0)
