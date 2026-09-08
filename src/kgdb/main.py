"""CLI entry point for kgdb."""

from __future__ import annotations

import argparse
import sys
import json
from pathlib import Path

from pydantic import ValidationError

from kgdb.graph import load_graph, load_knowledge_node
from kgdb.query import StructuredQuery, execute_query


def _handle_error(e: Exception, context: str = "") -> None:
    if isinstance(e, FileNotFoundError):
        print(f"Error: file not found: {e.filename}", file=sys.stderr)
        sys.exit(1)
    if isinstance(e, IsADirectoryError):
        print(f"Error: path is a directory: {e.filename}", file=sys.stderr)
        sys.exit(1)
    if isinstance(e, json.JSONDecodeError):
        filename = getattr(e, "filename", "") or ""
        if str(filename).endswith(".yaml") or str(filename).endswith(".yml"):
             print(f"Error: YAML not supported, use JSON: {filename}", file=sys.stderr)
             sys.exit(1)
        print("Error: invalid JSON", file=sys.stderr)
        sys.exit(1)
    if isinstance(e, ValidationError) and context == "ingest":
        print("Error: validation failed. If this is an SLDB export, use `ingest-sldb` command instead.", file=sys.stderr)
        sys.exit(1)
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

def _build_parser() -> argparse.ArgumentParser:
    class _NoDuplicateAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if getattr(namespace, self.dest, None) is not None:
                parser.error(f"argument {option_string}: not allowed multiple times")
            setattr(namespace, self.dest, values)

    from kgdb import __version__

    parser = argparse.ArgumentParser(
        prog="kgdb",
        description="Knowledge Graph Database (KGDB) command line interface."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, description="Available commands")

    get_parser = subparsers.add_parser("get", help="Get a specific node from the graph")
    get_parser.add_argument("--graph", required=True, action=_NoDuplicateAction, help="Path to the JSON graph file")
    get_parser.add_argument("--node", required=True, action=_NoDuplicateAction, help="ID of the node to retrieve")

    list_parser = subparsers.add_parser("list", help="List all node IDs in the graph")
    list_parser.add_argument("--graph", required=True, action=_NoDuplicateAction, help="Path to the JSON graph file")

    query_parser = subparsers.add_parser("query", help="Query the graph using a declarative JSON query file")
    query_parser.add_argument("--graph", required=True, action=_NoDuplicateAction, help="Path to the JSON graph file")
    query_parser.add_argument(
        "--query-file",
        required=True,
        action=_NoDuplicateAction,
        help="Path to a JSON file containing the query definition (e.g., node identity filters or graph scope/neighborhood rules)"
    )

    edges_parser = subparsers.add_parser("edges", help="Get outbound edges for a specific node")
    edges_parser.add_argument("--graph", required=True, action=_NoDuplicateAction, help="Path to the JSON graph file")
    edges_parser.add_argument("--node", required=True, action=_NoDuplicateAction, help="ID of the source node")

    ingest_parser = subparsers.add_parser("ingest", help="Build the typed graph of an sldb store (--store), or ingest a GraphSnapshot payload (--input)")
    ingest_parser.add_argument("--store", action=_NoDuplicateAction, help="Path to the .sldb store to assemble; every edge is validated against its RelationTypeDoc")
    ingest_parser.add_argument("--pythonpath", action=_NoDuplicateAction, help="Project path where the store's models import from")
    ingest_parser.add_argument("--exclude-tag", action="append", default=None, help="Leave out documents carrying this semantic tag (default: type.pron.move); repeatable")
    ingest_parser.add_argument("--input", action=_NoDuplicateAction, help="Path to a GraphSnapshot JSON file to ingest as-is (legacy path, no typing)")
    ingest_parser.add_argument("--output", required=True, action=_NoDuplicateAction, help="Path where the output networkx JSON graph will be saved")

    init_parser = subparsers.add_parser("init", help="Prepare an sldb store for typed relations: register kgdb's models, track the builtin relation types, register predicates")
    init_parser.add_argument("--store", required=True, action=_NoDuplicateAction, help="Path to the .sldb store")
    init_parser.add_argument("--pythonpath", action=_NoDuplicateAction, help="Project path (passed to sldb when resolving models)")

    ingest_sldb_parser = subparsers.add_parser("ingest-sldb", help="Ingest an SLDB semantic export payload into a persistent networkx graph")
    ingest_sldb_parser.add_argument("--input", required=True, action=_NoDuplicateAction, help="Path to the input JSON file (must be sldb_kgdb_semantic_export format)")
    ingest_sldb_parser.add_argument("--output", required=True, action=_NoDuplicateAction, help="Path where the output networkx JSON graph will be saved")

    return parser


def _load_query(query_file: Path) -> StructuredQuery:
    try:
        data = json.loads(query_file.read_text(encoding="utf-8"))
        return StructuredQuery.model_validate(data)
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            e.filename = query_file
        _handle_error(e)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "init":
        from kgdb.world import init_world

        try:
            report = init_world(args.store, args.pythonpath)
            print(f"Initialized {args.store}: {report.summary()}")
        except Exception as e:
            _handle_error(e)
        return

    if args.command == "ingest" and args.store:
        from kgdb.graph.utils import add_knowledge_node, save_graph
        from kgdb.ingest.typed import TypedIngestError, build_typed_snapshot
        import networkx as nx

        try:
            snapshot, report = build_typed_snapshot(args.store, args.pythonpath, args.exclude_tag or ("type.pron.move",))
            graph = nx.MultiDiGraph()
            for node in snapshot.nodes:
                add_knowledge_node(graph, node)
            save_graph(graph, Path(args.output))
            print(f"Ingested {report['nodes']} nodes and {report['edges']} typed edges ({len(report['relation_types'])} relation types) to {args.output}")
        except TypedIngestError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            _handle_error(e)
        return

    if args.command == "ingest":
        if not args.input:
            print("Error: ingest needs --store (typed graph of a store) or --input (GraphSnapshot file)", file=sys.stderr)
            sys.exit(2)
        from kgdb.contracts.io import GraphSnapshot
        from kgdb.graph.utils import add_knowledge_node, save_graph
        import networkx as nx
        
        try:
            input_path = Path(args.input)
            data = json.loads(input_path.read_text(encoding="utf-8"))
            if "version" not in data:
                print("Error: missing version field in graph snapshot", file=sys.stderr)
                sys.exit(1)
            
            if data["version"] not in ("1.0", "1"):
                try:
                    v = float(data["version"])
                    if v > 1.0:
                        print(f"Error: unsupported version '{data['version']}'", file=sys.stderr)
                        sys.exit(1)
                    else:
                        print(f"Error: invalid version format: {data['version']}", file=sys.stderr)
                        sys.exit(1)
                except ValueError:
                    print(f"Error: invalid version format: {data['version']}", file=sys.stderr)
                    sys.exit(1)

            snapshot = GraphSnapshot.model_validate(data)
            
            # Check for dangling edges
            node_ids = {node.identity.node_id for node in snapshot.nodes}
            for node in snapshot.nodes:
                for edge in node.edges:
                    if edge.target_id not in node_ids:
                        print(f"Warning: dangling edge from '{node.identity.node_id}' to nonexistent node '{edge.target_id}'", file=sys.stderr)
                        
            graph = nx.DiGraph()
            for node in snapshot.nodes:
                add_knowledge_node(graph, node)
                
            save_graph(graph, Path(args.output))
            print(f"Ingested {len(snapshot.nodes)} nodes to {args.output}")
        except Exception as e:
            if isinstance(e, json.JSONDecodeError):
                e.filename = input_path
            _handle_error(e, context="ingest")
        return

    if args.command == "ingest-sldb":
        from kgdb.graph.utils import add_knowledge_node, save_graph
        from kgdb.ingest import sldb_semantic_export_to_snapshot
        import networkx as nx

        try:
            input_path = Path(args.input)
            data = json.loads(input_path.read_text(encoding="utf-8"))
            snapshot = sldb_semantic_export_to_snapshot(data)

            # Check for dangling edges
            node_ids = {node.identity.node_id for node in snapshot.nodes}
            for node in snapshot.nodes:
                for edge in node.edges:
                    if edge.target_id not in node_ids:
                        print(f"Warning: dangling edge from '{node.identity.node_id}' to nonexistent node '{edge.target_id}'", file=sys.stderr)

            graph = nx.DiGraph()
            for node in snapshot.nodes:
                add_knowledge_node(graph, node)

            save_graph(graph, Path(args.output))
            print(f"Ingested {len(snapshot.nodes)} SLDB semantic nodes to {args.output}")
        except Exception as e:
            if isinstance(e, json.JSONDecodeError):
                e.filename = input_path
            _handle_error(e)
        return

    try:
        graph_path = Path(args.graph)
        try:
            # Need to trigger read_text to catch IsADirectoryError and FileNotFoundError consistently here
            graph_path.read_text(encoding="utf-8")
        except IsADirectoryError as e:
            raise
        except FileNotFoundError as e:
            raise
        
        graph = load_graph(graph_path)
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            e.filename = graph_path
        _handle_error(e)

    try:
        if args.command == "get":
            node = load_knowledge_node(graph, args.node)
            try:
                print(json.dumps(node.model_dump(), indent=2, ensure_ascii=False))
            except BrokenPipeError:
                pass
            return

        if args.command == "list":
            try:
                print(json.dumps(sorted(graph.nodes), indent=2, ensure_ascii=False))
            except BrokenPipeError:
                pass
            return

        if args.command == "query":
            query = _load_query(Path(args.query_file))
            nodes = [node.model_dump() for node in execute_query(graph, query)]
            try:
                print(json.dumps(nodes, indent=2, ensure_ascii=False))
            except BrokenPipeError:
                pass
            return

        if args.command == "edges":
            edges = []
            for _, target, data in graph.out_edges(args.node, data=True):
                edges.append({"target_id": target, **data})
            try:
                print(json.dumps(edges, indent=2, ensure_ascii=False))
            except BrokenPipeError:
                pass
            return
    except Exception as e:
        _handle_error(e)

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
