---
id: task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test
status: draft
references: []
depends_on: []
pills:
- pill-provenance-survives-the-sldb-to-kgdb-handoff
- pill-fixtures-are-consumer-contract-tests
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
files: []
routine: routine-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test
checklists:
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-execution-ready
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-testing-ready
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-closeout-ready
current_node: checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Cross-repo SLDB export to KGDB ingest roundtrip test

## Rationale

_Explain why this task exists or the business driver behind it._

ADR Implementation Guidance: under-specifying the export boundary makes KGDB ingestion brittle. We need a contract-level roundtrip test that exercises the handoff end to end against real SLDB exports.

## Goal

_Describe the concrete result this task must produce._

A pytest fixture builds a real SLDB semantic-export payload, ingests it via KGDB, and asserts the resulting graph snapshot preserves every export field (model, document, path, tags, sections, DAG nodes, equivalences, hashes, provenance).

## Scope

_State what is in scope and what is out of scope._

Add an end-to-end test that constructs an SLDB export, runs it through KGDB ingest, and asserts no semantic loss; cover the schema in a parameterized matrix.

## Implementation Path

_Outline the expected implementation route or affected surface._

Build a small SLDB export builder in the test fixture (or use a real one if available in sldb/tests); run KGDB ingest against it; assert identity, structure, and provenance survive.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Test suite passes against multiple export shapes; failures point at the exact export field that was dropped or mangled; CI guard prevents regressions.
