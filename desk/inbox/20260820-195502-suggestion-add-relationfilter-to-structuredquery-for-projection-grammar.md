---
kind: suggestion
sender_project: graph_ui
created_at: 2026-08-20T19:55:02
status: open
---

# Add RelationFilter to StructuredQuery for projection grammar

graph_ui's projection-grammar feature (graph_ui/desk/drawer/PROJECTION_GRAMMAR_SPEC.md section 3.2) needs an additive relation-type filter in kgdb's query language, which does not exist today (graph_ui atom-kgdb-s-query-language-has-no-relation-type-filter-yet).

Proposed additive change:
- New RelationFilter in src/kgdb/query/language.py: relation_types: list[VocabularyTerm] (allow-list, empty = all), direction: Literal['outgoing','incoming','both'] = 'both'.
- Add relations: list[RelationFilter] = Field(default_factory=list) to StructuredQuery.
- One new branch in src/kgdb/query/executor.py: after resolving the node set, filter edges by relation_type membership and direction.

Constraints:
- Keep kgdb domain-agnostic: filtering only, NO visual/encoding/layout.
- READ executor.py IN FULL before editing (NetworkX-backed); shape unverified vs executor internals (SPEC section 7 risk).
- Typed-relation reference: deskops/graph/extract_edges.py.

Validation: kgdb pytest proving allow-list, empty=all, and each direction.
Source of truth: graph_ui/desk/drawer/PROJECTION_GRAMMAR_SPEC.md section 3.2.
