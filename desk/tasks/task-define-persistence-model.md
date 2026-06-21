---
id: task-define-persistence-model
status: draft
references: []
depends_on:
- task-define-graph-io-contract
pills:
- pill-substrate-is-dumb
- pill-snapshot-is-the-public-output-surface
files: []
routine: routine-task-define-persistence-model
checklists:
- checklist-task-define-persistence-model-execution-ready
- checklist-task-define-persistence-model-testing-ready
- checklist-task-define-persistence-model-closeout-ready
current_node: checklist-task-define-persistence-model-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Define persistence model

## Rationale

_Explain why this task exists or the business driver behind it._

Graph state must roundtrip deterministically; persistence entry shapes are the substrate's storage contract.

## Goal

_Describe the concrete result this task must produce._

Define PersistenceEntry and TransactionManifest in src/kgdb/contracts/persistence.py; document ledger-based graph storage semantics.

## Scope

_State what is in scope and what is out of scope._

Persistence contract types only; no actual store backend implementation.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add src/kgdb/contracts/persistence.py exposing PersistenceEntry and TransactionManifest; export from kgdb.contracts.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

PersistenceEntry and TransactionManifest are importable from kgdb.contracts and the contract is documented.
