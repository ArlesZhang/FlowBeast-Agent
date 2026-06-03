"""
Import Checker - Enforces architectural boundaries for FlowBeast.

RULE: Config centralization — all core modules should use flowbeast.core.config.
"""

import ast
from pathlib import Path
from typing import Dict, List


# Core modules to check
CORE_MODULES = {
    "flowbeast.fp3": "FP3 (viral memory system)",
    "flowbeast.drama": "Drama (narrative generation)",
    "flowbeast.core": "Core (configuration)",
}


def get_module_name(file_path: Path, base_dir: Path) -> str:
    """Convert file path to module name (e.g., flowbeast.fp3.store)."""
    try:
        rel_path = file_path.relative_to(base_dir)
        parts = list(rel_path.parts)
        if parts[-1] == "__init__.py":
            parts = parts[:-1]
        elif parts[-1].endswith(".py"):
            parts[-1] = parts[-1][:-3]
        return ".".join(parts) if parts else ""
    except ValueError:
        return ""


def check_file_config(file_path: Path, base_dir: Path) -> bool:
    """Check if a file imports from flowbeast.core.config. Returns True if it does."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return True  # Skip unparseable files

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "flowbeast.core.config":
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "flowbeast.core.config":
                return True
    return False


def get_core_modules_without_config(directory: Path) -> Dict[str, List[str]]:
    """Find core modules that don't import from flowbeast.core.config."""
    modules_without_config: Dict[str, List[str]] = {}

    for py_file in directory.rglob("*.py"):
        module_name = get_module_name(py_file, directory)

        is_core = any(module_name.startswith(core) for core in CORE_MODULES.keys())
        if not is_core:
            continue

        if not check_file_config(py_file, directory):
            modules_without_config.setdefault(module_name, []).append(str(py_file))

    return modules_without_config


def check_imports(base_dir: str = None) -> int:
    """
    Main entry point. Checks core modules for config usage.
    Returns 0 if clean, 1 if issues found.
    """
    base = Path(base_dir or Path(__file__).parent.parent.parent)

    source_dirs = [
        base / "flowbeast" / "fp3",
        base / "flowbeast" / "drama",
        base / "flowbeast" / "core",
    ]

    modules_without_config: Dict[str, List[str]] = {}
    for src_dir in source_dirs:
        if src_dir.exists():
            result = get_core_modules_without_config(src_dir)
            modules_without_config.update(result)

    if modules_without_config:
        print("\nCore modules not using flowbeast.core.config:")
        for module, files in modules_without_config.items():
            print(f"  - {module}:")
            for f in files:
                print(f"      {Path(f).relative_to(base)}")
        return 1

    print("✓ No import violations found")
    return 0


if __name__ == "__main__":
    import sys
    exit_code = check_imports()
    sys.exit(exit_code)
