# Conventions

- Keep KGDB semantically dumb: accept/store/query graph records, but do not infer ontology, reason over terms, or hardcode downstream project semantics.
- Contracts are Pydantic v2 models; favor explicit `Field` descriptions and small validators for coercion/shape validation.
- `KnowledgeNode` facets use `FacetPayload` with `extra="allow"` to preserve downstream metadata without KGDB understanding it.
- Graph persistence stores node attributes `type`, `status`, and full `schema`; edges store `relation` and `metadata`.
- Tests resolve fixtures from test file/repo root, not package-relative paths.
- Desk tasks should not be marked closed unless explicitly asked; task status can remain as-is even after implementation handoff.