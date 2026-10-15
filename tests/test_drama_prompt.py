"""Tests for drama prompt template: build_prompt and 爽文 rules."""

from flowbeast.drama.prompt import build_prompt, NARRATIVE_STRUCTURES


class TestNarrativeStructures:
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
        assert any(s["name"] in prompt for s in NARRATIVE_STRUCTURES), (
            "no narrative structure name found in prompt"
        )

    def test_specific_style_chosen(self):
        prompt = build_prompt("test", narrative_style="classic_reversal")
        assert "classic_reversal" in prompt
