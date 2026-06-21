---
id: task-provenance-fr-3-parse-atom-provenance-declarations
status: draft
references: []
depends_on: []
pills:
- pill-provenance-edges-are-typed
- pill-provenance-survives-the-sldb-to-kgdb-handoff
files: []
routine: routine-task-provenance-fr-3-parse-atom-provenance-declarations
checklists:
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-execution-ready
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-testing-ready
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-closeout-ready
current_node: checklist-task-provenance-fr-3-parse-atom-provenance-declarations-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Provenance FR-3: parse atom provenance declarations

## Rationale

_Explain why this task exists or the business driver behind it._

Provenance requirement FR-3: KGDB must parse provenance blocks from atom frontmatter (source_id, relation, derivation, optional locator/confidence/notes) and resolve each source_id against the canonical catalog.

## Goal

_Describe the concrete result this task must produce._

Atom frontmatter provenance entries are read, validated against the catalog, and stored on the atom node for downstream edge emission.

## Scope

_State what is in scope and what is out of scope._

Add a provenance parser that reads the provenance: list from atom frontmatter and records it as atom node metadata.

## Implementation Path

_Outline the expected implementation route or affected surface._

Extend atom ingest to parse provenance blocks, validate required fields, and store parsed entries on the atom node for edge builders.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Atoms with valid provenance blocks have the parsed entries available on their node; malformed entries surface as reflection findings (VR-3).
