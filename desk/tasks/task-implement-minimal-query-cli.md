---
id: task-implement-minimal-query-cli
status: draft
references: []
depends_on: ["task-implement-minimal-query-api"]
pills:
- pill-trace-is-the-public-query-surface
- pill-kgdb-cli-is-the-stable-public-surface
files: []
tags:
- workspace:desk
- artifact:task
---

# Implement minimal query CLI

## Rationale
Users and scripts need to inspect graph state via CLI.

## Goal
kgdb query <graph-path> returns a structured string deterministically.

## Scope
CLI: `kgdb query` command.

## Implementation Path
Wire into src/kgdb/main.py

## Validation
- kgdb query --help

## Done When
CLI returns valid data.
