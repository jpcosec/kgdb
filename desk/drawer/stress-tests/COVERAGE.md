# COVERAGE.md: kgdb stress-test coverage plan

## CLI surfaces

| Comando | ST | Estado |
|---------|----|--------|
| `kgdb get` | ST-get | executed |
| `kgdb list` | ST-list | executed |
| `kgdb query` | ST-query | executed |
| `kgdb edges` | ST-edges | executed |
| `kgdb ingest` | ST-ingest | executed |
| `kgdb ingest-sldb` | ST-ingest-sldb | executed |
| Graph snapshots (formatos, versiones) | ST-snapshots | executed |
| Contracts y fixtures | ST-contracts | executed |
| Edge cases (performance, UTF-8, paths) | ST-edge-cases | executed |

## Use-cases cubiertos

| UC | Narrativa | STs que lo cubren |
|----|-----------|-------------------|
| UC-01 | Explorar un grafo | ST-get, ST-list, ST-edges, ST-snapshots |
| UC-02 | Ingestar datos | ST-ingest, ST-ingest-sldb, ST-snapshots, ST-contracts |
| UC-03 | Query un grafo | ST-query |
| UC-04 | Validación de contratos | ST-contracts |
| UC-05 | Python API | ST-api |
| UC-06 | Edge traversal | ST-edges |

## Superficies cubiertas (round-01)

| Superficie | ST | Estado |
|------------|----|--------|
| Python API (GraphSnapshot, KnowledgeNode, StructuredQuery) | ST-api | seed |
| Query server (REPL mode) | ST-query-server | seed |
| PersistenceEntry / TransactionManifest | ST-persistence | seed |
| Integration tests (end-to-end) | ST-integration | seed |
| Entry points: kgdb vs python -m kgdb | ST-entry-points | seed |

## Superficies futuras (no cubiertas)

| Superficie | Por qué | Prioridad |
|------------|---------|-----------|
| (ninguna actualmente) | | |
<!-- 
Template for adding more STs:
| `kgdb <comando>` | ST-XXX | seed/executed/complete |
-->
