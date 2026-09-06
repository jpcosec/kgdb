---
id: cmd-kgdb-query
system: kgdb
command_path: query
synopsis: Query the graph using a declarative JSON query file
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# query

## Synopsis

Query the graph using a declarative JSON query file

## Purpose

The `kgdb query` command: Query the graph using a declarative JSON query file.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'query'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--graph | required | Path to the JSON graph file
--query-file | required | Path to a JSON file containing the query definition (e.g., node identity filters or graph scope/neighborhood rules)

## Usage

kgdb query [-h] --graph GRAPH --query-file QUERY_FILE
