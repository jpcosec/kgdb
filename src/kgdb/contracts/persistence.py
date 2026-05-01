"""Persistence contracts for kgdb."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from kgdb.contracts.node import KnowledgeNode


class PersistenceEntry(BaseModel):
    """A single node or edge update with a hash for integrity."""

    action: Literal["create", "update", "delete"] = Field(
        description="The type of operation performed (e.g., node creation, edge update)."
    )
    node_id: str = Field(
        description="The unique identifier of the node being affected (or source node for edges)."
    )
    payload: Optional[KnowledgeNode] = Field(
        default=None,
        description="The node data snapshot if applicable.",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="The UTC timestamp when this entry was generated.",
    )
    entry_hash: str = Field(
        description="Cryptographic hash (SHA-256) of the entry payload for local integrity."
    )


class TransactionManifest(BaseModel):
    """A collection of persistence entries forming a consistent graph transition."""

    transaction_id: str = Field(
        description="Unique UUID or sequential ID for this transaction."
    )
    entries: list[PersistenceEntry] = Field(
        default_factory=list,
        description="Ordered list of operations contained in this transaction.",
    )
    previous_hash: Optional[str] = Field(
        default=None,
        description="The hash_chain of the preceding TransactionManifest in the ledger.",
    )
    hash_chain: str = Field(
        description="The rolling cryptographic hash that links this transaction to all previous ones."
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Contextual metadata like 'author', 'reason', or 'source_system'.",
    )
