import json
from pathlib import Path

import networkx as nx
import pytest
from pydantic import ValidationError

from kgdb.contracts import Edge, GraphSnapshot, SystemIdentity
from kgdb.graph.utils import add_knowledge_node, load_knowledge_node


REPO_ROOT = Path(__file__).resolve().parents[1]
DOWNSTREAM_VOCABULARY_FIXTURE = (
    REPO_ROOT / "desk" / "fixtures" / "downstream_vocabulary_v1.json"
)


def test_downstream_vocabulary_terms_validate_and_round_trip():
    snapshot = GraphSnapshot.model_validate_json(
        DOWNSTREAM_VOCABULARY_FIXTURE.read_text(encoding="utf-8")
    )

    node_types = {node.identity.node_type for node in snapshot.nodes}
    relation_types = {
        edge.relation_type for node in snapshot.nodes for edge in node.edges
    }

    assert node_types == {
        "atom",
        "task",
        "issue",
        "sldb_model",
        "source_file",
        "test_file",
    }
    assert relation_types == {
        "materializes",
        "validates",
        "invokes",
        "routes",
        "generated_from",
        "source_for",
        "violates",
    }

    graph = nx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)

    reloaded = load_knowledge_node(graph, "deskops://atom/kgdb")
    assert reloaded.identity.node_type == "atom"
    assert [edge.relation_type for edge in reloaded.edges] == [
        "materializes",
        "source_for",
    ]


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (SystemIdentity, {"node_id": "node://bad", "node_type": ""}),
        (SystemIdentity, {"node_id": "node://bad", "node_type": "source file"}),
        (Edge, {"target_id": "node://bad", "relation_type": ""}),
        (Edge, {"target_id": "node://bad", "relation_type": "generated from"}),
    ],
)
def test_vocabulary_terms_keep_basic_shape_validation(model, payload):
    with pytest.raises(ValidationError):
        model.model_validate(payload)


def test_graph_bundle_schema_exposes_extensible_vocabulary_terms():
    schema_path = REPO_ROOT / "contracts" / "schemas" / "kgdb_graph_bundle.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    vocabulary = schema["$defs"]["vocabularyTerm"]
    assert vocabulary["type"] == "string"
    assert "enum" not in vocabulary
    assert vocabulary["pattern"] == "^[A-Za-z][A-Za-z0-9_.:-]*$"
