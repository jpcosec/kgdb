---
id: pill-provenance-survives-the-sldb-to-kgdb-handoff
tags:
- workspace:desk
- artifact:pill
---

# Provenance survives the SLDB to KGDB handoff

## What

_Define the context or guardrail this pill carries._

Every SLDB semantic-export field (model, document, path, tags, sections, DAG nodes, equivalences, hashes, provenance) must roundtrip into KGDB as preserved identity on graph nodes and edges.

## Why

_Explain why this context matters for safe execution._

Without roundtripped identity, KGDB cannot trace graph facts back to authored text; the substrate becomes a black box and downstream audit fails.

## When

_Describe when an agent should apply this pill._

Designing the SLDB export contract, the KGDB ingest path for SLDB payloads, or any resolver that maps graph nodes back to SLDB artifacts.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task-ingest-sldb-semantic-export-payloads, task-preserve-sldb-structural-provenance-through-kgdb-handoff, and the SL-3 roundtrip test.

## How

_Describe the correct way to apply this guidance._

Capture identity refs (doc/section/field/tags/model/hash) on every SLDB-derived node and edge. Expose a resolver API. Roundtrip-test the full chain end-to-end.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not silently drop any export field during ingest; do not invent identity fields the source doesn't carry; do not break the chain by re-keying nodes without preserving source pointers.
