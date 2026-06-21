# Round 01: Initial execution of kgdb stress tests

## Summary
- STs executed: ST-get, ST-list, ST-query, ST-edges, ST-ingest, ST-ingest-sldb, ST-snapshots, ST-edge-cases, ST-contracts
- Total findings: 15

## Findings

### Finding KGDB-01: `load_graph()` incompatible with GraphSnapshot format (all read-only commands broken)
- **ST**: ST-get, ST-list, ST-query, ST-edges, ST-snapshots, ST-edge-cases, ST-contracts
- **Step**: 2 (and all steps requiring `--graph` with native fixture)
- **Command**: `kgdb get --graph desk/fixtures/substrate_v1.json --node "system:ecosystem"`
- **Expected**: Node data returned for existing node
- **Observed**:
  ```
  Traceback (most recent call last):
    File ".../networks/readwrite/json_graph/node_link.py", line 247, in node_link_graph
      for d in data[edges]:
               ~~~~^^^^^^^
  KeyError: 'edges'
  ```
- **Severity**: high
- **Type**: silent-failure / consistency
- **Details**: `src/kgdb/graph/utils.py:40` uses `networkx.node_link_graph()` which expects top-level `nodes` and `links`/`edges` keys (NetworkX node-link format). But the native GraphSnapshot format stores edges nested within each node (`nodes[].edges`), not at the top level. Every read-only CLI command (get, list, query, edges) depends on `load_graph()` and is therefore broken for all GraphSnapshot-format fixtures. Only `ingest` works because it manually converts GraphSnapshot → NetworkX format. The output of `ingest` (node-link format) can then be used by the other commands, but this is not documented and creates a confusing two-step workflow.

---

### Finding KGDB-02: Raw Python tracebacks instead of user-friendly error messages
- **ST**: ST-get, ST-list, ST-query, ST-ingest, ST-contracts, ST-snapshots
- **Step**: Multiple (all error cases)
- **Command**: (various)
- **Expected**: Clean, semantic error messages suggesting corrective action
- **Observed**: Full Python tracebacks for `FileNotFoundError`, `JSONDecodeError`, `KeyError`, `IsADirectoryError` with internal file paths and line numbers
- **Severity**: medium
- **Type**: error-message
- **Details**: Examples:
  - `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/nonexistent'` — raw traceback
  - `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` — raw traceback
  - `IsADirectoryError: [Errno 21] Is a directory: 'desk/fixtures'` — raw traceback
  - `KeyError: 'edges'` — raw traceback

---

### Finding KGDB-03: `ingest` silently accepts invalid/unsupported schemas without validation
- **ST**: ST-ingest, ST-snapshots
- **Step**: 6 (invalid schema), 7 (future version), 8 (missing version)
- **Command**:
  ```bash
  echo '{"version": "bad", "nodes": []}' | kgdb ingest --input ... --output ...
  echo '{"version": "999.0", "nodes": []}' | kgdb ingest --input ... --output ...
  echo '{"nodes": []}' | kgdb ingest --input ... --output ...
  ```
- **Expected**: Validation error for unsupported version, missing field, or invalid data
- **Observed**: All three produce `Ingested 0 nodes` with exit code 0 — no error, no warning
- **Severity**: medium
- **Type**: silent-failure / error-message
- **Details**: The `ingest` command does not validate:
  - Version string format
  - Version range (future versions silently accepted)
  - Required fields (version is optional in practice)
  - Node data integrity (empty nodes arrays with nonsensical versions pass)

---

### Finding KGDB-04: Contract schema does not match fixture structure
- **ST**: ST-contracts
- **Step**: 1 (validate substrate against schema)
- **Command**: `python3 -c "import json, jsonschema; ..."`
- **Expected**: `substrate_v1.json: valid`
- **Observed**:
  ```
  jsonschema.exceptions.ValidationError: 'edges' is a required property
  ```
- **Severity**: high
- **Type**: consistency
- **Details**: The schema `kgdb_graph_bundle.schema.json` requires a top-level `edges` array (`"required": ["nodes", "edges"]`), but the substrate fixture stores edges nested inside each node (no top-level `edges`). This means:
  1. The only existing fixture does not validate against its own schema
  2. The schema was designed for NetworkX node-link format (top-level edges)
  3. The fixture uses GraphSnapshot format (nested edges)
  4. These are two incompatible data models

---

### Finding KGDB-05: UTF-8/emoji in node IDs displayed as escaped unicode
- **ST**: ST-edge-cases
- **Step**: 14 (UTF-8 in node IDs)
- **Command**: `kgdb list --graph /tmp/utf8-ingested.json`
- **Expected**: `nodo-ñoño-🎉`
- **Observed**: `nodo-\u00f1o\u00f1o-\ud83c\udf89`
- **Severity**: low
- **Type**: consistency / CI-readiness
- **Details**: The CLI uses `json.dumps()` (or similar) for all output, which escapes non-ASCII characters by default. This breaks the user experience for international content and makes piping/scrolling harder.

---

### Finding KGDB-06: `kgdb` with no arguments exits 0 despite error
- **ST**: ST-edge-cases
- **Step**: 7c (no arguments)
- **Command**: `kgdb`
- **Expected**: Exit code 2 (argparse error)
- **Observed**: Exit code 0 even though it prints `kgdb: error: the following arguments are required: command`
- **Severity**: low
- **Type**: CI-readiness / error-message
- **Details**: Subcommands correctly exit 2 on missing required arguments (`kgdb get` → exit 2), but the top-level `kgdb` (no subcommand) exits 0 even though it prints an argparse error. This makes it unreliable to detect CLI errors via exit codes.

---

### Finding KGDB-07: YAML files produce confusing JSONDecodeError instead of "YAML not supported"
- **ST**: ST-snapshots
- **Step**: 2, 3
- **Command**: `kgdb list --graph .sldb/runtime/semantic_dag.yaml`
- **Expected**: Clear message like "YAML format not supported, use JSON"
- **Observed**:
  ```
  json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
  ```
- **Severity**: low
- **Type**: error-message / discoverability
- **Details**: The `.sldb/runtime/` directory contains YAML files. The CLI tries to parse them as JSON and fails with a confusing JSON parser error. A user exploring `.sldb/runtime/` would not know why `kgdb list --graph` fails on these files.

---

### Finding KGDB-08: Duplicate `--graph` flag not rejected
- **ST**: ST-edge-cases
- **Step**: 6
- **Command**: `kgdb list --graph desk/fixtures/substrate_v1.json --graph /tmp/other.json`
- **Expected**: Argparse error: "argument --graph: expected one argument" or "conflicting flag"
- **Observed**: Silently uses the first `--graph` value for the error (FileNotFoundError on `/tmp/other.json` because only `/tmp/other.json` fails). Argparse doesn't reject duplicates by default.
- **Severity**: low
- **Type**: edge-case
- **Details**: Python argparse allows duplicate flags by default (last one wins). If the user accidentally passes `--graph` twice, unexpected behavior occurs.

---

### Finding KGDB-09: Error output stream mixing
- **ST**: ST-edge-cases
- **Step**: 9, 10
- **Command**: `kgdb list --graph desk/fixtures/substrate_v1.json 2>/dev/null`
- **Expected**: Empty stdout, errors to stderr
- **Observed**: Errors correctly go to stderr (no output with `2>/dev/null`). When piping to `head -5`, the pipe capture stderr first (before head is invoked), showing the traceback in the pipe output. When piping list output to get (step 10 of ST-list), exit code 123 from pipefail.
- **Severity**: low
- **Type**: CI-readiness
- **Details**: Exit code 123 in piped commands is a concern for CI reliability.

---

### Finding KGDB-10: No `--query-file` option documentation in help
- **ST**: ST-query
- **Step**: 1
- **Command**: `kgdb query --help`
- **Expected**: Help text describing the JSON format expected by `--query-file`
- **Observed**:
  ```
  usage: kgdb query [-h] --graph GRAPH --query-file QUERY_FILE

  options:
    -h, --help       show this help message and exit
    --graph GRAPH
    --query-file QUERY_FILE
  ```
- **Severity**: low
- **Type**: discoverability
- **Details**: The `--help` output lists flags but gives no description of what they do, no example values, and no hint about the expected query file JSON schema. A user must read source code or documentation to know the format.

---

### Finding KGDB-11: Pydantic validation error shown as traceback when passing wrong format to `ingest`
- **ST**: ST-ingest-sldb
- **Step**: 8 (ingest SLDB export via `ingest`)
- **Command**: `kgdb ingest --input contracts/fixtures/sldb_kgdb_semantic_export.v1.json --output /tmp/out.json`
- **Expected**: Clear message like "Not a valid GraphSnapshot file. Use `ingest-sldb` for SLDB exports."
- **Observed**:
  ```
  pydantic_core._pydantic_core.ValidationError: 1 validation error for GraphSnapshot
  nodes
    Field required [type=missing, ...]
  ```
- **Severity**: medium
- **Type**: error-message / discoverability
- **Details**: When a user accidentally passes an SLDB export to `ingest` (instead of `ingest-sldb`), they get a Pydantic traceback with a link to pydantic.dev docs. A user-friendly message should suggest which command to use.

---

### Finding KGDB-12: Dangling edges in SLDB export accepted without warning
- **ST**: ST-ingest-sldb
- **Step**: 6
- **Command**: (modified SLDB export with dangling edge)
- **Expected**: Warning or error about edge targeting nonexistent node
- **Observed**: `Ingested 14 SLDB semantic nodes` (accepted without warning)
- **Severity**: low
- **Type**: silent-failure
- **Details**: Adding a `parent` reference to a nonexistent node ID is silently accepted. For a graph tool that emphasizes contract validation, dangling edges should at minimum produce a warning.

---

### Finding KGDB-13: Contract schema validation fails for the only existing fixture
- **ST**: ST-contracts
- **Step**: 1
- **Command**: `python3 -c "import json, jsonschema; ..."`
- **Expected**: Valid
- **Observed**: `jsonschema.exceptions.ValidationError: 'edges' is a required property`
- **Severity**: high
- **Type**: consistency
- **Details**: The substrate fixture (`desk/fixtures/substrate_v1.json`) fails validation against its own declared schema. The schema requires a top-level `edges` array, but the fixture uses GraphSnapshot format with edges nested inside nodes.

---

### Finding KGDB-14: No `--version` flag
- **ST**: ST-edge-cases
- **Step**: 7
- **Command**: `kgdb --version`
- **Expected**: Version string like `kgdb 0.1.0`
- **Observed**: `usage: kgdb [-h] {get,list,query,edges,ingest,ingest-sldb} ... kgdb: error: argument command: invalid choice: '--version'`
- **Severity**: low
- **Type**: discoverability
- **Details**: No `--version` flag exists. A user cannot check which version of kgdb is installed without examining `pyproject.toml` or `__init__.py`.

---

### Finding KGDB-15: `ingest` and `ingest-sldb` have identical `--help` with no distinction
- **ST**: ST-ingest, ST-ingest-sldb
- **Step**: 1
- **Command**: `kgdb ingest --help` / `kgdb ingest-sldb --help`
- **Expected**: Help text explaining what each subcommand does and what format it expects
- **Observed**: Both show:
  ```
  usage: kgdb ingest[-sldb] [-h] --input INPUT --output OUTPUT

  options:
    -h, --help       show this help message and exit
    --input INPUT
    --output OUTPUT
  ```
- **Severity**: low
- **Type**: discoverability
- **Details**: The two `ingest` subcommands have identical, minimal help text. No description explains:
  - What format `--input` expects (GraphSnapshot vs SLDB semantic export)
  - What `ingest-sldb` does differently from `ingest`
  - What the output format is
  - Example usage
