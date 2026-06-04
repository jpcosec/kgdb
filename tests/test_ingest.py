import json
from pathlib import Path
import pytest
from kgdb.main import main
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBSTRATE_FIXTURE = REPO_ROOT / "desk" / "fixtures" / "substrate_v1.json"

def test_ingest_substrate(tmp_path, monkeypatch):
    """Verify that a GraphSnapshot can be ingested via CLI."""
    input_file = SUBSTRATE_FIXTURE
    output_file = tmp_path / "substrate.kg.json"
    
    # Simulate CLI arguments
    test_args = ["kgdb", "ingest", "--input", str(input_file), "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", test_args)
    
    # Run main
    main()
    
    assert output_file.exists()
    
    # Verify content
    data = json.loads(output_file.read_text())
    assert "nodes" in data
    assert "links" in data
    assert len(data["nodes"]) == 10
    
    # Verify one node
    repo_node = next(n for n in data["nodes"] if n["id"] == "repo://hum-ecosystem")
    assert repo_node["type"] == "system"
