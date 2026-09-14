"""One authored edge, declared as an sldb document owned by kgdb."""

from __future__ import annotations

from pydantic import Field

from sldb import StructuredNLDoc


class RelationDoc(StructuredNLDoc):
    """One authored edge source -> target of a given relation type.

    Content-blind: it carries ids and a type token, never the content of its
    endpoints. It is a document of the world's sldb store; kgdb's ingest
    validates it against its RelationTypeDoc and turns it into an edge. It is
    not itself a node of the graph.
    """

    __family__ = "relation"
    __semantics__ = {
        "type": ["relation", "instance"],
        "layer": ["topology"],
    }
    # Metadatos de grafo para las UIs (misma convención que los modelos de
    # deskops): estos campos guardan ids de otros documentos.
    __references__ = ["source_id", "target_id"]
    __template__ = """---
source_id: ⸢rev•source_id⸥
target_id: ⸢rev•target_id⸥
relation_type: ⸢rev•relation_type⸥
condition: ⸢rev•condition⸥
---

# ⸢rev•title⸥

## Notes

⸢rev,markdown•notes⸥
""".strip()

    title: str = Field(description="Relation instance title shown as the H1 heading.")
    source_id: str = Field(
        description="Export id of the source document, Model:name (store:Model:name for a linked store)."
    )
    target_id: str = Field(
        description="Export id of the target document, Model:name (store:Model:name for a linked store)."
    )
    relation_type: str = Field(
        description="Vocabulary token naming the relation type; must match a tracked RelationTypeDoc name."
    )
    condition: str = Field(
        default="",
        description="sldb --where predicate for this edge only; empty inherits the type's condition.",
    )
    notes: str = Field(
        default="",
        description="Optional markdown notes about this specific authored edge.",
    )
