---
id: task-preserve-sldb-structural-provenance-through-kgdb-handoff
status: draft
references: []
depends_on: []
pills:
- pill-provenance-survives-the-sldb-to-kgdb-handoff
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
files: []
routine: routine-task-preserve-sldb-structural-provenance-through-kgdb-handoff
checklists:
- checklist-task-preserve-sldb-structural-provenance-through-kgdb-handoff-execution-ready
- checklist-task-preserve-sldb-structural-provenance-through-kgdb-handoff-testing-ready
- checklist-task-preserve-sldb-structural-provenance-through-kgdb-handoff-closeout-ready
current_node: checklist-task-preserve-sldb-structural-provenance-through-kgdb-handoff-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Preserve SLDB structural provenance through KGDB handoff

## Rationale

_Explain why this task exists or the business driver behind it._

ADR Consequence E: export boundary must preserve enough structure that KGDB can trace graph nodes and edges back to source document identity, section or field identity, semantic tags, model contract identity, and extraction/hash provenance.

## Goal

_Describe the concrete result this task must produce._

Every SLDB-derived graph node carries identity references to its source document, section/field, semantic tags, model contract, and extraction/hash provenance. KGDB query surfaces can resolve back to the originating SLDB artifact.

## Scope

_State what is in scope and what is out of scope._

Define a provenance block on graph nodes that captures doc/section/field identity, semantic tags, model contract, and hash. Expose resolution helpers that map a graph node back to its SLDB source.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add a stable ProvenanceRef schema on graph nodes; populate it during SLDB semantic-export ingest; expose graph_node_source() or equivalent for downstream tools.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Every SLDB-derived node has doc/section/field/tags/model/hash provenance; a resolver API maps graph nodes back to SLDB artifacts; roundtrip tests confirm no identity is dropped.
