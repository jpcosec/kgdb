# Task Completion

- Required validation for coding tasks: run `pytest` from repository root.
- For ingest/path-related changes, also run: `kgdb ingest --input desk/fixtures/substrate_v1.json --output /tmp/kgdb-substrate.kg.json` when the console script is available.
- Before committing only when explicitly requested: inspect `git status`, `git diff`, and recent log; do not commit desk task status changes unless requested.