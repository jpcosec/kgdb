# Fix fixture paths in tests

## Kind

bug

## Status

fixed-pending-closeout

## Problem

After setting `PYTHONPATH=src`, KGDB tests collect and run, but all four tests fail because they look for `kgdb/desk/fixtures/substrate_v1.json` relative to the repo root. The actual fixture path from the repo root is `desk/fixtures/substrate_v1.json`.

## Expected Behavior

Tests should locate fixtures reliably from the KGDB repository root or relative to the test file location.

## Actual Behavior

`PYTHONPATH=src pytest` collects 4 tests and all fail with `FileNotFoundError: kgdb/desk/fixtures/substrate_v1.json`.

## Questions

- Should tests resolve fixtures relative to `Path(__file__).parents[...]`?
- Should the fixture path be exposed as a shared test helper?
- Should CLI tests use absolute temp fixture paths rather than repo-relative paths?

## Context

This was observed while evaluating KGDB as the NetworkX-backed graph substrate for deskops knowledge graph integration.
