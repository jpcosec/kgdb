# ST-snapshots: kgdb graph snapshot formats and versions

**Basado en:** UC-01, UC-02

## Script

```bash
# 1. ¿Qué archivos de snapshot existen en .sldb/runtime/?
ls -la .sldb/runtime/

# 2. List sobre semantic_dag.yaml (formato YAML vs JSON)
kgdb list --graph .sldb/runtime/semantic_dag.yaml 2>&1 || echo "YAML not supported"

# 3. List sobre semantic_index.yaml
kgdb list --graph .sldb/runtime/semantic_index.yaml 2>&1 || echo "YAML not supported"

# 4. Inspeccionar el formato de un GraphSnapshot
python3 -c "
from kgdb.contracts.io import GraphSnapshot, QueryResult
print('GraphSnapshot fields:', list(GraphSnapshot.model_fields.keys()))
print('QueryResult fields:', list(QueryResult.model_fields.keys()))
"

# 5. Cargar un GraphSnapshot desde archivo JSON
python3 -c "
from kgdb.contracts.io import GraphSnapshot
snapshot = GraphSnapshot.model_validate_json(open('desk/fixtures/substrate_v1.json').read())
print(f'Nodes: {len(snapshot.nodes)}')
print(f'Version: {snapshot.version}')
print(f'Metadata: {snapshot.metadata}')
"

# 6. GraphSnapshot vacío
echo '{"version": "1.0", "nodes": [], "metadata": {}}' > /tmp/empty-snapshot.json
kgdb list --graph /tmp/empty-snapshot.json

# 7. Versión de schema no soportada
echo '{"version": "999.0", "nodes": [], "metadata": {}}' > /tmp/future-version.json
kgdb ingest --input /tmp/future-version.json --output /tmp/out.json

# 8. Snapshot sin campo version
echo '{"nodes": []}' > /tmp/no-version.json
kgdb ingest --input /tmp/no-version.json --output /tmp/out.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Qué archivos hay? ¿Son todos JSON o hay YAML? |
| 2 | ¿kgdb list soporta YAML? Si no, ¿error claro? |
| 3 | ¿Mismo comportamiento que semantic_dag.yaml? |
| 4 | ¿Los modelos Pydantic están actualizados? |
| 5 | ¿Carga correctamente? |
| 6 | ¿List vacío funciona? |
| 7 | ¿Error: unsupported version? |
| 8 | ¿Error: missing version field? |

## Modos de fracaso

- YAML format no soportado pero error confuso
- Versiones futuras no producen error claro
- Snapshot sin version produce Pydantic traceback en vez de mensaje user-friendly
- No hay comando para ver metadatos del snapshot (version, created_at, node count)
