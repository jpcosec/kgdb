# ST-list: kgdb list — list all node IDs

**Basado en:** UC-01

## Script

```bash
# 1. Help
kgdb list --help

# 2. List sobre grafo existente
kgdb list --graph desk/fixtures/substrate_v1.json

# 3. List sobre SLDB semantic export
kgdb list --graph contracts/fixtures/sldb_kgdb_semantic_export.v1.json

# 4. List sin --graph
kgdb list

# 5. List con archivo inexistente
kgdb list --graph /tmp/nonexistent.json

# 6. List con archivo JSON inválido
echo "not json" > /tmp/bad.json
kgdb list --graph /tmp/bad.json

# 7. List con grafo vacío (solo {} o {"nodes": []})
echo '{"nodes": []}' > /tmp/empty.json
kgdb list --graph /tmp/empty.json

# 8. List con output redirigido
kgdb list --graph desk/fixtures/substrate_v1.json > /tmp/kgdb-list-output.txt 2>&1

# 9. Pipe de list a head
kgdb list --graph contracts/fixtures/sldb_kgdb_semantic_export.v1.json 2>&1 | head -5

# 10. ¿El output de list se puede usar directamente como input de get?
kgdb list --graph desk/fixtures/substrate_v1.json | head -1 | xargs -I{} kgdb get --graph desk/fixtures/substrate_v1.json --node {}
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help muestra --graph como required? |
| 2 | ¿Cada línea es un node ID? ¿O tiene formato extra? |
| 3 | ¿Funciona con el formato de export de SLDB? |
| 4 | ¿Error argparse claro? |
| 5 | ¿Error: file not found? |
| 6 | ¿JSON parse error claro? |
| 7 | ¿Output vacío? ¿Exit code 0? |
| 8 | ¿Output limpio para piping? |
| 9 | ¿Hace paging? ¿El comando es instantáneo? |
| 10 | ¿Los IDs de list se pueden copiar-pegar en get? ¿O tienen formato extra? |

## Modos de fracaso

- Output con formato extra que impide copy-paste de IDs
- Sin salto de línea al final (rompe pipelines)
- Grapes grandes sin paginación o limit
- IDs de nodos mostrados en formato distinto al que espera --node
