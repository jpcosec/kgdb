# ST-get: kgdb get — retrieve a single node

**Basado en:** UC-01

## Script

```bash
# 1. Help
kgdb get --help

# 2. Get sobre grafo existente con ID válido
kgdb get --graph desk/fixtures/substrate_v1.json --node "system:ecosystem"

# 3. Get con ID que no existe
kgdb get --graph desk/fixtures/substrate_v1.json --node "nonexistent-id"

# 4. Get sin --node flag
kgdb get --graph desk/fixtures/substrate_v1.json

# 5. Get sin --graph flag
kgdb get --node "system:ecosystem"

# 6. Get con archivo inexistente
kgdb get --graph /tmp/nonexistent.json --node "system:ecosystem"

# 7. Get con archivo JSON inválido
echo "not json" > /tmp/bad.json
kgdb get --graph /tmp/bad.json --node "system:ecosystem"

# 8. Get con ID que tiene caracteres especiales (sldb:// URIs)
kgdb get --graph .sldb/runtime/semantic_dag.yaml --node "sldb://document/TaskDoc"

# 9. Get con --graph apuntando a archivo que no es grafo (ej: README.md)
kgdb get --graph README.md --node "test"

# 10. Get con output redirigido
kgdb get --graph desk/fixtures/substrate_v1.json --node "system:ecosystem" > /tmp/kgdb-get-output.txt 2>&1
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help muestra formato correcto de flags? ¿Muestra --graph y --node como required? |
| 2 | ¿El output muestra node_id, node_type, edges, facets? ¿Formato legible? |
| 3 | ¿Error claro? ¿Sugiere IDs válidos (list)? |
| 4 | ¿Error argparse claro? |
| 5 | ¿Error argparse claro? |
| 6 | ¿Error: file not found o algo menos claro? |
| 7 | ¿Error: JSON parse error? ¿Muestra línea? |
| 8 | ¿Maneja correctamente caracteres especiales en IDs? |
| 9 | ¿Error: not a valid graph? ¿O crash? |
| 10 | ¿Output limpio para piping? |

## Modos de fracaso

- Output sin estructura (no se distingue qué campo es qué)
- Error interno con traceback en vez de mensaje user-friendly
- --node flag required pero el mensaje de error no lo dice explícitamente
- Archivos no-grafo producen error confuso
- Caracteres especiales en node IDs producen error o crash
