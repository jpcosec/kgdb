import json
from pathlib import Path
import pytest
from kgdb.main import main
import sys

def test_ingest_substrate(tmp_path, monkeypatch):
    """Verify that a GraphSnapshot can be ingested via CLI."""
    input_file = Path("kgdb/desk/fixtures/substrate_v1.json")
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
    repo_node = next(n for n in data["nodes"] if n["id"] == "repo://wikipu-ecosystem")
    assert repo_node["type"] == "system"
