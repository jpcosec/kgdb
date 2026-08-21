import json
from pathlib import Path
import pytest
from kgdb.main import main
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBSTRATE_FIXTURE = REPO_ROOT / "desk" / "fixtures" / "substrate_v1.json"


def _ingest_substrate(graph_file: Path):
    """Shared helper: ingest the substrate fixture into a graph file."""
    from kgdb.contracts.io import GraphSnapshot
    from kgdb.graph.utils import add_knowledge_node, save_graph
    import networkx as nx
    snapshot = GraphSnapshot.model_validate_json(SUBSTRATE_FIXTURE.read_text())
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    save_graph(graph, graph_file)


def test_query_scoped(tmp_path, monkeypatch):
    """Verify that a scoped query works via CLI."""
    graph_file = tmp_path / "substrate.kg.json"
    _ingest_substrate(graph_file)

    query_data = {"scope": {"descendant_of": "repo://hum-ecosystem"}, "filters": []}
    query_file = tmp_path / "query.json"
    query_file.write_text(json.dumps(query_data))

    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()

    results = json.loads(f.getvalue())
    assert len(results) == 9
    node_ids = [n["identity"]["node_id"] for n in results]
    assert "repo://hum" in node_ids
    assert "repo://repopackage" in node_ids


def test_query_filter(tmp_path, monkeypatch):
    """Verify that a filtered query works via CLI."""
    graph_file = tmp_path / "substrate.kg.json"
    _ingest_substrate(graph_file)

    query_data = {
        "filters": [
            {"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "system"}]}
        ]
    }
    query_file = tmp_path / "query_filter.json"
    query_file.write_text(json.dumps(query_data))

    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()

    results = json.loads(f.getvalue())
    assert len(results) == 1
    assert results[0]["identity"]["node_id"] == "repo://hum-ecosystem"


def test_query_relation_filter_filters_edges(tmp_path, monkeypatch):
    """RelationFilter filters edges: only allowed relation_types survive."""
    graph_file = tmp_path / "substrate.kg.json"
    _ingest_substrate(graph_file)

    query_data = {"relations": [{"relation_types": ["depends_on"]}]}
    query_file = tmp_path / "query_depends_on.json"
    query_file.write_text(json.dumps(query_data))

    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()

    results = json.loads(f.getvalue())
    for node_data in results:
        for edge in node_data.get("edges", []):
            assert edge["relation_type"] == "depends_on", \
                f"Expected depends_on, got {edge['relation_type']}"


def test_query_relation_filter_empty_allows_all(tmp_path, monkeypatch):
    """Empty relation_types list = no type filtering: all edges pass."""
    graph_file = tmp_path / "substrate.kg.json"
    _ingest_substrate(graph_file)

    query_data = {"relations": [{"relation_types": []}]}
    query_file = tmp_path / "query_all_edges.json"
    query_file.write_text(json.dumps(query_data))

    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()

    results = json.loads(f.getvalue())
    types_found = set()
    for node_data in results:
        for edge in node_data.get("edges", []):
            types_found.add(edge["relation_type"])
    assert "depends_on" in types_found
    assert "contains" in types_found


def test_query_relation_filter_no_filter_keeps_all_edges(tmp_path, monkeypatch):
    """No RelationFilter at all: all original edges are kept unchanged."""
    graph_file = tmp_path / "substrate.kg.json"
    _ingest_substrate(graph_file)

    query_data = {"filters": [], "scope": None}
    query_file = tmp_path / "query_no_filter.json"
    query_file.write_text(json.dumps(query_data))

    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()

    results = json.loads(f.getvalue())
    types_found = set()
    for node_data in results:
        for edge in node_data.get("edges", []):
            types_found.add(edge["relation_type"])
    assert "depends_on" in types_found
    assert "contains" in types_found