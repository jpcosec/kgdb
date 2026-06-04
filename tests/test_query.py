import json
from pathlib import Path
import pytest
from kgdb.main import main
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBSTRATE_FIXTURE = REPO_ROOT / "desk" / "fixtures" / "substrate_v1.json"

def test_query_scoped(tmp_path, monkeypatch):
    """Verify that a scoped query works via CLI."""
    # 1. Ingest substrate to temp file
    input_fixture = SUBSTRATE_FIXTURE
    graph_file = tmp_path / "substrate.kg.json"
    
    # Ingest first
    from kgdb.contracts.io import GraphSnapshot
    from kgdb.graph.utils import add_knowledge_node, save_graph
    import networkx as nx
    
    snapshot = GraphSnapshot.model_validate_json(input_fixture.read_text())
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    save_graph(graph, graph_file)
    
    # 2. Create a query file
    # Query for descendants of 'repo://hum-ecosystem'
    query_data = {
        "scope": {
            "descendant_of": "repo://hum-ecosystem"
        },
        "filters": []
    }
    query_file = tmp_path / "query.json"
    query_file.write_text(json.dumps(query_data))
    
    # 3. Run query command
    # Use capsys to capture stdout
    from _pytest.capture import CaptureFixture
    
    test_args = ["kgdb", "query", "--graph", str(graph_file), "--query-file", str(query_file)]
    monkeypatch.setattr(sys, "argv", test_args)
    
    # We need to capture stdout
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    
    output = f.getvalue()
    results = json.loads(output)
    
    # In the substrate, hum-ecosystem contains all other nodes (repos)
    # nx.descendants(graph, 'repo://hum-ecosystem') should return 9 nodes
    assert len(results) == 9
    node_ids = [n["identity"]["node_id"] for n in results]
    assert "repo://hum" in node_ids
    assert "repo://repopackage" in node_ids

def test_query_filter(tmp_path, monkeypatch):
    """Verify that a filtered query works via CLI."""
    input_fixture = SUBSTRATE_FIXTURE
    graph_file = tmp_path / "substrate.kg.json"
    
    # Ingest
    from kgdb.contracts.io import GraphSnapshot
    from kgdb.graph.utils import add_knowledge_node, save_graph
    import networkx as nx
    snapshot = GraphSnapshot.model_validate_json(input_fixture.read_text())
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    save_graph(graph, graph_file)
    
    # Query for nodes where identity.node_type == 'system'
    query_data = {
        "filters": [
            {
                "facet": "identity",
                "conditions": [
                    {"field": "node_type", "op": "eq", "value": "system"}
                ]
            }
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
