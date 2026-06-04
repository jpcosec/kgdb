"""Base graph contracts for kgdb."""

from typing import Annotated, Any

from pydantic import BaseModel, Field


VocabularyTerm = Annotated[
    str,
    Field(
        min_length=1,
        pattern=r"^[A-Za-z][A-Za-z0-9_.:-]*$",
        description="A downstream-defined graph vocabulary token.",
    ),
]


class Edge(BaseModel):
    """Universal connection between nodes."""

    target_id: str = Field(description="The ID of the target node this edge points to.")
    relation_type: VocabularyTerm = Field(
        description="The downstream-defined relationship token this edge represents."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the edge.",
    )


class SystemIdentity(BaseModel):
    """The immutable base identity of any node in your universe."""

    node_id: str = Field(description="A unique absolute identifier for the node.")
    node_type: VocabularyTerm = Field(
        description="The downstream-defined entity type token this node represents."
    )
