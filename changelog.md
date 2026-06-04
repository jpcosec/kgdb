# Changelog

## 2026-05-01

- resolved task `006-prove-downstream-consumer-contract`: 006-prove-downstream-consumer-contract

- resolved task `004-implement-minimal-query`: 004-implement-minimal-query

- resolved task `003-implement-minimal-ingest`: 003-implement-minimal-ingest

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Defined `PersistenceEntry` and `TransactionManifest` contracts in `kgdb.contracts.persistence` for ledger-based graph storage.
- Defined `GraphSnapshot` and `QueryResult` contracts in `kgdb.contracts.io`.
- Exported new contracts via `kgdb.contracts`.
- resolved task `005-create-substrate-fixture`: Created `kgdb/desk/fixtures/substrate_v1.json` representing the core ecosystem modules
- resolved task `007-stabilize-local-test-workflow`: Plain `pytest` now works from the repo root and tests resolve the substrate fixture deterministically.
