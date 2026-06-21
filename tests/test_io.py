from kgdb.contracts.io import GraphSnapshot, QueryResult
from kgdb.contracts.node import KnowledgeNode

def test_graph_snapshot_structure():
    snapshot = GraphSnapshot(
        version="1.0",
        nodes=[],
        metadata={"key": "value"}
    )
    assert snapshot.version == "1.0"
    assert snapshot.nodes == []
    assert snapshot.metadata == {"key": "value"}
    assert snapshot.created_at is not None

def test_query_result_structure():
    result = QueryResult(
        primary_ids=["node1"],
        nodes=[],
        metadata={"query_time": 0.5}
    )
    assert result.primary_ids == ["node1"]
    assert result.nodes == []
    assert result.metadata == {"query_time": 0.5}
