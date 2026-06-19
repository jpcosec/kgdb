# KGDB Desk Standards

This `desk/` is the execution surface for `kgdb` work.

Use it to turn the graph-substrate vision into auditable implementation tasks.

---

## Purpose

Use this desk to:

- define the minimum real graph-storage slice
- track missing persistence and query capabilities
- prepare work that can be delegated safely to a subagent

Durable graph-substrate knowledge belongs in `README.md` and `docs/` when present.
Active implementation planning belongs here.

---

## Task Rules

1. Every task must point to a real substrate behavior.
2. Every task must include a concrete validation step.
3. Every task should prefer explicit graph IO over vague architecture language.
4. Keep `kgdb` dumb: persistence and query belong here; semantic judgment does not.

## CLI Contract Alignment

Tasks that touch CLI, graph loading, schema validation, ingest inputs, or command discoverability must keep fixture shape, schema, loader behavior, and CLI traversal aligned:

- Preserve one named graph representation at each boundary. If conversion is needed, make it explicit and tested.
- Do not silently treat fixture, schema, and NetworkX runtime formats as the same thing.
- Validate the fixture against the schema, load it through the public loader, and run the CLI command. Confirm both nodes and edges survive.
- Do not fix one command by converting only its private path.
- Do not fix schema by deleting edge requirements without replacing the contract.

## Drift Signals

Watch for these signals that graph alignment is broken:

- The only fixture fails its own schema.
- `ingest` and read-only commands require different graph shapes.
- Edge data exists before load but disappears after load.
- A downstream consumer must know internal NetworkX serialization details.
- User-facing errors still expose raw Python tracebacks.
- Loader behavior and ingest behavior accept different graph shapes.

## Testing

- Run tests from the repository root with plain `pytest`.
- Resolve repository fixtures from the test file or repository root; do not rely on package-relative working-directory paths.
