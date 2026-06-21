# ST-api: Python API — GraphSnapshot, KnowledgeNode, StructuredQuery

**Basado en:** UC-05

## Script

```bash
# 1. Import and inspect GraphSnapshot
python3 -c "
from kgdb.contracts.io import GraphSnapshot
print('GraphSnapshot fields:', list(GraphSnapshot.model_fields.keys()))
snapshot = GraphSnapshot.model_validate_json(open('desk/fixtures/substrate_v1.json').read())
print(f'Nodes: {len(snapshot.nodes)}')
print(f'Version: {snapshot.version}')
node = snapshot.nodes[0]
print(f'First node: {node.identity.node_id} ({node.identity.node_type})')
print(f'Edges: {len(node.edges)}')
print(f'Facets present: semantics={node.semantics is not None}, ast={node.ast is not None}')
# Check that model_dump roundtrips
dumped = snapshot.model_dump(mode='json')
import json
reloaded = GraphSnapshot.model_validate(dumped)
print(f'Roundtrip OK: {len(reloaded.nodes)} nodes')
"

# 2. Create a KnowledgeNode from scratch
python3 -c "
from kgdb.contracts.node import KnowledgeNode
from kgdb.contracts.base import SystemIdentity, Edge
node = KnowledgeNode(
    identity=SystemIdentity(node_id='test://manual', node_type='test'),
    edges=[Edge(target_id='test://other', relation_type='depends_on')],
)
print(f'Created node: {node.identity.node_id}')
print(f'Edge: {node.edges[0].target_id} ({node.edges[0].relation_type})')
# Serialize
raw = node.model_dump(mode='json')
print(f'JSON keys: {list(raw.keys())}')
"

# 3. Create and execute a StructuredQuery via Python
python3 -c "
from kgdb.query.language import StructuredQuery, FacetFilter, FieldCondition
from kgdb.query.executor import execute_query
from kgdb.graph.utils import load_graph
from pathlib import Path

# First ingest to get node-link format
import subprocess, json
subprocess.run(['kgdb', 'ingest', '--input', 'desk/fixtures/substrate_v1.json', '--output', '/tmp/api-test-graph.json'], check=True)

graph = load_graph(Path('/tmp/api-test-graph.json'))
print(f'Graph loaded: {len(graph.nodes)} nodes, {len(graph.edges)} edges')

query = StructuredQuery(
    filters=[FacetFilter(
        facet='identity',
        conditions=[FieldCondition(field='node_type', op='eq', value='system')]
    )]
)
results = execute_query(graph, query)
print(f'Query results: {len(results)} nodes')
for n in results:
    print(f'  - {n.identity.node_id}')
"

# 4. StructuredQuery with scope
python3 -c "
from kgdb.query.language import StructuredQuery, GraphScope
from kgdb.query.executor import execute_query
from kgdb.graph.utils import load_graph
from pathlib import Path

graph = load_graph(Path('/tmp/api-test-graph.json'))
query = StructuredQuery(
    scope=GraphScope(descendant_of='system:ecosystem'),
    filters=[]
)
results = execute_query(graph, query)
print(f'Descendants of system:ecosystem: {len(results)} nodes')
for n in results:
    print(f'  - {n.identity.node_id} ({n.identity.node_type})')
"

# 5. Invalid query — nonexistent condition field
python3 -c "
from kgdb.query.language import StructuredQuery, FacetFilter, FieldCondition
try:
    query = StructuredQuery(
        filters=[FacetFilter(
            facet='identity',
            conditions=[FieldCondition(field='imaginary_field', op='eq', value='x')]
        )]
    )
    print('Validation passed (unexpected)')
except Exception as e:
    print(f'Validation error: {type(e).__name__}: {e}')
"

# 6. GraphSnapshot with empty nodes list
python3 -c "
from kgdb.contracts.io import GraphSnapshot
snapshot = GraphSnapshot(nodes=[])
print(f'Empty snapshot: {len(snapshot.nodes)} nodes, version={snapshot.version}')
raw = snapshot.model_dump(mode='json')
print(f'JSON: {json.dumps(raw)}')
import json
"

# 7. KnowledgeNode with all facets
python3 -c "
from kgdb.contracts.node import KnowledgeNode, FacetPayload
from kgdb.contracts.base import SystemIdentity
node = KnowledgeNode(
    identity=SystemIdentity(node_id='full://test', node_type='test'),
    semantics=FacetPayload(raw_docstring='Test node'),
    adr=FacetPayload(status='accepted'),
)
print(f'Semantics: {node.semantics.model_dump()}')
print(f'ADR: {node.adr.model_dump()}')
"

# 8. StructuredQuery with unsupported operator
python3 -c "
from kgdb.query.language import StructuredQuery, FacetFilter, FieldCondition
query = StructuredQuery(
    filters=[FacetFilter(
        facet='identity',
        conditions=[FieldCondition(field='node_type', op='regex', value='sys.*')]
    )]
)
# This validates at schema level but may fail at execution
from kgdb.query.executor import execute_query
from kgdb.graph.utils import load_graph
from pathlib import Path

graph = load_graph(Path('/tmp/api-test-graph.json'))
try:
    results = execute_query(graph, query)
    print(f'Regex query returned {len(results)} results')
except Exception as e:
    print(f'Regex query failed: {type(e).__name__}: {e}')
"

# 9. Cleanup
rm -f /tmp/api-test-graph.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿GraphSnapshot carga correctamente? ¿Todos los campos están presentes? |
| 2 | ¿Creación manual de KnowledgeNode funciona? ¿Campos opcionales? |
| 3 | ¿StructuredQuery ejecutable desde Python? ¿Resultados correctos? |
| 4 | ¿Scope queries funcionan desde Python API? |
| 5 | ¿Validación de campos inexistentes? ¿Error claro? |
| 6 | ¿Snapshot vacío manejable? |
| 7 | ¿FacetPayload funciona como dict abierto? |
| 8 | ¿Operador no soportado produce error manejado? |
| 9 | ¿Roundtrip JSON serialization consistente? |

## Modos de fracaso

- Python API no se puede importar (broken imports)
- GraphSnapshot no carga fixtures conocidos (schema mismatch)
- StructuredQuery validation no existe o es muy permisiva
- FacetPayload como dict abierto produce comportamientos sorprendentes
- No hay documentación de la Python API (solo contracts)
- Roundtrip serialization pierde datos
