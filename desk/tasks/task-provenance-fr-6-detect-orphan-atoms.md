---
id: task-provenance-fr-6-detect-orphan-atoms
status: draft
references: []
depends_on: []
pills:
- pill-orphans-and-gaps-are-reflection-findings
- pill-validation-findings-are-structured-not-crashes
files: []
routine: routine-task-provenance-fr-6-detect-orphan-atoms
checklists:
- checklist-task-provenance-fr-6-detect-orphan-atoms-execution-ready
- checklist-task-provenance-fr-6-detect-orphan-atoms-testing-ready
- checklist-task-provenance-fr-6-detect-orphan-atoms-closeout-ready
current_node: checklist-task-provenance-fr-6-detect-orphan-atoms-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-6: detect orphan atoms

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-6: KGDB must detect atoms with no provenance declaration or with provenance declarations that fail to resolve, and report them as orphan or unsupported.

## Goal

_Describe the concrete result this task must produce._

Reflection output contains an orphan-atom finding for every atom lacking any resolved provenance support.

## Scope

_State what is in scope and what is out of scope._

Add a reflection rule that classifies atoms as orphans when they have no provenance block or every entry fails source resolution.

## Implementation Path

_Outline the expected implementation route or affected surface._

After edge emission, iterate atom nodes; flag those with zero successful provenance edges as orphans in the reflection artifact.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Given an atom with no provenance block (or only unresolved provenance), reflection emits an orphan-atom finding (AC-4, VR-2).
