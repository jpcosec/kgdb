# UC-06: Graph edge traversal

El usuario tiene un nodo en un grafo y quiere explorar su vecindario: qué nodos están conectados, con qué tipo de relación, y a qué profundidad.

## Pasos

1. Listar edges salientes de un nodo con `kgdb edges --graph <file> --node <id>`
2. Tomar un target de un edge y hacer `get` sobre él (traversal manual)
3. Intentar encontrar caminos entre nodos (si existe el comando)

## Preguntas de estrés

- ¿`kgdb edges` muestra source y target? ¿Relation type?
- ¿Los IDs en el output de edges se pueden copiar-pegar en `get`?
- ¿Hay un comando para hacer BFS/DFS traversal? Si no, ¿cómo se espera que el usuario explore?
- ¿Qué pasa si el nodo no existe en el grafo?
- ¿Qué pasa si el nodo existe pero no tiene edges?
- ¿Qué pasa con nodos que tienen muchos edges (paginación)?
