# Fix test import path for local pytest

## Kind

bug

## Status

fixed-pending-closeout

## Problem

Running `pytest` from the KGDB repo root fails during collection with `ModuleNotFoundError: No module named 'kgdb'` because the `src/` package is not on the import path unless the package is installed or `PYTHONPATH=src` is supplied.

## Expected Behavior

Local `pytest` should collect and run tests from a fresh checkout using the documented repository setup.

## Actual Behavior

`pytest` collected 0 items and raised import errors in `tests/test_ingest.py`, `tests/test_integration.py`, and `tests/test_query.py`.

## Questions

- Should the fix be documented setup (`pip install -e .`) or pyproject pytest configuration that adds `src` to the path?
- Should CI enforce the same command developers are expected to run locally?

## Context

This was observed while evaluating KGDB as the NetworkX-backed graph substrate for deskops knowledge graph integration.
