# Current Goal: Phase 1 — End-to-End Web Demo

## What "Done" Looks Like

A person opens a browser, types a topic, and sees a complete `prompt_package.json` with scene-by-scene breakdown — all within 60 seconds, no manual steps.

## Success Criteria (must all be true)

- [ ] `POST /v1/generate {"topic": "..."}` returns a valid prompt_package.json
- [ ] Response includes: title, core_hook, scenes[], shot_list[], quality_gate result
- [ ] Frontend shows the output in a human-readable format (not raw JSON)
- [ ] QualityGate score is visible in the response (score + ACCEPT/REVIEW/REJECT)
- [ ] At least 5 successful demo runs recorded in `flowbeast/data/outputs/`

## What This Is NOT

- Not "VTO operators working" — GRAFT/PARASITE are Phase 2
- Not "PromptAtom composition working" — PromptAtom is an unused schema, not a product requirement
- Not "Feedback loop working" — feedback.py exists but the weight-update loop is Phase 3
- Not "AI video generation" — we output prompt_package.json, Seedance/Kling handle video

## Constraints

- No new modules. No new abstractions. Wire what exists.
- `shot_director.py` and `asset_manager.py` are already built. Use them.
- `QualityGate` is already built. Use it.
- `FP3 store + retriever` is already built. Use it.
- The only new code is: `api/main.py` endpoint + minimal HTML frontend.

## Parallel Work: Phase 0 (Viral Corpus Building)

**While Phase 1 engineering is happening, start collecting viral scripts in parallel.**

- **Sprint model:** 2-3 scripts per day × 4 weeks = 30 scripts (Phase 2 entry gate)
- Human watches viral short dramas, fills `raw/NNN_title/` directory
- Agent runs `reverse_engineer.py --dir raw/` to extract ViralScripts
- **Target: 15 scripts by end of Week 2, 30 scripts by end of Week 4**

**🔴 Hard constraint:** No Phase 0 optimization before 30 real samples. Focus on acquisition only.

This does NOT block Phase 1. It prepares for Phase 2.

See: `.ai/tasks/000_viral_corpus_building.md`

## Stop Condition

I can open the browser, type a topic, and see a prompt package. Then I can show it to someone and they understand what FlowBeast does in 30 seconds.
