---
id: routine-task-provenance-fr-5-detect-unknown-source-ids
status: active
entrypoint: checklist-task-provenance-fr-5-detect-unknown-source-ids-execution-ready
decomposition:
- checklist-task-provenance-fr-5-detect-unknown-source-ids-execution-ready
- operator-task-provenance-fr-5-detect-unknown-source-ids-activate
- checklist-task-provenance-fr-5-detect-unknown-source-ids-testing-ready
- operator-task-provenance-fr-5-detect-unknown-source-ids-ready-for-testing
- checklist-task-provenance-fr-5-detect-unknown-source-ids-closeout-ready
- operator-task-provenance-fr-5-detect-unknown-source-ids-close
edges:
- edge-task-provenance-fr-5-detect-unknown-source-ids-execution-to-activate
- edge-task-provenance-fr-5-detect-unknown-source-ids-activate-to-testing
- edge-task-provenance-fr-5-detect-unknown-source-ids-testing-to-ready
- edge-task-provenance-fr-5-detect-unknown-source-ids-ready-to-closeout
- edge-task-provenance-fr-5-detect-unknown-source-ids-closeout-to-close
- edge-task-provenance-fr-5-detect-unknown-source-ids-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-5: detect unknown source IDs

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-5: detect unknown source IDs.
