# ST-query-server: Query server REPL mode

**Basado en:** UC-03, UC-05

## Script

```bash
# 1. Check if the module can be imported
python3 -c "
try:
    from kgdb.query.server import serve_structured_queries, query_graph
    print('Query server module: OK')
except ImportError as e:
    print(f'Query server NOT importable: {e}')
" 2>&1

# 2. Check if query_graph function works on the ingested graph
# (First ingest to get a valid node-link graph)
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/server-test-graph.json
python3 -c "
from kgdb.query.server import query_graph
from pathlib import Path
try:
    result = query_graph(Path('/tmp/server-test-graph.json'), query_type=None, node_id=None)
    print(f'query_graph returned: {type(result).__name__}')
    import json; print(json.dumps(result, indent=2)[:200])
except Exception as e:
    print(f'query_graph failed: {type(e).__name__}: {e}')
"

# 3. Try the stdin-based REPL mode
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "system"}]}]}' | python3 -c "
from kgdb.query.server import serve_structured_queries
from pathlib import Path
import sys
serve_structured_queries(Path('/tmp/server-test-graph.json'), input_stream=sys.stdin)
" 2>&1

# 4. REPL with empty line (should be skipped)
printf '{"filters": []}\n\n{"filters": []}\n' | python3 -c "
from kgdb.query.server import serve_structured_queries
from pathlib import Path
import sys
serve_structured_queries(Path('/tmp/server-test-graph.json'), input_stream=sys.stdin)
"

# 5. REPL with invalid JSON
echo 'not json' | python3 -c "
from kgdb.query.server import serve_structured_queries
from pathlib import Path
import sys
serve_structured_queries(Path('/tmp/server-test-graph.json'), input_stream=sys.stdin)
"

# 6. REPL with valid JSON but invalid query structure
echo '{\"filters\": [{\"facet\": \"unknown\"}]}' | python3 -c "
from kgdb.query.server import serve_structured_queries
from pathlib import Path
import sys
serve_structured_queries(Path('/tmp/server-test-graph.json'), input_stream=sys.stdin)
"

# 7. query_graph with search_query parameter
python3 -c "
from kgdb.query.server import query_graph
from pathlib import Path
try:
    result = query_graph(Path('/tmp/server-test-graph.json'), query_type=None, search_query='ecosystem')
    print(f'Search results: {len(result.get(\"nodes\", []))}')
except Exception as e:
    print(f'Search failed: {type(e).__name__}: {e}')
"

# 8. query_graph with tasks/gaps flags
python3 -c "
from kgdb.query.server import query_graph
from pathlib import Path
for flag in ['tasks', 'gaps', 'unimplemented']:
    try:
        result = query_graph(Path('/tmp/server-test-graph.json'), query_type=None, **{flag: True})
        print(f'{flag}: {len(result.get(\"nodes\", []))} results')
    except Exception as e:
        print(f'{flag} failed: {type(e).__name__}: {e}')
"

# 9. Exhaust input stream (EOF)
python3 -c "
from kgdb.query.server import serve_structured_queries
from pathlib import Path
import io
serve_structured_queries(Path('/tmp/server-test-graph.json'), input_stream=io.StringIO(''))
print('EOF handling: OK')
"

# 10. Query server with nonexistent graph file
python3 -c "
from kgdb.query.server import query_graph
from pathlib import Path
try:
    result = query_graph(Path('/tmp/nonexistent.json'), query_type=None)
    print(f'Returned: {result}')
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
"

# Cleanup
rm -f /tmp/server-test-graph.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El módulo query.server es importable? |
| 2 | ¿query_graph function existe y funciona? |
| 3 | ¿REPL mode procesa queries línea por línea? |
| 4 | ¿Empty lines se saltan sin error? |
| 5 | ¿Invalid JSON produce error JSON response (no crash)? |
| 6 | ¿Invalid query structure produce error JSON? |
| 7 | ¿Search query funciona? ¿Qué busca? |
| 8 | ¿Tasks/gaps/unimplemented flags funcionan? |
| 9 | ¿EOF handling graceful? |
| 10 | ¿Error clear para graph file inexistente? |

## Modos de fracaso

- `from .adapters import ...` falla porque adapters.py no existe
- REPL mode no documentado (no aparece en --help)
- Error responses no tienen formato consistente
- query_graph lanza excepción en vez de devolver dict error
- No hay CLI entry point para el REPL
