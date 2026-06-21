# ST-contracts: contract validation and fixtures

**Basado en:** UC-04

## Script

```bash
# 1. Validar fixture substrate contra schema
python3 -c "
import json, jsonschema
schema = json.load(open('contracts/schemas/kgdb_graph_bundle.schema.json'))
data = json.load(open('desk/fixtures/substrate_v1.json'))
jsonschema.validate(data, schema)
print('substrate_v1.json: valid')
"

# 2. Validar SLDB semantic export contra schema
python3 -c "
import json, jsonschema
schema = json.load(open('contracts/schemas/sldb_kgdb_semantic_export.schema.json'))
data = json.load(open('contracts/fixtures/sldb_kgdb_semantic_export.v1.json'))
jsonschema.validate(data, schema)
print('sldb export: valid')
"

# 3. ¿Los queries de ejemplo en contracts/queries/sldb/ se pueden ejecutar?
for q in contracts/queries/sldb/*.json; do
    echo "=== $q ==="
    kgdb query --graph desk/fixtures/substrate_v1.json --query-file "$q" 2>&1 || true
done

# 4. ¿El fixture downstream_vocabulary es válido?
kgdb list --graph desk/fixtures/downstream_vocabulary_v1.json

# 5. Verificar que integración.contract.yaml menciona las dependencias correctas
cat contracts/integration.contract.yaml

# 6. ¿Los tests de contrato pasan?
python3 -m pytest tests/test_sldb_semantic_contract.py -v --no-header 2>&1 | head -30
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El schema valida correctamente? |
| 2 | ¿El SLDB export cumple el schema? |
| 3 | ¿Los queries de ejemplo ejecutan sin error? ¿Devuelven resultados esperados? |
| 4 | ¿El fixture downstream es un grafo válido? |
| 5 | ¿El contrato de integración está actualizado? |
| 6 | ¿Los tests de contrato pasan? |

## Modos de fracaso

- Fixtures o schemas desactualizados (tests fallan)
- Queries de ejemplo no ejecutables (schema mismatch)
- Contrato de integración no refleja el código actual
- No hay un comando `kgdb validate` o `kgdb check` para verificar contratos desde CLI
