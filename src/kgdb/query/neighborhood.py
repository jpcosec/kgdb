"""Neighborhood traversal helpers for graph context collection."""

from __future__ import annotations

from collections import deque

from kgdb.graph import load_graph, load_knowledge_node


def collect_neighborhood_by_direction(
    graph, starting_nodes: set[str], depth: int, direction: str
) -> set[str]:
    """Collect nodes within a given depth and direction from starting nodes."""
    visited = set()
    queue = deque((node_id, 0) for node_id in starting_nodes)
    while queue:
        node_id, level = queue.popleft()
        if level >= depth:
            continue

        if direction == "incoming":
            neighbors = set(graph.predecessors(node_id))
        elif direction == "outgoing":
            neighbors = set(graph.successors(node_id))
        else:
            neighbors = set(graph.predecessors(node_id)) | set(
                graph.successors(node_id)
            )

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in starting_nodes:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
    return visited


def collect_neighborhood(graph, starting_nodes: list[str], depth: int) -> set[str]:
    """Legacy neighborhood traversal including the seed nodes."""
    return collect_neighborhood_by_direction(
        graph, set(starting_nodes), depth, direction="both"
    ) | set(starting_nodes)


def match_nodes_from_task(graph_path, task_hint: str | None) -> list[str]:
    """Identify relevant graph nodes from a natural-language task description."""
    if not task_hint:
        raise ValueError("Provide node_ids or a task_hint")
    graph = load_graph(graph_path)
    terms = {
        token
        for token in __import__("re").findall(r"[a-z0-9_]+", task_hint.lower())
        if len(token) > 2
    }
    scored: list[tuple[int, str]] = []
    for node_id in graph.nodes:
        node = load_knowledge_node(graph, node_id)
        haystack = " ".join(
            [
                node.identity.node_id,
                node.semantics.intent if node.semantics else "",
                " ".join(node.ast.signatures if node.ast else []),
            ]
        ).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            scored.append((score, node_id))
    return [node_id for _, node_id in sorted(scored, reverse=True)[:3]]
