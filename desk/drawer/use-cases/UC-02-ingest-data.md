# UC-02: Ingesting data into kgdb

El usuario tiene un archivo JSON con datos de grafo en un formato específico (substrate, SLDB semantic export).
Quiere convertirlo al formato interno de kgdb para poder consultarlo.

## Pasos

1. Ingestar un archivo substrate con `kgdb ingest --input <file> --output <file>`
2. Ingestar un export semántico de SLDB con `kgdb ingest-sldb --input <file> --output <file>`
3. Verificar que los nodos se ingestarion correctamente con `list`

## Preguntas de estrés

- ¿El mensaje de éxito indica cuántos nodos/edges se ingestarion?
- ¿Qué pasa si el input no existe?
- ¿Qué pasa si el input tiene JSON inválido?
- ¿Qué pasa si el input tiene un schema que no coincide?
- ¿Qué pasa si el output ya existe? (¿overwrite? ¿append? ¿error?)
- ¿Hay feedback de progreso para archivos grandes?
- ¿La diferencia entre `ingest` e `ingest-sldb` es clara desde `--help`?
