---
id: '007'
domain: testing
status: ready_for_closeout
priority: p0
depends_on: []
created: '2026-06-04'
---

# Stabilize local test workflow

## Objective

Make `pytest` work from a fresh KGDB checkout without manual path guessing, then fix fixture path assumptions so the existing ingest/query tests prove the graph substrate reliably.

## Reference

- Board: `desk/tasks/Board.md`
- Issues:
  - `desk/drawer/issues/issue-fix-test-import-path-for-local-pytest.md`
  - `desk/drawer/issues/issue-fix-fixture-paths-in-tests.md`

## What to Fix

- Plain `pytest` fails with `ModuleNotFoundError: No module named 'kgdb'`.
- `PYTHONPATH=src pytest` collects tests but fails because tests reference `kgdb/desk/fixtures/substrate_v1.json` from the repo root.

## How to Do It

- Decide whether local setup uses `pip install -e .` documentation or pytest configuration that adds `src` to the import path.
- Resolve fixtures relative to the test file or repo root consistently.
- Keep test commands documented in README or desk standards.

## Validation

- `pytest`
- `kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-substrate.kg.json`

## Handoff

- Implementation and validation were completed by a subagent on 2026-06-04.
- `pytest` passed with `4 passed`.
- Manual ingest smoke passed after installing this checkout in editable mode.
- The task remains `ready_for_closeout` because no dedicated closing commit has been made.
