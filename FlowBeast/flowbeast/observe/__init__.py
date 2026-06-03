"""
Observe: Observability and feedback layer.

Role: Quality assessment, scoring, dedup, and feedback learning.
Independent of pipeline internals — can be called by any generation system.

Components:
  - quality/ — QualityGate scorer, calibrator, dedup, gate
  - (future) — metrics, tracing, monitoring
"""
