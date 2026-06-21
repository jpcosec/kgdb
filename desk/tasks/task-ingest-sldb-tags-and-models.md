---
id: task-ingest-sldb-tags-and-models
status: draft
references: []
depends_on: ["task-ingest-sldb-documents-and-sections"]
pills:
- pill-snapshot-is-the-public-output-surface
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
- pill-provenance-survives-the-sldb-to-kgdb-handoff
files: []
tags:
- workspace:desk
- artifact:task
---

# Ingest SLDB semantic-export: Tags and Models

## Rationale
Second step of SLDB handoff involves semantic meaning.

## Goal
Extend SLDB payload ingestion to parse semantic tags and SLDB model references.

## Scope
Tags and model extraction rules.

## Implementation Path
Extend ingest parser.

## Validation
- pytest tests/test_sldb_tag_ingest.py

## Done When
Tags and models are captured as nodes/edges.
