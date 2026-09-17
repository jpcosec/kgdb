"""PLAN 15 M3: kgdb's incremental `build_typed_snapshot(..., previous=...)` against the same
store, after a write, equals the full rebuild — nodes, edges, metadata but for timestamps.
That equivalence is the binding invariant of the plan (stop if it breaks and is not understood).

Covers the write shapes the plan calls out: add a document, change one (a field value: same
hash_b for OTHER documents of the model, different for this one), delete one, change a model
(promote a draft field — same documents, a different version), and add an invalid RelationDoc
(must error exactly like the full rebuild does)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sldb import api as sldb_api

from kgdb.ingest import TypedIngestError, build_typed_snapshot
from kgdb.world import init_world

MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Table(StructuredNLDoc):
    __family__ = "restaurant"
    __template__ = "# \\u2e22rev\\u2022title\\u2e25\\n\\nCapacity: \\u2e22rev\\u2022capacity\\u2e25"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")


class Reservation(StructuredNLDoc):
    __family__ = "restaurant"
    __template__ = "# \\u2e22rev\\u2022title\\u2e25\\n\\nSize: \\u2e22rev\\u2022party_size\\u2e25"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")
'''


class World:
    def __init__(self, tmp_path: Path):
        sys.modules.pop("merkle_models", None)
        (tmp_path / "merkle_models.py").write_text(MODELS, encoding="utf-8")
        self.root = tmp_path / "world"
        self.root.mkdir()
        self.store = self.root / ".sldb"
        self.py = str(tmp_path)
        sldb_api.init_store(self.root)
        for m in ("Table", "Reservation"):
            sldb_api.add_model(self.store, f"merkle_models:{m}", self.py)
        init_world(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        sldb_api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def change(self, model: str, name: str, payload: dict) -> None:
        sldb_api.save_document_payload(self.store, model, name, payload, self.py)

    def delete(self, name: str) -> None:
        sldb_api.untrack_document(self.store, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], cardinality="many_to_many") -> None:
        self.create("RelationTypeDoc", f"rt-{name}", {
            "title": name, "name": name, "direction": "directed", "cardinality": cardinality, "axis": "WHERE",
            "source_types": source, "target_types": target, "condition": "", "description": f"{name} relation.",
        })

    def relation(self, name: str, src: str, tgt: str, rtype: str) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": "", "notes": ""})

    def promote_field(self, model: str, field: str, field_type: str, default) -> None:
        sldb_api.add_model_field(self.store, model, field, field_type, "x", json.dumps(default), self.py)
        sldb_api.promote_model_draft(self.store, model, self.py)
        sys.modules.pop("merkle_models", None)  # promote rewrites the module file; drop the cached import

    def build(self, previous=None):
        return build_typed_snapshot(self.store, self.py, previous=previous)


@pytest.fixture
def world(tmp_path: Path) -> World:
    w = World(tmp_path)
    w.create("Table", "table-12", {"title": "Table 12", "capacity": 6})
    w.create("Table", "table-14", {"title": "Table 14", "capacity": 8})
    w.create("Reservation", "res-1", {"title": "Ana", "party_size": 6})
    w.relation_type("assigned_to", ["Reservation"], ["Table"], cardinality="many_to_one")
    return w


def _sans_timestamp(snapshot):
    return {"nodes": sorted((n.identity.node_id, n.identity.node_type, [(e.target_id, e.relation_type, e.metadata) for e in n.edges]) for n in snapshot.nodes),
            "metadata": {k: v for k, v in snapshot.metadata.items()}}


def _assert_equivalent(incremental, full) -> None:
    assert _sans_timestamp(incremental) == _sans_timestamp(full)


def test_incremental_equals_full_after_adding_a_document(world: World):
    base, _ = world.build()
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    incremental, _ = world.build(previous=base)
    full, _ = world.build()
    _assert_equivalent(incremental, full)


def test_incremental_equals_full_after_changing_a_document(world: World):
    base, _ = world.build()
    world.change("Table", "table-14", {"title": "Table 14", "capacity": 10})
    incremental, _ = world.build(previous=base)
    full, _ = world.build()
    _assert_equivalent(incremental, full)
    # only the changed document's node moved; the untouched one is the identical object's data
    changed = next(n for n in incremental.nodes if n.identity.node_id == "sldb://document/Table:table-14")
    assert changed.semantics.hash_c != next(n for n in base.nodes if n.identity.node_id == "sldb://document/Table:table-14").semantics.hash_c


def test_incremental_equals_full_after_deleting_a_document(world: World):
    base, _ = world.build()
    world.delete("table-12")
    incremental, _ = world.build(previous=base)
    full, _ = world.build()
    _assert_equivalent(incremental, full)
    assert not any(n.identity.node_id == "sldb://document/Table:table-12" for n in incremental.nodes)


def test_deleting_a_related_document_errors_the_same_incremental_or_full(world: World):
    """Deleting the target of a still-tracked RelationDoc is an orphan, an error either way
    (removing both the relation and its target is sldb's own sections-index bookkeeping —
    tracked separately, not this plan's incremental invariant)."""
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    base, _ = world.build()
    world.delete("table-12")
    with pytest.raises(TypedIngestError) as exc_full:
        world.build()
    with pytest.raises(TypedIngestError) as exc_incremental:
        world.build(previous=base)
    assert exc_full.value.errors == exc_incremental.value.errors


def test_incremental_equals_full_after_changing_a_model(world: World):
    base, _ = world.build()
    world.promote_field("Table", "zone", "str", "indoor")
    incremental, _ = world.build(previous=base)
    full, _ = world.build()
    _assert_equivalent(incremental, full)
    assert any(n.identity.node_id == "sldb://field/Table.zone" for n in incremental.nodes)


def test_incremental_equals_full_over_several_writes_in_a_row(world: World):
    snap, _ = world.build()
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    snap, _ = world.build(previous=snap)
    world.create("Table", "table-20", {"title": "Table 20", "capacity": 2})
    snap, _ = world.build(previous=snap)
    world.change("Reservation", "res-1", {"title": "Ana", "party_size": 4})
    snap, _ = world.build(previous=snap)
    world.delete("table-14")
    snap, _ = world.build(previous=snap)
    full, _ = world.build()
    _assert_equivalent(snap, full)


def test_incremental_reuses_previous_verbatim_when_nothing_changed(world: World):
    base, _ = world.build()
    same, meta = world.build(previous=base)
    assert same is base
    assert meta is base.metadata


def test_invalid_relation_doc_errors_the_same_incremental_or_full(world: World):
    base, _ = world.build()
    world.relation("bad", "Reservation:res-1", "Table:table-12", "teleports_to")
    with pytest.raises(TypedIngestError) as exc_full:
        world.build()
    with pytest.raises(TypedIngestError) as exc_incremental:
        world.build(previous=base)
    assert exc_full.value.errors == exc_incremental.value.errors


def test_cardinality_violation_errors_the_same_incremental_or_full(world: World):
    world.relation("e1", "Reservation:res-1", "Table:table-12", "assigned_to")
    base, _ = world.build()
    world.relation("e2", "Reservation:res-1", "Table:table-14", "assigned_to")
    with pytest.raises(TypedIngestError) as exc_full:
        world.build()
    with pytest.raises(TypedIngestError) as exc_incremental:
        world.build(previous=base)
    assert exc_full.value.errors == exc_incremental.value.errors
