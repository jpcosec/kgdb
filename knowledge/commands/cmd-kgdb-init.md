---
id: cmd-kgdb-init
system: kgdb
command_path: init
synopsis: 'Prepare an sldb store for typed relations: register kgdb models, track
  the builtin relation types, register predicates'
tags:
- system:kgdb
- domain:graph_architecture
- kind:software
- impl:here
- entity:cli_command
provenance: src/kgdb/world.py
---

# init

## Synopsis

Prepare an sldb store for typed relations: register kgdb models, track the builtin relation types, register predicates

## Purpose

Make a world able to hold typed relations. After init, every edge kgdb produces or reads has a RelationTypeDoc behind it, including the structural ones.

## How It Works

Registers kgdb.models:RelationTypeDoc and kgdb.models:RelationDoc in the store through sldb; renders each builtin relation type (has_model, has_document, has_section, tagged_as, semantic_parent, semantic_equivalent, has_field, extends, applies_to_source, applies_to_target, names) as a RelationTypeDoc under kgdb/relation_types/ and tracks it; registers each name as an sldb predicate with its axis. Idempotent: a second run changes nothing.

## Arguments

--store | required | Path to the .sldb store
--pythonpath | optional | Project path passed to sldb when resolving models

## Usage

kgdb init --store .sldb --pythonpath .
