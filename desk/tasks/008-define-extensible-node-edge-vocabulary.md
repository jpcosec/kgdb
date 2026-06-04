---
id: '008'
domain: contract
status: open
priority: p0
depends_on: ['007']
created: '2026-06-04'
---

# Define extensible node edge vocabulary

## Objective

Replace or extend KGDB's hardcoded node and edge literals so downstream tools can use project-specific graph vocabularies without making KGDB a semantic reasoner.

## Reference

- Issue: `desk/drawer/issues/issue-support-deskops-node-and-edge-vocabulary.md`

## What to Fix

- `SystemIdentity.node_type` has a narrow fixed literal set.
- `Edge.relation_type` has a narrow fixed literal set.
- Deskops needs node kinds such as `atom`, `task`, `issue`, `sldb_model`, `source_file`, and `test_file`.
- Deskops needs relation roles such as `materializes`, `validates`, `invokes`, `routes`, `generated_from`, `source_for`, and `violates`.

## How to Do It

- Decide between broad strings, registered vocabularies, or generic relation types plus domain roles in metadata.
- Preserve validation hooks without hardcoding deskops-specific terms into KGDB core.
- Update graph bundle schema and tests.

## Validation

- Add a fixture containing downstream vocabulary terms.
- `pytest`
