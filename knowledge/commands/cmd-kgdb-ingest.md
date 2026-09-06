---
id: cmd-kgdb-ingest
system: kgdb
command_path: ingest
synopsis: Ingest a GraphSnapshot format payload into a persistent networkx graph
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# ingest

## Synopsis

Ingest a GraphSnapshot format payload into a persistent networkx graph

## Purpose

The `kgdb ingest` command: Ingest a GraphSnapshot format payload into a persistent networkx graph.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'ingest'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--input | required | Path to the input JSON file (must be GraphSnapshot format)
--output | required | Path where the output networkx JSON graph will be saved

## Usage

kgdb ingest [-h] --input INPUT --output OUTPUT
