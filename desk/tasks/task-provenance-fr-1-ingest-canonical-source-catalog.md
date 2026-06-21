---
id: task-provenance-fr-1-ingest-canonical-source-catalog
status: draft
references: []
depends_on: []
pills:
- pill-source-nodes-are-first-class
- pill-snapshot-is-the-public-output-surface
files: []
routine: routine-task-provenance-fr-1-ingest-canonical-source-catalog
checklists:
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-execution-ready
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-testing-ready
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-closeout-ready
current_node: checklist-task-provenance-fr-1-ingest-canonical-source-catalog-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-1: ingest canonical source catalog

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-1: KGDB must ingest a canonical source catalog from desk/registry/source-catalog.yaml and create one graph node per declared source entry.

## Goal

_Describe the concrete result this task must produce._

KGDB reads desk/registry/source-catalog.yaml, validates unique source IDs, and creates one source_doc graph node per entry with metadata (id, title, kind, family, path, stability, description).

## Scope

_State what is in scope and what is out of scope._

Add a source-catalog extractor that parses desk/registry/source-catalog.yaml and emits source_doc nodes during graph build.

## Implementation Path

_Outline the expected implementation route or affected surface._

Extend graph ingest to read the catalog YAML and emit one source_doc node per entry before atom ingestion runs.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Given a valid source-catalog.yaml, KGDB graph snapshot contains one source_doc node per entry with full metadata preserved (AC-1).
