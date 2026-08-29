---
kind: suggestion
sender_project: graph_ui
created_at: 2026-08-28T22:11:00
status: open
---

# Relation-as-first-class + express gemini_test flow view as a lens over kgdb

Origen: análisis de arquitectura en graph_ui. Specs en
`graph_ui/desk/drawer/RELATION_MODEL_LAYER_SPEC.md` y
`graph_ui/desk/drawer/PROJECTION_LAYERING_SPEC.md`; atoms
`atom-relations-are-their-own-content-blind-sldb-model-not-fields-inside-content`,
`atom-projection-is-layered-sldb-is-content-kgdb-is-graph-overlay-is-view`.

## Contexto de capas

sldb-content (qué es) -> sldb-relation (qué conecta con qué, content-blind) ->
kgdb (ensambla nodos ∪ aristas en GraphSnapshot) -> overlay (lente visual). Cada
capa ignora el interior de la siguiente.

## Dos piezas para kgdb

### 1. kgdb como ensamblador puro (baja de rango desde "materializador")

Hoy `kgdb/ingest/sldb.py` re-parsea campos-texto (`allowed_transitions`) para
materializar aristas. Con el modelo de relación autorado en sldb, kgdb solo
ensambla: node-docs ∪ edge-docs = GraphSnapshot. Además, `KnowledgeNode` tiene
facetas sesgadas a code-wiki (`ast`, `git`, `test_map`, `compliance`, `adr`)
que son inertes para dominios no-código; conviene decidir si se abren
(`identity + edges + semantics`) o se registran por dominio. Tensión abierta:
integridad referencial de aristas colgantes (validar en ensamblado).

### 2. Probar la gramática: flow view de gemini_test como lente sobre kgdb

gemini_test resuelve proyección con 3 lentes hardcodeados server-side
(`/api/taxonomy` por tags, `/api/viz/graph` por embeddings+PCA, `/api/flow` por
transiciones). Tomar `/api/flow` (la más limpia, ya es grafo declarado vía
`allowed_transitions`) y expresarla como vista declarativa sobre un
`GraphSnapshot` de kgdb: filtro por `relation_type=flows_to`, layout dirigido,
encoding por `kind`. Objetivo: igualar el output del endpoint bespoke SIN código
de vista server-side, validando que la gramática de proyección reemplaza los
lentes hardcodeados.

## Nota de dependencia

La pieza (2) necesita que ConversationStep esté disponible como node type en
graph_ui (ya resuelto: build-time generator sldb-model -> NodeTypeDefinition,
commit 8123184 en graph_ui) y un export sldb->GraphSnapshot real. GUARDRAIL: sin
mocks — requiere GraphSnapshot real, no fixtures fabricados.
