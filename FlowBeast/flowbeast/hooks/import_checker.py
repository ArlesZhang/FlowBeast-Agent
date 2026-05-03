"""
Import Checker - Enforces architectural boundaries for FlowBeast.

RULE 1: No legacy contamination
- fp3 must NOT import from flowbeast.legacy_workflows.*
- drama must NOT import from flowbeast.legacy_workflows.*
- agent must NOT import from flowbeast.legacy_workflows.* (unless explicitly adapter)

RULE 2: Config centralization
- All modules should use flowbeast.core.config

ADAPTIVE GUARDRAIL v2:
- Uses configurable whitelist system
- Only enforces structural constraints
- Avoids checking implementation details
"""

import ast
from pathlib import Path
from typing import Dict, List, Tuple


# Core modules that are protected from legacy imports
CORE_MODULES = {
    "flowbeast.fp3": "FP3 (viral knowledge base)",
    "flowbeast.drama": "Drama (narrative generation)",
    "flowbeast.agent": "Agent (orchestration)",
    "flowbeast.core": "Core (configuration)",
}

LEGACY_PATH = "flowbeast.legacy_workflows"


# Whitelist system for allowed imports (v2 upgrade)
# Format: {module_prefix: [allowed_legacy_paths]}
# This allows specific modules to import from legacy_workflows as needed
ALLOWED_IMPORTS = {
    # Agent module is allowed to import from legacy_workflows for workflow compilation
    "flowbeast.agent": [
        "flowbeast.legacy_workflows.ir.models",
        "flowbeast.legacy_workflows.ir.*",
        "flowbeast.legacy_workflows.*",
    ],
    # Future modules can be added here as needed
    # "flowbeast.new_module": ["flowbeast.legacy_workflows.adapters.*"],
}


class ImportViolation:
    """Represents an import policy violation."""

    def __init__(self, file_path: str, line_no: int,
                 importer: str, imported: str, rule: str):
        self.file_path = file_path
        self.line_no = line_no
        self.importer = importer
        self.imported = imported
        self.rule = rule

    def __str__(self) -> str:
        return (f"{self.file_path}:{self.line_no}: "
                f"Violation in '{self.importer}' -> '{self.imported}': {self.rule}")


class WhitelistChecker:
    """
    Checks if an import is allowed by the whitelist system.
    """

    def __init__(self, allowed_imports: Dict[str, List[str]] = None):
        self.allowed = allowed_imports or ALLOWED_IMPORTS

    def is_allowed(self, importer: str, imported: str) -> bool:
        """
        Check if the import is allowed by whitelist rules.
        """
        if not importer:
            return False

        # Check if importer has whitelist entries
        for allowed_prefix, allowed_patterns in self.allowed.items():
            if not importer.startswith(allowed_prefix):
                continue

            for pattern in allowed_patterns:
                # Exact match
                if imported == pattern:
                    return True
                # Wildcard match (e.g., flowbeast.legacy_workflows.ir.*)
                if pattern.endswith(".*"):
                    prefix = pattern[:-2]  # Remove ".*"
                    if imported.startswith(prefix + ".") or imported == prefix:
                        return True

        return False


class ImportChecker:
    """Checks Python files for illegal imports."""

    def __init__(self, base_dir: str = None, whitelist: WhitelistChecker = None):
        self.base_dir = Path(base_dir or Path(__file__).parent.parent.parent)
        self.violations: List[ImportViolation] = []
        self.whitelist = whitelist or WhitelistChecker()

    def get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name (e.g., flowbeast.fp3.store)."""
        try:
            rel_path = file_path.relative_to(self.base_dir)
            parts = list(rel_path.parts)
            if parts[-1] == "__init__.py":
                parts = parts[:-1]
            elif parts[-1].endswith(".py"):
                parts[-1] = parts[-1][:-3]
            return ".".join(parts) if parts else ""
        except ValueError:
            return ""

    def check_file(self, file_path: Path) -> List[ImportViolation]:
        """Check a single Python file for import violations."""
        violations = []

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            # Skip files that can't be parsed
            return violations

        module_name = self.get_module_name(file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if self._is_violation(module_name, alias.name):
                        violations.append(ImportViolation(
                            file_path=str(file_path),
                            line_no=node.lineno,
                            importer=module_name,
                            imported=alias.name,
                            rule=f"Cannot import from {LEGACY_PATH} into core module"
                        ))

            elif isinstance(node, ast.ImportFrom):
                if node.module and node.level == 0:  # Absolute import only
                    if self._is_violation(module_name, node.module):
                        violations.append(ImportViolation(
                            file_path=str(file_path),
                            line_no=node.lineno,
                            importer=module_name,
                            imported=node.module,
                            rule=f"Cannot import from {LEGACY_PATH} into core module"
                        ))

        self.violations.extend(violations)
        return violations

    def _is_violation(self, importer: str, imported: str) -> bool:
        """Check if this import violates architectural rules."""
        # Check if importer is a core module
        is_core = any(importer.startswith(core) for core in CORE_MODULES.keys())

        if not is_core:
            return False

        # Check if import is from legacy
        is_legacy = imported.startswith("flowbeast.legacy_workflows")

        if not is_legacy:
            return False

        # Check whitelist
        if self.whitelist.is_allowed(importer, imported):
            return False

        return True

    def check_directory(self, directory: Path) -> List[ImportViolation]:
        """Check all Python files in a directory."""
        violations = []
        for py_file in directory.rglob("*.py"):
            file_violations = self.check_file(py_file)
            violations.extend(file_violations)
        return violations

    def get_core_modules_without_config(self, directory: Path) -> Dict[str, List[str]]:
        """
        Find core modules that don't import from flowbeast.core.config.
        Returns dict of module_name -> list of files in that module.
        """
        modules_without_config: Dict[str, List[str]] = {}

        for py_file in directory.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, UnicodeDecodeError):
                continue

            module_name = self.get_module_name(py_file)

            # Only check core modules
            is_core = any(module_name.startswith(core) for core in CORE_MODULES.keys())
            if not is_core:
                continue

            uses_config = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "flowbeast.core.config":
                            uses_config = True
                            break
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module == "flowbeast.core.config":
                        uses_config = True

            if not uses_config and module_name:
                modules_without_config.setdefault(module_name, []).append(str(py_file))

        return modules_without_config

    def print_violations(self) -> int:
        """Print violations and return count."""
        if not self.violations:
            print("✓ No import violations found")
            return 0

        print("\nImport Violations Found:")
        print("-" * 60)
        for v in self.violations:
            print(f"  {v}")
        print("-" * 60)
        print(f"Total: {len(self.violations)} violation(s)\n")
        return len(self.violations)


def check_imports(base_dir: str = None, whitelist: WhitelistChecker = None) -> int:
    """
    Main entry point for import checking.
    Returns 0 if no violations, 1 if violations found.
    """
    checker = ImportChecker(base_dir, whitelist)
    base = Path(base_dir or checker.base_dir)

    # Check all source directories
    source_dirs = [
        base / "flowbeast" / "fp3",
        base / "flowbeast" / "drama",
        base / "flowbeast" / "agent",
        base / "flowbeast" / "core",
        base / "flowbeast" / "legacy_workflows",
    ]

    for src_dir in source_dirs:
        if src_dir.exists():
            checker.check_directory(src_dir)

    # Also check for core modules missing config import
    modules_without_config = checker.get_core_modules_without_config(base / "flowbeast")

    if modules_without_config:
        print("\nCore modules not using flowbeast.core.config:")
        for module, files in modules_without_config.items():
            print(f"  - {module}:")
            for f in files:
                print(f"      {Path(f).relative_to(base)}")

    return checker.print_violations()


if __name__ == "__main__":
    import sys
    exit_code = check_imports()
    sys.exit(exit_code)
