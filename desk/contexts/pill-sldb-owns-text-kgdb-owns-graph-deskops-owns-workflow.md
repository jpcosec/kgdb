---
id: pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
tags:
- workspace:desk
- artifact:pill
---

# SLDB owns text; KGDB owns graph; deskops owns workflow

## What

_Define the context or guardrail this pill carries._

SLDB owns canonical readable documents, AST-like structure, structural query, and graph-ready export. KGDB owns graph persistence, traversal, equivalence, inference. deskops owns workflow tasks, rituals, inbox and drawer routing.

## Why

_Explain why this context matters for safe execution._

If any of the three layers absorbs the others' concerns, the ecosystem becomes monolithic, contributors cannot tell where features belong, and downstream tools lose a neutral substrate.

## When

_Describe when an agent should apply this pill._

Evaluating any new feature; designing exports, imports, or APIs that cross project boundaries; reviewing pull requests.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to every task touching SLDB ingestion (SL-1..3), the KGDB boundary doc (BD-1), and cross-repo handoff design.

## How

_Describe the correct way to apply this guidance._

Ask whether a feature is primarily authored text, graph-native relation, or workflow routing. Place it in the layer that matches; keep boundaries documented and stable.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not put Markdown contract design or text rendering into KGDB; do not put graph traversal into SLDB; do not put workflow tasks into SLDB or KGDB.
