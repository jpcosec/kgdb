# Changelog

## 2026-05-01

- resolved task `006-prove-downstream-consumer-contract`: 006-prove-downstream-consumer-contract

- resolved task `004-implement-minimal-query`: 004-implement-minimal-query

- resolved task `003-implement-minimal-ingest`: 003-implement-minimal-ingest

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- `load_graph` now produces GraphSnapshot format (task 007).
- User-facing errors no longer expose raw Python tracebacks (task 008).
- Ingest commands validate input before processing (task 009).
- UTF-8 output and exit codes are consistent across all commands (task 010).
- Help text describes flags, formats, and `--version` is available (task 011).

### Docs
- Snapshot validation and graph trace surface documented in `README.md`.
- CLI alignment standards and drift signals documented in `desk/STANDARDS.md`.

### Added
- Defined `PersistenceEntry` and `TransactionManifest` contracts in `kgdb.contracts.persistence` for ledger-based graph storage.
- Defined `GraphSnapshot` and `QueryResult` contracts in `kgdb.contracts.io`.
- Exported new contracts via `kgdb.contracts`.
- resolved task `005-create-substrate-fixture`: Created `kgdb/desk/fixtures/substrate_v1.json` representing the core ecosystem modules
- resolved task `007-stabilize-local-test-workflow`: Plain `pytest` now works from the repo root and tests resolve the substrate fixture deterministically.

### Added (Phase 5 — Provenance)
- Imported `kgdb-provenance-requirements.md` from `paper_IEEE/desk/registry/` into `desk/drawer/registry/` as the source of truth for Phase 5.
- Seeded 10 deskops tasks (one per functional requirement FR-1..FR-10) covering source catalog ingest, first-class source nodes, atom provenance parsing, typed edge emission, unknown-source detection, orphan-atom detection, source coverage reflection, snapshot contract inclusion, reflection output contract, and backward-compatible degradation.
- Added YAML frontmatter to `desk/tasks/Board.md` so the `BoardDoc` model accepts it; frontmatter `tasks:` list now routes the 16 active tasks and the 10 draft provenance tasks.

### Added (Phase 6 — Inbox + SLDB Boundary)
- Triaged the four `desk/inbox/` messages (3 deskops-suggested substrate surfaces + 1 SLDB cross-project ADR handoff).
- Seeded 7 deskops tasks to keep KGDB ready for incoming knowledge-codebase handoffs: snapshot validation CLI/API, relation serialization roundtrip + malformed-input handling, graph trace query surface CLI/API, SLDB semantic-export ingestion, SLDB structural provenance preservation, cross-repo SLDB→KGDB roundtrip test, and a KGDB boundary architecture doc.
- Board.md frontmatter `tasks:` list now routes all 23 active tasks; Phase 6 added to delivery phases and Active table.

### Refactored — Hand-written tasks converted to deskops schema
- Deleted the 6 hand-written 001-006 task files (referenced pills/contexts that no longer exist post-closeout; the actual work landed as kgdb/7-12 commits `b238115`, `3e8bc87`, `34ca82c`, `fcb6c4a`, `885ac42`).
- Re-created the substrate slice via `deskops add task` (slug-IDs `task-define-graph-io-contract`, `task-define-persistence-model`, `task-implement-minimal-ingest`, `task-implement-minimal-query`, `task-create-substrate-fixture`, `task-prove-downstream-consumer-contract`); all 23 active tasks are now registered in `.sldb` and tracked by deskops.
- Board.md Active table uses short domain codes (IO, PM, ING, QRY, FIX, INT, FR-1..FR-10, SV-1, RS-1, TR-1, SL-1..SL-3, BD-1) for readability since the new task IDs are slug-derived.

### Added — Atomic pills (15)
- Pills capture reusable atomic concepts; they are not 1-to-1 with tasks by design.
- Coverage: substrate-is-dumb, source-nodes-are-first-class, provenance-edges-are-typed, orphans-and-gaps-are-reflection-findings, snapshot-is-the-public-output-surface, trace-is-the-public-query-surface, relation-serialization-must-roundtrip, validation-findings-are-structured-not-crashes, sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow, provenance-survives-the-sldb-to-kgdb-handoff, backward-compatible-degradation-findings-not-failures, board-md-frontmatter-is-the-routing-truth, closed-tasks-are-deleted-not-marked, fixtures-are-consumer-contract-tests, kgdb-cli-is-the-stable-public-surface.
- Wired pill references into each task's `pills:` frontmatter via `deskops edit task` using JSON lists (the SLDB field-value parser requires real list values).
- Board.md frontmatter `pills:` list now routes the 15 pills; Active Pills table maps each pill to its applicable tasks.
