---
id: '011'
domain: query
status: open
priority: p1
depends_on: ['010']
created: '2026-06-04'
---

# Add semantic graph query examples

## Objective

Add query fixtures and CLI examples that prove KGDB can answer useful questions over SLDB-derived graph data.

## Reference

- Issue: `desk/drawer/issues/issue-refactor-kgdb-to-parallel-sldb-semantic-layer.md`

## Questions to Prove

- Which documents are tagged with a semantic concept?
- Which semantic tags are parents or equivalents of this tag?
- Which sections belong to a document?
- Which documents sit in the neighborhood of a model or semantic tag?

## How to Do It

- Add structured query examples for semantic nodes and document nodes.
- Add CLI invocation examples to README or docs.
- Keep KGDB behavior graph-oriented; do not add semantic judgment.

## Validation

- `pytest`
- Manual `kgdb query --graph <fixture> --query-file <query>` examples documented.
