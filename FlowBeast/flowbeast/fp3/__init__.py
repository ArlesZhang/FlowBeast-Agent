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
from .feedback import extract_unit_from_script, extract_viral_script_from_script

__all__ = [
    "ViralUnit", "ViralScript",
    "HookStructure", "ConflictPattern", "EmotionalCurve", "PacingProfile", "CharacterArchetype",
    "PromptAtom",
    "FP3Store", "FP3Retriever", "inject_prompt",
    "build_fp3",
    "extract_unit_from_script", "extract_viral_script_from_script",
]
