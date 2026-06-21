---
id: task-provenance-fr-7-source-coverage-reflection
status: draft
references: []
depends_on: []
pills:
- pill-orphans-and-gaps-are-reflection-findings
files: []
routine: routine-task-provenance-fr-7-source-coverage-reflection
checklists:
- checklist-task-provenance-fr-7-source-coverage-reflection-execution-ready
- checklist-task-provenance-fr-7-source-coverage-reflection-testing-ready
- checklist-task-provenance-fr-7-source-coverage-reflection-closeout-ready
current_node: checklist-task-provenance-fr-7-source-coverage-reflection-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-7: source coverage reflection

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-7: KGDB must support reflection over source utilization, identifying unused sources, over-centralized patterns, and per-family coverage.

## Goal

_Describe the concrete result this task must produce._

Reflection output reports unused source nodes (no incoming support edges) and enables coverage review by source family.

## Scope

_State what is in scope and what is out of scope._

Add reflection rules that surface unused sources and coverage by family. Query examples: atoms from a given source, synthesized atoms, unused sources.

## Implementation Path

_Outline the expected implementation route or affected surface._

After edge emission, compute per-source in-degree from provenance edges; emit unused-source findings for zero-degree nodes; expose family grouping.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Given a source node unused by all atoms, reflection reports it as unused or uncovered (AC-5, VR-4); coverage can be queried by family.
