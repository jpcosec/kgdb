---
id: task-graph-trace-query-surface-cli
status: draft
references: []
depends_on: ["task-graph-trace-query-surface-api"]
pills:
- pill-trace-is-the-public-query-surface
- pill-kgdb-cli-is-the-stable-public-surface
files: []
tags:
- workspace:desk
- artifact:task
---

# Graph trace query surface CLI

## Rationale
Deskops lifecycle scripts need a CLI entry point for tracing.

## Goal
Wire `kgdb trace <node-id>` CLI returning connected nodes.

## Scope
CLI trace command and JSON formatting.

## Implementation Path
Wire trace into src/kgdb/main.py

## Validation
- kgdb trace --help

## Done When
kgdb trace outputs correctly formatted JSON.
