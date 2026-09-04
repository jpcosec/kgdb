# kgdb

`kgdb` is the graph persistence, traversal, and query substrate for the HUM ecosystem.

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
kgdb ingest-sldb --input kgdb.semantic.json --output kgdb.graph.json
kgdb list --graph kgdb.graph.json
kgdb get --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
kgdb edges --graph kgdb.graph.json --node sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload
kgdb query --graph kgdb.graph.json --query-file query.json
```

It runs in parallel with `sldb`:

- `sldb` owns semantic document truth: tracked Markdown documents, document models, semantic tags, section indexes, semantic DAG relationships, equivalences, and document/model/store hashes.
- `kgdb` owns graph persistence and traversal: validating graph-ready payloads, converting them into graph records, storing graph nodes and edges, and answering deterministic graph queries for downstream tools.

KGDB must not scrape `.sldb/runtime` or reinterpret Markdown semantics. It only ingests SLDB semantics through the versioned export contract that SLDB publishes.

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
