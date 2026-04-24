"""Knowledge node contract for kgdb."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from kgdb.contracts.base import Edge, SystemIdentity


class FacetPayload(BaseModel):
    """Attribute-addressable facet payload without ontology dependency."""

    model_config = ConfigDict(extra="allow")
    _DEFAULTS: ClassVar[dict[str, object]] = {
        "compiled_from": "wiki-compiler",
        "coverage_percent": None,
        "direction": "input",
        "exemption_reason": None,
        "failing_standards": list,
        "raw_docstring": None,
    }

    def __getattr__(self, name: str) -> object:
        extra = self.model_extra or {}
        if name in extra:
            return extra[name]
        defaults = type(self)._DEFAULTS
        if name in defaults:
            default = defaults[name]
            value = default() if callable(default) else default
            extra[name] = value
            return value
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )


class KnowledgeNode(BaseModel):
    """
    Any element in the system, from the root folder to a specific function.
    This is the building block of your LLM Wiki.
    """

    model_config = ConfigDict(validate_assignment=True)

    identity: SystemIdentity = Field(
        description="The unique identity and type of this node within the system."
    )
    edges: list[Edge] = Field(
        default_factory=list,
        description="A list of directed connections to other nodes.",
    )

    semantics: FacetPayload | None = Field(
        default=None, description="Semantic information like intent and raw docstrings."
    )
    ast: FacetPayload | None = Field(
        default=None,
        description="Abstract Syntax Tree related information about code structure.",
    )
    io_ports: list[FacetPayload] = Field(
        default_factory=list,
        description="Details about input/output ports.",
    )
    compliance: FacetPayload | None = Field(
        default=None,
        description="Compliance status against defined standards and rules.",
    )
    adr: FacetPayload | None = Field(
        default=None,
        description="Architectural Decision Record related information.",
    )
    test_map: FacetPayload | None = Field(
        default=None, description="Testing strategy and coverage."
    )
    git: FacetPayload | None = Field(
        default=None, description="Git metadata for file-backed or doc-backed nodes."
    )
    source: FacetPayload | None = Field(
        default=None, description="Provenance and source tracking metadata."
    )

    @field_validator(
        "semantics",
        "ast",
        "compliance",
        "adr",
        "test_map",
        "git",
        "source",
        mode="before",
    )
    @classmethod
    def _coerce_facet_payload(cls, value: object) -> object:
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value

    @field_validator("io_ports", mode="before")
    @classmethod
    def _coerce_facet_payload_list(cls, value: object) -> object:
        if isinstance(value, list):
            return [
                item.model_dump() if isinstance(item, BaseModel) else item
                for item in value
            ]
        return value
