# ST-edges: kgdb edges — list outgoing edges

**Basado en:** UC-01, UC-06

## Script

```bash
# 1. Help
kgdb edges --help

# 2. Edges sobre nodo existente con edges
kgdb edges --graph desk/fixtures/substrate_v1.json --node "system:ecosystem"

# 3. Edges sobre nodo existente sin edges
kgdb edges --graph desk/fixtures/substrate_v1.json --node "system:hermetic"

# 4. Edges con ID que no existe
kgdb edges --graph desk/fixtures/substrate_v1.json --node "nonexistent"

# 5. Edges sin --node
kgdb edges --graph desk/fixtures/substrate_v1.json

# 6. Edges sin --graph
kgdb edges --node "system:ecosystem"

# 7. Pipe edges output a get (traversal manual)
# Tomar el target_id del primer edge y pasarlo a get
kgdb edges --graph desk/fixtures/substrate_v1.json --node "system:ecosystem" 2>&1 | head -5

# 8. Nodo con sldb:// URI
kgdb edges --graph .sldb/runtime/semantic_index.yaml --node "sldb://document/..." 2>/dev/null || echo "sldb skip"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help es claro sobre el formato? |
| 2 | ¿Muestra source, target, relation_type, metadata? |
| 3 | ¿Exit 0 con output vacío? ¿O mensaje "no edges"? |
| 4 | ¿Error claro? |
| 5 | ¿Error argparse claro? |
| 6 | ¿Error argparse claro? |
| 7 | ¿El output de edges se puede parsear para extraer target IDs? |
| 8 | ¿Soporta URIs sldb://? |

## Modos de fracaso

- Edges muestra "no edges" como error (exit != 0) cuando debería ser informativo
- Formato de output no permite extraer target IDs programáticamente
- Nodos con muchos edges sin paginación
- Relation types no se muestran o están truncados
