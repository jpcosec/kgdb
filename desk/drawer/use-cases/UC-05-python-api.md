# UC-05: Python API usage

El usuario quiere usar kgdb como librería Python, no solo como CLI. Quiere cargar grafos, inspeccionar nodos, y ejecutar queries programáticamente.

## Pasos

1. Importar `GraphSnapshot`, `KnowledgeNode`, `StructuredQuery` desde `kgdb.contracts`
2. Cargar un archivo JSON de grafo como `GraphSnapshot`
3. Inspeccionar nodos, edges, metadata
4. Construir y ejecutar una `StructuredQuery` programáticamente
5. Usar `sldb_semantic_export_to_snapshot` desde `kgdb.ingest`

## Preguntas de estrés

- ¿Los modelos Pydantic son importables directamente?
- ¿`GraphSnapshot.model_validate_json()` carga grafos desde JSON correctamente?
- ¿Hay `__init__.py` que exporte los símbolos públicos?
- ¿La jerarquía de imports es intuitiva?
- ¿La función `sldb_semantic_export_to_snapshot` tiene tipo de retorno documentado?
