"""
Serves graph queries for the Librarian Agent protocol.
Supports path traversal and I/O searching via the CLI runtime.
Also provides a stdin-based REPL loop for StructuredQuery JSON execution.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import IO

import networkx as nx

from .adapters import StructuredQuery, execute_query, load_graph, load_knowledge_node


def serve_structured_queries(
    graph_path: Path,
    input_stream: IO[str] = sys.stdin,
    output_stream: IO[str] = sys.stdout,
) -> None:
    """
    Reads StructuredQuery JSON objects one per line from input_stream,
    executes each against the graph at graph_path, and writes results
    as JSON lines to output_stream.

    Malformed lines produce an error JSON response instead of crashing.
    Exits cleanly when the input stream is exhausted.
    """
    graph = load_graph(graph_path)
    for raw_line in input_stream:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        response = _handle_structured_query_line(graph, raw_line)
        output_stream.write(json.dumps(response) + "\n")
        output_stream.flush()


def _handle_structured_query_line(graph: nx.DiGraph, raw_line: str) -> dict:
    """Parses one line as a StructuredQuery JSON and returns a result dict."""
    try:
        data = json.loads(raw_line)
    except json.JSONDecodeError as exc:
        return {"error": f"Invalid JSON: {exc}"}
    try:
        query = StructuredQuery.model_validate(data)
    except Exception as exc:
        return {"error": f"Invalid StructuredQuery: {exc}"}
    try:
        nodes = execute_query(graph, query)
        return {"nodes": [n.model_dump() for n in nodes]}
    except Exception as exc:
        return {"error": f"Query execution failed: {exc}"}


def query_graph(
    graph_path: Path,
    query_type: str | None,
    node_id: str | None = None,
    relation_filter: str | None = None,
    medium: str | None = None,
    schema_ref: str | None = None,
    path_template: str | None = None,
    tasks: bool = False,
    gaps: bool = False,
    unimplemented: bool = False,
    search_query: str | None = None,
) -> dict[str, object]:
    """Executes a query against the knowledge graph and returns the result as a dictionary."""
    graph = load_graph(graph_path)
    if search_query:
        matches = []
        search_lower = search_query.lower()
        for candidate in graph.nodes:
            if candidate.startswith("doc:"):
                # extract file path from 'doc:wiki/foo.md'
                file_path = Path(candidate[4:])
                if file_path.exists() and file_path.is_file():
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        if search_lower in content.lower():
                            matches.append(
                                {"node_id": candidate, "file": str(file_path)}
                            )
                    except Exception:
                        pass
        return {
            "query_type": "search",
            "search_query": search_query,
            "nodes": matches,
        }

    if tasks or gaps or unimplemented:
        conditions = []
        if gaps:
            conditions.append(
                {"field": "node_id", "op": "starts_with", "value": "doc:desk/tasks/"}
            )
        elif unimplemented:
            conditions.append(
                {"field": "node_id", "op": "starts_with", "value": "doc:desk/tasks/"}
            )
        elif tasks:
            conditions.append(
                {"field": "node_id", "op": "starts_with", "value": "doc:desk/tasks/"}
            )

        query = StructuredQuery(
            filters=[
                {"facet": "identity", "conditions": conditions},
            ],
        )
        nodes = execute_query(graph, query)
        return {
            "query_type": "structured_query",
            "nodes": [n.model_dump() for n in nodes],
        }

    if query_type is None:
        raise ValueError(
            "A query type or a flag (--tasks, --gaps, --unimplemented) must be provided."
        )

    if query_type == "get_node":
        ensure_node(node_id)
        return {
            "query_type": query_type,
            "node": load_knowledge_node(graph, node_id).model_dump(),
        }
    if query_type == "get_ancestors":
        ensure_node(node_id)
        filtered = filter_graph_by_relation(graph, relation_filter)
        nodes = sorted(nx.ancestors(filtered, node_id))
        return {
            "query_type": query_type,
            "nodes": [
                load_knowledge_node(graph, value).model_dump() for value in nodes
            ],
        }
    if query_type == "get_descendants":
        ensure_node(node_id)
        filtered = filter_graph_by_relation(graph, relation_filter)
        nodes = sorted(nx.descendants(filtered, node_id))
        return {
            "query_type": query_type,
            "nodes": [
                load_knowledge_node(graph, value).model_dump() for value in nodes
            ],
        }
    if query_type == "find_by_io":
        matches = []
        for candidate in graph.nodes:
            node = load_knowledge_node(graph, candidate)
            if any(
                matches_io(port, medium, schema_ref, path_template)
                for port in node.io_ports
            ):
                matches.append(node.model_dump())
        return {"query_type": query_type, "nodes": matches}
    raise ValueError(f"Unsupported query type: {query_type}")


def filter_graph_by_relation(
    graph: nx.DiGraph, relation_filter: str | None
) -> nx.DiGraph:
    """Returns a subgraph containing only the edges that match the specified relation type."""
    if not relation_filter:
        return graph
    filtered = nx.DiGraph()
    filtered.add_nodes_from(graph.nodes(data=True))
    for source, target, data in graph.edges(data=True):
        if data.get("relation") == relation_filter:
            filtered.add_edge(source, target, **data)
    return filtered


def matches_io(
    port: object, medium: str | None, schema_ref: str | None, path_template: str | None
) -> bool:
    """Checks if an I/O port matches the specified medium, schema, or path template criteria."""
    values = port.model_dump() if hasattr(port, "model_dump") else dict(port)
    return (
        (medium is None or values.get("medium") == medium)
        and (schema_ref is None or values.get("schema_ref") == schema_ref)
        and (path_template is None or values.get("path_template") == path_template)
    )


def ensure_node(node_id: str | None) -> str:
    """Validates that a node ID is provided, raising an error if it is missing."""
    if not node_id:
        raise ValueError("node_id is required for this query type")
    return node_id


def query_main(
    graph_path: Path,
    query_type: str,
    node_id: str | None = None,
    relation_filter: str | None = None,
    medium: str | None = None,
    schema_ref: str | None = None,
    path_template: str | None = None,
    tasks: bool = False,
    gaps: bool = False,
    unimplemented: bool = False,
    search_query: str | None = None,
) -> None:
    """Main entry point for querying the graph and printing the results in JSON format."""
    result = query_graph(
        graph_path=graph_path,
        query_type=query_type,
        node_id=node_id,
        relation_filter=relation_filter,
        medium=medium,
        schema_ref=schema_ref,
        path_template=path_template,
        tasks=tasks,
        gaps=gaps,
        unimplemented=unimplemented,
        search_query=search_query,
    )
    payload = json.loads(json.dumps(result, default=serialize_model))
    print(json.dumps(payload, indent=2))


def serialize_model(value: object) -> object:
    """Serializes a model object to a JSON-compatible dictionary using model_dump."""
    if hasattr(value, "model_dump"):
        return value.model_dump()
    raise TypeError(f"Object of type {type(value)!r} is not JSON serializable")
