"""
QualityGate: accept/review/reject decisions for viral content.

Role: Orchestrates scoring (RuleBased or ReferenceAnchored), deduplication,
and audit logging. Returns GateDecision with score, action, and reason.
Three actions: ACCEPT (>= accept_threshold), REVIEW (>= review_threshold),
REJECT (below review_threshold).

Called in pipeline.py (_run_output_quality_gate) and feedback.py.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger

from .models import GateAction, GateDecision
from .scorer import BaseScorer
from .dedup import BaseDeduplicator
from ..schema import ViralUnit
from ..store import FP3Store
from ..builder import build_fp3


class QualityGate:
    """
    FP3 Quality Gate: score -> dedup -> gate -> audit pipeline.

    Dependency-injected: scorer and deduplicator are interfaces.
    """

    def __init__(
        self,
        scorer: BaseScorer,
        deduplicator: BaseDeduplicator,
        store: FP3Store,
        accept_threshold: float = 0.60,
        review_threshold: float = 0.40,
        audit_dir: Optional[Path] = None,
        enabled: bool = True,
    ):
        self.scorer = scorer
        self.deduplicator = deduplicator
        self.store = store
        self.accept_threshold = accept_threshold
        self.review_threshold = review_threshold
        self.enabled = enabled

        self.audit_dir = audit_dir or Path("flowbeast/data/quality_audit")
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            f"QualityGate initialized: enabled={enabled}, "
            f"accept={accept_threshold}, review={review_threshold}"
        )

    async def evaluate(self, unit: ViralUnit) -> GateDecision:
        hook_preview = unit.hook[:80]

        if not self.enabled:
            logger.info(f"QualityGate disabled, auto-accepting: [{hook_preview}]")
            return self._make_bypass_decision(unit)

        logger.info(f"QualityGate evaluating: [{hook_preview}]")

        # --- Stage 1: Score ---
        try:
            score_result = await self.scorer.score(unit)
        except Exception as exc:
            logger.error(f"Scoring failed for [{hook_preview}]: {exc}")
            from .models import ScoreResult, DedupResult
            return GateDecision(
                candidate_hook=hook_preview, action=GateAction.REVIEW,
                score_result=ScoreResult(
                    category_scores={}, weighted_total=0.0,
                    explanations={"error": str(exc)}, scorer_version="error",
                ),
                dedup_result=DedupResult(is_duplicate=False, similarity_score=0.0, threshold_used=0.0),
                reason=f"Scoring engine error: {exc}",
                audit_trail={"stage": "scoring", "error": str(exc)},
            )

        # --- Stage 2: Dedup ---
        try:
            dedup_result = await self.deduplicator.check_duplicate(unit, self.store)
        except Exception as exc:
            logger.error(f"Dedup failed for [{hook_preview}]: {exc}")
            from .models import DedupResult
            dedup_result = DedupResult(
                is_duplicate=False, similarity_score=0.0,
                threshold_used=getattr(self.deduplicator, "threshold", 0.0),
            )

        # --- Stage 3: Gate ---
        decision = self._apply_gate_rules(unit, score_result, dedup_result)

        # --- Stage 4: Audit ---
        self._write_audit_log(unit, decision)

        level = "SUCCESS" if decision.action == GateAction.ACCEPT else "WARNING"
        logger.log(
            level,
            f"QualityGate: {decision.action.value.upper()} [{hook_preview}] "
            f"(score={score_result.weighted_total:.3f}, dup={dedup_result.is_duplicate}) "
            f"reason: {decision.reason}"
        )

        return decision

    def store_unit(self, unit: ViralUnit) -> None:
        logger.info(f"Storing accepted unit to FP3: [{unit.hook[:60]}]")
        build_fp3([unit])

    async def evaluate_and_store(self, unit: ViralUnit) -> GateDecision:
        """Evaluate and auto-store if ACCEPT."""
        decision = await self.evaluate(unit)
        if decision.action == GateAction.ACCEPT:
            self.store_unit(unit)
        return decision

    # -- Private --

    def _apply_gate_rules(self, unit: ViralUnit, score_result, dedup_result) -> GateDecision:
        hook_preview = unit.hook[:80]

        if dedup_result.is_duplicate:
            closest = dedup_result.closest_match or {}
            return GateDecision(
                candidate_hook=hook_preview, action=GateAction.REJECT,
                score_result=score_result, dedup_result=dedup_result,
                reason=(
                    f"Duplicate: sim={dedup_result.similarity_score:.3f} "
                    f">= {dedup_result.threshold_used}. "
                    f"Closest: {closest.get('hook', 'N/A')[:50]}"
                ),
                audit_trail={"rule": "duplicate_reject"},
            )

        if score_result.weighted_total >= self.accept_threshold:
            return GateDecision(
                candidate_hook=hook_preview, action=GateAction.ACCEPT,
                score_result=score_result, dedup_result=dedup_result,
                reason=f"Score {score_result.weighted_total:.3f} >= {self.accept_threshold}",
                audit_trail={"rule": "score_accept"},
            )

        if score_result.weighted_total >= self.review_threshold:
            return GateDecision(
                candidate_hook=hook_preview, action=GateAction.REVIEW,
                score_result=score_result, dedup_result=dedup_result,
                reason=f"Score {score_result.weighted_total:.3f} in review zone",
                audit_trail={"rule": "score_review"},
            )

        return GateDecision(
            candidate_hook=hook_preview, action=GateAction.REJECT,
            score_result=score_result, dedup_result=dedup_result,
            reason=f"Score {score_result.weighted_total:.3f} < {self.review_threshold}",
            audit_trail={"rule": "score_reject"},
        )

    def _write_audit_log(self, unit: ViralUnit, decision: GateDecision) -> None:
        from datetime import timezone
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        safe_hook = "".join(c if c.isalnum() else "_" for c in unit.hook[:30])
        filename = self.audit_dir / f"{timestamp}_{safe_hook}_{decision.action.value}.json"

        audit_record = {
            "timestamp": decision.timestamp.isoformat(),
            "candidate": unit.model_dump(),
            "decision": decision.model_dump(mode="json"),
        }

        try:
            filename.write_text(json.dumps(audit_record, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.error(f"Failed to write audit log {filename}: {exc}")

    def _make_bypass_decision(self, unit: ViralUnit) -> GateDecision:
        from .models import ScoreResult, DedupResult
        return GateDecision(
            candidate_hook=unit.hook[:80], action=GateAction.ACCEPT,
            score_result=ScoreResult(
                category_scores={}, weighted_total=1.0,
                explanations={"bypass": "quality_gate_disabled"}, scorer_version="bypass",
            ),
            dedup_result=DedupResult(is_duplicate=False, similarity_score=0.0, threshold_used=0.0),
            reason="Quality gate is disabled",
            audit_trail={"bypass": True},
        )
