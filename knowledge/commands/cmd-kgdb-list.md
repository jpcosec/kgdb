---
id: cmd-kgdb-list
system: kgdb
command_path: list
synopsis: List all node IDs in the graph
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# list

## Synopsis

List all node IDs in the graph

## Purpose

The `kgdb list` command: List all node IDs in the graph.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'list'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--graph | required | Path to the JSON graph file

## Usage

kgdb list [-h] --graph GRAPH
