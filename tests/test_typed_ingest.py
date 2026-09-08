"""Typed ingest over a real sldb store: a small restaurant world built from scratch.

Covers: `kgdb init` registers the models, tracks the builtin relation types and
predicates; `build_typed_snapshot` produces model-named document nodes, field
nodes, relation_type nodes with applies_to edges, anchor `names` edges, and one
typed edge per RelationDoc with origin/condition/axis metadata; parallel edges of
different types between one pair survive the graph and save/load; validation
rejects unknown types, wrong endpoint classes, orphans and cardinality
violations; excluded tags drop documents; the CLI writes the graph.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx
import pytest

from sldb.cli import main as sldb_main

from kgdb.graph.utils import add_knowledge_node, load_graph, save_graph
from kgdb.ingest import TypedIngestError, build_typed_snapshot
from kgdb.main import main as kgdb_main
from kgdb.world import init_world

MODELS = '''from typing import Literal
from pydantic import Field
from sldb import StructuredNLDoc


class Party(StructuredNLDoc):
    __family__ = "restaurant"
    __template__ = "# ⸢rev•title⸥\\n\\nSize: ⸢rev•party_size⸥"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")


class Reservation(Party):
    __semantics__ = {"type": ["restaurant", "reservation"]}


class Table(StructuredNLDoc):
    __family__ = "restaurant"
    __semantics__ = {"type": ["restaurant", "table"]}
    __template__ = "# ⸢rev•title⸥\\n\\nCapacity: ⸢rev•capacity⸥"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")


class Note(StructuredNLDoc):
    __semantics__ = {"type": ["pron", "move"], "tags": ["type", "pron", "move"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Alias(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "anchor"]}
    __template__ = "# ⸢rev•symbol⸥\\n\\nRef: ⸢rev•ref⸥"
    symbol: str = Field(description="Word.")
    ref: str = Field(description="What it names.")
'''


def _run(argv: list[str]) -> None:
    assert sldb_main(argv) == 0


class World:
    def __init__(self, tmp_path: Path):
        sys.modules.pop("typed_models", None)
        (tmp_path / "typed_models.py").write_text(MODELS, encoding="utf-8")
        self.root = tmp_path / "world"
        self.root.mkdir()
        self.store = self.root / ".sldb"
        self.py = str(tmp_path)
        self.common = ["--store", str(self.store), "--pythonpath", self.py]
        _run(["stores", "init", "--path", str(self.root)])
        for m in ("Reservation", "Table", "Note", "Alias"):
            _run(["models", "add", f"typed_models:{m}", *self.common])
        init_world(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        _run(["docs", "create", "--model", model, "-o", str(self.root / f"{name}.md"), "--name", name, json.dumps(payload), *self.common])

    def relation_type(self, name: str, source: list[str], target: list[str], cardinality="many_to_many", condition="", direction="directed"):
        self.create("RelationTypeDoc", f"rt-{name}", {
            "title": name, "name": name, "direction": direction, "cardinality": cardinality, "axis": "WHERE",
            "source_types": source, "target_types": target, "condition": condition, "description": f"{name} relation.",
        })

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition="") -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": ""})

    def build(self):
        return build_typed_snapshot(self.store, self.py)


@pytest.fixture
def world(tmp_path: Path) -> World:
    w = World(tmp_path)
    w.create("Table", "table-12", {"title": "Table 12", "capacity": 6})
    w.create("Table", "table-14", {"title": "Table 14", "capacity": 8})
    w.create("Reservation", "res-1", {"title": "Ana", "party_size": 6})
    w.relation_type("assigned_to", ["Reservation"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
    w.relation_type("near", ["Party"], ["Table"])
    return w


def _edges(snapshot, src: str):
    node = next(n for n in snapshot.nodes if n.identity.node_id == src)
    return [(e.target_id, e.relation_type, e.metadata) for e in node.edges]


def test_init_is_idempotent_and_tracks_builtin_types(world: World):
    report = init_world(world.store, world.py)
    assert report.models_added == [] and report.types_written == [] and report.predicates_added == []
    snapshot, meta = world.build()
    assert "has_document" in meta["relation_types"] and "applies_to_source" in meta["relation_types"]
    assert (world.root / "kgdb" / "relation_types" / "tagged_as.md").exists()


def test_documents_are_typed_by_model_and_fields_become_nodes(world: World):
    snapshot, _ = world.build()
    ids = {n.identity.node_id: n for n in snapshot.nodes}
    assert ids["sldb://document/Table:table-12"].identity.node_type == "Table"
    field = ids["sldb://field/Table.capacity"]
    assert field.identity.node_type == "sldb_field" and field.semantics.description == "Seats."
    assert ("sldb://field/Table.capacity", "has_field", {"origin": "schema"}) in _edges(snapshot, "sldb://model/Table")
    # RelationDoc and RelationTypeDoc are not document nodes
    assert not any(i.startswith("sldb://document/RelationTypeDoc:") for i in ids)


def test_relation_types_become_nodes_with_applies_to_edges(world: World):
    snapshot, _ = world.build()
    edges = _edges(snapshot, "sldb://relation_type/assigned_to")
    assert ("sldb://model/Reservation", "applies_to_source", {"origin": "schema"}) in edges
    assert ("sldb://model/Table", "applies_to_target", {"origin": "schema"}) in edges


def test_relation_doc_becomes_typed_edge_inheriting_condition_and_axis(world: World):
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    snapshot, meta = world.build()
    (target, rel, m), = [e for e in _edges(snapshot, "sldb://document/Reservation:res-1") if e[1] == "assigned_to"]
    assert target == "sldb://document/Table:table-12"
    assert m == {"origin": "relation_doc", "relation_doc": "e1", "condition": "capacity >= {party_size}", "axis": "WHERE"}
    assert meta["relation_docs"] == 1
    assert not any(i.identity.node_id.startswith("sldb://document/RelationDoc:") for i in snapshot.nodes)


def test_source_class_inherits_through_base_models(world: World):
    # `near` accepts Party as source; res-1 is a Reservation, which extends Party
    world.relation("e2", "Reservation:res-1", "Table:table-12", "near")
    snapshot, _ = world.build()
    assert any(rel == "near" for _, rel, _ in _edges(snapshot, "sldb://document/Reservation:res-1"))


def test_parallel_typed_edges_survive_graph_and_save_load(world: World, tmp_path: Path):
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    world.relation("e2", "Reservation:res-1", "Table:table-12", "near")
    snapshot, _ = world.build()
    graph = nx.MultiDiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    out = tmp_path / "g.json"
    save_graph(graph, out)
    loaded = load_graph(out)
    rels = sorted(d["relation"] for _, _, d in loaded.out_edges("sldb://document/Reservation:res-1", data=True) if d["relation"] in ("assigned_to", "near"))
    assert rels == ["assigned_to", "near"]


def test_unknown_relation_type_is_an_error(world: World):
    world.relation("bad", "Reservation:res-1", "Table:table-12", "teleports_to")
    with pytest.raises(TypedIngestError) as exc:
        world.build()
    assert "unknown relation type 'teleports_to'" in str(exc.value)


def test_wrong_endpoint_class_is_an_error(world: World):
    world.relation("bad", "Table:table-12", "Reservation:res-1", "assigned_to")
    with pytest.raises(TypedIngestError) as exc:
        world.build()
    assert "source class 'Table' not in source_types" in str(exc.value)


def test_orphan_endpoint_is_an_error(world: World):
    world.relation("bad", "Reservation:res-1", "Table:table-99", "assigned_to")
    with pytest.raises(TypedIngestError) as exc:
        world.build()
    assert "target 'Table:table-99' is not a tracked document" in str(exc.value)


def test_cardinality_is_enforced(world: World):
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    world.relation("e2", "Reservation:res-1", "Table:table-14", "assigned_to")
    with pytest.raises(TypedIngestError) as exc:
        world.build()
    assert "has 2 'assigned_to' targets but cardinality is many_to_one" in str(exc.value)


def test_excluded_tag_drops_documents(world: World):
    world.create("Note", "move-1", {"title": "a move"})
    snapshot, meta = world.build()
    assert not any(n.identity.node_id == "sldb://document/Note:move-1" for n in snapshot.nodes)
    assert meta["excluded_documents"] == 1


def test_anchor_names_what_its_ref_points_to(world: World):
    world.create("Alias", "alias-large", {"symbol": "large", "ref": "predicate:Table:capacity >= 6"})
    world.create("Alias", "alias-seats", {"symbol": "seats", "ref": "field:Table.capacity"})
    snapshot, meta = world.build()
    assert ("sldb://model/Table", "names", {"origin": "alias"}) in _edges(snapshot, "sldb://anchor/large")
    assert ("sldb://field/Table.capacity", "names", {"origin": "alias"}) in _edges(snapshot, "sldb://anchor/seats")
    assert meta["anchors"] == 2


def test_cli_ingest_store_writes_multigraph(world: World, tmp_path: Path, monkeypatch, capsys):
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    out = tmp_path / "graph.json"
    monkeypatch.setattr(sys, "argv", ["kgdb", "ingest", "--store", str(world.store), "--pythonpath", world.py, "--output", str(out)])
    kgdb_main()
    assert "typed edges" in capsys.readouterr().out
    data = json.loads(out.read_text())
    assert data.get("multigraph") is True
    monkeypatch.setattr(sys, "argv", ["kgdb", "edges", "--graph", str(out), "--node", "sldb://document/Reservation:res-1"])
    kgdb_main()
    assert "assigned_to" in capsys.readouterr().out
