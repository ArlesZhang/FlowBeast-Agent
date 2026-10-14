#!/usr/bin/env python3
"""Validate FlowBeast configuration paths and settings."""

from flowbeast.core.config import (
    settings,
    FP3_INDEX_PATH,
    FP3_META_PATH,
    OUTPUTS_DIR,
    VECTOR_STORE_PATH,
)


def test_fp3_paths_are_path_objects():
    assert hasattr(FP3_INDEX_PATH, "parent")
    assert hasattr(FP3_META_PATH, "parent")


def test_fp3_index_parent_exists():
    assert FP3_INDEX_PATH.parent.exists()


def test_settings_has_required_attributes():
    assert hasattr(settings, "FLOWBEAST_OUTPUT_DIR")
    assert hasattr(settings, "MODEL_PROVIDER")
