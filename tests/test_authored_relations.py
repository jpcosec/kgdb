"""Tests for the pure-assembler authored-relation ingest.

Uses the exact document shape emitted by `sldb serve /graph`: content docs plus
relation docs tagged `type.relation.instance`, no edge derivation.
"""

from __future__ import annotations

import pytest

from kgdb.ingest import OrphanEdgeError, assemble_authored_graph


def _content(doc_id: str, model: str = "conversation-step") -> dict:
    return {
        "id": doc_id,
        "model_name": model,
        "path": f"docs/{doc_id}.md",
        "payload": {"title": doc_id},
        "semantic_tags": ["type.content"],
    }


def _relation(rel_id: str, src: str, tgt: str, rtype: str = "flows_to") -> dict:
    return {
        "id": rel_id,
        "model_name": "RelationDoc",
        "path": f"docs/{rel_id}.md",
        "payload": {
            "title": rel_id,
            "source_id": src,
            "target_id": tgt,
            "relation_type": rtype,
        },
        "semantic_tags": ["layer.topology", "type.relation.instance"],
    }


def test_assembles_nodes_and_authored_edges():
    docs = [
        _content("step-1"),
        _content("step-2"),
        _content("step-3"),
        _relation("e1", "step-1", "step-2"),
        _relation("e2", "step-2", "step-3"),
    ]
    snapshot, dropped = assemble_authored_graph(docs)

    assert dropped == []
    nodes_by_id = {n.identity.node_id: n for n in snapshot.nodes}
    assert set(nodes_by_id) == {"step-1", "step-2", "step-3"}
    # edges routed onto their source nodes, not derived from content
    assert [(e.target_id, e.relation_type) for e in nodes_by_id["step-1"].edges] == [
        ("step-2", "flows_to")
    ]
    assert [(e.target_id, e.relation_type) for e in nodes_by_id["step-2"].edges] == [
        ("step-3", "flows_to")
    ]
    assert nodes_by_id["step-3"].edges == []
    assert snapshot.metadata["relation_docs"] == 2
    assert snapshot.metadata["content_docs"] == 3


def test_node_type_comes_from_content_model():
    snapshot, _ = assemble_authored_graph([_content("s1", model="conversation-step")])
    assert snapshot.nodes[0].identity.node_type == "conversation-step"


def test_orphan_edge_raises_by_default():
    docs = [_content("step-1"), _relation("e1", "step-1", "ghost")]
    with pytest.raises(OrphanEdgeError) as exc:
        assemble_authored_graph(docs)
    assert "ghost" in str(exc.value)


def test_orphan_edge_drop_policy_reports_and_continues():
    docs = [
        _content("step-1"),
        _content("step-2"),
        _relation("e1", "step-1", "step-2"),
        _relation("e-bad", "step-1", "ghost"),
    ]
    snapshot, dropped = assemble_authored_graph(docs, orphan_policy="drop")

    assert len(dropped) == 1
    assert dropped[0]["relation_id"] == "e-bad"
    assert dropped[0]["missing"] == "ghost"
    # good edge survived
    nodes_by_id = {n.identity.node_id: n for n in snapshot.nodes}
    assert len(nodes_by_id["step-1"].edges) == 1
    assert snapshot.metadata["dropped_orphans"] == 1


def test_content_only_yields_edgeless_nodes():
    snapshot, dropped = assemble_authored_graph([_content("a"), _content("b")])
    assert dropped == []
    assert all(n.edges == [] for n in snapshot.nodes)
