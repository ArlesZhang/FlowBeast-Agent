# 0002 - Unified Embedding Interface

Date: 2026-04-29

## Status

Proposed

## Context

Current embedding implementation has vendor-specific code duplication.

## Decision

Create unified `EmbeddingClient` interface.

## Consequences

- Single responsibility
- Easier testing
- Better extensibility
