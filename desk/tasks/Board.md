---
id: kgdb-tasks-board
scope: tools/kgdb
tasks:
  - desk/tasks/task-define-graph-io-contract.md
  - desk/tasks/task-define-persistence-model.md
  - desk/tasks/task-implement-minimal-ingest-api.md
  - desk/tasks/task-implement-minimal-ingest-cli.md
  - desk/tasks/task-implement-minimal-query-api.md
  - desk/tasks/task-implement-minimal-query-cli.md
  - desk/tasks/task-create-substrate-fixture.md
  - desk/tasks/task-prove-downstream-consumer-contract.md
  - desk/tasks/task-provenance-fr-1-ingest-canonical-source-catalog.md
  - desk/tasks/task-provenance-fr-2-emit-first-class-source-nodes.md
  - desk/tasks/task-provenance-fr-3-parse-atom-provenance-declarations.md
  - desk/tasks/task-provenance-fr-4-emit-typed-provenance-edges.md
  - desk/tasks/task-provenance-fr-5-detect-unknown-source-ids.md
  - desk/tasks/task-provenance-fr-6-detect-orphan-atoms.md
  - desk/tasks/task-provenance-fr-7-source-coverage-reflection.md
  - desk/tasks/task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract.md
  - desk/tasks/task-provenance-fr-9-reflection-output-contract-for-findings.md
  - desk/tasks/task-provenance-fr-10-backward-compatible-degradation.md
  - desk/tasks/task-snapshot-validation-cli-and-python-api.md
  - desk/tasks/task-relation-serialization-roundtrip-and-malformed-input-handling.md
  - desk/tasks/task-graph-trace-query-surface-api.md
  - desk/tasks/task-graph-trace-query-surface-cli.md
  - desk/tasks/task-ingest-sldb-documents-and-sections.md
  - desk/tasks/task-ingest-sldb-tags-and-models.md
  - desk/tasks/task-ingest-sldb-equivalences-and-hashes.md
  - desk/tasks/task-preserve-sldb-structural-provenance-through-kgdb-handoff.md
  - desk/tasks/task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test.md
  - desk/tasks/task-document-kgdb-boundary-with-sldb-and-deskops.md
pills:
  - desk/contexts/pill-substrate-is-dumb.md
  - desk/contexts/pill-source-nodes-are-first-class.md
  - desk/contexts/pill-provenance-edges-are-typed.md
  - desk/contexts/pill-orphans-and-gaps-are-reflection-findings.md
  - desk/contexts/pill-snapshot-is-the-public-output-surface.md
  - desk/contexts/pill-trace-is-the-public-query-surface.md
  - desk/contexts/pill-relation-serialization-must-roundtrip.md
  - desk/contexts/pill-validation-findings-are-structured-not-crashes.md
  - desk/contexts/pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow.md
  - desk/contexts/pill-provenance-survives-the-sldb-to-kgdb-handoff.md
  - desk/contexts/pill-backward-compatible-degradation-findings-not-failures.md
  - desk/contexts/pill-board-md-frontmatter-is-the-routing-truth.md
  - desk/contexts/pill-closed-tasks-are-deleted-not-marked.md
  - desk/contexts/pill-fixtures-are-consumer-contract-tests.md
  - desk/contexts/pill-kgdb-cli-is-the-stable-public-surface.md
rituals:
  - desk/rituals/closeout.md
  - desk/rituals/execution.md
  - desk/rituals/testing.md
tags:
  - workspace:desk
  - system:kgdb
---

# KGDB Tasks Board

## Purpose

- Objective: make `kgdb` a real graph persistence/query substrate ready to receive structured knowledge-codebase handoffs.
- Pill count and task count are not 1-to-1 by design: pills capture atomic reusable concepts; tasks describe concrete deliverables. Coverage, not parity.

## Notes

- Phase 4 (Stress-Test Corrections) closed via commit `9f23979`.
- Phase 5 (Provenance) seeded from `desk/drawer/registry/kgdb-provenance-requirements.md`.
- Phase 6 (Inbox + SLDB Boundary) seeded from `desk/inbox/` and the SLDB ADR at `sldb/docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`.
- All active tasks tracked by deskops; all 15 atomic pills generated via `deskops add pill`.

## Delivery Phases

### Phase 1 - Define the substrate contract
- `desk/tasks/task-define-graph-io-contract.md`
- `desk/tasks/task-define-persistence-model.md`

### Phase 2 - Prove ingest and query
- `desk/tasks/task-implement-minimal-ingest-api.md`
- `desk/tasks/task-implement-minimal-ingest-cli.md`
- `desk/tasks/task-implement-minimal-query-api.md`
- `desk/tasks/task-implement-minimal-query-cli.md`

### Phase 3 - Prove downstream use
- `desk/tasks/task-create-substrate-fixture.md`
- `desk/tasks/task-prove-downstream-consumer-contract.md`

### Phase 4 - Stress-Test Corrections *(closed)*
- `desk/tasks/007-fix-load_graph-graphsnapshot-format.md` ✓
- `desk/tasks/008-add-user-friendly-error-messages.md` ✓
- `desk/tasks/009-add-ingest-input-validation.md` ✓
- `desk/tasks/010-fix-utf8-output-and-exit-code-consistency.md` ✓
- `desk/tasks/011-improve-cli-discoverability.md` ✓

### Phase 5 - Provenance-Aware Knowledge Grounding
Source: `desk/drawer/registry/kgdb-provenance-requirements.md`
- `desk/tasks/task-provenance-fr-1-ingest-canonical-source-catalog.md`
- `desk/tasks/task-provenance-fr-2-emit-first-class-source-nodes.md`
- `desk/tasks/task-provenance-fr-3-parse-atom-provenance-declarations.md`
- `desk/tasks/task-provenance-fr-4-emit-typed-provenance-edges.md`
- `desk/tasks/task-provenance-fr-5-detect-unknown-source-ids.md`
- `desk/tasks/task-provenance-fr-6-detect-orphan-atoms.md`
- `desk/tasks/task-provenance-fr-7-source-coverage-reflection.md`
- `desk/tasks/task-provenance-fr-8-include-sources-and-edges-in-snapshot-contract.md`
- `desk/tasks/task-provenance-fr-9-reflection-output-contract-for-findings.md`
- `desk/tasks/task-provenance-fr-10-backward-compatible-degradation.md`

### Phase 6 - Inbox + SLDB Boundary Alignment
Sources: `desk/inbox/*` (4 messages), `sldb/docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`
- `desk/tasks/task-snapshot-validation-cli-and-python-api.md`
- `desk/tasks/task-relation-serialization-roundtrip-and-malformed-input-handling.md`
- `desk/tasks/task-graph-trace-query-surface-api.md`
- `desk/tasks/task-graph-trace-query-surface-cli.md`
- `desk/tasks/task-ingest-sldb-documents-and-sections.md`
- `desk/tasks/task-ingest-sldb-tags-and-models.md`
- `desk/tasks/task-ingest-sldb-equivalences-and-hashes.md`
- `desk/tasks/task-preserve-sldb-structural-provenance-through-kgdb-handoff.md`
- `desk/tasks/task-cross-repo-sldb-export-to-kgdb-ingest-roundtrip-test.md`
- `desk/tasks/task-document-kgdb-boundary-with-sldb-and-deskops.md`

## Active

### Execution Level 0
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| IO | contract | Define graph IO contract | none |

### Execution Level 1
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| PM | persistence | Define persistence model | IO |

### Execution Level 2
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| ING-API | ingest | Implement minimal ingest API | PM |
| QRY-API | query | Implement minimal query API | PM |
| FIX | fixtures | Create substrate fixture | PM |
| FR-1 | provenance | Ingest canonical source catalog | PM |
| RS-1 | serialization | Relation serialization roundtrip | PM |
| TR-API | query | Graph trace API | PM |

### Execution Level 3
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| ING-CLI | ingest | Implement minimal ingest CLI | ING-API |
| QRY-CLI | query | Implement minimal query CLI | QRY-API |
| TR-CLI | query | Graph trace CLI | TR-API |
| FR-2 | provenance | Emit first-class source nodes | FR-1 |
| FR-3 | provenance | Parse atom provenance declarations | FR-1 |

### Execution Level 4
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| INT | integration | Prove downstream consumer contract | ING-CLI, QRY-CLI, FIX |
| FR-4 | provenance | Emit typed provenance edges | FR-2, FR-3 |
| FR-5 | provenance | Detect unknown source IDs | FR-3 |

### Execution Level 5
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| FR-6 | provenance | Detect orphan atoms | FR-4, FR-5 |
| FR-7 | provenance | Source coverage reflection | FR-4 |
| FR-8 | provenance | Include sources/edges in snapshot contract | FR-2, FR-4 |

### Execution Level 6
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| FR-9 | provenance | Reflection output contract for findings | FR-5, FR-6, FR-7 |
| SV-1 | validation | Snapshot validation CLI and Python API | FR-8 |
| SL-1A | boundary | Ingest SLDB documents and sections | PM, FR-8 |

### Execution Level 7
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| FR-10 | provenance | Backward-compatible degradation | FR-1..FR-9 |
| SL-1B | boundary | Ingest SLDB tags and models | SL-1A |

### Execution Level 8
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| SL-1C | boundary | Ingest SLDB equivalences and hashes | SL-1B |

### Execution Level 9
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| SL-2 | boundary | Preserve SLDB structural provenance | SL-1C |

### Execution Level 10
| ID | Domain | Task | Depends On |
|----|--------|------|------------|
| SL-3 | boundary | Cross-repo SLDB ingest roundtrip test | SL-1C, SL-2 |
| BD-1 | docs | Document KGDB boundary with SLDB/deskops | SL-1C, SL-2 |

## Active Pills (atomic, not 1-to-1 with tasks)

| Pill | Concept | Applies to |
|------|---------|------------|
| `pill-substrate-is-dumb` | KGDB holds graph state, no semantic reasoning | All substrate tasks |
| `pill-source-nodes-are-first-class` | source_doc nodes are graph nodes, not side references | FR-1, FR-2, FR-8 |
| `pill-provenance-edges-are-typed` | relation+derivation+locator+confidence are required on edges | FR-3, FR-4, FR-8, FR-9 |
| `pill-orphans-and-gaps-are-reflection-findings` | missing provenance / unknown source / unused source = finding, never silent | FR-5, FR-6, FR-7, FR-9 |
| `pill-snapshot-is-the-public-output-surface` | downstream reads snapshots, never raw graph state | IO, PM, ING, FIX, INT, FR-1, FR-2, FR-4, FR-8, RS-1, SV-1, SL-1 |
| `pill-trace-is-the-public-query-surface` | consumers query trace, never parse snapshot JSON | QRY, INT, TR-1 |
| `pill-relation-serialization-must-roundtrip` | edges serialize/deserialize identically or fail explicitly | RS-1, IO, FR-4 |
| `pill-validation-findings-are-structured-not-crashes` | every validation finding is structured, never a traceback | SV-1, FR-5, FR-6, FR-7, FR-9, FR-10 |
| `pill-sldb-owns-text-kgdb-owns-graph-deskops-owns-workflow` | ADR boundary: keep layers separated | SL-1, SL-2, SL-3, BD-1 |
| `pill-provenance-survives-the-sldb-to-kgdb-handoff` | doc/section/field/tags/model/hash identity roundtrip | FR-3, FR-4, SL-1, SL-2, SL-3 |
| `pill-backward-compatible-degradation-findings-not-failures` | absent data → findings, not exceptions, unless strict mode | ING, FR-10 |
| `pill-board-md-frontmatter-is-the-routing-truth` | frontmatter tasks/pills/rituals are authoritative | All routing edits; BD-1 |
| `pill-closed-tasks-are-deleted-not-marked` | closeout deletes files; no status: closed accumulation | Closeout ritual |
| `pill-fixtures-are-consumer-contract-tests` | fixtures prove consumer shape; must validate against contract | FIX, INT, SL-3 |
| `pill-kgdb-cli-is-the-stable-public-surface` | CLI surface is stable; backends can change | TR-1, all CLI tasks |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Start from `desk/SPEC.md`.
2. Define contracts before implementation.
3. Prove each phase with fixtures before advancing.
4. Pills and tasks are not 1-to-1. Pills capture atomic reusable concepts.

## Task Details

- Define graph IO contract [draft] - Define GraphSnapshot and QueryResult dataclasses in src/kgdb/contracts/io.py with required fields, types, and serialization rules.
- Define persistence model [draft] - Define PersistenceEntry and TransactionManifest in src/kgdb/contracts/persistence.py; document ledger-based graph storage semantics.


- Create substrate fixture [draft] - Create desk/fixtures/substrate_v1.json representing the core ecosystem modules as nodes and edges; GraphSnapshot-valid; replayable.
- Prove downstream consumer contract [draft] - An integration test ingests substrate_v1.json, queries it, and asserts a downstream consumer (e.g., a stub adapter) receives a QueryResult matching the documented shape.
- Provenance FR-1: ingest canonical source catalog [draft] - KGDB reads desk/registry/source-catalog.yaml, validates unique source IDs, and creates one source_doc graph node per entry with metadata (id, title, kind, family, path, stability, description).
- Provenance FR-2: emit first-class source nodes [draft] - Every ingested source-catalog entry becomes a source_doc graph node exposing node_id, node_type, label, path, kind, family, stability, description per the graph-node contract in section 8.3.
- Provenance FR-3: parse atom provenance declarations [draft] - Atom frontmatter provenance entries are read, validated against the catalog, and stored on the atom node for downstream edge emission.
- Provenance FR-4: emit typed provenance edges [draft] - Each valid provenance declaration produces a typed edge from the atom to its source node, preserving relation, derivation, locator, and confidence.
- Provenance FR-5: detect unknown source IDs [draft] - Reflection output contains an unresolved-source finding for every provenance entry whose source_id is missing from the catalog.
- Provenance FR-6: detect orphan atoms [draft] - Reflection output contains an orphan-atom finding for every atom lacking any resolved provenance support.
- Provenance FR-7: source coverage reflection [draft] - Reflection output reports unused source nodes (no incoming support edges) and enables coverage review by source family.
- Provenance FR-8: include sources and edges in snapshot contract [draft] - The snapshot JSON contract explicitly covers source_doc nodes and provenance edges alongside existing atom and reference nodes.
- Provenance FR-9: reflection output contract for findings [draft] - Reflection output defines a stable schema for provenance findings: id, atom_id, source_id, relation, severity, message.
- Provenance FR-10: backward-compatible degradation [draft] - When source catalog or atom provenance blocks are missing, KGDB graph build still succeeds and emits provenance findings instead of erroring.
- Snapshot validation: CLI and Python API [draft] - kgdb snapshot validate <path> validates a snapshot JSON against the registered graph contract; Python API validate_snapshot(path) -> ValidationResult with structured findings; non-zero exit with diagnostic list on invalid; exit 0 on valid.
- Relation serialization roundtrip and malformed-input handling [draft] - Edge serialization roundtrips identically across graph build, snapshot storage, and graph query. Unknown or malformed edge types produce clear errors, not silent drops. Tests cover simple, typed, provenance-bearing, and malformed edges.


- Preserve SLDB structural provenance through KGDB handoff [draft] - Every SLDB-derived graph node carries identity references to its source document, section/field, semantic tags, model contract, and extraction/hash provenance. KGDB query surfaces can resolve back to the originating SLDB artifact.
- Cross-repo SLDB export to KGDB ingest roundtrip test [draft] - A pytest fixture builds a real SLDB semantic-export payload, ingests it via KGDB, and asserts the resulting graph snapshot preserves every export field (model, document, path, tags, sections, DAG nodes, equivalences, hashes, provenance).
- Document KGDB boundary with SLDB and deskops [draft] - KGDB docs/ contains an architecture page that states KGDB owns graph persistence, traversal, equivalence, and inference; does NOT own document authoring or rendering; hands off with SLDB at the semantic-export boundary; coexists with deskops as workflow layer.