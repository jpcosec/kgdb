---
id: pill-trace-is-the-public-query-surface
tags:
- workspace:desk
- artifact:pill
---

# Trace is the public query surface

## What

_Define the context or guardrail this pill carries._

kgdb trace is KGDB's public query surface for graph traversal. Consumers query the trace API; they never parse the snapshot JSON by hand.

## Why

_Explain why this context matters for safe execution._

Without a stable trace surface, every consumer reinvents traversal, and deskops lifecycle gates cannot verify graph integrity without parsing internal data.

## When

_Describe when an agent should apply this pill._

Designing or changing query surfaces, especially task-graph-trace-query-surface-cli-and-python-api.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to the kgdb trace CLI, the trace_node() Python API, and any consumer that wants node connections.

## How

_Describe the correct way to apply this guidance._

Expose a stable trace query with --depth and --format flags. Return structured output (table or JSON). Handle missing/disconnected/empty graphs explicitly.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not require consumers to parse the snapshot JSON themselves; do not change the trace output shape without versioning; do not crash on missing nodes.
