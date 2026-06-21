---
id: routine-task-provenance-fr-6-detect-orphan-atoms
status: active
entrypoint: checklist-task-provenance-fr-6-detect-orphan-atoms-execution-ready
decomposition:
- checklist-task-provenance-fr-6-detect-orphan-atoms-execution-ready
- operator-task-provenance-fr-6-detect-orphan-atoms-activate
- checklist-task-provenance-fr-6-detect-orphan-atoms-testing-ready
- operator-task-provenance-fr-6-detect-orphan-atoms-ready-for-testing
- checklist-task-provenance-fr-6-detect-orphan-atoms-closeout-ready
- operator-task-provenance-fr-6-detect-orphan-atoms-close
edges:
- edge-task-provenance-fr-6-detect-orphan-atoms-execution-to-activate
- edge-task-provenance-fr-6-detect-orphan-atoms-activate-to-testing
- edge-task-provenance-fr-6-detect-orphan-atoms-testing-to-ready
- edge-task-provenance-fr-6-detect-orphan-atoms-ready-to-closeout
- edge-task-provenance-fr-6-detect-orphan-atoms-closeout-to-close
- edge-task-provenance-fr-6-detect-orphan-atoms-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-6: detect orphan atoms

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-6: detect orphan atoms.
