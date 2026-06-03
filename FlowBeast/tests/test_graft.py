"""
Tests for the GRAFT v0 operator.

Run: uv run pytest tests/test_graft.py -q
"""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

from flowbeast.vto.graft import (
    graft_operator,
    GRAFTResult,
    _extract_hook_structure,
    _extract_conflict_pattern,
    _build_graft_prompt,
)


class TestGRAFTResult:
    def test_to_dict(self):
        result = GRAFTResult(
            topic="test topic",
            source_viral_script={"source_title": "test"},
            extracted_hook_structure={"hook_type": "冲突爆发"},
            extracted_conflict_pattern={"conflict_type": "权力碾压"},
            graft_prompt="some prompt",
            graft_applied=True,
        )
        d = result.to_dict()
        assert d["topic"] == "test topic"
        assert d["graft_applied"] is True
        assert d["source_viral_script"] == {"source_title": "test"}
        assert d["extracted_hook_structure"]["hook_type"] == "冲突爆发"
        assert "some prompt" in d["graft_prompt_summary"]


class TestExtractHookStructure:
    def test_full_viral_script(self):
        script = {
            "hook_structure": {
                "hook_type": "悬念开场",
                "opening_line": "第一句话",
                "time_to_hook": "immediate",
                "audience_question": "会发生什么？",
                "emotional_payload": "紧张",
            },
            "hook": "fallback hook",
        }
        hs = _extract_hook_structure(script)
        assert hs["hook_type"] == "悬念开场"
        assert hs["opening_line"] == "第一句话"
        assert hs["emotional_payload"] == "紧张"

    def test_minimal_viral_script(self):
        script = {"hook": "simple hook"}
        hs = _extract_hook_structure(script)
        assert hs["hook_type"] == "冲突爆发"  # default
        assert hs["opening_line"] == "simple hook"


class TestExtractConflictPattern:
    def test_full_viral_script(self):
        script = {
            "conflict_pattern": {
                "conflict_type": "身份揭露",
                "escalation_curve": ["压抑", "爆发"],
                "reversal_count": 2,
                "highest_stakes": "生存",
            }
        }
        cp = _extract_conflict_pattern(script)
        assert cp["conflict_type"] == "身份揭露"
        assert cp["reversal_count"] == 2
        assert cp["highest_stakes"] == "生存"

    def test_minimal_viral_script(self):
        script = {}
        cp = _extract_conflict_pattern(script)
        assert cp["conflict_type"] == "权力碾压"  # default
        assert cp["escalation_curve"] == ["压抑", "升级", "爆发", "反转"]


class TestBuildGRAFTPrompt:
    def test_prompt_contains_topic(self):
        prompt = _build_graft_prompt(
            topic="test topic 123",
            hook_structure={"hook_type": "悬念", "emotional_payload": "tension"},
            conflict_pattern={"conflict_type": "power", "escalation_curve": ["A", "B"], "reversal_count": 1, "highest_stakes": "dignity"},
            source_script={"source_title": "source", "hook": "hook text", "pattern": "pattern"},
        )
        assert "test topic 123" in prompt
        assert "悬念" in prompt
        assert "power" in prompt

    def test_prompt_contains_instructions(self):
        prompt = _build_graft_prompt(
            topic="t",
            hook_structure={"hook_type": "ht", "emotional_payload": "ep"},
            conflict_pattern={"conflict_type": "ct", "escalation_curve": ["e"], "reversal_count": 1, "highest_stakes": "hs"},
            source_script={},
        )
        assert "钩子迁移" in prompt
        assert "冲突引擎迁移" in prompt
        assert "情绪载荷保留" in prompt
        assert "反转机制" in prompt
        assert "最高赌注对齐" in prompt


class TestGRAFTOperator:
    def test_no_retrieval_fallback(self):
        """When FP3 retrieval fails, GRAFT returns graft_applied=False."""
        with patch("flowbeast.vto.graft._retrieve_viral_script", return_value=None):
            result = graft_operator("any topic")
        assert result.graft_applied is False
        assert result.source_viral_script is None

    def test_successful_graft(self):
        """When FP3 retrieval succeeds, GRAFT extracts and builds prompt."""
        mock_script = {
            "source_title": "Test Script",
            "source_platform": "test",
            "hook_structure": {
                "hook_type": "悬念开场",
                "opening_line": "test hook",
                "time_to_hook": "immediate",
                "audience_question": "?",
                "emotional_payload": "curiosity",
            },
            "conflict_pattern": {
                "conflict_type": "权力碾压",
                "escalation_curve": ["压抑", "反转"],
                "reversal_count": 1,
                "highest_stakes": "尊严",
            },
            "hook": "test hook",
            "pattern": "test pattern",
            "_similarity": 0.85,
        }
        with patch("flowbeast.vto.graft._retrieve_viral_script", return_value=mock_script):
            result = graft_operator("new topic")

        assert result.graft_applied is True
        assert result.extracted_hook_structure["hook_type"] == "悬念开场"
        assert result.extracted_conflict_pattern["conflict_type"] == "权力碾压"
        assert "new topic" in result.graft_prompt
        assert "悬念开场" in result.graft_prompt
