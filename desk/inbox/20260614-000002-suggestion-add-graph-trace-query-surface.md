---
kind: suggestion
sender_project: deskops
created_at: 2026-06-14T00:00:02
status: open
---

# Add graph trace query surface

Deskops needs CLI and API surfaces to query atom → file → doc → test relationships from a built graph. Currently there's no stable way to trace a node's connections without reading raw graph JSON.

## Scope

- `kgdb trace <node-id>` — show connected nodes, their types, and relation types
- `kgdb trace <node-id> --depth 2` — recursive trace up to N hops
- Output format: human-readable table by default, `--format json` for scripting
- Python API: `trace_node(graph_path, node_id, depth=1) -> TraceResult`
- Handle missing nodes, disconnected nodes, and empty graphs gracefully

## Motivation

Deskops lifecycle gates and drift checks need to verify traceability. Currently there's no query surface; users and automation must parse raw snapshot JSON.

## Done When

- `kgdb trace` returns connected nodes with relation types
- Depth parameter expands the query up to N hops
- Missing node produces clear "not found" message (not a crash)
- JSON format outputs structured trace data
