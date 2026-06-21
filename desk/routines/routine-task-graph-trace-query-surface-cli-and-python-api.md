---
id: routine-task-graph-trace-query-surface-cli-and-python-api
status: active
entrypoint: checklist-task-graph-trace-query-surface-cli-and-python-api-execution-ready
decomposition:
- checklist-task-graph-trace-query-surface-cli-and-python-api-execution-ready
- operator-task-graph-trace-query-surface-cli-and-python-api-activate
- checklist-task-graph-trace-query-surface-cli-and-python-api-testing-ready
- operator-task-graph-trace-query-surface-cli-and-python-api-ready-for-testing
- checklist-task-graph-trace-query-surface-cli-and-python-api-closeout-ready
- operator-task-graph-trace-query-surface-cli-and-python-api-close
edges:
- edge-task-graph-trace-query-surface-cli-and-python-api-execution-to-activate
- edge-task-graph-trace-query-surface-cli-and-python-api-activate-to-testing
- edge-task-graph-trace-query-surface-cli-and-python-api-testing-to-ready
- edge-task-graph-trace-query-surface-cli-and-python-api-ready-to-closeout
- edge-task-graph-trace-query-surface-cli-and-python-api-closeout-to-close
- edge-task-graph-trace-query-surface-cli-and-python-api-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Graph trace query surface CLI and Python API

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Graph trace query surface CLI and Python API.
