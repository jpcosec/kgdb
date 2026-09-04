---
name: use-kgdb
description: Use when working with KGDB graph snapshots, graph contracts, nodes, edges, provenance, or deskops graph build/missing/neighbors commands.
---

# Use KGDB

KGDB owns graph contracts and runtime validation for knowledge graph snapshots.

Use KGDB when the task involves:

- Graph snapshot schemas or validation.
- Node and edge contracts.
- Provenance for graph nodes/edges.
- `deskops graph build`, `deskops graph missing`, or `deskops graph neighbors`.
- `.sldb/runtime/knowledge_graph.kg.json` outputs.

Current deskops flow:

- `deskops.graph.extract_docs` extracts document nodes from `desk/`, `docs/`, and `spec/`.
- `deskops.graph.extract_sources` extracts source/config/test/spec file nodes.
- `deskops.graph.extract_edges` extracts declared references from docs.
- `deskops.graph.snapshot` builds a KGDB `GraphSnapshot`-compatible payload and validates it with `kgdb.contracts.io.GraphSnapshot`.

Common commands:

```bash
deskops graph build --root .
deskops graph missing --root .
deskops graph neighbors atom:<atom-id> --root .
```

Output policy:

- Runtime graph output belongs under `.sldb/runtime/`.
- Generated graph snapshots are runtime state, not source documentation.
- Preserve provenance for every extracted node and declared edge.
- Missing references should be reported as findings, not silently ignored.

Review checklist:

- Are node IDs stable and deterministic?
- Are edge roles explicit and constrained?
- Does every edge carry provenance path and locator?
- Does the snapshot validate against KGDB contracts?
- Are runtime outputs ignored and reproducible?
