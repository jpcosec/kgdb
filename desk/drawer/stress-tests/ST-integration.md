# ST-integration: End-to-end integration tests

**Basado en:** UC-01, UC-02, UC-03, UC-04

## Script

```bash
# 1. Run the existing integration test
python3 -m pytest tests/test_integration.py -v --no-header 2>&1

# 2. Full workflow: ingest → list → get → edges → query → ingest-sldb
echo "=== 2a. ingest ==="
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/e2e-ingested.json 2>&1

echo "=== 2b. list ==="
kgdb list --graph /tmp/e2e-ingested.json 2>&1

echo "=== 2c. get ==="
kgdb get --graph /tmp/e2e-ingested.json --node "repo://hum-ecosystem" 2>&1

echo "=== 2d. edges ==="
kgdb edges --graph /tmp/e2e-ingested.json --node "repo://hum-ecosystem" 2>&1

echo "=== 2e. query (simple filter) ==="
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "system"}]}]}' > /tmp/e2e-query.json
kgdb query --graph /tmp/e2e-ingested.json --query-file /tmp/e2e-query.json 2>&1

echo "=== 2f. ingest-sldb ==="
kgdb ingest-sldb --input contracts/fixtures/sldb_kgdb_semantic_export.v1.json --output /tmp/e2e-sldb.json 2>&1

echo "=== 2g. list SLDB ==="
kgdb list --graph /tmp/e2e-sldb.json 2>&1

# 3. Cross-format: use ingested SLDB as graph for query
echo "=== 3. Query on SLDB graph ==="
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "sldb_model"}]}]}' > /tmp/e2e-sldb-query.json
kgdb query --graph /tmp/e2e-sldb.json --query-file /tmp/e2e-sldb-query.json 2>&1

# 4. Graph constructed via Python API → ingested → queried
echo "=== 4. Python roundtrip ==="
python3 -c "
from kgdb.contracts.io import GraphSnapshot
from kgdb.contracts.node import KnowledgeNode
from kgdb.contracts.base import SystemIdentity, Edge
import json

snapshot = GraphSnapshot(nodes=[
    KnowledgeNode(identity=SystemIdentity(node_id='manual://a', node_type='manual'), edges=[Edge(target_id='manual://b', relation_type='connects')]),
    KnowledgeNode(identity=SystemIdentity(node_id='manual://b', node_type='manual')),
])
with open('/tmp/e2e-manual.json', 'w') as f:
    json.dump(snapshot.model_dump(mode='json'), f)
print('Created manual snapshot')
"
kgdb ingest --input /tmp/e2e-manual.json --output /tmp/e2e-manual-ingested.json 2>&1
kgdb list --graph /tmp/e2e-manual-ingested.json 2>&1
kgdb get --graph /tmp/e2e-manual-ingested.json --node "manual://a" 2>&1

# 5. Idempotency: double-check ingestion is deterministic
echo "=== 5. Idempotency ==="
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/e2e-idem-a.json 2>&1
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/e2e-idem-b.json 2>&1
diff /tmp/e2e-idem-a.json /tmp/e2e-idem-b.json && echo "Idempotent: OK" || echo "Idempotent: FAIL"

# 6. Contract compliance: does ingested graph match schema?
python3 -c "
import json, jsonschema
schema = json.load(open('contracts/schemas/kgdb_graph_bundle.schema.json'))
data = json.load(open('/tmp/e2e-ingested.json'))
try:
    jsonschema.validate(data, schema)
    print('Ingested graph valid against schema: OK')
except jsonschema.exceptions.ValidationError as e:
    print(f'Ingested graph schema validation: FAIL - {e.message}')
"

# 7. Error recovery: ingest on corrupted graph → does not leave broken file
echo "=== 7. Error recovery ==="
rm -f /tmp/e2e-recovery.json
echo 'corrupted' > /tmp/e2e-corrupt.json
kgdb ingest --input /tmp/e2e-corrupt.json --output /tmp/e2e-recovery.json 2>&1 || true
if [ -f /tmp/e2e-recovery.json ]; then
    echo "Partial output file exists (risky)"
else
    echo "No partial output: OK"
fi

# 8. Pipe consistency: list | get pipeline
echo "=== 8. Pipe consistency ==="
FIRST_ID=$(kgdb list --graph /tmp/e2e-ingested.json 2>/dev/null | python3 -c "import sys, json; ids=json.load(sys.stdin); print(ids[0])")
echo "First ID: $FIRST_ID"
kgdb get --graph /tmp/e2e-ingested.json --node "$FIRST_ID" 2>&1 | head -5

# 9. Cleanup
rm -f /tmp/e2e-*.json /tmp/manual*.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿test_integration.py pasa? |
| 2a-g | ¿Workflow completo funciona? |
| 3 | ¿Query funciona en grafo SLDB ingestado? |
| 4 | ¿Python API → ingest → CLI roundtrip? |
| 5 | ¿Ingest es idempotente? |
| 6 | ¿Ingested graph cumple schema? |
| 7 | ¿Partial output en errores de ingest? |
| 8 | ¿Pipe list → get funciona? |

## Modos de fracaso

- Ingest produce output que no valida contra schema
- Partial output en errores de ingest (archivo corrupto)
- Workflow completo requiere pasos no documentados
- Pipe list → get falla por difference de formato
- Python API no compatible con ingest (model_dump vs CLI)
