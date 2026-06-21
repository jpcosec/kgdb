---
id: task-provenance-fr-10-backward-compatible-degradation
status: draft
references: []
depends_on: []
pills:
- pill-backward-compatible-degradation-findings-not-failures
- pill-validation-findings-are-structured-not-crashes
files: []
routine: routine-task-provenance-fr-10-backward-compatible-degradation
checklists:
- checklist-task-provenance-fr-10-backward-compatible-degradation-execution-ready
- checklist-task-provenance-fr-10-backward-compatible-degradation-testing-ready
- checklist-task-provenance-fr-10-backward-compatible-degradation-closeout-ready
current_node: checklist-task-provenance-fr-10-backward-compatible-degradation-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-10: backward-compatible degradation

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-10: KGDB must degrade safely when provenance data is absent. Existing graph functionality keeps working; missing provenance produces findings, not failures, unless strict mode is opted in.

## Goal

_Describe the concrete result this task must produce._

When source catalog or atom provenance blocks are missing, KGDB graph build still succeeds and emits provenance findings instead of erroring.

## Scope

_State what is in scope and what is out of scope._

Guard the source-catalog ingest and provenance parsing paths so absence yields empty-but-valid graphs plus findings; add a strict-mode flag for fail-fast enforcement.

## Implementation Path

_Outline the expected implementation route or affected surface._

Make catalog and provenance ingest optional-by-default; route absence into reflection findings; add a strict flag the CLI can enable.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Existing graph build passes on a desk with no source catalog and no provenance blocks, and reflection reports missing-provenance findings (AC-7).
