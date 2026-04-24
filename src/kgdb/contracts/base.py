"""Base graph contracts for kgdb."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class Edge(BaseModel):
    """Universal connection between nodes."""

    target_id: str = Field(description="The ID of the target node this edge points to.")
    relation_type: Literal[
        "contains",
        "depends_on",
        "reads_from",
        "writes_to",
        "documents",
        "transcludes",
        "extends",
        "implements",
    ] = Field(description="The type of relationship this edge represents.")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the edge.",
    )


class SystemIdentity(BaseModel):
    """The immutable base identity of any node in your universe."""

    node_id: str = Field(description="A unique absolute identifier for the node.")
    node_type: Literal[
        "directory",
        "file",
        "code_construct",
        "doc_standard",
        "concept",
        "index",
        "how_to",
        "adr",
        "reference",
        "faq",
        "selfDoc",
        "system",
    ] = Field(description="The type of entity this node represents.")
