---
id: routine-task-snapshot-validation-cli-and-python-api
status: active
entrypoint: checklist-task-snapshot-validation-cli-and-python-api-execution-ready
decomposition:
- checklist-task-snapshot-validation-cli-and-python-api-execution-ready
- operator-task-snapshot-validation-cli-and-python-api-activate
- checklist-task-snapshot-validation-cli-and-python-api-testing-ready
- operator-task-snapshot-validation-cli-and-python-api-ready-for-testing
- checklist-task-snapshot-validation-cli-and-python-api-closeout-ready
- operator-task-snapshot-validation-cli-and-python-api-close
edges:
- edge-task-snapshot-validation-cli-and-python-api-execution-to-activate
- edge-task-snapshot-validation-cli-and-python-api-activate-to-testing
- edge-task-snapshot-validation-cli-and-python-api-testing-to-ready
- edge-task-snapshot-validation-cli-and-python-api-ready-to-closeout
- edge-task-snapshot-validation-cli-and-python-api-closeout-to-close
- edge-task-snapshot-validation-cli-and-python-api-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Snapshot validation: CLI and Python API

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Snapshot validation: CLI and Python API.
