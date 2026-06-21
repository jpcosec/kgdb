---
id: task-ingest-sldb-documents-and-sections
status: draft
references: []
depends_on: ["task-define-persistence-model", "task-provenance-fr-8"]
pills:
- pill-snapshot-is-the-public-output-surface
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
- pill-provenance-survives-the-sldb-to-kgdb-handoff
files: []
tags:
- workspace:desk
- artifact:task
---

# Ingest SLDB semantic-export: Documents and Sections

## Rationale
The SLDB handoff is too large for one task. First, handle core structural nodes.

## Goal
Ingest SLDB export payloads purely for document, path, and section structural nodes.

## Scope
Documents and sections tree hierarchy only.

## Implementation Path
Update ingest logic for sldb export formats.

## Validation
- pytest tests/test_sldb_doc_ingest.py

## Done When
Documents and sections are properly converted into graph nodes.
