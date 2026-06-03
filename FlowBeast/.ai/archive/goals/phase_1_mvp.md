# Phase 1 MVP — Detailed Checklist

## Definition

A working web demo where a user types a topic and receives a complete prompt package — proving FlowBeast is a product, not a research project.

**Important:** This is NOT "just an HTTP endpoint." A demo system includes:
- Backend API (FastAPI endpoint)
- Async/long-running job handling (generation takes 30-60s)
- Status/progress tracking
- Frontend UX (input, loading, results, error states)
- Result display (script, shots, audio player, download)
- Error handling (LLM failures, JSON parse errors, timeouts)
- File serving (audio MP3s, prompt_package.json download)

**Phase 1 = 70% code + 30% productization.**

## Technical Checklist

### Backend (FastAPI)

- [ ] `POST /v1/generate` accepts `{"topic": "..."}`
- [ ] Returns `job_id` immediately (async, don't block for 60s)
- [ ] Background task runs `run_full_pipeline(topic)`
- [ ] `GET /v1/jobs/{job_id}` returns current status + partial results
- [ ] Returns JSON containing:
  - `script` — the generated script (title, core_hook, scenes)
  - `shot_list` — beat_type-driven shot list from `shot_director.py`
  - `prompt_package` — the final compiler output from `asset_manager.py`
  - `quality` — QualityGate score + action (ACCEPT/REVIEW/REJECT)
  - `audio_paths` — list of generated MP3 files
- [ ] Returns proper HTTP error codes (422 for bad input, 500 for pipeline failure)
- [ ] Logs each request with run_id for debugging
- [ ] **Handles LLM failures gracefully** (JSON parse errors, rate limits, empty responses)

### Frontend (minimal HTML/JS)

- [ ] Single page: text input + "Generate" button
- [ ] Shows loading state during generation (can take 30-60s)
- [ ] Polls `/v1/jobs/{job_id}` for status updates
- [ ] Displays output in sections:
  - Script summary (title, genre, core_hook)
  - Scene-by-scene breakdown with dialogue
  - Shot list table (shot_id, beat_type, shot_type, duration)
  - QualityGate result (score bar + action badge)
  - Audio player for episode MP3 (if generated)
- [ ] "Download prompt_package.json" button
- [ ] Error state display (when generation fails)

### Integration Tests

- [ ] 5 successful end-to-end runs with different topics
- [ ] Each run produces: script.json, shot_list.json, prompt_package.json, production_report.json, audio/
- [ ] QualityGate ACCEPT or REVIEW on at least 3 of 5 runs

## What's Explicitly NOT in Phase 1

- No VTO operators (GRAFT/PARASITE) — Phase 2
- No PromptAtom composition engine — architecture mismatch, see `decisions/002_what_we_do_not_do.md`
- No feedback weight updates — Phase 3
- No video generation API calls — out of scope permanently
- No user authentication — demo only
- No database — file system is fine for Phase 1
- **No additional tests** — priority is user-visible output, not coverage

## Estimated Effort

- Backend endpoint + async job handling: 3-4 hours
- Frontend (HTML + JS + polling + error states): 4-6 hours
- Integration testing (5 runs, verify outputs): 2-3 hours
- Polish (loading states, error messages, file serving): 2-3 hours
- **Total: 10-16 hours of focused work**

**Note:** This is a Demo System, not just an API. The UX (waiting, error handling, result display) matters as much as the code.
