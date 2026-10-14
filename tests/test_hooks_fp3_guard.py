"""Tests for fp3_guard module."""

import pytest
import tempfile
import os
from pathlib import Path

from flowbeast.hooks.fp3_guard import (
    FP3Guard,
    check_fp3_integrity,
    FP3IntegrityViolation,
)


class TestFP3Guard:
    """Test the FP3Guard class."""

    def test_violation_string_format(self):
        """Test FP3IntegrityViolation string representation."""
        v = FP3IntegrityViolation(
            file_path="/path/to/file.py",
            line_no=10,
            issue_type="Missing file",
            description="Required file missing",
            severity="error",
        )
        s = str(v)
        assert "file.py" in s
        assert "10" in s
        assert "error" in s.lower()

    def test_check_all_no_fp3_dir(self):
        """Test checking when FP3 dir doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guard = FP3Guard(Path(tmpdir) / "nonexistent")
            violations = guard.check_all()
            # Should have violations about missing files
            assert len(violations) > 0

    def test_verify_fp3_structure(self):
        """Test FP3 structure verification (v2 upgrade)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # FP3Guard expects a path like ".../flowbeast/fp3"
            # so create the full path structure
            fp3_dir = Path(tmpdir) / "flowbeast" / "fp3"
            fp3_dir.mkdir(parents=True)

            # Create minimal store.py with VectorStore class
            (fp3_dir / "store.py").write_text('''
from flowbeast.core.config import settings

class VectorStore:
    def add(self, data):
        """Add data to store."""
        pass

    def search(self, query):
        """Search for similar items."""
        pass

    def score(self, item):
        """Score an item."""
        pass
''')

            # Create minimal retriever.py
            (fp3_dir / "retriever.py").write_text('''
class Retriever:
    def retrieve(self, query):
        """Retrieve similar items from store."""
        pass
''')

            # Create minimal embedding.py
            (fp3_dir / "embedding.py").write_text('''
def embed(text):
    """Embed text into vector space."""
    pass
''')

            guard = FP3Guard(fp3_dir)
            assert guard.verify_fp3_structure() is True

    def test_check_for_bypass_patterns(self):
        """Test bypass pattern detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp3_dir = Path(tmpdir) / "flowbeast" / "fp3"
            fp3_dir.mkdir(parents=True)

            # Create store.py with bypass comment
            (fp3_dir / "store.py").write_text('''
# quality check disabled - bypass
def score(data):
    return 1.0
''')

            (fp3_dir / "retriever.py").write_text('''
class Retriever:
    def retrieve(self, query):
        pass
''')

            (fp3_dir / "embedding.py").write_text('''
def embed(text):
    return [1.0]
''')

            guard = FP3Guard(fp3_dir)
            violations = guard.check_for_bypass_patterns()

            # Should detect the bypass comment
            assert len(violations) > 0
            assert any("bypass" in v.description.lower() for v in violations)


class TestFP3GuardIntegration:
    """Integration tests for FP3 guard."""

    def test_main_check_function(self):
        """Test the main check_fp3_integrity function."""
        # This should run without errors
        result = check_fp3_integrity()
        assert isinstance(result, int)
