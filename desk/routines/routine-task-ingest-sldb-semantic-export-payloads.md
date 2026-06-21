---
id: routine-task-ingest-sldb-semantic-export-payloads
status: active
entrypoint: checklist-task-ingest-sldb-semantic-export-payloads-execution-ready
decomposition:
- checklist-task-ingest-sldb-semantic-export-payloads-execution-ready
- operator-task-ingest-sldb-semantic-export-payloads-activate
- checklist-task-ingest-sldb-semantic-export-payloads-testing-ready
- operator-task-ingest-sldb-semantic-export-payloads-ready-for-testing
- checklist-task-ingest-sldb-semantic-export-payloads-closeout-ready
- operator-task-ingest-sldb-semantic-export-payloads-close
edges:
- edge-task-ingest-sldb-semantic-export-payloads-execution-to-activate
- edge-task-ingest-sldb-semantic-export-payloads-activate-to-testing
- edge-task-ingest-sldb-semantic-export-payloads-testing-to-ready
- edge-task-ingest-sldb-semantic-export-payloads-ready-to-closeout
- edge-task-ingest-sldb-semantic-export-payloads-closeout-to-close
- edge-task-ingest-sldb-semantic-export-payloads-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Ingest SLDB semantic-export payloads

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Ingest SLDB semantic-export payloads.
