---
kind: suggestion
sender_project: kgdb
created_at: 2026-06-19T00:30:03
status: open
---

# SLDB text-layer vs KGDB graph-layer ADR and summary

The SLDB repo now has two lengthy drawer documents that capture the architectural boundary discussion between SLDB as the structured text layer and KGDB as the graph layer. Please review these source notes for downstream KGDB boundary alignment and ingestion/export implications.\n\nSystem-rooted source paths:\n- /home/jp/proyectos/hum-ecosystem/tools/sldb/desk/drawer/summary-structured-text-and-layer-boundary.md\n- /home/jp/proyectos/hum-ecosystem/tools/sldb/desk/drawer/adr-sldb-text-layer-vs-kgdb-graph-layer.md\n\nThe summary explains the broader reasoning around structured text, document ASTs, addressability, query, composition, and knowledge codebases. The ADR formalizes the decision that SLDB should own canonical readable document structure, structural query, and textual recomposition, while KGDB should own graph-native traversal, equivalence, inference, and higher-order relational reasoning.\n\nThis message is intended as a durable cross-project handoff so KGDB can align its role with the exported-text-to-graph boundary rather than treating authored documents and graph truth as the same layer.
