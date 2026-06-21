---
id: routine-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test
status: active
entrypoint: checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-execution-ready
decomposition:
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-execution-ready
- operator-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-activate
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-testing-ready
- operator-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-ready-for-testing
- checklist-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-closeout-ready
- operator-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-close
edges:
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-execution-to-activate
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-activate-to-testing
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-testing-to-ready
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-ready-to-closeout
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-closeout-to-close
- edge-task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Cross-repo SLDB export to KGDB ingest roundtrip test

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Cross-repo SLDB export to KGDB ingest roundtrip test.
