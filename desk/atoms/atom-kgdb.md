---
atom_id: kgdb
status: draft
kind: code
maturity: active
created_by: subagent
date: 2026-06-02
---

# KGDB

## What it is
KGDB is the graph persistence, traversal, and query substrate of the hum ecosystem — a Python library and CLI that stores, ingests, and queries directed graphs of typed knowledge nodes. It was extracted from the `wikipu` project on 2026-04-24 to serve as a standalone, dumb graph-store that other ecosystem tools (hum, ontology, truth_machine, graph_ui) depend on for structured graph IO.

## Why
The hum ecosystem needs a shared substrate where graph knowledge (node-typed, edge-typed directed graphs) can be persisted deterministically and queried without introducing semantic reasoning or workflow orchestration. Downstream tools defined in `desk/SPEC.md` (hum, ontology, truth_machine, graph_ui) all need a reliable graph store they can read from and write to through a common contract surface. KGDB owns that contract surface (`kgdb_graph_bundle` export, `sldb_document_payload` consumption).

## How it's made
Python ≥3.10, Pydantic ≥2.0 for typed contracts, NetworkX ≥3.0 for in-memory graph operations. CLI entry point via `argparse` (`kgdb` command with get/list/query/edges/ingest subcommands). Tests are `pytest` (filed under `tests/test_ingest.py`, `test_query.py`, `test_integration.py`). Package layout uses `src/` layout with `setuptools`. Integration contracts live in `contracts/` as YAML + JSON Schema.

## When
Created 2026-04-24 when the graph core was extracted from `wikipu`. Three implementation tasks were closed on 2026-05-01 (minimal ingest, minimal query, downstream consumer contract). The `SPEC.md` was written before those tasks; `STANDARDS.md` codifies the desk workflow. This is a relatively young component (6 weeks old as of this writing), built alongside other hum ecosystem tools at the same phase.

## Purpose
To be the dumb persistence and query substrate that every other hum ecosystem tool reads graph data from and writes graph data through — intentionally limited to graph IO with zero semantic reasoning, zero formal evaluation, and zero UI. The purpose is explicit in `desk/SPEC.md`: "kgdb should be the dumb graph persistence and query substrate of the ecosystem."

## Patterns
- **Contract-first design**: Graph models (`KnowledgeNode`, `Edge`, `GraphSnapshot`, `StructuredQuery`) are Pydantic BaseModel contracts defined before implementation, with JSON Schema exported to `contracts/schemas/`.
- **Ledger-style persistence**: `TransactionManifest` with rolling `hash_chain` links entries into an auditable ledger — a pattern shared with the broader ecosystem's integrity approach.
- **Desk-driven development**: Planning and spec work lives in `desk/` (SPEC.md, STANDARDS.md, tasks/, rituals/, fixtures/) while implementation lives in `src/` — same pattern as other hum-ecosystem tools.
- **Integration contract surface**: `contracts/integration.contract.yaml` declares explicit import/export schemas and cross-module compatibility requirements (currently depends on `sldb`).
- **Structured query model**: `StructuredQuery` with `FacetFilter`, `FieldCondition`, and `GraphScope` provides typed, composable query definitions rather than raw traversal logic.

## State of maturity
Active but early (v0.1.0). The core graph model, ingest pipeline, and query language are implemented and tested. CLI supports get, list, query, edges, and ingest commands. A substrate fixture (`desk/fixtures/substrate_v1.json`) proves the ingest cycle. Contracts for persistence ledger (`PersistenceEntry`, `TransactionManifest`) are defined but not yet wired into the runtime. The `query/server.py` module exists but is not connected to the CLI. Integration with `sldb` is declared in the contract surface but not implemented end-to-end. Tests exist but cannot run without the package installed (no `pip install -e .` in CI or test setup).

## Open questions
- How does `query/server.py` connect to the CLI or to a long-running process — is it meant to be a query server, or was it speculative?
- The `sldb` integration is declared in `integration.contract.yaml` but there is no code path that consumes an `sldb_document_payload` — is this integration still in flight or descoped?
- Why can tests not be collected via `pytest` without first installing the package (`ModuleNotFoundError: No module named 'kgdb'`) — is there a missing `pip install -e .` step in the test workflow?
- What is the desk/drawer/ meant to hold — it's empty and the README says "deferred desk work" with no specifics.
- `PersistenceEntry` and `TransactionManifest` define an append-only ledger pattern, but no persistence backend (file, DB, etc.) is implemented — what is the target persistence strategy?

## References
- `desk/SPEC.md` — delivery specification for the graph substrate
- `desk/STANDARDS.md` — desk workflow rules for kgdb development
- `desk/tasks/` — resolved tasks 001–006 covering contracts, ingest, query, fixture, and downstream consumer
- `contracts/integration.contract.yaml` — cross-module contract surface with sldb
- `contracts/schemas/` — JSON Schema exports for graph bundle and document payload
- `src/kgdb/` — Python package with contracts, graph, query, and CLI
- `tests/` — pytest test suite
- `desk/fixtures/substrate_v1.json` — 10-node proof-of-ingest fixture
- `.sldb/` — sldb runtime state (semantic index and DAG)
