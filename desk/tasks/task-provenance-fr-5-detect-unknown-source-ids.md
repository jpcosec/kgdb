---
id: task-provenance-fr-5-detect-unknown-source-ids
status: draft
references: []
depends_on: []
pills:
- pill-orphans-and-gaps-are-reflection-findings
- pill-validation-findings-are-structured-not-crashes
files: []
routine: routine-task-provenance-fr-5-detect-unknown-source-ids
checklists:
- checklist-task-provenance-fr-5-detect-unknown-source-ids-execution-ready
- checklist-task-provenance-fr-5-detect-unknown-source-ids-testing-ready
- checklist-task-provenance-fr-5-detect-unknown-source-ids-closeout-ready
current_node: checklist-task-provenance-fr-5-detect-unknown-source-ids-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-5: detect unknown source IDs

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-5: KGDB must not silently discard unresolved source_id references. They must appear in machine-readable reflection output with the offending atom and source_id.

## Goal

_Describe the concrete result this task must produce._

Reflection output contains an unresolved-source finding for every provenance entry whose source_id is missing from the catalog.

## Scope

_State what is in scope and what is out of scope._

Add a reflection rule that flags unresolved source IDs and includes atom id, declared source_id, and severity.

## Implementation Path

_Outline the expected implementation route or affected surface._

During ingest, resolve each provenance entry against the catalog; queue a finding for any miss; emit findings in the reflection artifact.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Given an atom referencing a nonexistent source_id, reflection emits an explicit unresolved-source finding naming the atom and the bad source_id (AC-3, VR-1).
