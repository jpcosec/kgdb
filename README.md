# kgdb

> **Absorbed by sldb (2026-09-20).** sldb is now one product with two internal layers, text and
> graph; see [the ADR](../sldb/docs/architecture/sldb-absorbs-kgdb.md). This repo is frozen: it
> keeps working for the consumers that still import it, and no new capability lands here.
>
> Since 2026-09-20 it is also **hollow**: the contracts, the query language and the sldb ingest are
> re-exports of sldb's, so `kgdb.contracts.KnowledgeNode is sldb.store.graph.KnowledgeNode` — one
> class in the ecosystem, not two that look alike. What is still implemented here is the networkx
> layer sldb deliberately does not have: `kgdb.graph.utils` (a `MultiDiGraph` view of a snapshot),
> the executor and neighborhood walk that run **over a networkx graph**, the JSON-lines query
> server, and `kgdb.ingest.typed`, the frozen assembler the parity test compares against.
>
> | what you used here | where it lives now |
> |---|---|
> | `kgdb.models.*` (`RelationTypeDoc`, `RelationDoc`, builtins) | `sldb.models.*` — this package re-exports them |
> | `kgdb.world.init_world` | `sldb.api.init_relations` — this one delegates |
> | `kgdb.ingest.typed.build_typed_snapshot` | sldb's edge index, rebuilt by the write itself: `sldb.api.load_edge_index` |
> | `kgdb.query.{StructuredQuery, execute_query}` | `sldb.store.graph` / `sldb.api.graph.execute_query` |
> | `kgdb.query.neighborhood.collect_neighborhood*` | `sldb.api.graph.collect_neighborhood*` |
> | `kgdb.contracts.io.{GraphSnapshot, QueryResult}` | `sldb.store.graph` |
> | `kgdb.graph.{save_graph, load_graph}` | `sldb.store.graph.graph_io` — same node-link JSON, no networkx |
> | `kgdb.ingest.sldb.sldb_semantic_export_to_snapshot` | `sldb.api.graph.ingest_sldb` |
> | `kgdb ingest \| get \| list \| query \| edges` | `sldb edges …` and `sldb graph …` |
> | `kgdb.contracts.persistence` (declared, never implemented) | implemented as sldb's write journal: `sldb journal` |
>
> What did not come along: the networkx dependency (sldb traverses its own adjacency maps) and the
> JSON-lines query server. `kgdb.ingest.typed` stays here as the oracle the parity test compares
> against.

`kgdb` was the graph persistence, traversal, and query substrate for the HUM ecosystem.

## Installation

Requires Python 3.10 or later.

```bash
# Clone the repo (or use the hum-ecosystem checkout)
pip install -e .
```

Or install the package directly from its directory:

```bash
cd /path/to/hum-ecosystem/tools/kgdb
pip install -e .
```

The CLI entry point `kgdb` becomes available after installation.

### Dependencies

- `pydantic>=2.0.0`
- `networkx>=3.0`

### Development install

```bash
pip install -e ".[dev]"
pip install pytest pytest-asyncio
pytest
```

## CLI Usage

After install, the `kgdb` console script is on your PATH:

```bash
kgdb --help
kgdb init --store .sldb --pythonpath .                                   # typed relations: models, builtin types, predicates
kgdb ingest --store .sldb --pythonpath . --output kgdb.graph.json        # the typed graph of a store
kgdb ingest-sldb --input kgdb.semantic.json --output kgdb.graph.json     # legacy: structural graph from an export file
kgdb list --graph kgdb.graph.json
kgdb get --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
kgdb edges --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
kgdb query --graph kgdb.graph.json --query-file query.json
```

It runs in parallel with `sldb`:

- `sldb` owns semantic document truth: tracked Markdown documents, document models, semantic tags, section indexes, semantic DAG relationships, equivalences, and document/model/store hashes.
- `kgdb` owns graph persistence and traversal: validating graph-ready payloads, converting them into graph records, storing graph nodes and edges, and answering deterministic graph queries for downstream tools.

KGDB must not scrape `.sldb/runtime` or reinterpret Markdown semantics. It reads SLDB through its library and its versioned export contract, never its runtime files.

## Typed Relations

Since 2026-09-09 kgdb types its relations, and the types are sldb documents. Since the fusion
of kgdb into sldb (branch `fusion-kgdb`) the two models and the builtin types live in sldb
(`sldb.models.relation_type_doc`, `sldb.models.relation_doc`, `sldb.models.builtin_relation_types`);
`kgdb.models` re-exports them, and sldb's own edge index (`sldb.api.load_edge_index`) holds the
same nodes and edges `build_typed_snapshot` builds — `tests/test_edge_index_parity.py` is the gate.

- `kgdb.models.RelationTypeDoc` declares a relation type: `name`, `direction`, `cardinality`, `axis`
  (the predicate axis it answers), `source_types` / `target_types` (model names, with inheritance
  through `base_models`, or kgdb node types), and a default `condition` every edge inherits.
- `kgdb.models.RelationDoc` is one authored edge: `source_id`, `target_id` (sldb export ids,
  `Model:name`), `relation_type`, an optional `condition` override, notes. It is a document of the
  world's store and it is **not** a node of the graph.
- The structural relations kgdb itself produces (`has_model`, `has_document`, `has_section`,
  `tagged_as`, `semantic_parent`, `semantic_equivalent`, `has_field`, `extends`,
  `applies_to_source`, `applies_to_target`, `names`) ship as RelationTypeDocs in
  `kgdb.models.builtin`, so a graph is described entirely by documents.

`kgdb init` (now `sldb.api.init_relations`, which it calls) registers the two models, writes the
builtin relation types under `sldb/relation_types/` and tracks them, and registers each relation
name as an sldb predicate with its axis. It is idempotent.

`kgdb ingest --store` runs sldb's semantic export by library, then adds: document nodes typed by
their model name; an `sldb_field` node per model field (type, description) with `has_field` edges and
`extends` edges from `base_models`; a `relation_type` node per RelationTypeDoc with `applies_to_*`
edges to the models it names (so "what verbs apply to this class" is `edges_to` on the model node);
an `anchor` node per alias document with `names` edges to what its `ref` names; and one typed edge
per RelationDoc, hung on its source, with `origin`, `condition` and `axis` in its metadata.
Documents tagged `type.pron.move` (a ledger) are left out; `--exclude-tag` changes that.

Every edge is then validated: its type is a tracked RelationTypeDoc, both endpoints exist, their
classes are allowed, cardinality holds, undirected types get their reverse edge. Any violation is an
error and nothing is written. The world prevents at authoring time; kgdb detects at assembly time.

The persisted graph is a `networkx.MultiDiGraph` keyed by `(source, target, relation_type)`, so two
relations between the same pair of nodes both survive (the legacy `DiGraph` collapsed them).
`kgdb edges`, `kgdb query` and the Python API work on both.

Not yet in the typed graph: predicate links written in prose (`[implements:: [[x]]]`); sldb recovers
them but does not export them.

## Purpose

Use KGDB to:

- Persist graph records produced by SLDB or another structured graph producer.
- Traverse stored graph relationships deterministically.
- Query graph nodes by identity, semantics, and graph scope.
- Provide downstream tools with graph state without making those tools depend on SLDB internals.

KGDB is intentionally dumb. It stores and traverses graph facts; it does not decide whether SLDB's semantic interpretation is correct.

### Snapshot validation

KGDB owns snapshot validation. Invalid snapshots must be caught before they propagate to downstream consumers or drift checks. Validation must:

- Report specific contract violations (missing fields, wrong types, unknown node/edge types).
- Never crash on malformed input.
- Apply to all ingest paths (`ingest`, `ingest-sldb`) consistently.

Consumers (deskops, hum, truth_machine) should call KGDB's validation API, not parse raw snapshot JSON themselves.

### Graph trace surface

KGDB's query surface includes graph traceability: resolving relationships between atoms, files, documents, tests, and other graph nodes. Deskops lifecycle gates and drift checks consume this surface.

The trace surface must:

- Handle missing nodes, disconnected graphs, and edge cases gracefully without crashing.
- Be available through both the CLI (`kgdb query`, `kgdb get`, `kgdb edges`) and the Python API.
- Not require downstream consumers to understand internal NetworkX serialization details.

## Non-Goals

KGDB does not own:

- Semantic reasoning over Markdown documents.
- SLDB document model definitions or semantic tag assignment.
- Direct reads from `.sldb/runtime` as an ingest mechanism.
- Formal truth evaluation.
- UI layout or workflow-shell orchestration.
- Source-code relation extraction unless a downstream adapter provides those graph facts explicitly.

## SLDB Semantic Ingest Contract

KGDB consumes `sldb_kgdb_semantic_export` version `1`.

The schema is defined at `contracts/schemas/sldb_kgdb_semantic_export.schema.json`, and KGDB declares the dependency in `contracts/integration.contract.yaml`.

The payload includes:

- Contract metadata and producer metadata.
- Store provenance, including store root, store path, store hash, and runtime source paths as provenance only.
- SLDB model entries and model hashes.
- SLDB document entries, document index hashes, document content hashes, paths, and semantic tags.
- SLDB section entries, section paths, titles, breadcrumbs, derived `about` terms, semantic tags, slugs, heading levels, and source line ranges when available.
- Semantic DAG nodes, parent links, and equivalence mappings.

KGDB converts the payload into graph nodes with these node types:

- `sldb_store`
- `sldb_model`
- `sldb_document`
- `sldb_section`
- `semantic_tag`

KGDB generates these SLDB-owned semantic graph relations:

- `has_model`
- `has_document`
- `has_section`
- `tagged_as`
- `semantic_parent`
- `semantic_equivalent`

The current stable node identifiers use the `sldb://` namespace, for example `sldb://document/TaskDoc:001-example` and `sldb://semantic_tag/domain.contract`.

## Export From SLDB

Run the export from the project that owns the `.sldb` store:

```bash
sldb stores semantic-export --store .sldb --pythonpath . --format kgdb --encoding json --rebuild -o kgdb.semantic.json
```

Use `-o -` or omit `-o` to write the export to stdout. Use `--encoding yaml` when a YAML handoff is easier to inspect. `--rebuild` refreshes semantic and section indexes before export.

The SLDB export command publishes semantic truth as a bulk handoff contract. It is not a KGDB query and it is not permission to scrape SLDB runtime files.

## Ingest Into KGDB

Convert an SLDB semantic export into a persisted KGDB graph:

```bash
kgdb ingest-sldb --input kgdb.semantic.json --output kgdb.graph.json
```

The command validates the payload contract name and version before conversion. It writes a NetworkX-backed graph JSON file containing the SLDB semantic nodes, edges, hashes, and provenance metadata.

The same ingest path is available from Python:

```python
import json
from pathlib import Path

from kgdb.ingest import sldb_semantic_export_to_snapshot

payload = json.loads(Path("kgdb.semantic.json").read_text(encoding="utf-8"))
snapshot = sldb_semantic_export_to_snapshot(payload)
```

## Query KGDB

Downstream tools query KGDB's persisted graph instead of bypassing SLDB semantic ownership.

For example, find SLDB documents tagged with `domain.contract` by querying ancestors of the semantic tag node and filtering for `sldb_document` nodes:

```json
{
  "scope": {
    "ancestor_of": "sldb://semantic_tag/domain.contract"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "sldb_document"
        }
      ]
    }
  ]
}
```

Save the query as `query.json`, then run:

```bash
kgdb query --graph kgdb.graph.json --query-file query.json
```

Structured examples for the SLDB semantic fixture live in `contracts/queries/sldb/`.
Create the example graph, then run any query file against it:

```bash
kgdb ingest-sldb \
  --input contracts/fixtures/sldb_kgdb_semantic_export.v1.json \
  --output /tmp/sldb.kg.json
```

```bash
kgdb query \
  --graph /tmp/sldb.kg.json \
  --query-file contracts/queries/sldb/documents_tagged_domain_contract.json
```

```bash
kgdb query \
  --graph /tmp/sldb.kg.json \
  --query-file contracts/queries/sldb/semantic_neighborhood_integration_kgdb.json
```

```bash
kgdb query \
  --graph /tmp/sldb.kg.json \
  --query-file contracts/queries/sldb/sections_for_taskdoc_document.json
```

```bash
kgdb query \
  --graph /tmp/sldb.kg.json \
  --query-file contracts/queries/sldb/documents_near_taskdoc_model.json
```

```bash
kgdb query \
  --graph /tmp/sldb.kg.json \
  --query-file contracts/queries/sldb/documents_near_domain_workflow_task_tag.json
```

The example queries prove these graph questions:

- `documents_tagged_domain_contract.json`: documents with an outgoing path to `sldb://semantic_tag/domain.contract`.
- `semantic_neighborhood_integration_kgdb.json`: semantic parents and equivalents reachable from `sldb://semantic_tag/integration.kgdb`.
- `sections_for_taskdoc_document.json`: sections reachable from a document node.
- `documents_near_taskdoc_model.json`: document nodes reachable from `sldb://model/TaskDoc`.
- `documents_near_domain_workflow_task_tag.json`: document nodes with an outgoing path to `sldb://semantic_tag/domain.workflow.task`.

Other supported read commands are:

```bash
kgdb list --graph kgdb.graph.json
kgdb get --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
kgdb edges --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
```

Downstream adapters may add non-SLDB graph facts after ingest, such as source-file relationships, workflow provenance, or UI projection edges. Those facts should point at SLDB export IDs or `sldb://` nodes as stable anchors, but they do not become SLDB semantic truth. If a tool needs to change semantic tags, document sections, equivalences, or model meaning, it must update SLDB and re-export rather than mutating KGDB as the source of truth.
