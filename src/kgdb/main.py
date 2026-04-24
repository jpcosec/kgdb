"""CLI entry point for kgdb."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from kgdb.graph import load_graph, load_knowledge_node
from kgdb.query import StructuredQuery, execute_query


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kgdb")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--graph", required=True)
    get_parser.add_argument("--node", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--graph", required=True)

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--graph", required=True)
    query_parser.add_argument("--query-file", required=True)

    edges_parser = subparsers.add_parser("edges")
    edges_parser.add_argument("--graph", required=True)
    edges_parser.add_argument("--node", required=True)

    return parser


def _load_query(query_file: Path) -> StructuredQuery:
    data = json.loads(query_file.read_text(encoding="utf-8"))
    return StructuredQuery.model_validate(data)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    graph = load_graph(Path(args.graph))

    if args.command == "get":
        node = load_knowledge_node(graph, args.node)
        print(json.dumps(node.model_dump(), indent=2))
        return

    if args.command == "list":
        print(json.dumps(sorted(graph.nodes), indent=2))
        return

    if args.command == "query":
        query = _load_query(Path(args.query_file))
        nodes = [node.model_dump() for node in execute_query(graph, query)]
        print(json.dumps(nodes, indent=2))
        return

    if args.command == "edges":
        edges = []
        for _, target, data in graph.out_edges(args.node, data=True):
            edges.append({"target_id": target, **data})
        print(json.dumps(edges, indent=2))
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
