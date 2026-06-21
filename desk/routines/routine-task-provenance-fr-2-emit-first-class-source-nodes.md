---
id: routine-task-provenance-fr-2-emit-first-class-source-nodes
status: active
entrypoint: checklist-task-provenance-fr-2-emit-first-class-source-nodes-execution-ready
decomposition:
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-execution-ready
- operator-task-provenance-fr-2-emit-first-class-source-nodes-activate
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-testing-ready
- operator-task-provenance-fr-2-emit-first-class-source-nodes-ready-for-testing
- checklist-task-provenance-fr-2-emit-first-class-source-nodes-closeout-ready
- operator-task-provenance-fr-2-emit-first-class-source-nodes-close
edges:
- edge-task-provenance-fr-2-emit-first-class-source-nodes-execution-to-activate
- edge-task-provenance-fr-2-emit-first-class-source-nodes-activate-to-testing
- edge-task-provenance-fr-2-emit-first-class-source-nodes-testing-to-ready
- edge-task-provenance-fr-2-emit-first-class-source-nodes-ready-to-closeout
- edge-task-provenance-fr-2-emit-first-class-source-nodes-closeout-to-close
- edge-task-provenance-fr-2-emit-first-class-source-nodes-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-2: emit first-class source nodes

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-2: emit first-class source nodes.
