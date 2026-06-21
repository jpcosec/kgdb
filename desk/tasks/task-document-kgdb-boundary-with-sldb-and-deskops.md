---
id: task-document-kgdb-boundary-with-sldb-and-deskops
status: draft
references: []
depends_on: []
pills:
- pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow
- pill-board-md-frontmatter-is-the-routing-truth
files: []
routine: routine-task-document-kgdb-boundary-with-sldb-and-deskops
checklists:
- checklist-task-document-kgdb-boundary-with-sldb-and-deskops-execution-ready
- checklist-task-document-kgdb-boundary-with-sldb-and-deskops-testing-ready
- checklist-task-document-kgdb-boundary-with-sldb-and-deskops-closeout-ready
current_node: checklist-task-document-kgdb-boundary-with-sldb-and-deskops-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Document KGDB boundary with SLDB and deskops

## Rationale

_Explain why this task exists or the business driver behind it._

ADR: contributors need to evaluate new features against a stable frame. KGDB must publish its boundary statements (text vs graph vs deskops) so future tasks get routed to the correct layer.

## Goal

_Describe the concrete result this task must produce._

KGDB docs/ contains an architecture page that states KGDB owns graph persistence, traversal, equivalence, and inference; does NOT own document authoring or rendering; hands off with SLDB at the semantic-export boundary; coexists with deskops as workflow layer.

## Scope

_State what is in scope and what is out of scope._

Add docs/architecture/kgdb-text-vs-graph-boundary.md (or equivalent) restating the boundary from the KGDB side; reference the SLDB ADR and the deskops interaction note.

## Implementation Path

_Outline the expected implementation route or affected surface._

Write a short boundary document modeled on the SLDB ADR; include a KGDB-specific implementation-guidance checklist (graph persistence, traversal, equivalence, inference, system-wide query). Cross-link from README.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

docs/architecture/ contains a boundary document that explicitly says what KGDB owns, what it does NOT own, and how it hands off with SLDB and deskops; README links to it.
