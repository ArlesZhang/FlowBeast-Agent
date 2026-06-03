# Task 003: Implement PARASITE Operator

## Status: ⬜ Not Started
## Priority: 🟡 High (Phase 2, after GRAFT)
## Depends on: `002_graft_operator.md`
## Related: CLAUDE.md VTO section

## Objective

Implement the PARASITE operator: inject a real-time trending event into an existing viral narrative spine, producing content that rides current traffic while maintaining proven structure.

## Definition

```
PARASITE: trend_event → inject(narrative_spine) → new ViralScript
```

## Acceptance Criteria

- [ ] Accept a trending event input (headline/summary string, or structured trend object)
- [ ] Select the best-matching narrative spine from FP3 (by topic/emotion affinity)
- [ ] Generate a script where the trend event is the surface topic but the underlying narrative spine is preserved
- [ ] Output passes `QualityGate`
- [ ] Include a `trend_source` field in output metadata for traceability

## Key Files

- `flowbeast/drama/trending.py` — already fetches Weibo hot search (partially done)
- `flowbeast/drama/generator.py` — already injects trend_context into prompt (partially done)
- `flowbeast/fp3/retriever.py` — retrieve compatible narrative spines
- `flowbeast/fp3/injector.py` — inject trend + spine into prompt

## Design Notes

PARASITE differs from GRAFT: GRAFT swaps topic onto a hook atom; PARASITE wraps a trend event around a full narrative spine (hook + conflict + emotion curve).

**Current state:** `trending.py` fetches Weibo topics and `generator.py` passes them to `build_prompt()`. But this is just "topic suggestion" — not true PARASITE. True PARASITE would:
1. Fetch trend
2. Retrieve a compatible narrative spine from FP3
3. Inject both into the prompt with explicit instructions to wrap the trend around the spine

Trend input sources (future):
- Manual string (MVP)
- Weibo hot search (already implemented in trending.py)
- Google Trends RSS (future)

## Open Questions

- How to measure whether a trend is "compatible" with a given narrative spine?
- Should trend freshness (recency) weight into spine selection?
