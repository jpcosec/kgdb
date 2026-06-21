---
id: task-provenance-fr-2-emit-first-class-source-nodes
status: draft
references: []
depends_on: []
pills:
- pill-source-nodes-are-first-class
- pill-snapshot-is-the-public-output-surface
files: []
routine: routine-task-provenance-fr-2-emit-first-class-source-nodes
checklists:
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-execution-ready
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-testing-ready
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-closeout-ready
current_node: checklist-task-provenance-fr-2-emit-first-class-source-nodes-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-2: emit first-class source nodes

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-2: source entries must appear as first-class graph nodes with stable identity, node_type=source_doc, full metadata, and path preserved in output.

## Goal

_Describe the concrete result this task must produce._

Every ingested source-catalog entry becomes a source_doc graph node exposing node_id, node_type, label, path, kind, family, stability, description per the graph-node contract in section 8.3.

## Scope

_State what is in scope and what is out of scope._

Define source_doc node shape and ensure snapshot output preserves all metadata fields.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add SourceNode dataclass/model and ensure JSON snapshot writer serializes identity and semantics blocks per contract.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Snapshot JSON contains source_doc nodes whose structure matches the contract example in section 8.3.
