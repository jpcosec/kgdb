---
id: cmd-kgdb-ingest
system: kgdb
command_path: ingest
synopsis: Build the typed graph of an sldb store (--store), or ingest a GraphSnapshot
  payload (--input)
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

Build the typed graph of an sldb store (--store), or ingest a GraphSnapshot payload (--input)

## Purpose

The `kgdb ingest` command: Ingest a GraphSnapshot format payload into a persistent networkx graph.

## How It Works

With --store: runs sldb semantic-export by library, types document nodes by model, adds field, relation_type and anchor nodes with has_field, extends, applies_to_source, applies_to_target and names edges, turns each RelationDoc into a typed edge on its source (origin, condition, axis in metadata), excludes documents with the excluded tags, validates every edge (type exists, endpoints exist, classes allowed with inheritance, cardinality, direction) and writes a MultiDiGraph. With --input: ingests a GraphSnapshot JSON as-is (legacy, untyped).

## Arguments

--store | optional | Path to the .sldb store to assemble; every edge is validated against its RelationTypeDoc
--pythonpath | optional | Project path where the store models import from
--exclude-tag | optional | Leave out documents carrying this semantic tag (default type.pron.move); repeatable
--input | optional | Path to a GraphSnapshot JSON file to ingest as-is (legacy path, no typing)
--output | required | Path where the output networkx JSON graph will be saved

## Usage

kgdb ingest --store .sldb --pythonpath . --output kgdb.graph.json
kgdb ingest --input snapshot.json --output kgdb.graph.json
