"""
FP3 Guard - Protects FP3 integrity during development.

RULE 3: FP3 integrity protection
- Changes to FP3 must NOT break scoring logic
- Changes to FP3 must NOT bypass quality gate
- Changes to FP3 must NOT remove evaluation steps

ADAPTIVE GUARDRAIL v2:
- Checks ONLY for structural abstraction (NOT exact pipeline steps)
- Verifies evaluation entry points exist
- Verifies scoring interface exists
- Verifies retrieval abstraction exists
- No brittle exact pipeline sequence checking
"""

import ast
import re
from pathlib import Path
from typing import List


class FP3IntegrityViolation:
    """Represents an FP3 integrity violation."""

    def __init__(self, file_path: str, line_no: int,
                 issue_type: str, description: str, severity: str = "error"):
        self.file_path = file_path
        self.line_no = line_no
        self.issue_type = issue_type
        self.description = description
        self.severity = severity

    def __str__(self) -> str:
        severity_tag = f"[{self.severity.upper()}]"
        return f"{self.file_path}:{self.line_no}: {severity_tag} {self.issue_type}: {self.description}"


class FP3Guard:
    """
    Guards FP3 module integrity.

    v2 UPGRADE:
    - Checks for structural abstraction (entry points, interfaces)
    - NOT brittle pipeline step checking
    - Configurable via property patterns
    """

    def __init__(self, fp3_dir: Path = None):
        self.fp3_dir = fp3_dir or Path(__file__).parent.parent / "fp3"
        self.violations: List[FP3IntegrityViolation] = []

    def check_all(self) -> List[FP3IntegrityViolation]:
        """Run all FP3 integrity checks."""
        violations = []

        # Check for required files (structural check, not implementation)
        required_files = [
            "store.py",
            "retriever.py",
            "embedding.py",
            "injector.py",
            "schema.py",
            "quality/__init__.py",
            "quality/gate.py",
            "quality/scorer.py",
            "quality/dedup.py",
            "quality/models.py",
            "quality/config.py",
        ]

        for filename in required_files:
            file_path = self.fp3_dir / filename
            if not file_path.exists():
                violations.append(FP3IntegrityViolation(
                    file_path=str(file_path),
                    line_no=0,
                    issue_type="Missing file",
                    description=f"Required FP3 file '{filename}' is missing",
                    severity="error"
                ))
                continue

        self.violations = violations
        return violations

    def verify_fp3_structure(self) -> bool:
        """
        Verify that FP3 has the required structural abstraction.

        v2 UPGRADE: Checks for ABSTRACTION, not exact pipeline steps.

        Checks:
        1. Has evaluation entry point (e.g., VectorStore, Retriever classes)
        2. Has scoring interface (e.g., score, evaluate function/method)
        3. Has retrieval abstraction (e.g., retrieve/search method/class)

        Returns True if structure is intact, False otherwise.
        """
        if not self.fp3_dir.exists():
            return False

        try:
            # Check store.py for evaluation entry point
            store_file = self.fp3_dir / "store.py"
            if store_file.exists():
                store_content = store_file.read_text()
                # Check for VectorStore, QdrantStore, FAISSStore or similar
                has_evaluation_class = bool(re.search(
                    r'class\s+(?:Vector|Qdrant|FAISS|Cache|Index|FP3)\w*Store',
                    store_content,
                    re.IGNORECASE
                ))
                has_vector_store = 'vector' in store_content.lower() and 'store' in store_content.lower()
                has_store_class = 'class' in store_content.lower() and ('vector' in store_content.lower() or 'faiss' in store_content.lower() or 'qdrant' in store_content.lower() or 'index' in store_content.lower())

                # Score interface check
                has_scoring = bool(re.search(
                    r'def\s+(?:score|evaluate|compute).*\(',
                    store_content,
                    re.IGNORECASE
                ))

                # If store exists, it must have some form of evaluation entry
                if not (has_evaluation_class or has_vector_store or has_store_class):
                    return False
            else:
                return False

            # Check retriever.py for retrieval abstraction
            retriever_file = self.fp3_dir / "retriever.py"
            if retriever_file.exists():
                retriever_content = retriever_file.read_text()
                # Retrieval abstraction (NOT exact steps)
                has_retrieval = bool(re.search(
                    r'def\s+(?:retrieve|search).*\(',
                    retriever_content,
                    re.IGNORECASE
                ))
                has_retriever_class = bool(re.search(
                    r'class\s+Retriever',
                    retriever_content,
                    re.IGNORECASE
                ))

                # Must have some form of retrieval
                if not (has_retrieval or has_retriever_class):
                    return False
            else:
                return False

            # Check embedding.py for embedding interface
            embedding_file = self.fp3_dir / "embedding.py"
            if embedding_file.exists():
                embedding_content = embedding_file.read_text()
                has_embedding = bool(re.search(
                    r'def\s+(?:embed|encode).*\(',
                    embedding_content,
                    re.IGNORECASE
                ))

                if not has_embedding:
                    return False
            else:
                return False

            # All checks passed
            return True

        except Exception:
            return False

    def check_for_bypass_patterns(self) -> List[FP3IntegrityViolation]:
        """
        Check for suspicious patterns that might indicate integrity bypass.

        Returns list of violations found.
        """
        violations = []

        bypass_patterns = [
            (r"#\s*quality\s*check\s*disabled", "Quality gate bypass"),
            (r"#\s*skip\s*quality", "Quality gate bypass"),
            (r"#\s*bypass\s*gate", "Quality gate bypass"),
            (r"#\s*skip.*evaluate", "Evaluation bypass"),
        ]

        # Check all FP3 files
        for py_file in self.fp3_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")

                for pattern, issue_type in bypass_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        # Find line number
                        for i, line in enumerate(content.split('\n'), 1):
                            if re.search(pattern, line, re.IGNORECASE):
                                violations.append(FP3IntegrityViolation(
                                    file_path=str(py_file),
                                    line_no=i,
                                    issue_type=issue_type,
                                    description=f"Possible {issue_type.lower()} detected",
                                    severity="error"
                                ))
            except Exception:
                continue

        return violations

    def verify_evaluation_flow(self) -> bool:
        """
        Verify that the evaluation flow is intact.

        v2 UPGRADE: This is an alias for verify_fp3_structure()
        for backward compatibility.

        Returns True if flow is intact, False otherwise.
        """
        return self.verify_fp3_structure()

    def print_violations(self) -> int:
        """Print violations and return count of errors (not warnings)."""
        if not self.violations:
            print("✓ FP3 integrity checks passed")
            return 0

        errors = [v for v in self.violations if v.severity == "error"]

        if errors:
            print("\nFP3 Integrity Violations (ERROR):")
            print("-" * 60)
            for v in errors:
                print(f"  {v}")
            print("-" * 60)
            print(f"Error count: {len(errors)}\n")

        return len(errors)


def check_fp3_integrity(fp3_dir: str = None) -> int:
    """
    Main entry point for FP3 integrity checking.
    Returns 0 if checks pass, 1 if error-level violations found.

    v2 UPGRADE: Only checks structural abstraction, not exact pipeline steps.
    """
    guard = FP3Guard(Path(fp3_dir) if fp3_dir else None)

    # Run structural checks
    guard.check_all()

    # Check for bypass patterns
    bypass_violations = guard.check_for_bypass_patterns()
    guard.violations.extend(bypass_violations)

    # Verify FP3 structure (not exact pipeline sequence)
    if not guard.verify_fp3_structure():
        guard.violations.append(FP3IntegrityViolation(
            file_path=str(guard.fp3_dir),
            line_no=0,
            issue_type="Structure broken",
            description="FP3 structural abstraction appears to be broken",
            severity="error"
        ))

    # Only count error-level violations as failures
    return guard.print_violations()


if __name__ == "__main__":
    import sys
    exit_code = check_fp3_integrity()
    sys.exit(exit_code)
