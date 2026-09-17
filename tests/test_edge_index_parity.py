"""Parity gate of the fusion of kgdb into sldb: sldb's edge index (per-document shards under
`.sldb/runtime/edges/`, read through `sldb.api`) says exactly what `build_typed_snapshot`
says about the same store — the same nodes (id, class, semantics) and the same edges
(source, target, relation, metadata), edge for edge.

What is left out of the comparison, on purpose: the store node's semantics (absolute paths
and `hash_a`) and a model node's `hash_b` — the index does not persist what moves with every
write or with where the project is checked out; and each node's `source` provenance facet,
which repeats the whole export payload on every node.

Second case: after editing ONE document only its shard is rewritten (every other shard's
mtime is intact) and parity still holds. Errors are compared too: what `TypedIngestError`
raises is what `check_edges` reports.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pytest

from sldb import api as sldb_api

from kgdb.ingest import TypedIngestError, build_typed_snapshot
from kgdb.world import init_world

MODELS = '''from pydantic import Field
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
    __semantics__ = {"type": ["restaurant", "table"], "layer": ["floor"]}
    __template__ = "# ⸢rev•title⸥\\n\\nCapacity: ⸢rev•capacity⸥\\n\\n## Location\\n\\n⸢rev,markdown•location⸥\\n\\n## Notes\\n\\n⸢rev,markdown•notes⸥"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")
    location: str = Field(default="", description="Where it is.")
    notes: str = Field(default="", description="Notes.")


class Note(StructuredNLDoc):
    __semantics__ = {"type": ["pron", "move"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Alias(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "anchor"]}
    __template__ = "# ⸢rev•symbol⸥\\n\\nRef: ⸢rev•ref⸥"
    symbol: str = Field(description="Word.")
    ref: str = Field(description="What it names.")
'''

MODULE = "parity_models"
LEDGER = ("type.pron.move",)
VOLATILE = {"sldb_store": None, "sldb_model": {"hash_b"}}  # None: the whole semantics


class World:
    def __init__(self, tmp_path: Path):
        sys.modules.pop(MODULE, None)
        (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
        self.root = tmp_path / "world"
        self.root.mkdir()
        self.store = self.root / ".sldb"
        self.py = str(tmp_path)
        sldb_api.init_store(self.root)
        for m in ("Reservation", "Table", "Note", "Alias"):
            sldb_api.add_model(self.store, f"{MODULE}:{m}", self.py)
        init_world(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        sldb_api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], cardinality="many_to_many", condition="", direction="directed"):
        self.create("RelationTypeDoc", f"rt-{name}", {
            "title": name, "name": name, "direction": direction, "cardinality": cardinality, "axis": "WHERE",
            "source_types": source, "target_types": target, "condition": condition, "description": f"{name} relation.",
        })

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition="") -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": ""})

    def shard_mtimes(self) -> dict[str, int]:
        runtime = self.store / "runtime"
        return {str(p.relative_to(runtime)): p.stat().st_mtime_ns for p in sorted(runtime.glob("edges*/**/*.yaml")) + sorted(runtime.glob("edges*.yaml"))}


@pytest.fixture
def world(tmp_path: Path) -> World:
    w = World(tmp_path)
    w.create("Table", "table-12", {"title": "Table 12", "capacity": 6, "location": "By the window.", "notes": "Wobbly."})
    w.create("Table", "table-14", {"title": "Table 14", "capacity": 8, "location": "Patio.", "notes": ""})
    w.create("Reservation", "res-1", {"title": "Ana", "party_size": 6})
    w.create("Reservation", "res-2", {"title": "Luis", "party_size": 2})
    w.create("Note", "move-1", {"title": "a ledger move"})
    w.relation_type("assigned_to", ["Reservation"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
    w.relation_type("near", ["Table"], ["Table"], direction="undirected")
    w.relation_type("seats", ["Party"], ["Table"])
    w.relation("res-1-t12", "Reservation:res-1", "Table:table-12", "assigned_to")
    w.relation("res-2-t14", "Reservation:res-2", "Table:table-14", "assigned_to", condition="capacity >= 2")
    w.relation("t12-near-t14", "Table:table-12", "Table:table-14", "near")
    w.relation("res-1-seats", "Reservation:res-1", "Table:table-12", "seats")
    w.create("Alias", "mesa", {"symbol": "mesa", "ref": "model:Table"})
    w.create("Alias", "cupo", {"symbol": "cupo", "ref": "(field Table capacity)"})
    w.create("Alias", "ventana", {"symbol": "ventana", "ref": "doc:Table:table-12"})
    w.create("Alias", "asignar", {"symbol": "asignar", "ref": "(assert assigned_to)"})
    return w


def _semantics(node_type: str, semantics: dict) -> dict:
    drop = VOLATILE.get(node_type, set())
    return {} if drop is None else {k: v for k, v in semantics.items() if k not in drop}


def _of_snapshot(snapshot) -> tuple[dict, Counter]:
    nodes = {n.identity.node_id: (n.identity.node_type, _semantics(n.identity.node_type, n.semantics.model_dump() if n.semantics else {})) for n in snapshot.nodes}
    edges = Counter((n.identity.node_id, e.target_id, e.relation_type, json.dumps(e.metadata, sort_keys=True)) for n in snapshot.nodes for e in n.edges)
    return nodes, edges


def _of_index(index) -> tuple[dict, Counter]:
    nodes = {n.id: (n.node_type, _semantics(n.node_type, n.semantics)) for n in index.nodes.values()}
    edges = Counter((e.source, e.target, e.relation, json.dumps(e.metadata, sort_keys=True)) for e in index.edges)
    return nodes, edges


def assert_parity(world: World, exclude_tags=LEDGER) -> None:
    # the index is read FIRST: build_typed_snapshot rebuilds sldb's derived indexes on its way,
    # and what is under test is what the write path alone left in the shards
    index = sldb_api.load_edge_index(world.store, include_linked=False, exclude_tags=exclude_tags)
    idx_nodes, idx_edges = _of_index(index)
    snapshot, _ = build_typed_snapshot(world.store, world.py, exclude_tags=exclude_tags)
    snap_nodes, snap_edges = _of_snapshot(snapshot)
    assert sorted(idx_nodes) == sorted(snap_nodes)
    for node_id, expected in snap_nodes.items():
        assert idx_nodes[node_id] == expected, node_id
    assert idx_edges == snap_edges, {"only_in_index": idx_edges - snap_edges, "only_in_snapshot": snap_edges - idx_edges}
    assert index.stale == [] and sldb_api.check_edges(world.store, include_linked=False, exclude_tags=exclude_tags).ok


def test_the_index_is_the_typed_snapshot_edge_for_edge(world: World):
    assert_parity(world)
    snapshot, meta = build_typed_snapshot(world.store, world.py)
    assert meta["edges"] > 100 and meta["relation_docs"] == 4 and meta["anchors"] == 4 and meta["excluded_documents"] == 1
    kinds = {n.identity.node_type for n in snapshot.nodes}
    assert {"sldb_store", "sldb_model", "sldb_field", "sldb_section", "semantic_tag", "relation_type", "anchor", "Table", "Reservation"} <= kinds


def test_parity_holds_whatever_the_reader_excludes(world: World):
    assert_parity(world, exclude_tags=())
    assert_parity(world, exclude_tags=("type.knowledge.anchor",))
    tables_out = ("type.restaurant.table",)  # every relation loses an endpoint: both sides say so
    with pytest.raises(TypedIngestError) as raised:
        build_typed_snapshot(world.store, world.py, exclude_tags=tables_out)
    report = sldb_api.check_edges(world.store, include_linked=False, exclude_tags=tables_out)
    assert sorted(report.errors) == sorted(raised.value.errors) and len(report.errors) == 4


def test_editing_one_document_rewrites_only_its_shard_and_keeps_parity(world: World):
    assert_parity(world)
    before = world.shard_mtimes()
    sldb_api.save_document_payload(world.store, "Table", "table-14", {"title": "Table 14", "capacity": 10, "location": "Patio, under the vine.", "notes": "Moved."}, world.py)
    after = world.shard_mtimes()
    assert sorted(after) == sorted(before)
    assert [name for name in before if before[name] != after[name]] == ["edges/Table/table-14.yaml"]
    assert_parity(world)


def test_parity_survives_adding_and_untracking_documents(world: World):
    world.create("Table", "table-20", {"title": "Table 20", "capacity": 4, "location": "", "notes": ""})
    world.relation("t20-near-t12", "Table:table-20", "Table:table-12", "near")
    assert_parity(world)
    sldb_api.untrack_document(world.store, "t20-near-t12", world.py)
    sldb_api.untrack_document(world.store, "table-20", world.py)
    assert_parity(world)


def test_what_typed_ingest_raises_is_what_check_edges_reports(world: World):
    world.relation("orphan", "Reservation:res-1", "Table:nowhere", "assigned_to")
    world.relation("second-table", "Reservation:res-1", "Table:table-14", "assigned_to")
    world.relation("wrong-class", "Table:table-12", "Reservation:res-2", "assigned_to")
    world.relation("untyped", "Reservation:res-2", "Table:table-12", "prefers")
    with pytest.raises(TypedIngestError) as raised:
        build_typed_snapshot(world.store, world.py)
    report = sldb_api.check_edges(world.store, include_linked=False, exclude_tags=LEDGER)
    assert sorted(report.errors) == sorted(raised.value.errors)
    assert len(report.errors) >= 5 and report.stale == []


def test_parity_survives_promoting_a_model_field(world: World):
    sldb_api.add_model_field(world.store, "Reservation", "zone", "str", "Where they sit.", json.dumps("indoor"), world.py)
    sldb_api.promote_model_draft(world.store, "Reservation", world.py)
    sys.modules.pop(MODULE, None)  # promote rewrites the module file; drop the cached import
    assert sldb_api.edge_node(world.store, "sldb://field/Reservation.zone", include_linked=False) is not None
    assert_parity(world)
