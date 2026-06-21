# ST-query: kgdb query — execute structured queries

**Basado en:** UC-03

## Script

```bash
# 1. Help
kgdb query --help

# 2. Query simple: filter by node_type
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "system"}]}]}' > /tmp/query-simple.json
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-simple.json

# 3. Query con scope descendant_of sobre un nodo específico
cat > /tmp/query-scope.json << 'EOF'
{
  "scope": {"descendant_of": "system:ecosystem"},
  "filters": []
}
EOF
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-scope.json

# 4. Query sin resultados
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "nonexistent_type"}]}]}' > /tmp/query-empty.json
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-empty.json

# 5. Query con JSON inválido
echo "not json" > /tmp/query-bad.json
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-bad.json

# 6. Query con archivo inexistente
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/nonexistent.json

# 7. Query sin --query-file
kgdb query --graph desk/fixtures/substrate_v1.json

# 8. Query sin --graph
kgdb query --query-file /tmp/query-simple.json

# 9. Query con campo desconocido en filter
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "imaginary_field", "op": "eq", "value": "x"}]}]}' > /tmp/query-unknown-field.json
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-unknown-field.json

# 10. Query con operador no soportado
echo '{"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "regex", "value": "sys.*"}]}]}' > /tmp/query-bad-op.json
kgdb query --graph desk/fixtures/substrate_v1.json --query-file /tmp/query-bad-op.json

# 11. Query una de las queries de ejemplo en contracts/
kgdb query --graph desk/fixtures/substrate_v1.json --query-file contracts/queries/sldb/documents_near_domain_workflow_task_tag.json
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help documenta el formato del archivo de query? |
| 2 | ¿Output filtra correctamente? ¿Formato estructurado? |
| 3 | ¿Scope funciona? ¿Output incluye todos los descendientes? |
| 4 | ¿Output vacío con exit 0? ¿O exit != 0 por "no results"? |
| 5 | ¿JSON parse error claro? |
| 6 | ¿File not found error? |
| 7 | ¿Error argparse claro? |
| 8 | ¿Error argparse claro? |
| 9 | ¿Error de schema validation? ¿O no valida? |
| 10 | ¿Error de operador no soportado? |
| 11 | ¿Las queries de ejemplo son válidas y ejecutables? |

## Modos de fracaso

- Query file format no documentado en --help
- Errores de validación poco claros (Pydantic traceback)
- Scope o filters no funcionan como el usuario espera
- Output no estructurado (no se puede procesar)
- Exit codes no distinguen "0 resultados" de "error"
