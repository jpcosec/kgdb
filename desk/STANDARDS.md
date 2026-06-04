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

## Testing

- Run tests from the repository root with plain `pytest`.
- Resolve repository fixtures from the test file or repository root; do not rely on package-relative working-directory paths.
