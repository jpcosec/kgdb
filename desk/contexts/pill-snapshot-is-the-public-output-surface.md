---
id: pill-snapshot-is-the-public-output-surface
tags:
- workspace:desk
- artifact:pill
---

# Snapshot is the public output surface

## What

_Define the context or guardrail this pill carries._

The GraphSnapshot JSON is KGDB's public output contract. Downstream tools read snapshots, never raw graph state, never internal in-memory structures.

## Why

_Explain why this context matters for safe execution._

Internal data structures may change; the snapshot must not. A stable snapshot contract is what makes downstream tools upgrade-safe and KGDB replaceable.

## When

_Describe when an agent should apply this pill._

Designing or changing the IO contract, persistence layer, ingest path, or any output shape.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task-define-graph-io-contract, the GraphSnapshot contract, and SV-1 (snapshot validation).

## How

_Describe the correct way to apply this guidance._

Treat the snapshot schema as the public API. Add new fields; never remove or rename existing ones without a major version bump. Validate snapshots against this contract.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not expose NetworkX-internal types in the snapshot; do not let internal refactors leak into the contract; do not skip validation when writing the snapshot.
