---
id: '010'
domain: ingest
status: open
priority: p1
depends_on: ['009']
created: '2026-06-04'
---

# Implement SLDB semantic ingest

## Objective

Implement a KGDB ingest path that converts the SLDB semantic ingest contract into a KGDB graph using NetworkX-backed storage.

## Reference

- Issue: `desk/drawer/issues/issue-implement-sldb-document-payload-consumption.md`
- Issue: `desk/drawer/issues/issue-refactor-kgdb-to-parallel-sldb-semantic-layer.md`

## What to Fix

- KGDB has generic graph ingest but no SLDB-specific import path.
- SLDB semantic tags and DAG/index data are not represented as graph nodes/edges.

## How to Do It

- Add import/conversion code from SLDB semantic payload to `GraphSnapshot` or direct graph output.
- Add CLI support if appropriate, for example `kgdb ingest-sldb --input <payload> --output <graph>`.
- Preserve source provenance and hashes as metadata.

## Validation

- Fixture-based ingest test.
- Query test proving documents can be found through semantic tags.
- `pytest`
