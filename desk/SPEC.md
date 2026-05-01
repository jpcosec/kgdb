# KGDB Delivery Spec

`kgdb` should be the dumb graph persistence and query substrate of the ecosystem.

It should answer:

- how graph knowledge is stored
- how graph knowledge is queried
- how structured payloads become graph records
- how downstream tools retrieve graph state deterministically

---

## Real Use Case

We want a structured payload emitted from `sldb` or another knowledge component to become persisted graph data that can later be:

- queried by `hum`
- audited by `ontology`
- validated against formal expectations by `truth_machine`
- projected into human-facing tools like `graph_ui`

The first delivery slice should prove:

1. ingest a small graph payload
2. persist it
3. query it deterministically
4. export enough shape for downstream consumers

---

## Minimal Feature Slice To Deliver

1. define the minimal persisted graph model
2. support graph ingest from structured input
3. support deterministic query/traversal
4. define a clean output contract for downstream consumers

---

## What Is Currently Missing

- the README is still too thin to define real substrate behavior
- there is no explicit delivery fixture proving the intended ingest/query loop
- downstream consumer contracts are not yet spelled out here

---

## Non-Goals

Out of scope for the first slice:

- semantic reasoning
- formal truth evaluation
- UI logic
- workflow-shell orchestration
