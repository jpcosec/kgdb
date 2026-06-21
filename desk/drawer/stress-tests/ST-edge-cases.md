# ST-edge-cases: kgdb edge cases and error handling

**Basado en:** UC-01, UC-02, UC-03

## Script

```bash
# 1. --graph con path relativo vs absoluto
kgdb list --graph desk/fixtures/substrate_v1.json
kgdb list --graph $(pwd)/desk/fixtures/substrate_v1.json

# 2. --graph con path que no existe
kgdb list --graph /tmp/nonexistent

# 3. --graph con directorio (no archivo)
kgdb list --graph desk/fixtures/

# 4. --node con string vacío
kgdb get --graph desk/fixtures/substrate_v1.json --node ""

# 5. --node con ID muy largo
LONG_ID=$(python3 -c "print('a' * 10000)")
kgdb get --graph desk/fixtures/substrate_v1.json --node "$LONG_ID"

# 6. Flag duplicado
kgdb list --graph desk/fixtures/substrate_v1.json --graph /tmp/other.json

# 7. Help consistency: -h vs --help vs sin args
kgdb -h
kgdb --help
kgdb 2>&1 | head -5

# 8. Subcomando sin args
kgdb get
kgdb list
kgdb query
kgdb edges
kgdb ingest

# 9. Output redirection: stdout vs stderr
kgdb list --graph desk/fixtures/substrate_v1.json 2>/dev/null   # solo stdout
kgdb list --graph desk/fixtures/substrate_v1.json >/dev/null     # solo stderr

# 10. Subcomando desconocido
kgdb unknown-command

# 11. Flag desconocido
kgdb list --unknown-flag

# 12. Environment: HOME=/nonexistent
HOME=/nonexistent kgdb list --graph desk/fixtures/substrate_v1.json

# 13. Archivo de grafo muy grande (performance)
# Nota: generar un archivo grande con muchos nodos
python3 -c "
import json
nodes = []
for i in range(10000):
    nodes.append({
        'identity': {'node_id': f'node-{i:05d}', 'node_type': 'test'},
        'edges': [{'target_id': f'node-{(i+1)%10000:05d}', 'relation_type': 'test_edge', 'metadata': {}}],
        'facets': {}
    })
with open('/tmp/large-graph.json', 'w') as f:
    json.dump({'version': '1.0', 'nodes': nodes, 'metadata': {}}, f)
"
time kgdb list --graph /tmp/large-graph.json
time kgdb get --graph /tmp/large-graph.json --node node-05000

# 14. UTF-8 en node IDs
python3 -c "
import json
with open('/tmp/utf8-graph.json', 'w') as f:
    json.dump({
        'version': '1.0',
        'nodes': [{
            'identity': {'node_id': 'nodo-ñoño-🎉', 'node_type': 'test'},
            'edges': [],
            'facets': {}
        }],
        'metadata': {}
    }, f)
"
kgdb list --graph /tmp/utf8-graph.json
kgdb get --graph /tmp/utf8-graph.json --node 'nodo-ñoño-🎉'
kgdb edges --graph /tmp/utf8-graph.json --node 'nodo-ñoño-🎉'
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Path relativo y absoluto producen mismo resultado? |
| 2 | ¿Error claro? |
| 3 | ¿Error: "is a directory"? |
| 4 | ¿Error: empty ID? ¿O intenta buscar ""? |
| 5 | ¿Error manejado o crash? |
| 6 | ¿Error: duplicate flag? ¿O el último gana? |
| 7 | ¿-h y --help son idénticos? ¿Sin args muestra help o error? |
| 8 | ¿Error argparse claro para cada subcomando? |
| 9 | ¿Los mensajes de error van a stderr? ¿Los mensajes normales a stdout? |
| 10 | ¿Error: "unknown command"? |
| 11 | ¿Error: "unrecognized arguments"? |
| 12 | ¿Crash o funciona sin HOME? |
| 13 | ¿Performance aceptable? ¿Progreso? ¿Se cuelga? |
| 14 | ¿Soporta UTF-8 en node IDs? |

## Modos de fracaso

- Error messages a stdout en vez de stderr
- Paths relativos no resueltos correctamente
- IDs muy largos crashean en vez de truncarse
- UTF-8 en IDs produce error de encoding
- Performance pésima con 10K nodos (sin indicador de progreso)
