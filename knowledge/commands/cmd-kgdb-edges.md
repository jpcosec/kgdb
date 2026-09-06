---
id: cmd-kgdb-edges
system: kgdb
command_path: edges
synopsis: Get outbound edges for a specific node
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# edges

## Synopsis

Get outbound edges for a specific node

## Purpose

The `kgdb edges` command: Get outbound edges for a specific node.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'edges'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--graph | required | Path to the JSON graph file
--node | required | ID of the source node

## Usage

kgdb edges [-h] --graph GRAPH --node NODE
