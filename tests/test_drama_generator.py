"""Tests for drama generator: JSON extraction and structure validation."""

import pytest

from flowbeast.drama.generator import extract_json, validate_script_structure


class TestExtractJson:
    def test_plain_json(self):
        text = '{"title": "test", "scenes": []}'
        assert extract_json(text) == text

    def test_json_with_surrounding_text(self):
        text = 'Here is the script:\n{"title": "test", "scenes": []}\nDone.'
        assert extract_json(text) == '{"title": "test", "scenes": []}'

    def test_markdown_fenced_json(self):
        text = '```json\n{"title": "test", "scenes": []}\n```'
        assert extract_json(text) == '{"title": "test", "scenes": []}'

    def test_nested_json_preserved(self):
        text = '{"scenes": [{"dialogue": [{"text": "hi"}]}]}'
        result = extract_json(text)
        assert "dialogue" in result

    def test_no_json_raises_error(self):
        with pytest.raises(ValueError, match="未找到JSON结构"):
            extract_json("this is just plain text with no json")


class TestValidateScriptStructure:
    def test_valid_script(self):
        script = {
            "title": "Test",
            "core_hook": "hook",
            "scenes": [
                {"id": 1, "dialogue": [{"speaker": "A", "text": "line"}]},
                {"id": 2, "dialogue": [{"speaker": "B", "text": "line"}]},
                {"id": 3, "dialogue": [{"speaker": "C", "text": "line"}]},
            ],
        }
        assert validate_script_structure(script) == []

    def test_missing_title(self):
        assert "missing title" in validate_script_structure({"scenes": []})

    def test_missing_core_hook(self):
        assert "missing core_hook" in validate_script_structure({"title": "x"})

    def test_too_few_scenes(self):
        script = {"title": "x", "core_hook": "y", "scenes": [{"id": 1, "dialogue": []}]}
        issues = validate_script_structure(script)
        assert any("too few scenes" in i for i in issues)

    def test_empty_dialogue(self):
        script = {
            "title": "x", "core_hook": "y",
            "scenes": [
                {"id": 1, "dialogue": []},
                {"id": 2, "dialogue": [{"speaker": "A", "text": "ok"}]},
                {"id": 3, "dialogue": [{"speaker": "B", "text": "ok"}]},
            ],
        }
        issues = validate_script_structure(script)
        assert any("empty dialogue" in i for i in issues)

    def test_empty_text_in_dialogue(self):
        script = {
            "title": "x", "core_hook": "y",
            "scenes": [
                {"id": 1, "dialogue": [{"speaker": "A", "text": ""}]},
                {"id": 2, "dialogue": [{"speaker": "B", "text": "ok"}]},
                {"id": 3, "dialogue": [{"speaker": "C", "text": "ok"}]},
            ],
        }
        issues = validate_script_structure(script)
        assert any("empty text" in i for i in issues)

    def test_scenes_not_a_list(self):
        script = {"title": "x", "core_hook": "y", "scenes": "not a list"}
        assert "scenes is not a list" in validate_script_structure(script)

    def test_missing_dialogue_list(self):
        script = {
            "title": "x", "core_hook": "y",
            "scenes": [{"id": 1}, {"id": 2}, {"id": 3}],
        }
        issues = validate_script_structure(script)
        assert any("missing dialogue list" in i for i in issues)
