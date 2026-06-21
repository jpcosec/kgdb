---
id: pill-substrate-is-dumb
tags:
- workspace:desk
- artifact:pill
---

# Substrate is dumb

## What

_Define the context or guardrail this pill carries._

KGDB holds graph state, validates snapshots, runs queries. It does no semantic reasoning, no project-specific interpretation, no workflow logic.

## Why

_Explain why this context matters for safe execution._

If KGDB absorbs semantic concerns it stops being a substrate and becomes an application; downstream tools lose a neutral layer they can all rely on.

## When

_Describe when an agent should apply this pill._

Evaluating any feature that looks like interpretation, classification, ranking, or domain-specific logic; evaluating whether a new concern belongs in KGDB or downstream.

## Where

_Name the files, surfaces, or scope this pill applies to._

All of src/kgdb/. Applies to every substrate task and every change to the IO, persistence, ingest, or query surfaces.

## How

_Describe the correct way to apply this guidance._

Keep semantic tags, equivalence, and inference out of KGDB. Push those concerns into downstream consumers or into SLDB at the export boundary.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not add field-level meaning to GraphSnapshot fields, do not interpret provenance for the user, do not hard-code workflow-specific edge semantics.
