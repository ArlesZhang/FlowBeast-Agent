"""
FP3 PromptAtom: composable prompt fragment — one atomic piece of viral content prompt.

Role: The basic unit of the Viral Prompt Compiler. Each atom is independently
embeddable, searchable in FP3, and directly consumable by AI video tools.

Workflow: seed_data.py → PromptAtom → embed_prompt_atom() → store.add()
          retriever.py → search() → PromptAtom.from_dict() → assemble into prompt package
"""

from typing import List, Optional

from pydantic import BaseModel


class PromptAtom(BaseModel):
    """
    A composable prompt fragment — one atomic piece of viral content prompt.

    Analogy: PromptAtom ≈ AST node in a compiler. It represents one
    lexical unit of the viral content language.
    """

    atom_id: str                           # "hook_suspense_001", "style_dark_fantasy"
    prompt_fragment: str                   # Actual English prompt text
    layer: str                             # "narrative" | "visual" | "camera" | "audio"
    role: str                              # "hook", "style_lock", "shot_suffix", etc.
    embedding: Optional[List[float]] = None
    vto_metadata: dict = {}                # {"graft_compatible": True, ...}
    source: str = ""                       # "seed_data", "reverse_engineered", "generated"
    version: int = 1
    tags: List[str] = []

    def to_prompt_text(self) -> str:
        """Return the raw prompt fragment for direct use in AI video tools."""
        return self.prompt_fragment

    @classmethod
    def from_dict(cls, d: dict) -> "PromptAtom":
        """Deserialize from FP3 store metadata."""
        return cls(**d)
