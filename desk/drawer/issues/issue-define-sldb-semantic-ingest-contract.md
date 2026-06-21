# Define SLDB semantic ingest contract

## Kind

feature

## Status

open

## Problem

KGDB declares consumption of `sldb_document_payload`, but SLDB's useful graph inputs now include more than raw document payloads: model semantics, document semantic tags, semantic DAG prefix edges, equivalences, document indexes, section context records, and store hashes.

## Desired Outcome

Define a versioned contract for ingesting SLDB semantic artifacts into KGDB without forcing KGDB to understand SLDB internals or reimplement SLDB semantic search.

## Candidate Payload Shape

```yaml
store:
  path: .sldb
  root: /path/to/project
models:
  - name: AtomDoc
    semantics:
      - type.knowledge.atom
documents:
  - name: atom-example
    model: AtomDoc
    path: desk/atoms/example.md
    semantic_tags:
      - topic:atoms
sections:
  - document: atom-example
    path: answer
    title: Answer
semantic_dag:
  nodes:
    - id: type.knowledge.atom
      parents:
        - type.knowledge
  equivalences: {}
```

## Questions

- Should the ingest contract be owned by SLDB, KGDB, or a shared ecosystem contract package?
- Should KGDB preserve SLDB hashes as graph provenance metadata?
- Which relations should be generated: `has_model`, `has_document`, `has_section`, `tagged_as`, `semantic_parent`, `semantic_equivalent`?
- Should the contract support source files in the same payload, or should source files come from deskops/hum adapters?
