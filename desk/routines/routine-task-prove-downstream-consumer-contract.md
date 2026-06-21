---
id: routine-task-prove-downstream-consumer-contract
status: active
entrypoint: checklist-task-prove-downstream-consumer-contract-execution-ready
decomposition:
- checklist-task-prove-downstream-consumer-contract-execution-ready
- operator-task-prove-downstream-consumer-contract-activate
- checklist-task-prove-downstream-consumer-contract-testing-ready
- operator-task-prove-downstream-consumer-contract-ready-for-testing
- checklist-task-prove-downstream-consumer-contract-closeout-ready
- operator-task-prove-downstream-consumer-contract-close
edges:
- edge-task-prove-downstream-consumer-contract-execution-to-activate
- edge-task-prove-downstream-consumer-contract-activate-to-testing
- edge-task-prove-downstream-consumer-contract-testing-to-ready
- edge-task-prove-downstream-consumer-contract-ready-to-closeout
- edge-task-prove-downstream-consumer-contract-closeout-to-close
- edge-task-prove-downstream-consumer-contract-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Prove downstream consumer contract

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Prove downstream consumer contract.
