---
kind: suggestion
sender_project: deskops
created_at: 2026-06-14T00:00:01
status: open
---

# Stabilize relation serialization

Deskops graph build extracts relations (edges) from source files. The serialization format must roundtrip reliably between graph build, snapshot storage, and graph query tools.

## Scope

- Edge serialization must preserve source, target, relation type, and provenance metadata
- Deserialization must reconstruct the same edge objects
- Unknown or malformed edge types should be reported, not silently dropped
- Test coverage for: simple edges, typed edges, edges with provenance, malformed edge entries

## Motivation

Relation data is the core of graph traceability. Silent serialization bugs produce invisible broken links.

## Done When

- Roundtrip test: serialize → write → read → deserialize produces identical edge objects
- Malformed edge entry in snapshot produces a clear error during deserialization
- All edge types in active use have serialization tests
