# UC-03: Querying a knowledge graph

El usuario tiene un grafo ingestado y quiere hacer consultas estructuradas: filtrar nodos por tipo, buscar subgrafos, encontrar vecinos semánticos.

## Pasos

1. Ejecutar una query guardada en archivo con `kgdb query --graph <file> --query-file <query.json>`
2. Probar diferentes tipos de scope (descendant_of, ancestor_of, node_id_prefix)
3. Probar filtros por facet (identity, semantics, ast, compliance, etc.)
4. Probar diferentes operadores (eq, ne, contains, starts_with, etc.)

## Preguntas de estrés

- ¿El formato del archivo de query está documentado en --help?
- ¿Qué pasa si el query file tiene JSON inválido?
- ¿Qué pasa si el query file tiene campos que no existen en el schema?
- ¿Los errores de validación de query son claros?
- ¿El output de query es utilizable (formato estructurado)?
- ¿Se pueden concatenar queries (pipe)?
- ¿Hay un formato de output legible por humanos vs machine-parseable?
