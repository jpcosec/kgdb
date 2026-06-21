---
id: task-provenance-fr-4-emit-typed-provenance-edges
status: draft
references: []
depends_on: []
pills:
- pill-provenance-edges-are-typed
- pill-provenance-survives-the-sldb-to-kgdb-handoff
- pill-snapshot-is-the-public-output-surface
files: []
routine: routine-task-provenance-fr-4-emit-typed-provenance-edges
checklists:
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-execution-ready
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-testing-ready
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-closeout-ready
current_node: checklist-task-provenance-fr-4-emit-typed-provenance-edges-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-4: emit typed provenance edges

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-4: KGDB must create typed edges from atoms to source nodes with relation (supported_by, synthesized_from, design_derived_from, about_dataset) and derivation metadata.

## Goal

_Describe the concrete result this task must produce._

Each valid provenance declaration produces a typed edge from the atom to its source node, preserving relation, derivation, locator, and confidence.

## Scope

_State what is in scope and what is out of scope._

Add a provenance-edge builder that consumes parsed atom provenance and emits edges with the contract shape from section 8.4.

## Implementation Path

_Outline the expected implementation route or affected surface._

After atom ingest, iterate atom provenance entries and emit one edge per entry with full metadata in the snapshot.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Given an atom with a valid provenance block referencing a known source_id, the snapshot contains a typed edge atom -> source_doc with relation and derivation preserved (AC-2).
