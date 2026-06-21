---
id: task-provenance-fr-9-reflection-output-contract-for-findings
status: draft
references: []
depends_on: []
pills:
- pill-orphans-and-gaps-are-reflection-findings
- pill-validation-findings-are-structured-not-crashes
- pill-provenance-edges-are-typed
files: []
routine: routine-task-provenance-fr-9-reflection-output-contract-for-findings
checklists:
- checklist-task-provenance-fr-9-reflection-output-contract-for-findings-execution-ready
- checklist-task-provenance-fr-9-reflection-output-contract-for-findings-testing-ready
- checklist-task-provenance-fr-9-reflection-output-contract-for-findings-closeout-ready
current_node: checklist-task-provenance-fr-9-reflection-output-contract-for-findings-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-9: reflection output contract for findings

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-9: KGDB reflection must produce machine-readable findings for unknown source_id, orphan atom, malformed provenance, unused source, and (optionally) insufficient synthesis support.

## Goal

_Describe the concrete result this task must produce._

Reflection output defines a stable schema for provenance findings: id, atom_id, source_id, relation, severity, message.

## Scope

_State what is in scope and what is out of scope._

Extend the reflection artifact schema with the provenance finding classes listed in FR-9; serialize in the existing or extended reflection format.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add Finding dataclass entries for each provenance class; update reflection writer to emit them; ensure VR-3, VR-6 are satisfied.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Reflection artifact serializes each provenance finding class in a stable structured format suitable for downstream inspection and CI automation (VR-3, VR-6).
