---
id: task-snapshot-validation-cli-and-python-api
status: draft
references: []
depends_on: []
pills:
- pill-snapshot-is-the-public-output-surface
- pill-validation-findings-are-structured-not-crashes
files: []
routine: routine-task-snapshot-validation-cli-and-python-api
checklists:
- checklist-task-snapshot-validation-cli-and-python-api-execution-ready
- checklist-task-snapshot-validation-cli-and-python-api-testing-ready
- checklist-task-snapshot-validation-cli-and-python-api-closeout-ready
current_node: checklist-task-snapshot-validation-cli-and-python-api-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Snapshot validation: CLI and Python API

## Rationale

_Explain why this task exists or the business driver behind it._

Inbox 20260614-000000: deskops graph build emits snapshots but there is no validation that they match the KGDB contract schema before downstream graph missing/trace queries consume them.

## Goal

_Describe the concrete result this task must produce._

kgdb snapshot validate <path> validates a snapshot JSON against the registered graph contract; Python API validate_snapshot(path) -> ValidationResult with structured findings; non-zero exit with diagnostic list on invalid; exit 0 on valid.

## Scope

_State what is in scope and what is out of scope._

Add a  command plus a validate_snapshot(path) Python API. Validate required fields, types, and node/edge type allowlists.

## Implementation Path

_Outline the expected implementation route or affected surface._

Define a ValidationResult dataclass with findings[]; reuse the existing GraphSnapshot contract for required fields and type checks; wire the CLI into the kgdb command surface.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

Invalid snapshot (missing field, wrong type, unknown node/edge type) exits non-zero with a structured diagnostic list; valid snapshot exits 0 with a summary; Python API returns structured findings.
