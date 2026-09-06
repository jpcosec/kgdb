---
id: cmd-kgdb-ingest-sldb
system: kgdb
command_path: ingest-sldb
synopsis: Ingest an SLDB semantic export payload into a persistent networkx graph
tags:
- system:kgdb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/kgdb/main.py
---

# ingest-sldb

## Synopsis

Ingest an SLDB semantic export payload into a persistent networkx graph

## Purpose

The `kgdb ingest-sldb` command: Ingest an SLDB semantic export payload into a persistent networkx graph.

## How It Works

Implemented in src/kgdb/main.py via the argparse subcommand 'ingest-sldb'. It parses the listed arguments and dispatches to the corresponding kgdb graph-runtime handler.

## Arguments

--input | required | Path to the input JSON file (must be sldb_kgdb_semantic_export format)
--output | required | Path where the output networkx JSON graph will be saved

## Usage

kgdb ingest-sldb [-h] --input INPUT --output OUTPUT
