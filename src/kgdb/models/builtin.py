"""The relation types kgdb itself produces, shipped as RelationTypeDoc payloads.

``kgdb init`` writes each of these as a tracked document in the world's store so
that every structural edge of the graph has a type, like any authored edge.
Node classes here are kgdb node types (``sldb_store``, ``sldb_model``, ...);
authored relation types use model names instead.
"""

from __future__ import annotations

BUILTIN_RELATION_TYPES: list[dict] = [
    {
        "name": "has_model",
        "axis": "WHAT",
        "cardinality": "one_to_many",
        "source_types": ["sldb_store"],
        "target_types": ["sldb_model"],
        "description": "The store registers this model.",
    },
    {
        "name": "has_document",
        "axis": "WHAT",
        "cardinality": "one_to_many",
        "source_types": ["sldb_model"],
        "target_types": [],
        "description": "The model has this document as an instance.",
    },
    {
        "name": "has_section",
        "axis": "WHERE",
        "cardinality": "one_to_many",
        "source_types": [],
        "target_types": ["sldb_section"],
        "description": "The document contains this section.",
    },
    {
        "name": "tagged_as",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": [],
        "target_types": ["semantic_tag"],
        "description": "The model, document or section carries this semantic tag.",
    },
    {
        "name": "semantic_parent",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["semantic_tag"],
        "target_types": ["semantic_tag"],
        "description": "This tag is a child of that tag in the semantic DAG.",
    },
    {
        "name": "semantic_equivalent",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["semantic_tag"],
        "target_types": ["semantic_tag"],
        "description": "This local tag maps to that global tag across linked stores.",
    },
    {
        "name": "has_field",
        "axis": "WHAT",
        "cardinality": "one_to_many",
        "source_types": ["sldb_model"],
        "target_types": ["sldb_field"],
        "description": "The model declares this field; the field node carries its type and description.",
    },
    {
        "name": "extends",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["sldb_model"],
        "target_types": ["sldb_model"],
        "description": "The model inherits from that model (base_models); instances of the source are instances of the target.",
    },
    {
        "name": "applies_to_source",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["relation_type"],
        "target_types": ["sldb_model"],
        "description": "Instances of this model may be the source of edges of this relation type: the verbs a class can be subject of.",
    },
    {
        "name": "applies_to_target",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["relation_type"],
        "target_types": ["sldb_model"],
        "description": "Instances of this model may be the target of edges of this relation type.",
    },
    {
        "name": "names",
        "axis": "WHAT",
        "cardinality": "many_to_many",
        "source_types": ["anchor"],
        "target_types": [],
        "description": "The anchor (an alias word) names this model, field, relation type or document.",
    },
]


def builtin_payload(spec: dict) -> dict:
    """Full RelationTypeDoc payload for one builtin spec."""
    return {
        "title": spec["name"],
        "name": spec["name"],
        "direction": "directed",
        "cardinality": spec["cardinality"],
        "axis": spec["axis"],
        "source_types": list(spec["source_types"]),
        "target_types": list(spec["target_types"]),
        "condition": "",
        "description": spec["description"],
    }


def builtin_doc_name(spec: dict) -> str:
    return f"reltype-{spec['name']}"
