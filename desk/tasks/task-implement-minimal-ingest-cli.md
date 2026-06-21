---
id: task-implement-minimal-ingest-cli
status: draft
references: []
depends_on: ["task-implement-minimal-ingest-api"]
pills:
- pill-snapshot-is-the-public-output-surface
- pill-kgdb-cli-is-the-stable-public-surface
files: []
tags:
- workspace:desk
- artifact:task
---

# Implement minimal ingest CLI

## Rationale
Users and automation tools need a CLI command to trigger ingest.

## Goal
kgdb ingest command correctly wires arguments into the ingest API.

## Scope
CLI: `kgdb ingest`.

## Implementation Path
Wire into src/kgdb/main.py

## Validation
- kgdb ingest --help

## Done When
kgdb ingest <payload> successfully calls the API and persists the manifest.
