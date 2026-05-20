You are working inside the FlowBeast monorepo.

## 🎯 Goal

Implement a Hooks system that enforces architectural integrity and protects the FP3/IP2 core system during development.

This is NOT a generic linting system.

This is a SYSTEM GUARDRAIL layer.

---

## 🧠 Project Context (CRITICAL)

FlowBeast architecture:

CORE:
- flowbeast/fp3/       → viral knowledge base (FP3)
- flowbeast/drama/     → narrative generation (IP2)
- flowbeast/agent/     → orchestration (IP1)
- flowbeast/core/      → config

LEGACY (ISOLATED):
- flowbeast/legacy_workflows/*

---

## 🚨 HARD RULES (MUST ENFORCE)

### RULE 1 — No legacy contamination

The following MUST NEVER happen:

- fp3 imports anything from:
  flowbeast.legacy_workflows.*

- drama imports anything from:
  flowbeast.legacy_workflows.*

- agent imports legacy unless explicitly marked as adapter

---

### RULE 2 — Config centralization

All modules must use:

- flowbeast.core.config

NO direct env parsing or scattered config logic.

---

### RULE 3 — FP3 integrity protection

Changes to FP3 must NOT:

- break scoring logic
- bypass quality gate
- remove evaluation steps

---

## 🎯 Your Task

Design and implement a Hooks system with the following capabilities:

---

### 1. Pre-commit Hook (MANDATORY)

Checks:

- illegal imports (core → legacy)
- missing type hints (basic level)
- file-level sanity checks

---

### 2. Pre-push Hook (MANDATORY)

Runs:

- FP3 tests
- key pipeline tests

Fails if:

- any FP3-related test fails

---

### 3. Optional: Code Pattern Checker

Detect:

- overly long functions (>100 lines)
- missing docstrings in core modules
- suspicious logic in fp3 scoring

---

## 🧩 Implementation Requirements

- Use Python (no external heavy frameworks)
- Simple and maintainable
- Hook scripts should live in:

  /flowbeast/hooks/

- Provide:

  - hook_runner.py
  - import_checker.py
  - fp3_guard.py

---

## 📦 Output Required

1. Hook system architecture
2. Python implementation (minimal but working)
3. Example pre-commit and pre-push integration
4. Clear instructions on how to enable hooks locally

---

## ⚠️ Constraints

- DO NOT over-engineer
- DO NOT introduce complex frameworks
- Focus on reliability and clarity

---

## 🎯 Final Goal

The Hooks system must act as:

👉 "Architectural Firewall for FlowBeast"

preventing accidental system degradation during rapid development.
