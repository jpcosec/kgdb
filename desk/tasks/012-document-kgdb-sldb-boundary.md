---
id: '012'
domain: docs
status: open
priority: p1
depends_on: ['010']
created: '2026-06-04'
---

# Document KGDB SLDB boundary

## Objective

Update KGDB documentation so users understand that KGDB runs in parallel with SLDB: SLDB owns semantic document truth, while KGDB owns graph persistence and traversal.

## Reference

- Issue: `desk/drawer/issues/issue-refactor-kgdb-to-parallel-sldb-semantic-layer.md`

## What to Document

- KGDB purpose and non-goals.
- SLDB semantic ingest contract.
- How to export from SLDB and ingest into KGDB.
- How downstream tools query KGDB without bypassing SLDB's semantic ownership.

## Validation

- README examples match actual CLI behavior.
- `pytest`
