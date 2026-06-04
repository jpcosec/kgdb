---
id: '009'
domain: contract
status: open
priority: p0
depends_on: ['008']
created: '2026-06-04'
---

# Define SLDB semantic ingest contract

## Objective

Define a versioned KGDB input contract for SLDB semantic artifacts: models, documents, semantic tags, semantic DAG nodes, equivalences, sections, hashes, and provenance.

## Reference

- Issue: `desk/drawer/issues/issue-define-sldb-semantic-ingest-contract.md`

## What to Fix

- `contracts/schemas/sldb_document_payload.schema.json` is currently unconstrained.
- KGDB declares SLDB consumption but has no contract for SLDB's current semantic layer.

## How to Do It

- Define the minimal semantic ingest payload shape.
- Decide which relations KGDB generates from SLDB artifacts.
- Update `contracts/integration.contract.yaml` if the consumed contract name changes.
- Add a JSON Schema and fixture.

## Validation

- Schema validation for the fixture.
- `pytest`
