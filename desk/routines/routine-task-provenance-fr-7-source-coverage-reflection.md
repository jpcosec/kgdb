---
id: routine-task-provenance-fr-7-source-coverage-reflection
status: active
entrypoint: checklist-task-provenance-fr-7-source-coverage-reflection-execution-ready
decomposition:
- checklist-task-provenance-fr-7-source-coverage-reflection-execution-ready
- operator-task-provenance-fr-7-source-coverage-reflection-activate
- checklist-task-provenance-fr-7-source-coverage-reflection-testing-ready
- operator-task-provenance-fr-7-source-coverage-reflection-ready-for-testing
- checklist-task-provenance-fr-7-source-coverage-reflection-closeout-ready
- operator-task-provenance-fr-7-source-coverage-reflection-close
edges:
- edge-task-provenance-fr-7-source-coverage-reflection-execution-to-activate
- edge-task-provenance-fr-7-source-coverage-reflection-activate-to-testing
- edge-task-provenance-fr-7-source-coverage-reflection-testing-to-ready
- edge-task-provenance-fr-7-source-coverage-reflection-ready-to-closeout
- edge-task-provenance-fr-7-source-coverage-reflection-closeout-to-close
- edge-task-provenance-fr-7-source-coverage-reflection-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-7: source coverage reflection

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-7: source coverage reflection.
