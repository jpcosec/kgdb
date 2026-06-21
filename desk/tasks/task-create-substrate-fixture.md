---
id: task-create-substrate-fixture
status: draft
references: []
depends_on:
- task-define-graph-io-contract
pills:
- pill-substrate-is-dumb
- pill-fixtures-are-consumer-contract-tests
- pill-snapshot-is-the-public-output-surface
files: []
routine: routine-task-create-substrate-fixture
checklists:
- checklist-task-create-substrate-fixture-execution-ready
- checklist-task-create-substrate-fixture-testing-ready
- checklist-task-create-substrate-fixture-closeout-ready
current_node: checklist-task-create-substrate-fixture-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Create substrate fixture

## Rationale

_Explain why this task exists or the business driver behind it._

Without a stable fixture, downstream consumer contracts are aspirational; they need a real substrate shape to bind against.

## Goal

_Describe the concrete result this task must produce._

Create desk/fixtures/substrate_v1.json representing the core ecosystem modules as nodes and edges; GraphSnapshot-valid; replayable.

## Scope

_State what is in scope and what is out of scope._

Single fixture file in desk/fixtures/; documented structure; used by consumer-contract tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

Hand-author a fixture that captures a small but representative subgraph; validate it against GraphSnapshot contract; add fixture-loading helper under tests/.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

substrate_v1.json validates against the IO contract and a pytest fixture loads it deterministically.
