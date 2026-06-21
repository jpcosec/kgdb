---
id: task-implement-minimal-ingest-api
status: draft
references: []
depends_on: ["task-define-persistence-model"]
pills:
- pill-substrate-is-dumb
- pill-snapshot-is-the-public-output-surface
- pill-backward-compatible-degradation-findings-not-failures
files: []
tags:
- workspace:desk
- artifact:task
---

# Implement minimal ingest API

## Rationale
Without an ingest API path, the IO and persistence contracts are theoretical.

## Goal
Python API accepts a structured payload, validates against the IO contract, produces a GraphSnapshot, and persists a TransactionManifest.

## Scope
Python API only. No CLI yet. Inputs: structured dictionaries.

## Implementation Path
Add src/kgdb/ingest/ module logic.

## Validation
- pytest tests/test_ingest_api.py

## Done When
Python API can successfully write a GraphSnapshot matching the IO contract.
