---
id: cmd-kgdb-get
system: kgdb
command_path: get
synopsis: Get a specific node from the graph
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# get

## Synopsis

Get a specific node from the graph

## Purpose

The `kgdb get` command: Get a specific node from the graph.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'get'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--graph | required | Path to the JSON graph file
--node | required | ID of the node to retrieve

## Usage

kgdb get [-h] --graph GRAPH --node NODE
