---
id: task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract
status: draft
references: []
depends_on: []
pills:
- pill-snapshot-is-the-public-output-surface
- pill-source-nodes-are-first-class
- pill-provenance-edges-are-typed
files: []
routine: routine-task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract
checklists:
- checklist-task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract-execution-ready
- checklist-task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract-testing-ready
- checklist-task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract-closeout-ready
current_node: checklist-task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-8: include sources and edges in snapshot contract

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-8: KGDB graph snapshots must include source nodes and provenance edges as machine-readable structures, preserving source metadata and relation semantics for downstream tools.

## Goal

_Describe the concrete result this task must produce._

The snapshot JSON contract explicitly covers source_doc nodes and provenance edges alongside existing atom and reference nodes.

## Scope

_State what is in scope and what is out of scope._

Extend snapshot writer to serialize source nodes and provenance edges in the same machine-readable form as other graph facts.

## Implementation Path

_Outline the expected implementation route or affected surface._

Update the snapshot serializer to include source_doc nodes and provenance edges; document the contract addition in README or STANDARDS.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Snapshot JSON contains source nodes and provenance edge data and is consumable for queries like which atoms come from a given source (AC-6).
