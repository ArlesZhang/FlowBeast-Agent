"""Tests for drama prompt template: build_prompt and 爽文 rules."""

from flowbeast.drama.prompt import build_prompt, NARRATIVE_STRUCTURES


class TestNarrativeStructures:
    def test_has_structures(self):
        assert len(NARRATIVE_STRUCTURES) >= 3

    def test_each_structure_has_required_fields(self):
        for s in NARRATIVE_STRUCTURES:
            assert "name" in s
            assert "pattern" in s
            assert "emotion_global" in s
            assert len(s["emotion_global"]) >= 3

    def test_emotion_curve_ends_on_catharsis(self):
        """All narrative structures must end on a positive emotion."""
        catharsis_words = {"catharsis", "satisfaction", "vindication"}
        for s in NARRATIVE_STRUCTURES:
            last = s["emotion_global"][-1].lower()
            assert any(c in last for c in catharsis_words), (
                f"Structure {s['name']} doesn't end on catharsis: {last}"
            )


class TestBuildPrompt:
    def test_contains_topic(self):
        prompt = build_prompt("程序员被开除后逆袭")
        assert "程序员被开除后逆袭" in prompt

    def test_contains_critical_rules(self):
        prompt = build_prompt("test")
        assert "HOOK" in prompt or "hook" in prompt
        assert "DIALOGUE" in prompt or "dialogue" in prompt
        assert "20" in prompt  # max 20 chars rule
        assert "FACE-SLAP" in prompt or "face-slap" in prompt.lower()

    def test_contains_json_format_instruction(self):
        prompt = build_prompt("test")
        assert "JSON" in prompt
        assert "scenes" in prompt

    def test_trend_context_appended(self):
        prompt = build_prompt("test", trend_context="Trending: AI revolution")
        assert "Trending context" in prompt
        assert "AI revolution" in prompt

    def test_fp3_injected_appended(self):
        prompt = build_prompt("test", fp3_injected="viral pattern: identity reveal")
        assert "Reference viral patterns" in prompt
        assert "identity reveal" in prompt

    def test_random_style_chosen_when_none(self):
        prompt = build_prompt("test", narrative_style=None)
        # Should pick one of the structures
        for s in NARRATIVE_STRUCTURES:
            if s["name"] in prompt:
                break
        else:
            pytest.fail("No narrative structure name found in prompt")

    def test_specific_style_chosen(self):
        prompt = build_prompt("test", narrative_style="classic_reversal")
        assert "classic_reversal" in prompt
