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
        attrs = {"relation": edge.relation_type, "metadata": edge.metadata}
        if graph.is_multigraph():
            # one edge per (source, target, relation_type): a typed graph has parallel edges
            graph.add_edge(node.identity.node_id, edge.target_id, key=edge.relation_type, **attrs)
        else:
            graph.add_edge(node.identity.node_id, edge.target_id, **attrs)


def load_graph(graph_path: Path) -> nx.DiGraph:
    """
    Loads a Knowledge Graph from a JSON file. Node-link JSON comes back as the graph
    class it was saved from (MultiDiGraph for typed graphs, DiGraph for legacy ones);
    a native GraphSnapshot is loaded as a MultiDiGraph so parallel typed edges survive.
    """
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    
    # Check if this is a GraphSnapshot format (has 'nodes' but no top-level 'links'/'edges')
    if "nodes" in data and "links" not in data and "edges" not in data:
        graph = nx.MultiDiGraph()
        for node_data in data["nodes"]:
            # Handle possible KnowledgeNode dict parsing
            node_id = node_data.get("identity", {}).get("node_id")
            if not node_id:
                continue
                
            node_type = node_data.get("identity", {}).get("node_type", "concept")
            
            # The schema is stored on the node in add_knowledge_node
            status = "unknown"
            if "compliance" in node_data and isinstance(node_data["compliance"], dict):
                status = node_data["compliance"].get("status", "unknown")
                
            graph.add_node(
                node_id,
                type=node_type,
                status=status,
                schema=node_data,
            )
            
            # Process edges nested inside the node
            for edge in node_data.get("edges", []):
                target_id = edge.get("target_id")
                if target_id:
                    graph.add_edge(
                        node_id,
                        target_id,
                        key=edge.get("relation_type"),
                        relation=edge.get("relation_type"),
                        metadata=edge.get("metadata", {}),
                    )
        return graph
        
    # Fallback to standard NetworkX format
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
