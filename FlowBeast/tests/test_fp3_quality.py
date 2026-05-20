import asyncio
import json
import pytest

from flowbeast.fp3.quality.models import (
    GateAction, ScoreResult, DedupResult, GateDecision,
)
from flowbeast.fp3.quality.config import quality_settings
from flowbeast.fp3.quality.scorer import RuleBasedScorer
from flowbeast.fp3.quality.dedup import EmbeddingDeduplicator
from flowbeast.fp3.quality.gate import QualityGate
from flowbeast.fp3.quality import create_quality_gate
from flowbeast.fp3.schema import ViralUnit
from flowbeast.fp3.store import FP3Store


def _run(coro):
    return asyncio.run(coro)


# --- Fixtures ---

@pytest.fixture
def sample_viral_unit():
    return ViralUnit(
        hook="她被开除后，前东家求她回去救命",
        pattern="身份反转",
        emotion=["satisfaction", "shock", "tension"],
    )


@pytest.fixture
def weak_viral_unit():
    return ViralUnit(
        hook="一个普通的故事",
        pattern="通用",
        emotion=["neutral"],
    )


@pytest.fixture
def scorer():
    return RuleBasedScorer(weights=quality_settings.weights_dict)


@pytest.fixture
def fp3_store(tmp_path, monkeypatch):
    index_p = tmp_path / "fp3.index"
    meta_p = tmp_path / "fp3_meta.json"
    monkeypatch.setattr("flowbeast.core.config.settings.FP3_INDEX_PATH", index_p)
    monkeypatch.setattr("flowbeast.core.config.settings.FP3_META_PATH", meta_p)
    return FP3Store()


# --- Tests: Models ---

class TestModels:
    def test_gate_action_values(self):
        assert GateAction.ACCEPT.value == "accept"
        assert GateAction.REJECT.value == "reject"
        assert GateAction.REVIEW.value == "review"

    def test_score_result_validation(self):
        sr = ScoreResult(
            category_scores={"hook_strength": 0.7},
            weighted_total=0.7,
            explanations={"hook_strength": "test"},
        )
        assert sr.weighted_total == 0.7

    def test_gate_decision_serializes(self, sample_viral_unit, scorer):
        score = _run(scorer.score(sample_viral_unit))
        gd = GateDecision(
            candidate_hook=sample_viral_unit.hook[:80],
            action=GateAction.ACCEPT,
            score_result=score,
            dedup_result=DedupResult(is_duplicate=False, similarity_score=0.0, threshold_used=0.85),
            reason="test",
        )
        dumped = gd.model_dump(mode="json")
        assert dumped["action"] == "accept"
        assert "score_result" in dumped


# --- Tests: RuleBasedScorer ---

class TestRuleBasedScorer:
    def test_score_strong_unit(self, scorer, sample_viral_unit):
        result = _run(scorer.score(sample_viral_unit))
        assert 0.0 <= result.weighted_total <= 1.0
        assert result.category_scores, "Should have category scores"
        assert all(0.0 <= v <= 1.0 for v in result.category_scores.values())
        assert result.explanations, "Should have explanations"

    def test_score_weak_unit(self, scorer, weak_viral_unit):
        result = _run(scorer.score(weak_viral_unit))
        assert 0.0 <= result.weighted_total <= 1.0
        strong = ViralUnit(
            hook="她被开除后，前东家求她回去救命",
            pattern="身份反转", emotion=["satisfaction", "shock", "tension"],
        )
        strong_result = _run(scorer.score(strong))
        assert result.weighted_total < strong_result.weighted_total

    def test_score_empty_hook(self, scorer):
        unit = ViralUnit(hook="", pattern="", emotion=[])
        result = _run(scorer.score(unit))
        assert result.category_scores["hook_strength"] == 0.0


# --- Tests: EmbeddingDeduplicator ---

class TestEmbeddingDeduplicator:
    def test_l2_to_cosine_math(self):
        assert EmbeddingDeduplicator._l2_to_cosine(0.0) == 1.0
        assert EmbeddingDeduplicator._l2_to_cosine(2.0) == 0.0
        assert EmbeddingDeduplicator._l2_to_cosine(1.0) == pytest.approx(0.5)

    def test_empty_store_no_duplicate(self, fp3_store):
        dedup = EmbeddingDeduplicator(similarity_threshold=0.85)
        unit = ViralUnit(hook="test", pattern="test", emotion=["neutral"])
        result = _run(dedup.check_duplicate(unit, fp3_store))
        assert not result.is_duplicate
        assert result.similarity_score == 0.0


# --- Tests: QualityGate ---

class TestQualityGate:
    def _make_gate(self, store, accept=0.60, review=0.40, enabled=True, audit_dir=None):
        scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
        dedup = EmbeddingDeduplicator(similarity_threshold=0.85, search_k=5)
        return QualityGate(
            scorer=scorer, deduplicator=dedup, store=store,
            accept_threshold=accept, review_threshold=review, enabled=enabled,
            audit_dir=audit_dir,
        )

    def test_disabled_gate_always_accepts(self, fp3_store):
        gate = self._make_gate(fp3_store, enabled=False)
        unit = ViralUnit(hook="test", pattern="test", emotion=[])
        decision = _run(gate.evaluate(unit))
        assert decision.action == GateAction.ACCEPT

    def test_low_score_rejected(self, fp3_store):
        gate = self._make_gate(fp3_store, accept=0.99, review=0.99)
        unit = ViralUnit(hook="一个普通的故事", pattern="通用", emotion=["neutral"])
        decision = _run(gate.evaluate(unit))
        assert decision.action == GateAction.REJECT

    def test_audit_file_written(self, fp3_store, tmp_path):
        audit_dir = tmp_path / "audit"
        gate = self._make_gate(fp3_store, audit_dir=audit_dir)
        unit = ViralUnit(hook="她被开除后，前东家求她回去救命", pattern="身份反转", emotion=["satisfaction"])
        _run(gate.evaluate(unit))
        files = list(audit_dir.glob("*.json"))
        assert len(files) >= 1, "Audit file should be written"
        data = json.loads(files[0].read_text())
        assert "candidate" in data
        assert "decision" in data
