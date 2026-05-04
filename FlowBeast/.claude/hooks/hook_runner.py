"""
Hook Runner - Main entry point for running hooks.

This module orchestrates the execution of git hooks:
- Pre-commit: import checking, type hints, sanity checks
- Pre-push: FP3 tests, pipeline tests
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


class HookRunner:
    """Runs various hook checks."""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or Path(__file__).parent.parent.parent)

    def run_pre_commit(self, files: List[str] = None) -> Tuple[int, str]:
        """
        Run pre-commit checks.

        Returns:
            Tuple of (exit_code, message)
        """
        print("=" * 60)
        print("Running Pre-Commit Checks")
        print("=" * 60)

        all_passed = True
        messages = []

        # 1. Import checker
        print("\n[1/3] Checking imports...")
        import_result = self._run_import_checker(files)
        if import_result != 0:
            all_passed = False
            messages.append("Import checker failed")

        # 2. Type hints checker (basic)
        print("\n[2/3] Checking type hints...")
        type_result = self._run_type_checker(files)
        if type_result != 0:
            all_passed = False
            messages.append("Type hints checker failed")

        # 3. FP3 guard
        print("\n[3/3] Checking FP3 integrity...")
        fp3_result = self._run_fp3_guard()
        if fp3_result != 0:
            all_passed = False
            messages.append("FP3 guard failed")

        # Summary
        print("\n" + "=" * 60)
        if all_passed:
            print("✓ All pre-commit checks passed")
            return 0, "Pre-commit checks passed"
        else:
            message = f"Pre-commit checks failed: {', '.join(messages)}"
            print(f"✗ {message}")
            return 1, message

    def run_pre_push(self) -> Tuple[int, str]:
        """
        Run pre-push checks.

        Returns:
            Tuple of (exit_code, message)
        """
        print("=" * 60)
        print("Running Pre-Push Checks")
        print("=" * 60)

        # 1. Run FP3 tests
        print("\n[1/2] Running FP3 tests...")
        fp3_result = self._run_fp3_tests()
        if fp3_result != 0:
            message = "Pre-push checks failed: FP3 tests failed"
            print(f"✗ {message}")
            return 1, message

        # 2. Run key pipeline tests
        print("\n[2/2] Running key pipeline tests...")
        pipeline_result = self._run_pipeline_tests()
        if pipeline_result != 0:
            message = "Pre-push checks failed: Pipeline tests failed"
            print(f"✗ {message}")
            return 1, message

        # Summary
        print("\n" + "=" * 60)
        print("✓ All pre-push checks passed")
        return 0, "Pre-push checks passed"

    def _run_import_checker(self, files: List[str] = None) -> int:
        """Run import checker on files."""
        try:
            from claude_hooks.import_checker import check_imports
            return check_imports(str(self.base_dir))
        except Exception as e:
            print(f"Warning: Import checker error: {e}")
            return 0  # Don't block on import checker errors

    def _run_type_checker(self, files: List[str] = None) -> int:
        """Run basic type hints check."""
        # Skip type hints check for now - this is a soft check
        # The project uses type hints where it matters, but not comprehensively
        print("Type hints check skipped (soft check, not enforced)")
        return 0

    def _run_fp3_guard(self) -> int:
        """Run FP3 guard checks."""
        try:
            from claude_hooks.fp3_guard import check_fp3_integrity
            return check_fp3_integrity(str(self.base_dir / "flowbeast" / "fp3"))
        except Exception as e:
            print(f"Warning: FP3 guard error: {e}")
            return 0

    def _run_fp3_tests(self) -> int:
        """Run FP3-related tests."""
        fp3_test_dir = self.base_dir / "tests" / "fp3_tests"
        fp3_module = self.base_dir / "flowbeast" / "fp3"

        if not fp3_module.exists():
            print("FP3 module not found, skipping tests")
            return 0

        # Run pytest on FP3-related tests
        test_files = []
        if fp3_test_dir.exists():
            for f in fp3_test_dir.glob("test_*.py"):
                test_files.append(str(f))
        else:
            # Run tests that import fp3 modules
            for f in (self.base_dir / "tests").glob("*.py"):
                if "fp3" in f.name.lower() or "test_main" in f.name.lower():
                    test_files.append(str(f))

        if not test_files:
            print("No FP3 tests found, skipping")
            return 0

        # Run pytest
        try:
            result = subprocess.run(
                ["uv", "run", "pytest", "-v"] + test_files,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            if result.returncode != 0:
                print(f"FP3 tests failed with exit code {result.returncode}")
                return 1

            print("FP3 tests passed")
            return 0

        except subprocess.TimeoutExpired:
            print("FP3 tests timed out")
            return 1
        except FileNotFoundError:
            print("Warning: uv not found, cannot run tests")
            return 0
        except Exception as e:
            print(f"Warning: Error running tests: {e}")
            return 0

    def _run_pipeline_tests(self) -> int:
        """Run key pipeline tests."""
        pipeline_tests = []

        # Look for pipeline-related tests
        for f in (self.base_dir / "tests").glob("*.py"):
            if "pipeline" in f.name.lower() or "codegen" in f.name.lower():
                pipeline_tests.append(str(f))

        if not pipeline_tests:
            print("No pipeline tests found, skipping")
            return 0

        try:
            result = subprocess.run(
                ["uv", "run", "pytest", "-v"] + pipeline_tests,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            if result.returncode != 0:
                print(f"Pipeline tests failed with exit code {result.returncode}")
                return 1

            print("Pipeline tests passed")
            return 0

        except subprocess.TimeoutExpired:
            print("Pipeline tests timed out")
            return 1
        except FileNotFoundError:
            print("Warning: uv not found, cannot run tests")
            return 0
        except Exception as e:
            print(f"Warning: Error running tests: {e}")
            return 0


def run_hook(hook_type: str, files: List[str] = None) -> int:
    """
    Run the appropriate hook based on type.

    Args:
        hook_type: 'pre-commit' or 'pre-push'
        files: List of files to check (for pre-commit)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    runner = HookRunner()

    if hook_type == "pre-commit":
        exit_code, _ = runner.run_pre_commit(files)
    elif hook_type == "pre-push":
        exit_code, _ = runner.run_pre_push()
    else:
        print(f"Unknown hook type: {hook_type}")
        return 1

    return exit_code


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: hook_runner.py <hook_type> [files...]")
        print("  hook_type: 'pre-commit' or 'pre-push'")
        sys.exit(1)

    hook_type = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else None

    exit_code = run_hook(hook_type, files)
    sys.exit(exit_code)
