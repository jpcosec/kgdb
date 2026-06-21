---
kind: suggestion
sender_project: deskops
created_at: 2026-06-14T00:00:00
status: open
---

# Stabilize graph snapshot validation

Deskops `graph build` produces snapshots. Currently there is no validation that a snapshot file matches the expected KGDB contract schema before downstream tools consume it.

## Scope

- `kgdb snapshot validate <path>` — validate a snapshot JSON file against the registered graph contract
- Report specific violations: missing required fields, wrong types, unknown node/edge types
- Exit 0 if valid, non-zero with diagnostic list if invalid
- Python API: `validate_snapshot(path: Path) -> ValidationResult` with structured findings

## Motivation

Deskops needs to trust that graph snapshots are structurally valid before running `graph missing` or `graph trace` queries. KGDB owns the snapshot contract and validation.

## Done When

- Invalid snapshot (missing field, wrong type) produces specific error messages, not a JSON parse crash
- Valid snapshot exits 0 with a summary
- Python API returns structured findings
