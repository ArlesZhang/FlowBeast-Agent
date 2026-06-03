"""Tests for import_checker module."""

import pytest
import tempfile
import os
from pathlib import Path

from flowbeast.hooks.import_checker import (
    CORE_MODULES,
    check_imports,
    get_module_name,
    check_file_config,
    get_core_modules_without_config,
)


class TestConfigCheck:
    """Test config centralization checks."""

    def test_file_with_config_returns_true(self):
        """Test that a file importing core.config passes."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write("from flowbeast.core.config import settings\n")
            f.flush()
            assert check_file_config(Path(f.name), Path("/")) is True
            os.unlink(f.name)

    def test_file_without_config_returns_false(self):
        """Test that a file without core.config import fails."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write("import os\nimport json\n")
            f.flush()
            assert check_file_config(Path(f.name), Path("/")) is False
            os.unlink(f.name)

    def test_get_module_name(self):
        """Test module name extraction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            abs_path = Path(tmpdir) / "flowbeast" / "fp3" / "store.py"
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            module_name = get_module_name(abs_path, Path(tmpdir))
            assert "flowbeast.fp3.store" in module_name


class TestCoreModulesWithoutConfig:
    """Test finding core modules missing config imports."""

    def test_no_violations_for_clean_fp3(self):
        """Test fp3 module with config import has no violations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp3_dir = Path(tmpdir) / "flowbeast" / "fp3"
            fp3_dir.mkdir(parents=True)
            (fp3_dir / "__init__.py").write_text("")
            (fp3_dir / "store.py").write_text(
                "from flowbeast.core.config import settings\n"
            )
            result = get_core_modules_without_config(fp3_dir)
            assert len(result) == 0


class TestIntegration:
    """Integration tests."""

    def test_check_imports_runs(self):
        """Test that check_imports runs without crashing."""
        result = check_imports()
        assert isinstance(result, int)

    def test_core_modules_constants(self):
        """Test that core module constants are defined."""
        assert len(CORE_MODULES) > 0
        assert "flowbeast.fp3" in CORE_MODULES
        assert "flowbeast.drama" in CORE_MODULES
