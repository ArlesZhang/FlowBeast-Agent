"""
Legacy Workflows - Former NL-to-IR-to-Pandas Pipeline

This package contains the old orthogonal workflow compilation system.
It is kept for backward compatibility but is NOT part of FlowBeast's
core content generation architecture.

DO NOT USE FOR NEW FEATURES - use flowbeast/fp3/ and flowbeast/drama/ instead.
"""

# Keep original imports for backward compatibility
from flowbeast.legacy_workflows.ir.models import DataWorkflow, WorkflowStep, StepType, ErrorFeedback
from flowbeast.legacy_workflows.compiler.core import compile_workflow
from flowbeast.legacy_workflows.codegen.pandas_generator import PandasCodeGenerator
from flowbeast.legacy_workflows.execution.runner import PipelineRunner

__all__ = [
    "DataWorkflow",
    "WorkflowStep", 
    "StepType",
    "ErrorFeedback",
    "compile_workflow",
    "PandasCodeGenerator",
    "PipelineRunner",
]
