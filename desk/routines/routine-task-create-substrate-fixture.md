---
id: routine-task-create-substrate-fixture
status: active
entrypoint: checklist-task-create-substrate-fixture-execution-ready
decomposition:
- checklist-task-create-substrate-fixture-execution-ready
- operator-task-create-substrate-fixture-activate
- checklist-task-create-substrate-fixture-testing-ready
- operator-task-create-substrate-fixture-ready-for-testing
- checklist-task-create-substrate-fixture-closeout-ready
- operator-task-create-substrate-fixture-close
edges:
- edge-task-create-substrate-fixture-execution-to-activate
- edge-task-create-substrate-fixture-activate-to-testing
- edge-task-create-substrate-fixture-testing-to-ready
- edge-task-create-substrate-fixture-ready-to-closeout
- edge-task-create-substrate-fixture-closeout-to-close
- edge-task-create-substrate-fixture-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Create substrate fixture

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Create substrate fixture.
