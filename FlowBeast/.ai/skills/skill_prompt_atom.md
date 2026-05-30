# Skill: PromptAtom — Composable Prompt Fragments

## Purpose
PromptAtom is the basic unit of the Viral Prompt Compiler. Each atom is one independently embeddable, searchable, and composable piece of a viral content prompt — analogous to an AST node in a compiler.

## Schema

```python
class PromptAtom(BaseModel):
    atom_id: str                    # e.g. "hook_suspense_001", "style_dark_fantasy"
    prompt_fragment: str            # Actual English prompt text for AI video tools
    layer: str                      # "narrative" | "visual" | "camera" | "audio"
    role: str                       # "hook", "style_lock", "shot_suffix", etc.
    embedding: Optional[List[float]]
    vto_metadata: dict              # {"graft_compatible": True, ...}
    source: str                     # "seed_data" | "reverse_engineered" | "generated"
    version: int
    tags: List[str]
```

## Layers and Roles

| Layer | Example Roles | Example atom_id |
|-------|--------------|-----------------|
| `narrative` | hook, conflict_kernel, character_slot, emotion_track | `hook_suspense_001` |
| `visual` | style_lock, character_design, scene_composition | `style_dark_fantasy` |
| `camera` | shot_type, angle, movement | `shot_closeup_dramatic` |
| `audio` | voice_profile, bgm_curve, sfx | `voice_male_tense` |

## Key Files
- `flowbeast/fp3/prompt_atom.py` — model definition
- `flowbeast/fp3/seed_data.py` — seeds initial atoms into FP3
- `flowbeast/fp3/store.py` — FAISS-backed vector storage for atoms
- `flowbeast/fp3/retriever.py` — k-nearest-neighbor search by embedding
- `flowbeast/fp3/embedding.py` — text → vector via cloud API (gemini/openai/qwen/ollama)

## Workflow
```
seed_data.py / reverse_engineer.py
    → PromptAtom → embed_prompt_atom() → store.add() → FAISS index
    → retriever.search(query_embedding) → List[PromptAtom]
    → compose into prompt_package.json
```

## Composition Rules
Atoms from different layers compose orthogonally:
```
narrative(hook + conflict + emotion) × visual(style + character) × camera(shot) × audio(voice + bgm)
= complete prompt_package.json
```
Atoms within the same layer may conflict (e.g., two hooks) — the `vto_metadata` dict tracks compatibility flags.
