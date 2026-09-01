"""Pure-assembler ingest for authored relation documents.

Per RELATION_MODEL_LAYER_SPEC: the graph is the union of content-model
instances (nodes) and relation-model instances (edges). kgdb does NOT derive
edges from text fields here; it only assembles authored nodes and authored
`Relation` instances, routing each edge onto its source node.

This is additive and independent from `ingest/sldb.py` (which still derives
edges from an sldb semantic export). It consumes the shape emitted by
`sldb serve /graph`: a list of documents, each `{id, model_name, payload,
semantic_tags}`. Content docs become nodes; relation docs become edges.

Referential integrity is validated AT ASSEMBLY TIME (not warned at CLI time):
an authored edge whose source or target is not among the assembled nodes is an
orphan. Policy is caller-selectable: raise, or drop-with-report.
"""

from __future__ import annotations

from typing import Any, Literal

from kgdb.contracts import Edge, GraphSnapshot, KnowledgeNode, SystemIdentity


RELATION_INSTANCE_TAG = "type.relation.instance"

OrphanPolicy = Literal["raise", "drop"]


class OrphanEdgeError(ValueError):
    """Raised when an authored relation references a missing node."""


def assemble_authored_graph(
    documents: list[dict[str, Any]],
    *,
    node_id_field: str = "id",
    orphan_policy: OrphanPolicy = "raise",
    version: str = "1.0",
) -> tuple[GraphSnapshot, list[dict[str, str]]]:
    """Assemble a GraphSnapshot from authored content + relation documents.

    Args:
        documents: `sldb serve /graph` documents. A document is a relation
            instance when its ``semantic_tags`` include ``type.relation.instance``;
            otherwise it is a content node.
        node_id_field: which document key identifies a content node.
        orphan_policy: ``"raise"`` rejects orphan edges; ``"drop"`` discards them
            and returns them in the report.
        version: snapshot schema version.

    Returns:
        (snapshot, dropped_orphans). ``dropped_orphans`` is empty unless
        ``orphan_policy == "drop"``.
    """
    content_docs = [d for d in documents if not _is_relation(d)]
    relation_docs = [d for d in documents if _is_relation(d)]

    nodes_by_id: dict[str, KnowledgeNode] = {}
    for doc in content_docs:
        node_id = str(doc[node_id_field])
        nodes_by_id[node_id] = KnowledgeNode(
            identity=SystemIdentity(
                node_id=node_id,
                node_type=_node_type(doc),
            ),
            edges=[],
            semantics=doc.get("payload", {}),
            source={"authored": True, "model": doc.get("model_name")},
        )

    dropped: list[dict[str, str]] = []
    for rel in relation_docs:
        payload = rel.get("payload", {})
        source_id = str(payload.get("source_id", ""))
        target_id = str(payload.get("target_id", ""))
        relation_type = str(payload.get("relation_type", ""))

        missing = _missing_endpoints(source_id, target_id, nodes_by_id)
        if missing:
            if orphan_policy == "raise":
                raise OrphanEdgeError(
                    f"authored relation '{rel.get('id')}' references missing "
                    f"node(s): {', '.join(missing)}"
                )
            dropped.append(
                {
                    "relation_id": str(rel.get("id", "")),
                    "source_id": source_id,
                    "target_id": target_id,
                    "missing": ",".join(missing),
                }
            )
            continue

        nodes_by_id[source_id].edges.append(
            Edge(
                target_id=target_id,
                relation_type=relation_type,
                metadata={"authored": True, "relation_id": rel.get("id")},
            )
        )

    snapshot = GraphSnapshot(
        version=version,
        nodes=list(nodes_by_id.values()),
        metadata={
            "generated_from": "authored_relations",
            "content_docs": len(content_docs),
            "relation_docs": len(relation_docs),
            "dropped_orphans": len(dropped),
        },
    )
    return snapshot, dropped


def _is_relation(doc: dict[str, Any]) -> bool:
    return RELATION_INSTANCE_TAG in (doc.get("semantic_tags") or [])


def _node_type(doc: dict[str, Any]) -> str:
    model = doc.get("model_name") or "sldb_document"
    # VocabularyTerm grammar: must start with a letter; sanitize separators.
    return str(model).replace(" ", "_")


def _missing_endpoints(
    source_id: str, target_id: str, nodes_by_id: dict[str, KnowledgeNode]
) -> list[str]:
    missing = []
    if source_id not in nodes_by_id:
        missing.append(source_id or "<empty source_id>")
    if target_id not in nodes_by_id:
        missing.append(target_id or "<empty target_id>")
    return missing
