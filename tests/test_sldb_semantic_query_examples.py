import json
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import networkx as nx

from kgdb.graph.utils import add_knowledge_node, save_graph
from kgdb.ingest import sldb_semantic_export_to_snapshot
from kgdb.main import main


REPO_ROOT = Path(__file__).resolve().parents[1]
SLDB_FIXTURE = REPO_ROOT / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"
QUERY_DIR = REPO_ROOT / "contracts" / "queries" / "sldb"

DOCUMENT_ID = "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
SECTION_ID = (
    "sldb://section/TaskDoc:001-define-kgdb-semantic-export-payload"
    "#define-kgdb-semantic-export-payload"
)


def test_sldb_semantic_query_examples_answer_expected_graph_questions(tmp_path, monkeypatch):
    graph_file = _write_sldb_graph(tmp_path / "sldb.kg.json")

    assert _query_node_ids(
        monkeypatch, graph_file, "documents_tagged_domain_contract.json"
    ) == {DOCUMENT_ID}
    assert _query_node_ids(
        monkeypatch, graph_file, "semantic_neighborhood_integration_kgdb.json"
    ) == {
        "sldb://semantic_tag/integration",
        "sldb://semantic_tag/knowledge_graph.kgdb",
    }
    assert _query_node_ids(
        monkeypatch, graph_file, "sections_for_taskdoc_document.json"
    ) == {SECTION_ID}
    assert _query_node_ids(
        monkeypatch, graph_file, "documents_near_taskdoc_model.json"
    ) == {DOCUMENT_ID}
    assert _query_node_ids(
        monkeypatch, graph_file, "documents_near_domain_workflow_task_tag.json"
    ) == {DOCUMENT_ID}


def _write_sldb_graph(graph_file: Path) -> Path:
    payload = json.loads(SLDB_FIXTURE.read_text(encoding="utf-8"))
    snapshot = sldb_semantic_export_to_snapshot(payload)
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    save_graph(graph, graph_file)
    return graph_file


def _query_node_ids(monkeypatch, graph_file: Path, query_name: str) -> set[str]:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kgdb",
            "query",
            "--graph",
            str(graph_file),
            "--query-file",
            str(QUERY_DIR / query_name),
        ],
    )

    output = StringIO()
    with redirect_stdout(output):
        main()

    return {node["identity"]["node_id"] for node in json.loads(output.getvalue())}
