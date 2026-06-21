"""SLDB semantic export conversion for kgdb."""

from __future__ import annotations

from typing import Any

from kgdb.contracts import Edge, GraphSnapshot, KnowledgeNode, SystemIdentity


CONTRACT_NAME = "sldb_kgdb_semantic_export"
CONTRACT_VERSION = 1


def sldb_semantic_export_to_snapshot(payload: dict[str, Any]) -> GraphSnapshot:
    """Convert an SLDB semantic export payload into a KGDB graph snapshot."""
    _validate_contract(payload)

    provenance = _base_provenance(payload)
    tag_ids = _collect_semantic_tags(payload)
    nodes: list[KnowledgeNode] = []

    store_node_id = "sldb://store"
    nodes.append(_store_node(payload, store_node_id, provenance))

    for tag in sorted(tag_ids):
        nodes.append(_semantic_tag_node(tag, payload, provenance))

    for model in payload["models"]:
        documents = [
            document
            for document in payload["documents"]
            if document["model"] == model["name"]
        ]
        nodes.append(_model_node(model, documents, store_node_id, provenance))

    for document in payload["documents"]:
        sections = [
            section
            for section in payload["sections"]
            if section["document_id"] == document["id"]
        ]
        nodes.append(_document_node(document, sections, provenance))

    for section in payload["sections"]:
        nodes.append(_section_node(section, provenance))

    return GraphSnapshot(
        version="1.0",
        nodes=nodes,
        metadata={
            "source_contract": payload["contract"],
            "producer": payload["producer"],
            "store": payload["store"],
            "generated_from": CONTRACT_NAME,
        },
    )


def _validate_contract(payload: dict[str, Any]) -> None:
    contract = payload.get("contract", {})
    if contract.get("name") != CONTRACT_NAME or contract.get("version") != CONTRACT_VERSION:
        raise ValueError(f"Expected {CONTRACT_NAME} version {CONTRACT_VERSION}")


def _base_provenance(payload: dict[str, Any]) -> dict[str, Any]:
    store = payload["store"]
    return {
        "contract": payload["contract"],
        "producer": payload["producer"],
        "store": {
            "root": store["root"],
            "store_path": store["store_path"],
            "hash_a": store["hash_a"],
            "runtime_sources": store.get("runtime_sources", {}),
        },
    }


def _collect_semantic_tags(payload: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for model in payload["models"]:
        tags.update(model["semantics"])
    for document in payload["documents"]:
        tags.update(document["semantic_tags"])
    for section in payload["sections"]:
        tags.update(section["semantic_tags"])
    for semantic_node in payload["semantic_dag"]["nodes"]:
        tags.add(semantic_node["id"])
        tags.update(semantic_node["parents"])
    for tag, equivalents in payload["semantic_dag"]["equivalences"].items():
        tags.add(tag)
        tags.update(equivalents)
    return tags


def _store_node(
    payload: dict[str, Any], store_node_id: str, provenance: dict[str, Any]
) -> KnowledgeNode:
    store = payload["store"]
    return KnowledgeNode(
        identity=SystemIdentity(node_id=store_node_id, node_type="sldb_store"),
        edges=[
            Edge(target_id=_model_id(model["name"]), relation_type="has_model")
            for model in payload["models"]
        ],
        semantics={
            "root": store["root"],
            "store_path": store["store_path"],
            "hash_a": store["hash_a"],
        },
        source=provenance,
    )


def _semantic_tag_node(
    tag: str, payload: dict[str, Any], provenance: dict[str, Any]
) -> KnowledgeNode:
    parents_by_tag = {
        semantic_node["id"]: semantic_node["parents"]
        for semantic_node in payload["semantic_dag"]["nodes"]
    }
    equivalences = payload["semantic_dag"]["equivalences"].get(tag, [])
    edges = [
        Edge(target_id=_semantic_tag_id(parent), relation_type="semantic_parent")
        for parent in parents_by_tag.get(tag, [])
    ]
    edges.extend(
        Edge(target_id=_semantic_tag_id(equivalent), relation_type="semantic_equivalent")
        for equivalent in equivalences
    )
    return KnowledgeNode(
        identity=SystemIdentity(node_id=_semantic_tag_id(tag), node_type="semantic_tag"),
        edges=edges,
        semantics={"tag": tag},
        source=provenance,
    )


def _model_node(
    model: dict[str, Any],
    documents: list[dict[str, Any]],
    store_node_id: str,
    provenance: dict[str, Any],
) -> KnowledgeNode:
    model_id = _model_id(model["name"])
    return KnowledgeNode(
        identity=SystemIdentity(node_id=model_id, node_type="sldb_model"),
        edges=[
            Edge(target_id=_document_id(document["id"]), relation_type="has_document")
            for document in documents
        ]
        + [
            Edge(target_id=_semantic_tag_id(tag), relation_type="tagged_as")
            for tag in model["semantics"]
        ],
        semantics={
            "name": model["name"],
            "model_ref": model["model_ref"],
            "path": model["path"],
            "version": model["version"],
            "canonical": model["canonical"],
            "family": model.get("family"),
            "semantic_tags": model["semantics"],
            "base_models": model["base_models"],
            "hash_b": model["hash_b"],
        },
        source={**provenance, "model": model, "parent_store_node_id": store_node_id},
    )


def _document_node(
    document: dict[str, Any], sections: list[dict[str, Any]], provenance: dict[str, Any]
) -> KnowledgeNode:
    return KnowledgeNode(
        identity=SystemIdentity(
            node_id=_document_id(document["id"]), node_type="sldb_document"
        ),
        edges=[
            Edge(target_id=_section_id(section["id"]), relation_type="has_section")
            for section in sections
        ]
        + [
            Edge(target_id=_semantic_tag_id(tag), relation_type="tagged_as")
            for tag in document["semantic_tags"]
        ],
        semantics={
            "export_id": document["id"],
            "name": document["name"],
            "model": document["model"],
            "path": document["path"],
            "semantic_tags": document["semantic_tags"],
            "hash_c": document["hash_c"],
            "hash_d": document["hash_d"],
        },
        source={**provenance, "document": document},
    )


def _section_node(section: dict[str, Any], provenance: dict[str, Any]) -> KnowledgeNode:
    return KnowledgeNode(
        identity=SystemIdentity(node_id=_section_id(section["id"]), node_type="sldb_section"),
        edges=[
            Edge(target_id=_semantic_tag_id(tag), relation_type="tagged_as")
            for tag in section["semantic_tags"]
        ],
        semantics={
            "export_id": section["id"],
            "document_id": section["document_id"],
            "path": section["path"],
            "title": section["title"],
            "breadcrumbs": section["breadcrumbs"],
            "about": section["about"],
            "semantic_tags": section["semantic_tags"],
            "slug": section["slug"],
            "level": section["level"],
            "line_start": section.get("line_start"),
            "line_end": section.get("line_end"),
        },
        source={**provenance, "section": section},
    )


def _model_id(name: str) -> str:
    return f"sldb://model/{name}"


def _document_id(document_id: str) -> str:
    return f"sldb://document/{document_id}"


def _section_id(section_id: str) -> str:
    return f"sldb://section/{section_id}"


def _semantic_tag_id(tag: str) -> str:
    return f"sldb://semantic_tag/{tag}"
