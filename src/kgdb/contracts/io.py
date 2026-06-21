"""Graph IO contracts for kgdb."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from kgdb.contracts.node import KnowledgeNode


class GraphSnapshot(BaseModel):
    """
    A point-in-time capture of the entire graph or a significant subgraph.
    Used for bulk persistence, backups, and inter-module transfers.
    """

    version: str = Field(
        ..., description="Schema version of the snapshot format."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The UTC timestamp when this snapshot was generated.",
    )
    nodes: list[KnowledgeNode] = Field(
        description="The complete list of nodes included in this snapshot."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata about the snapshot (e.g., source branch, environment).",
    )


class QueryResult(BaseModel):
    """
    The formal envelope for query results.
    Includes the primary matches and optionally their structural neighborhood.
    """

    primary_ids: list[str] = Field(
        description="IDs of nodes that explicitly matched the query filters."
    )
    nodes: list[KnowledgeNode] = Field(
        description="The set of nodes comprising both primary matches and their neighborhood."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution metadata (e.g., query time, result count).",
    )
