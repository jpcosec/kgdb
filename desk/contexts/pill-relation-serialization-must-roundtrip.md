---
id: pill-relation-serialization-must-roundtrip
tags:
- workspace:desk
- artifact:pill
---

# Relation serialization must roundtrip

## What

_Define the context or guardrail this pill carries._

Every edge serialized to the snapshot must deserialize back to an identical edge object. Roundtrip is the contract; byte-equality is the test.

## Why

_Explain why this context matters for safe execution._

Silent serialization bugs produce invisible broken links; traceability looks fine until downstream consumers can't reconstruct the edge they need.

## When

_Describe when an agent should apply this pill._

Designing or changing the edge serialization format, adding a new edge class, or modifying the snapshot writer.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task-relation-serialization-roundtrip-and-malformed-input-handling, the snapshot writer, and edge deserialization paths.

## How

_Describe the correct way to apply this guidance._

Lock the edge serialization schema. Add roundtrip tests for every edge class (simple, typed, provenance-bearing). Make malformed edge entries raise structured errors.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not rely on Python repr; do not accept silently truncated edge fields; do not skip edge fields during deserialization without raising.
