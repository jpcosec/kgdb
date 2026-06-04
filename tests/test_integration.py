import json
from pathlib import Path
import pytest
from kgdb.contracts.io import QueryResult
from kgdb.graph.utils import load_graph, load_knowledge_node

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBSTRATE_FIXTURE = REPO_ROOT / "desk" / "fixtures" / "substrate_v1.json"

def test_downstream_consumption_contract():
    """
    Prove that kgdb output can be transformed into a Graph UI payload.
    This simulates the 'graph_ui' L1 adapter consuming kgdb results.
    """
    from kgdb.contracts.io import GraphSnapshot
    from kgdb.graph.utils import add_knowledge_node
    import networkx as nx
    
    graph_path = SUBSTRATE_FIXTURE
    snapshot = GraphSnapshot.model_validate_json(graph_path.read_text())
    
    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    
    # Simulate a query result
    nodes = [load_knowledge_node(graph, node_id) for node_id in graph.nodes]
    query_result = QueryResult(
        primary_ids=list(graph.nodes),
        nodes=nodes,
        metadata={"source": "kgdb-integration-test"}
    )
    
    # Transformation logic (what a downstream consumer would do)
    ui_payload = {
        "nodes": [
            {
                "id": node.identity.node_id,
                "label": node.identity.node_id.split("/")[-1],
                "node_type": node.identity.node_type,
                "metadata": node.semantics.model_dump() if node.semantics else {}
            }
            for node in query_result.nodes
        ],
        "edges": []
    }
    
    for node in query_result.nodes:
        for edge in node.edges:
            ui_payload["edges"].append({
                "source": node.identity.node_id,
                "target": edge.target_id,
                "relation_type": edge.relation_type
            })
            
    # Verification
    assert len(ui_payload["nodes"]) == 10
    assert len(ui_payload["edges"]) > 0
    
    # Check one node
    repo_node = next(n for n in ui_payload["nodes"] if n["id"] == "repo://hum-ecosystem")
    assert repo_node["node_type"] == "system"
    
    # Check one edge
    edge = next(e for e in ui_payload["edges"] if e["source"] == "repo://hum-ecosystem" and e["target"] == "repo://kgdb")
    assert edge["relation_type"] == "contains"
