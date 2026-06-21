# UC-04: Contract validation and integration

El usuario quiere verificar que los contratos entre kgdb, SLDB, y downstream tools se cumplen.
Esto incluye validar schemas JSON, fixtures de test, y el contrato de integración.

## Pasos

1. Validar que un archivo de grafo cumple con el schema `kgdb_graph_bundle.schema.json`
2. Validar que un export semántico de SLDB cumple con el schema de contrato
3. Verificar que las queries de ejemplo en `contracts/queries/sldb/` son válidas
4. Ejecutar queries de ejemplo contra un fixture de prueba

## Preguntas de estrés

- ¿Hay un comando `kgdb validate` o hay que hacerlo externamente con `jsonschema`?
- ¿Los schemas están actualizados? (vs los fixtures)
- ¿Los queries de ejemplo en contracts/ funcionan con los fixtures actuales?
- ¿El contrato de integración (`integration.contract.yaml`) está sincronizado con el código?
- ¿Hay tests que fallen por fixtures desactualizados?
