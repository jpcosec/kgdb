# ST-ingest: kgdb ingest — generic graph ingestion

**Basado en:** UC-02

## Script

```bash
# 1. Help
kgdb ingest --help

# 2. Ingest archivo substrate válido a output
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-ingest-output.json

# 3. Verificar el output
kgdb list --graph /tmp/kgdb-ingest-output.json

# 4. Ingest con input que no existe
kgdb ingest --input /tmp/nonexistent.json --output /tmp/out.json

# 5. Ingest con input JSON inválido
echo "not a graph" > /tmp/bad-input.json
kgdb ingest --input /tmp/bad-input.json --output /tmp/out.json

# 6. Ingest con input que no es GraphSnapshot válido
echo '{"version": "bad", "nodes": []}' > /tmp/invalid-schema.json
kgdb ingest --input /tmp/invalid-schema.json --output /tmp/out.json

# 7. Ingest sin --input
kgdb ingest --output /tmp/out.json

# 8. Ingest sin --output
kgdb ingest --input desk/fixtures/substrate_v1.json

# 9. Ingest idempotent: mismo input, mismo output
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-ingest-output2.json
kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-ingest-output2.json

# 10. Ingest sobre archivo abierto/ocupado (si aplica)
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help muestra --input y --output como required? |
| 2 | ¿Mensaje de éxito? ¿Cuenta nodos/edges? |
| 3 | ¿El output ingestado es un grafo válido? |
| 4 | ¿Error: file not found? |
| 5 | ¿JSON parse error claro? |
| 6 | ¿Validation error del schema? |
| 7 | ¿Error argparse claro? |
| 8 | ¿Error argparse claro? |
| 9 | ¿Idempotente? ¿Overwrite sin warning? |
| 10 | ¿Error graceful si no puede escribir? |

## Modos de fracaso

- Sin feedback de qué se ingestó (cantidad de nodos/edges)
- Output corrupto si falla a mitad de camino
- Overwrite de output sin confirmación
- Error messages que no distinguen entre file not found, JSON parse error, y schema validation error
