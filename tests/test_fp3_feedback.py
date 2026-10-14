"""Tests for FP3 feedback extraction: convert generated script JSON into ViralUnit."""

from flowbeast.fp3.feedback import extract_unit_from_script
from flowbeast.fp3.schema import ViralUnit


class TestExtractUnitFromScript:
    def test_basic_extraction(self):
        script_data = {
            "script": {
                "core_hook": "她被开除后，前东家求她回去救命",
                "genre": "revenge",
                "tags": ["face-slap", "identity-reveal"],
                "emotion_curve_global": ["suppression", "shock", "catharsis"],
            }
        }
        unit = extract_unit_from_script(script_data)
        assert isinstance(unit, ViralUnit)
        assert "她被开除后" in unit.hook
        assert "revenge" in unit.pattern
        assert "face-slap" in unit.pattern

    def test_missing_core_hook_falls_back_to_title(self):
        script_data = {
            "script": {
                "title": "fallback title",
                "genre": "generic",
                "tags": ["unknown"],
                "emotion_curve_global": ["neutral"],
            }
        }
        unit = extract_unit_from_script(script_data)
        assert unit.hook == "fallback title"

    def test_missing_tags_defaults_to_unknown(self):
        script_data = {
            "script": {
                "core_hook": "hook without tags",
                "genre": "drama",
                "emotion_curve_global": ["neutral"],
            }
        }
        unit = extract_unit_from_script(script_data)
        assert "unknown" in unit.pattern

    def test_empty_script_defaults(self):
        unit = extract_unit_from_script({})
        assert unit.hook == "unnamed"
        assert unit.pattern == "generic | unknown"
