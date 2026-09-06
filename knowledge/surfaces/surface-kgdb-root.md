---
id: surface-kgdb-root
system: kgdb
surface: kgdb
tags:
- system:kgdb
- domain:graph_architecture
- kind:software
- impl:external
- entity:cli_surface
provenance: src/kgdb/main.py
---

# kgdb

## Purpose

The root CLI surface of kgdb: the graph persistence, traversal and query substrate. Groups 6 commands.

## How It Works

Registered in src/kgdb/main.py via argparse subparsers. Each command loads a persistent networkx graph and dispatches to a graph-runtime handler.

## Commands

get
list
query
edges
ingest
ingest-sldb
