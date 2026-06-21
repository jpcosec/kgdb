# Implement SLDB document payload consumption

## Kind

feature

## Status

open

## Problem

`contracts/integration.contract.yaml` declares that KGDB consumes `sldb_document_payload`, but `contracts/schemas/sldb_document_payload.schema.json` is currently an unconstrained object and there is no code path that converts SLDB document payloads into graph records.

## Desired Outcome

Define and implement a minimal SLDB-to-KGDB ingestion path that can accept modeled documents and produce graph nodes/edges with source provenance.

## Questions

- Should SLDB emit graph-ready document payloads, or should KGDB parse SLDB indexes/doc payloads directly?
- Which SLDB fields are required: model name, document path, document id/name, fields, semantics, tracked hashes, section ids?
- Should source-file links be emitted by SLDB, deskops, or KGDB?
- Should the first integration target deskops `AtomDoc` and task/issue docs?

## Context

Deskops needs graph queries over atoms, docs, tasks, and source files. KGDB already declares the SLDB dependency but does not yet provide the integration bridge.
