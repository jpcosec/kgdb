---
id: task-ingest-sldb-equivalences-and-hashes
status: draft
references: []
depends_on: ["task-ingest-sldb-tags-and-models"]
pills:
- pill-snapshot-is-the-public-output-surface
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
- pill-provenance-survives-the-sldb-to-kgdb-handoff
files: []
tags:
- workspace:desk
- artifact:task
---

# Ingest SLDB semantic-export: Equivalences and Hashes

## Rationale
Final step of SLDB handoff ensuring cryptographic tracking.

## Goal
Extend SLDB payload ingestion to parse cryptographic hashes and structural equivalences.

## Scope
Hashes, signatures, equivalences.

## Implementation Path
Extend ingest parser.

## Validation
- pytest tests/test_sldb_hash_ingest.py

## Done When
Hashes and equivalences are preserved.
