"""Utilities for manipulating and persisting the graph."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from kgdb.contracts import KnowledgeNode


def add_knowledge_node(graph: nx.DiGraph, node: KnowledgeNode) -> None:
    """
    Integrates a KnowledgeNode and its associated edges into a NetworkX DiGraph.
    """
    status = node.compliance.status if node.compliance else "unknown"
    graph.add_node(
        node.identity.node_id,
        type=node.identity.node_type,
        status=status,
        schema=node.model_dump(),
    )
    for edge in node.edges:
        graph.add_edge(
            node.identity.node_id,
            edge.target_id,
            relation=edge.relation_type,
            metadata=edge.metadata,
        )


def load_graph(graph_path: Path) -> nx.DiGraph:
    """
    Loads a Knowledge Graph from a JSON file into a NetworkX DiGraph instance.
    """
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    edge_key = "links" if "links" in data else "edges"
    return json_graph.node_link_graph(data, edges=edge_key)


def save_graph(graph: nx.DiGraph, graph_path: Path) -> None:
    """
    Serializes a NetworkX DiGraph to a JSON file on disk.
    """
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    data = json_graph.node_link_data(graph, edges="links")
    graph_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_knowledge_node(graph: nx.DiGraph, node_id: str) -> KnowledgeNode:
    """
    Retrieves and reconstructs a KnowledgeNode from its representation in a DiGraph.
    """
    schema = graph.nodes[node_id].get("schema")
    if schema:
        return KnowledgeNode.model_validate(schema)
    return KnowledgeNode.model_validate(
        {
            "identity": {
                "node_id": node_id,
                "node_type": graph.nodes[node_id].get("type", "concept"),
            },
            "edges": [],
        }
    )


def iter_knowledge_nodes(graph: nx.DiGraph) -> list[KnowledgeNode]:
    """
    Returns an iterator yielding all KnowledgeNode objects present in the graph.
    """
    return [load_knowledge_node(graph, node_id) for node_id in graph.nodes]
