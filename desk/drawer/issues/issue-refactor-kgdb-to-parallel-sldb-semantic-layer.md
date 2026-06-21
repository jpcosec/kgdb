# Refactor KGDB to parallel SLDB semantic layer

## Kind

architecture

## Status

open

## Problem

KGDB has not been actively evolved alongside SLDB. SLDB now has a semantic layer with model semantics, document semantic tags, semantic DAG nodes, equivalences, semantic indexes, section context indexes, and physical/semantic retrieval. KGDB still exposes a narrow generic graph substrate and does not consume SLDB semantic artifacts end-to-end.

## Desired Outcome

Refactor KGDB into the graph companion for SLDB: a NetworkX-backed persistence/query layer that can ingest SLDB semantic/document/index payloads, preserve provenance, and expose graph traversal without duplicating SLDB's document modeling or semantic tag ownership.

## Boundary

- SLDB owns modeled Markdown contracts, extraction, rendering, validation, semantic tags, semantic DAG/index generation, and document field/section operations.
- KGDB owns graph snapshots, graph persistence, traversal, graph query, graph exchange contracts, and downstream graph payloads.
- Deskops owns workflow-specific graph vocabulary and source-file relation extraction.
- Ontology/OWL layers may later consume KGDB graph bundles, but KGDB should remain a dumb graph substrate.

## Refactor Slices

1. Stabilize KGDB local tests and fixture paths.
2. Replace hardcoded node/edge literals with downstream-extensible vocabularies or validated string roles.
3. Define an SLDB semantic payload contract that includes model, document, path, tags, sections, DAG nodes, equivalences, hashes, and provenance.
4. Implement SLDB semantic payload ingestion into KGDB `GraphSnapshot` or a new import command.
5. Add graph query examples for semantic tags, document neighborhoods, and source-file links.
6. Add deskops adapter that emits workflow/source-file relations into KGDB without making KGDB deskops-specific.

## Questions

- Should KGDB import directly from `.sldb/runtime/semantic_index.yaml` and `.sldb/runtime/semantic_dag.yaml`, or consume a normalized SLDB export command?
- Should KGDB store semantic tags as nodes, node attributes, or both?
- Should SLDB section context records become first-class graph nodes?
- Should KGDB own an append-only graph ledger before or after the SLDB integration?
- What graph file location should downstream repos use: `.sldb/runtime`, `.kgdb`, or project-specific runtime output?

## Related Issues

- issue-support-deskops-node-and-edge-vocabulary
- issue-implement-sldb-document-payload-consumption
- issue-fix-test-import-path-for-local-pytest
- issue-fix-fixture-paths-in-tests
