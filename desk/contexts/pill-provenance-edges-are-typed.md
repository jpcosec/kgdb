---
id: pill-provenance-edges-are-typed
tags:
- workspace:desk
- artifact:pill
---

# Provenance edges are typed

## What

_Define the context or guardrail this pill carries._

Every edge from an atom to a source_doc carries relation (supported_by, synthesized_from, design_derived_from, about_dataset) and derivation (direct_quote, paraphrase, summary, synthesis, design_inference), with optional locator and confidence.

## Why

_Explain why this context matters for safe execution._

Untyped or undifferentiated provenance edges cannot be reasoned over; downstream audit and trust work becomes impossible without stable typed edges.

## When

_Describe when an agent should apply this pill._

Parsing atom provenance blocks, emitting provenance edges, or designing the reflection rules over provenance.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to FR-3, FR-4, FR-9 and the edge contract in section 8.4 of desk/drawer/registry/kgdb-provenance-requirements.md.

## How

_Describe the correct way to apply this guidance._

Always emit relation and derivation as required fields. Validate relation against the allowed set; validate derivation against the suggested set when strict mode is on. Preserve locator and confidence when present.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not collapse provenance into a generic reference edge; do not silently drop unknown relation values; do not store provenance only on the atom without an edge.
