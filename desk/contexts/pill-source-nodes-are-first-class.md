---
id: pill-source-nodes-are-first-class
tags:
- workspace:desk
- artifact:pill
---

# Source nodes are first-class

## What

_Define the context or guardrail this pill carries._

Every entry in desk/registry/source-catalog.yaml becomes a source_doc graph node with full metadata, not a side reference or external lookup.

## Why

_Explain why this context matters for safe execution._

If sources live outside the graph, downstream tools cannot query source coverage, orphan atoms, or provenance in graph-native ways; the substrate loses the ability to reason about origin.

## When

_Describe when an agent should apply this pill._

Designing the source catalog, defining the source-node shape, or emitting edges from atoms to sources.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to desk/registry/source-catalog.yaml, the FR-1 and FR-2 tasks, and any node that emits source_doc nodes.

## How

_Describe the correct way to apply this guidance._

Treat each catalog entry as one source_doc node. Preserve id, title, kind, family, path, stability, description as node fields. Make them queryable like any other node.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not store source metadata in a sidecar file; do not reference sources by string lookup; do not collapse sources into atom metadata.
