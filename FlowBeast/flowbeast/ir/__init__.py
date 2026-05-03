"""
DEPRECATED: This module has moved to flowbeast.legacy_workflows.ir

For backward compatibility only. Do not import new code from here.
"""
import warnings

warnings.warn(
    "flowbeast.ir is deprecated. Use flowbeast.legacy_workflows.ir instead.",
    DeprecationWarning,
    stacklevel=2
)

from flowbeast.legacy_workflows.ir.models import DataWorkflow, WorkflowStep, StepType, ErrorFeedback

__all__ = ["DataWorkflow", "WorkflowStep", "StepType", "ErrorFeedback"]
