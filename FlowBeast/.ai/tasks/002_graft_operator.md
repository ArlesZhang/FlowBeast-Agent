# Task 002: Implement GRAFT Operator

## Status: ⬜ Not Started
## Priority: 🟡 High (Phase 2, after Phase 1 demo works)
## Depends on: `001_demo_ui_endpoint.md`
## Related: `.ai/skills/skill_vto.md` (if it existed — now in CLAUDE.md)

## Objective

Implement the GRAFT transformation operator: preserve a proven viral structure (hook atom) and graft it onto a new topic/context, producing a structurally familiar but semantically novel script.

## Definition

```
GRAFT: viral_A.hook_atom + topic_B.context → new ViralScript
```

## Acceptance Criteria

- [ ] Given a source `ViralScript` with a high-scoring `hook_structure`, extract the hook atom
- [ ] Given a new topic string, generate a script that preserves the source hook's `hook_type` and structural pattern but swaps the semantic domain
- [ ] Output passes `QualityGate` (score >= 0.60, no duplicate match in FP3)
- [ ] The resulting script must NOT be a semantic clone of the source (dedup similarity < threshold)

## Key Files

- `flowbeast/fp3/injector.py` — injection point where GRAFT result enters the prompt
- `flowbeast/fp3/retriever.py` — retrieves source viral atoms
- `flowbeast/drama/generator.py` — LLM call with GRAFT-enriched prompt

## Design Notes

GRAFT is the simplest VTO operator. Start here as the template for all other operators.

The LLM prompt should receive:
1. The source hook atom (structure, type, audience question)
2. The new topic context
3. An explicit instruction to preserve structure but swap domain

**Current state:** `injector.py` appends retrieved examples as reference cases. GRAFT would add an explicit transformation instruction before injection.

## Open Questions

- Should GRAFT be a pre-prompt transformation (modifying atoms before injection) or a prompt instruction (telling the LLM to graft)?
- How to prevent the LLM from ignoring the structural constraint and generating freely?
