---
id: routine-task-provenance-fr-3-parse-atom-provenance-declarations
status: active
entrypoint: checklist-task-provenance-fr-3-parse-atom-provenance-declarations-execution-ready
decomposition:
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-execution-ready
- operator-task-provenance-fr-3-parse-atom-provenance-declarations-activate
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-testing-ready
- operator-task-provenance-fr-3-parse-atom-provenance-declarations-ready-for-testing
- checklist-task-provenance-fr-3-parse-atom-provenance-declarations-closeout-ready
- operator-task-provenance-fr-3-parse-atom-provenance-declarations-close
edges:
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-execution-to-activate
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-activate-to-testing
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-testing-to-ready
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-ready-to-closeout
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-closeout-to-close
- edge-task-provenance-fr-3-parse-atom-provenance-declarations-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-3: parse atom provenance declarations

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-3: parse atom provenance declarations.
