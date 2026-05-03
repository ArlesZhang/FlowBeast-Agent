"""
DEPRECATED: This module has moved to flowbeast.legacy_workflows.compiler

For backward compatibility only. Do not import new code from here.
"""
import warnings

warnings.warn(
    "flowbeast.compiler is deprecated. Use flowbeast.legacy_workflows.compiler instead.",
    DeprecationWarning,
    stacklevel=2
)

from flowbeast.legacy_workflows.compiler.core import generate_code, compile_workflow

__all__ = ["generate_code", "compile_workflow"]
