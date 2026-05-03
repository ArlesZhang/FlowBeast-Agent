You are working inside the FlowBeast monorepo.

## 🎯 Context

The Hooks system has already been implemented and is functional.

Current state:
- flowbeast/hooks/ exists with:
  - import_checker.py
  - fp3_guard.py
  - hook_runner.py
- Git hooks (pre-commit, pre-push) are active
- All tests pass
- Core architecture is already aligned:
  - fp3 / drama / agent / core are CORE
  - legacy_workflows is isolated

---

## 🚨 Your Task

Refactor and upgrade the existing Hooks system into an:

👉 **Adaptive Guardrail System (v2)**

WITHOUT breaking existing functionality.

---

## ⚠️ HARD CONSTRAINTS (MUST FOLLOW)

- DO NOT modify FP3 logic
- DO NOT break existing tests
- DO NOT change module structure
- DO NOT remove existing hooks
- DO NOT introduce heavy dependencies
- DO NOT re-run architectural refactoring

---

## 🎯 UPGRADE GOALS

### 1. Make Hooks EVOLVABLE (CRITICAL)

Current problem:
- Hooks are too rigid and may block future development

You must:

- Convert hard-coded rules into configurable policies
- Avoid checking implementation details
- Only enforce structural constraints

---

## 🧩 REQUIRED CHANGES

### ✅ 1. FP3 Guard Refactor (VERY IMPORTANT)

Current issue:
- fp3_guard checks specific pipeline steps (embedding → index → search → retrieve)

This is too brittle.

---

### 🔥 Replace with:

Check ONLY:

- existence of evaluation entry points
- presence of scoring interface / function
- presence of retrieval abstraction (NOT exact steps)

DO NOT enforce exact pipeline sequence.

---

### ✅ 2. Import Checker → Add Whitelist System

Current issue:
- rules are too strict

---

### 🔥 Implement:

A whitelist-based override system:

Example:

```python
ALLOWED_IMPORTS = {
    "flowbeast.fp3": [
        "flowbeast.legacy_workflows.adapters.*"
    ]
}
