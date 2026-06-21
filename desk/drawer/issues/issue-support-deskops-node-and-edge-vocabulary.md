# Support deskops node and edge vocabulary

## Kind

feature

## Status

open

## Problem

KGDB already provides a NetworkX-backed graph substrate, but its current `SystemIdentity.node_type` and `Edge.relation_type` literals are too narrow for deskops knowledge graphs. Deskops needs nodes such as atoms, tasks, issues, docs, specs, diagrams, primitives, SLDB models, CLI commands, source files, and tests, plus relations such as materializes, validates, invokes, routes, generated_from, source_for, and violates.

## Desired Outcome

Decide how KGDB should support downstream vocabularies without becoming a semantic reasoner. Options include broadening literals, using plain strings with validation hooks, adding project-specific vocabulary registries, or carrying external vocabulary metadata.

## Questions

- Should KGDB keep fixed literals or allow downstream projects to register node and edge vocabularies?
- Should KGDB distinguish generic graph relation type from domain-specific relation role?
- How should KGDB validate a graph bundle from deskops without hardcoding deskops terms?
- Should ontology/OWL mappings be stored as optional metadata on node/edge vocabulary entries?

## Context

Deskops wants to build a knowledge graph connecting desk docs and source files, using KGDB/NetworkX as the first runtime rather than introducing OWL as the first implementation layer.
