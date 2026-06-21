---
id: pill-backward-compatible-degradation-findings-not-failures
tags:
- workspace:desk
- artifact:pill
---

# Backward-compatible degradation: findings, not failures

## What

_Define the context or guardrail this pill carries._

Missing source catalog, missing provenance blocks, and absent historical fields produce findings, not exceptions or graph-build failures, unless strict mode is explicitly enabled.

## Why

_Explain why this context matters for safe execution._

Strict-by-default blocks adoption and breaks existing graphs; loose-by-default with opt-in strict mode lets projects turn on provenance as they mature without breaking older data.

## When

_Describe when an agent should apply this pill._

Designing ingest paths, validation rules, or strict-mode flags; especially FR-10.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to FR-10, the snapshot validation entry points, and any optional ingest path (source catalog, SLDB semantic export, atom provenance blocks).

## How

_Describe the correct way to apply this guidance._

Make optional inputs genuinely optional. Route absence into findings. Expose a strict-mode flag the CLI can enable to fail fast when projects are ready.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not require all fields by default; do not raise on missing provenance; do not change behavior silently when strict mode toggles.
