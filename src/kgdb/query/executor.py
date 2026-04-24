"""Structured query execution for kgdb."""

from __future__ import annotations

from typing import Any

import networkx as nx

from kgdb.contracts import KnowledgeNode
from kgdb.graph import load_knowledge_node
from kgdb.query.language import FacetFilter, FieldCondition, GraphScope, StructuredQuery


def execute_query(graph: nx.DiGraph, query: StructuredQuery) -> list[KnowledgeNode]:
    """Execute a StructuredQuery against a graph. Returns matching nodes."""
    candidate_ids = _apply_scope(graph, query.scope)
    results = []
    for node_id in candidate_ids:
        node = load_knowledge_node(graph, node_id)
        if all(_facet_matches(node, facet_filter) for facet_filter in query.filters):
            results.append(node)
    return results


def _apply_scope(graph: nx.DiGraph, scope: GraphScope | None) -> list[str]:
    """Filters the graph nodes based on the provided GraphScope. Returns a list of node IDs."""
    if scope is None:
        return list(graph.nodes)
    if scope.descendant_of:
        if scope.descendant_of not in graph:
            return []
        return list(nx.descendants(graph, scope.descendant_of))
    if scope.ancestor_of:
        if scope.ancestor_of not in graph:
            return []
        return list(nx.ancestors(graph, scope.ancestor_of))
    if scope.node_id_prefix:
        return [
            node_id
            for node_id in graph.nodes
            if node_id.startswith(scope.node_id_prefix)
        ]
    return list(graph.nodes)


def _facet_matches(node: KnowledgeNode, facet_filter: FacetFilter) -> bool:
    """Checks if a KnowledgeNode matches the criteria defined in a FacetFilter."""
    facet_value = _get_facet(node, facet_filter.facet)
    return all(
        _condition_matches(facet_value, condition)
        for condition in facet_filter.conditions
    )


def _get_facet(node: KnowledgeNode, facet_name: str) -> object:
    """Retrieves the value of a specific facet from a KnowledgeNode."""
    mapping = {
        "identity": node.identity,
        "semantics": node.semantics,
        "ast": node.ast,
        "compliance": node.compliance,
        "adr": node.adr,
        "test_map": node.test_map,
        "io": node.io_ports or None,
    }
    return mapping.get(facet_name)


def _condition_matches(facet_value: object, condition: FieldCondition) -> bool:
    """Evaluates whether a facet's field value satisfies a FieldCondition."""
    if condition.op == "is_null":
        return _resolve_field(facet_value, condition.field) is None
    if condition.op == "is_not_null":
        return _resolve_field(facet_value, condition.field) is not None
    actual = _resolve_field(facet_value, condition.field)
    if condition.op == "eq":
        return actual == condition.value
    if condition.op == "ne":
        return actual != condition.value
    if condition.op == "contains":
        return isinstance(actual, list) and condition.value in actual
    if condition.op == "gt":
        return actual is not None and actual > condition.value
    if condition.op == "lt":
        return actual is not None and actual < condition.value
    if condition.op == "starts_with":
        return isinstance(actual, str) and actual.startswith(condition.value)
    return False


def _resolve_field(facet_value: object, field: str) -> Any:
    """Extracts the value of a specific field from a facet object."""
    if facet_value is None:
        return None
    if isinstance(facet_value, list):
        values = [getattr(item, field, None) for item in facet_value]
        non_null = [value for value in values if value is not None]
        return non_null[0] if non_null else None
    return getattr(facet_value, field, None)
