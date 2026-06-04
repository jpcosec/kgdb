import json
import sys
from pathlib import Path

import networkx as nx

from kgdb.graph.utils import add_knowledge_node, load_graph, load_knowledge_node
from kgdb.ingest import sldb_semantic_export_to_snapshot
from kgdb.main import main
from kgdb.query import StructuredQuery, execute_query


REPO_ROOT = Path(__file__).resolve().parents[1]
SLDB_FIXTURE = REPO_ROOT / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"


def test_sldb_semantic_export_converts_to_kgdb_snapshot():
    payload = json.loads(SLDB_FIXTURE.read_text(encoding="utf-8"))

    snapshot = sldb_semantic_export_to_snapshot(payload)
    nodes_by_id = {node.identity.node_id: node for node in snapshot.nodes}

    assert nodes_by_id["sldb://store"].identity.node_type == "sldb_store"
    assert nodes_by_id["sldb://model/TaskDoc"].identity.node_type == "sldb_model"
    assert (
        nodes_by_id[
            "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
        ].identity.node_type
        == "sldb_document"
    )
    assert nodes_by_id["sldb://semantic_tag/domain.contract"].identity.node_type == (
        "semantic_tag"
    )

    store_edges = nodes_by_id["sldb://store"].edges
    assert (store_edges[0].target_id, store_edges[0].relation_type) == (
        "sldb://model/TaskDoc",
        "has_model",
    )

    document = nodes_by_id[
        "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    ]
    assert document.semantics.hash_c == "hash-doc-index-001"
    assert document.semantics.hash_d == "hash-doc-content-001"
    assert document.source.store["hash_a"] == "hash-store-001"
    assert document.source.producer["name"] == "sldb"
    assert any(
        edge.target_id == "sldb://semantic_tag/domain.contract"
        and edge.relation_type == "tagged_as"
        for edge in document.edges
    )


def test_sldb_semantic_graph_finds_documents_through_tags():
    payload = json.loads(SLDB_FIXTURE.read_text(encoding="utf-8"))
    snapshot = sldb_semantic_export_to_snapshot(payload)
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)

    query = StructuredQuery.model_validate(
        {
            "scope": {"ancestor_of": "sldb://semantic_tag/domain.contract"},
            "filters": [
                {
                    "facet": "identity",
                    "conditions": [
                        {"field": "node_type", "op": "eq", "value": "sldb_document"}
                    ],
                }
            ],
        }
    )

    results = execute_query(graph, query)

    assert [node.identity.node_id for node in results] == [
        "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    ]


def test_ingest_sldb_cli_writes_networkx_graph(tmp_path, monkeypatch):
    output_file = tmp_path / "sldb.kg.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kgdb",
            "ingest-sldb",
            "--input",
            str(SLDB_FIXTURE),
            "--output",
            str(output_file),
        ],
    )

    main()

    graph = load_graph(output_file)
    document = load_knowledge_node(
        graph, "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    )

    assert output_file.exists()
    assert graph.nodes["sldb://semantic_tag/integration.kgdb"]["type"] == "semantic_tag"
    assert graph.has_edge(
        "sldb://semantic_tag/integration.kgdb",
        "sldb://semantic_tag/knowledge_graph.kgdb",
    )
    assert document.semantics.path == (
        "desk/tasks/001-define-kgdb-semantic-export-payload.md"
    )
