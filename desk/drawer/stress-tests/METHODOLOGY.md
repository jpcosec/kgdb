# UX stress-test methodology (kgdb)

## Qué es

Un UX stress-test es una exploración sistemática de la interfaz CLI desde la perspectiva de un usuario. No busca "encuentra bugs en el código" sino "encuentra dónde la experiencia se rompe, confunde o contradice el modelo mental que el usuario construyó".

## Principios

1. **Read-only.** No se edita ningún archivo. No se modifica el sistema bajo test. Solo se ejecutan comandos y se observa.
2. **El usuario no sabe lo que sabe el desarrollador.** El test asume que el usuario no leyó el código fuente. Solo conoce `--help`, la documentación superficial, y su intuición.
3. **Modelo mental primero.** Cada test se basa en una `use-case` narrativa (UC-XX) que describe qué quiere lograr el usuario. El test verifica si el sistema lo deja lograr eso sin fricción.
4. **Anchor en atoms.** Si `atom-kgdb.md` dice "kgdb es el substrate dumb de grafos", el test verifica: ¿el CLI es dumb? ¿O tiene lógica semántica que debería estar en sldb? ¿O faltan comandos que el atom sugiere?
5. **Fricción es el hallazgo.** Un error con traceback es un hallazgo. Un comando que existe pero se comporta distinto a lo esperado es un hallazgo. Un output silencioso donde debería haber feedback es un hallazgo. Una inconsistencia entre formatos de archivo es un hallazgo.

## Estructura de un test

Cada test vive en `desk/drawer/stress-tests/st-XX-nombre.md` y contiene:

```markdown
# ST-XX: Nombre

**Basado en:** UC-XX

## Script

Secuencia de comandos CLI que el usuario ejecuta. Textual, uno por línea.
Incluye casos felices, casos borde, y casos de error.

## Puntos de estrés

Tabla: por cada paso del script, qué observar.
No es "funciona o no funciona". Es "el output es claro?",
"el error sugiere qué hacer?", "el usuario queda en un estado conocido?".

## Modos de fracaso

Lista de formas en que la experiencia se rompe.
```

## Cómo se ejecuta

1. Elegir un ST basado en un UC
2. Preparar setup si hace falta (crear graph snapshot de prueba)
3. Ejecutar el script manualmente o mediante subagente
4. **Observar**, no juzgar. Anotar outputs textuales, exit codes, comportamientos sorprendentes
5. Escribir hallazgos en `findings/round-NN-descripcion.md`

## Qué observar en cada comando

| Dimensión | Preguntas |
|---|---|
| **Discoverability** | ¿El comando aparece en `--help`? ¿Su nombre es obvio? |
| **Error messages** | ¿El error es para un humano o para un desarrollador? ¿Muestra traceback interno o mensaje semántico? ¿Sugiere qué hacer? |
| **Exit codes** | ¿0 para éxito, 1 para error manejado, 2 para argparse? |
| **Silent failures** | ¿Hay comandos que devuelven 0 sin output cuando deberían haber fallado? |
| **Consistency** | ¿Subcomandos similares (get/list/edges) se comportan igual? |
| **Naming** | ¿Los flags siguen un patrón (`--graph`, `--node`, `--input`, `--output`)? |
| **State** | ¿El comando deja al usuario en un estado conocido? ¿Puede ver qué pasó? |
| **Output** | ¿El output es scrolleable? ¿Tiene estructura (tablas, columnas)? |
| **Edge cases** | ¿IDs vacíos, paths con espacios, graph files corruptos, JSON inválido? |
| **CI readiness** | ¿Se puede pipear? ¿Hay `--format json`? ¿Hay colores ANSI que rompen logs? |

## Cobertura esperada

Cada superficie del CLI debe tener al menos un ST:

| Superficie | ST asociado |
|---|---|
| `kgdb get` | ST-get |
| `kgdb list` | ST-list |
| `kgdb query` | ST-query |
| `kgdb edges` | ST-edges |
| `kgdb ingest` | ST-ingest |
| `kgdb ingest-sldb` | ST-ingest-sldb |
| Graph snapshots (formatos, versiones) | ST-snapshots |
| Query files (structured queries) | ST-query-files |
| Edge cases (archivos corruptos, missing) | ST-edge-cases |
| Python API | ST-api |
| Fixtures de contrato | ST-contracts |

## Lo que NO es un UX stress-test

- No es un test unitario (no prueba funciones aisladas)
- No es un test de integración (no verifica que módulos conecten)
- No es un test de regresión (no verifica que bugs anteriores no hayan vuelto)
- No es una auditoría de seguridad
- No es una revisión de código
