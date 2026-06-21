---
id: task-graph-trace-query-surface-api
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

# Graph trace query surface API

## Rationale
Deskops needs an API to query atom relationships.

## Goal
Implement trace_node(graph_path, node_id, depth) Python API.

## Scope
Traversal algorithm and python dataclasses.

## Implementation Path
Add tracing logic to src/kgdb/query/

## Validation
- pytest tests/test_trace_api.py

## Done When
API returns a structured TraceResult of connected nodes.
