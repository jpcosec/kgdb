# ST-ingest-sldb: kgdb ingest-sldb — SLDB semantic export ingestion

**Basado en:** UC-02

## Script

```bash
# 1. Help
kgdb ingest-sldb --help

# 2. Ingest SLDB semantic export válido
kgdb ingest-sldb --input contracts/fixtures/sldb_kgdb_semantic_export.v1.json --output /tmp/kgdb-sldb-output.json

# 3. Verificar el output
kgdb list --graph /tmp/kgdb-sldb-output.json

# 4. Ingest con input que no es SLDB export (substrate en vez de semantic export)
kgdb ingest-sldb --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-sldb-bad.json

# 5. Ingest con SLDB export de versión incorrecta
# (modificar versión en el JSON)
cat contracts/fixtures/sldb_kgdb_semantic_export.v1.json | sed 's/"sldb_kgdb_semantic_export" v1/"sldb_kgdb_semantic_export" v0/' > /tmp/wrong-version.json
kgdb ingest-sldb --input /tmp/wrong-version.json --output /tmp/kgdb-sldb-version.json

# 6. Ingest con archivo que tiene el schema correcto pero datos inválidos
# (por ejemplo, edge que apunta a nodo inexistente)
cat contracts/fixtures/sldb_kgdb_semantic_export.v1.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
# Add an edge to nonexistent node
data['@graph'][0]['nodes'][0]['edges'].append({'relation_type': 'has_model', 'target_id': 'nonexistent'})
json.dump(data, sys.stdout)
" > /tmp/sldb-bad-edges.json
kgdb ingest-sldb --input /tmp/sldb-bad-edges.json --output /tmp/kgdb-sldb-bad-edges.json

# 7. Ingest sin --input
kgdb ingest-sldb --output /tmp/out.json

# 8. Diferencia entre ingest e ingest-sldb: ¿puedo hacer ingest de un SLDB export?
kgdb ingest --input contracts/fixtures/sldb_kgdb_semantic_export.v1.json --output /tmp/kgdb-ingest-sldb-as-generic.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué formato espera? ¿Documenta la versión del contrato? |
| 2 | ¿Cuántos nodos/edges se crearon? ¿Los tipos de nodo son correctos (sldb_store, sldb_model, etc.)? |
| 3 | ¿El output tiene estructura de grafo kgdb estándar? |
| 4 | ¿Error claro? ¿"Not a valid SLDB export"? |
| 5 | ¿Error: version mismatch? ¿Mensaje claro? |
| 6 | ¿Valida edges? ¿O permite dangling edges? |
| 7 | ¿Error argparse claro? |
| 8 | ¿`ingest` acepta SLDB exports? ¿O solo ingest-sldb? La diferencia no es obvia. |

## Modos de fracaso

- La diferencia entre `ingest` e `ingest-sldb` no es clara desde --help
- SLDB export con versión incorrecta da error confuso (Pydantic traceback en vez de "expected version X got Y")
- Dangling edges en el input no se reportan como warning
- Output no se puede usar inmediatamente con query/list/get
