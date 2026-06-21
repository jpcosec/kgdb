---
id: routine-task-provenance-fr-4-emit-typed-provenance-edges
status: active
entrypoint: checklist-task-provenance-fr-4-emit-typed-provenance-edges-execution-ready
decomposition:
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-execution-ready
- operator-task-provenance-fr-4-emit-typed-provenance-edges-activate
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-testing-ready
- operator-task-provenance-fr-4-emit-typed-provenance-edges-ready-for-testing
- checklist-task-provenance-fr-4-emit-typed-provenance-edges-closeout-ready
- operator-task-provenance-fr-4-emit-typed-provenance-edges-close
edges:
- edge-task-provenance-fr-4-emit-typed-provenance-edges-execution-to-activate
- edge-task-provenance-fr-4-emit-typed-provenance-edges-activate-to-testing
- edge-task-provenance-fr-4-emit-typed-provenance-edges-testing-to-ready
- edge-task-provenance-fr-4-emit-typed-provenance-edges-ready-to-closeout
- edge-task-provenance-fr-4-emit-typed-provenance-edges-closeout-to-close
- edge-task-provenance-fr-4-emit-typed-provenance-edges-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-4: emit typed provenance edges

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-4: emit typed provenance edges.
