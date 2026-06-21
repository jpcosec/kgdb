---
id: routine-task-provenance-fr-1-ingest-canonical-source-catalog
status: active
entrypoint: checklist-task-provenance-fr-1-ingest-canonical-source-catalog-execution-ready
decomposition:
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-execution-ready
- operator-task-provenance-fr-1-ingest-canonical-source-catalog-activate
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-testing-ready
- operator-task-provenance-fr-1-ingest-canonical-source-catalog-ready-for-testing
- checklist-task-provenance-fr-1-ingest-canonical-source-catalog-closeout-ready
- operator-task-provenance-fr-1-ingest-canonical-source-catalog-close
edges:
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-execution-to-activate
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-activate-to-testing
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-testing-to-ready
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-ready-to-closeout
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-closeout-to-close
- edge-task-provenance-fr-1-ingest-canonical-source-catalog-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Provenance FR-1: ingest canonical source catalog

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Provenance FR-1: ingest canonical source catalog.
