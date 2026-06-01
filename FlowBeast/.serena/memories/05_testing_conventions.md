# Testing Conventions

## Run Tests
```bash
uv run pytest tests/ -q          # all tests
uv run pytest tests/test_graft.py -q  # specific file
```

## Test Structure
- Tests are in `tests/` directory
- One test file per module under test
- Use pytest fixtures for shared setup
- No `sys.path` hacks — `pythonpath = ["."]` in `pyproject.toml`
- `conftest.py` exists only when genuinely needed (project root auto-added by pytest)

## Coverage Philosophy
- Test the critical path: what the user depends on
- Prioritize: feedback_ingest, prompt builder, generator, QualityGate, GRAFT
- Lower priority: Pydantic schemas, trivial getters, config validation
- Don't test what the framework already tests (Pydantic validation, FAISS internals)

## Current Test Files
- `test_fp3_quality.py` — QualityGate scoring, dedup, gate decision, calibration
- `test_main.py` — Entry point logic (import, seeding skip/run, pipeline failure, DramaPipeline guard)
- `test_graft.py` — GRAFT operator (9 tests)
- `test_hooks_fp3_guard.py` — FP3 integrity checks, bypass detection
- `test_hooks_import_checker.py` — Architecture enforcement (config centralization)
- `test_config.py` — Path validation
- `test_drama_generator.py` — extract_json edge cases, validate_script_structure
- `test_drama_prompt.py` — narrative structure, build_prompt rules
- `test_fp3_feedback.py` — extract_unit_from_script

## Evidence Package
- `tests/evidence_package.py` — Script to generate evidence runs for demo validation
- Each evidence run produces: script.json, prompt_package.json, production_report.json, audio

## Test Count: 57 passing (as of 2026-05-31)
