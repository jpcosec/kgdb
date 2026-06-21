# Core

- KGDB is intended as a dumb graph persistence/query substrate; semantic reasoning, truth evaluation, UI logic, and orchestration are out of scope per `desk/SPEC.md`.
- Source layout: Python package under `src/kgdb`; tests under `tests`; active task/desk workflow under `desk/`.
- Main contracts live in `src/kgdb/contracts`: `base.py` for `SystemIdentity`/`Edge`, `node.py` for `KnowledgeNode` facets, `io.py` for `GraphSnapshot`/`QueryResult`, `persistence.py` for transaction manifests.
- Runtime graph storage uses NetworkX `DiGraph`; `src/kgdb/graph/utils.py` converts `KnowledgeNode` objects to node-link JSON with node `schema` copies for round-trip reconstruction.
- CLI entrypoint is `kgdb.main:main`; supports `ingest`, `query`, `get`, `list`, and `edges`.
- Desk workflow rules and non-goals are in `desk/STANDARDS.md` and `desk/tasks/Board.md`.
- Read `mem:tech_stack` for packaging/dependencies; `mem:suggested_commands` for practical commands; `mem:conventions` for project-specific coding contracts; `mem:task_completion` for done checks.