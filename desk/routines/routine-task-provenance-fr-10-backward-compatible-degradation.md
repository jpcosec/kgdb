---
id: routine-task-provenance-fr-10-backward-compatible-degradation
status: active
entrypoint: checklist-task-provenance-fr-10-backward-compatible-degradation-execution-ready
decomposition:
- checklist-task-provenance-fr-10-backward-compatible-degradation-execution-ready
- operator-task-provenance-fr-10-backward-compatible-degradation-activate
- checklist-task-provenance-fr-10-backward-compatible-degradation-testing-ready
- operator-task-provenance-fr-10-backward-compatible-degradation-ready-for-testing
- checklist-task-provenance-fr-10-backward-compatible-degradation-closeout-ready
- operator-task-provenance-fr-10-backward-compatible-degradation-close
edges:
- edge-task-provenance-fr-10-backward-compatible-degradation-execution-to-activate
- edge-task-provenance-fr-10-backward-compatible-degradation-activate-to-testing
- edge-task-provenance-fr-10-backward-compatible-degradation-testing-to-ready
- edge-task-provenance-fr-10-backward-compatible-degradation-ready-to-closeout
- edge-task-provenance-fr-10-backward-compatible-degradation-closeout-to-close
- edge-task-provenance-fr-10-backward-compatible-degradation-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-10: backward-compatible degradation

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-10: backward-compatible degradation.
