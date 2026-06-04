import json
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "contracts" / "schemas" / "sldb_kgdb_semantic_export.schema.json"
FIXTURE_PATH = REPO_ROOT / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"
INTEGRATION_CONTRACT_PATH = REPO_ROOT / "contracts" / "integration.contract.yaml"


def test_sldb_semantic_export_fixture_matches_schema():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=fixture, schema=schema)


def test_sldb_semantic_export_schema_is_versioned_and_strict():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert schema["additionalProperties"] is False
    assert schema["properties"]["contract"]["properties"]["name"]["const"] == "sldb_kgdb_semantic_export"
    assert schema["properties"]["contract"]["properties"]["version"]["const"] == 1


def test_kgdb_consumes_sldb_semantic_export_contract():
    contract_text = INTEGRATION_CONTRACT_PATH.read_text(encoding="utf-8")

    assert "name: sldb_kgdb_semantic_export" in contract_text
    assert "schema: contracts/schemas/sldb_kgdb_semantic_export.schema.json" in contract_text
    assert "name: sldb_document_payload" not in contract_text


def test_sldb_semantic_export_declares_generated_graph_vocabulary():
    contract_text = INTEGRATION_CONTRACT_PATH.read_text(encoding="utf-8")

    for node_type in [
        "sldb_model",
        "sldb_document",
        "sldb_section",
        "semantic_tag",
        "sldb_store",
    ]:
        assert node_type in contract_text

    for relation_type in [
        "has_model",
        "has_document",
        "has_section",
        "tagged_as",
        "semantic_parent",
        "semantic_equivalent",
    ]:
        assert relation_type in contract_text
