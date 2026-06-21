# UC-01: Exploring a knowledge graph

El usuario acaba de recibir un archivo JSON con un grafo de conocimiento exportado desde SLDB.
Quiere entender qué nodos contiene, inspeccionar nodos específicos, y ver las conexiones entre ellos.

## Pasos

1. Listar todos los nodos del grafo con `kgdb list --graph <file>`
2. Obtener un nodo específico por ID con `kgdb get --graph <file> --node <id>`
3. Listar los edges salientes de un nodo con `kgdb edges --graph <file> --node <id>`

## Preguntas de estrés

- ¿Los IDs de nodos son discoverables desde `list`?
- ¿El formato de output de `list` permite copiar IDs para usar en `get`/`edges`?
- ¿Qué pasa si el node ID tiene caracteres especiales (`sldb://` URIs)?
- ¿Qué pasa si el archivo no existe?
- ¿Los formatos de output son consistentes entre get/list/edges?
