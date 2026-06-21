---
id: task-implement-minimal-query-api
status: draft
references: []
depends_on: ["task-define-persistence-model"]
pills:
- pill-substrate-is-dumb
- pill-trace-is-the-public-query-surface
files: []
tags:
- workspace:desk
- artifact:task
---

# Implement minimal query API

## Rationale
Graph data must be retrievable programmatically before CLI tools can expose it.

## Goal
Python API for deterministically querying the persisted graph representation.

## Scope
Python query functions returning QueryResult objects.

## Implementation Path
Add src/kgdb/query/ API functions.

## Validation
- pytest tests/test_query_api.py

## Done When
Python functions return QueryResult deterministically.
