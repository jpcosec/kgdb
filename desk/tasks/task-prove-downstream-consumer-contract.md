---
id: task-prove-downstream-consumer-contract
status: draft
references: []
depends_on:
- task-implement-minimal-query
- task-create-substrate-fixture
pills:
- pill-substrate-is-dumb
- pill-fixtures-are-consumer-contract-tests
- pill-snapshot-is-the-public-output-surface
- pill-trace-is-the-public-query-surface
files: []
routine: routine-task-prove-downstream-consumer-contract
checklists:
- checklist-task-prove-downstream-consumer-contract-execution-ready
- checklist-task-prove-downstream-consumer-contract-testing-ready
- checklist-task-prove-downstream-consumer-contract-closeout-ready
current_node: checklist-task-prove-downstream-consumer-contract-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Prove downstream consumer contract

## Rationale

_Explain why this task exists or the business driver behind it._

A substrate without proven consumer contracts is a self-contained demo; downstream tools (hum, ontology, truth_machine, graph_ui) need stable shape guarantees.

## Goal

_Describe the concrete result this task must produce._

An integration test ingests substrate_v1.json, queries it, and asserts a downstream consumer (e.g., a stub adapter) receives a QueryResult matching the documented shape.

## Scope

_State what is in scope and what is out of scope._

One integration test that proves the consumer-contract shape; stub consumer; full pytest path.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add tests/test_integration.py that loads the substrate fixture, runs a query, hands the QueryResult to a stub consumer, asserts the expected consumer-facing shape.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

tests/test_integration.py runs end-to-end against the substrate fixture and asserts the documented downstream consumer shape; CI green.
