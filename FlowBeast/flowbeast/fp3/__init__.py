"""FP3 — Viral Memory System (RAG memory for FlowBeast)."""

from .schema import (
    ViralUnit,
    ViralScript,
    HookStructure,
    ConflictPattern,
    EmotionalCurve,
    PacingProfile,
    CharacterArchetype,
)
from .prompt_atom import PromptAtom
from .store import FP3Store
from .retriever import FP3Retriever
from .injector import inject_prompt
from .builder import build_fp3
from .feedback import FP3Feedback

__all__ = [
    "ViralUnit", "ViralScript",
    "HookStructure", "ConflictPattern", "EmotionalCurve", "PacingProfile", "CharacterArchetype",
    "PromptAtom",
    "FP3Store", "FP3Retriever", "inject_prompt",
    "build_fp3", "FP3Feedback",
]
