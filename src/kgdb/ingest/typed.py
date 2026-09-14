"""Typed ingest: build the graph of an sldb store, every edge typed by a RelationTypeDoc.

One pass over a store produces one GraphSnapshot:

- the structural nodes and edges of the semantic export (store, models, documents,
  sections, tags), with document ``node_type`` set to the model name;
- a ``sldb_field`` node per model field (type and description) with ``has_field``
  edges, and ``extends`` edges from ``base_models``;
- a ``relation_type`` node per tracked RelationTypeDoc with ``applies_to_source`` /
  ``applies_to_target`` edges to the models it names;
- an ``anchor`` node per alias document with ``names`` edges to what its ``ref``
  names;
- one edge per RelationDoc, hung on its source, carrying origin, condition and
  axis in metadata; the RelationDoc itself is not a node;
- documents carrying an excluded tag (the ledger) are left out.

Then every edge is validated against its relation type: the type exists as a
tracked RelationTypeDoc (the structural ones come from ``kgdb init``), both
endpoints exist, their classes are allowed (model names inherit through
``base_models``), cardinality holds, and undirected types get their reverse
edge. Any violation is an error, never a warning: the world prevents at
authoring time, kgdb detects at assembly time.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.schema import field_descriptor
from sldb.cli.store_context import get_store_context
from sldb.store.export import export_kgdb_semantic_payload
from sldb.store.query import load_runtime_documents

from kgdb.contracts import Edge, GraphSnapshot, KnowledgeNode, SystemIdentity
from kgdb.ingest.sldb import sldb_semantic_export_to_snapshot

DEFAULT_EXCLUDED_TAGS = ("type.pron.move",)
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
ANCHOR_TAG = "type.knowledge.anchor"


class TypedIngestError(ValueError):
    """The store cannot be assembled into a valid typed graph."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("typed ingest failed:\n" + "\n".join(f"- {e}" for e in errors))


def doc_node_id(export_id: str) -> str:
    return f"sldb://document/{export_id}"


def model_node_id(name: str) -> str:
    return f"sldb://model/{name}"


def field_node_id(model: str, field: str) -> str:
    return f"sldb://field/{model}.{field}"


def relation_type_node_id(name: str) -> str:
    return f"sldb://relation_type/{name}"


def anchor_node_id(symbol: str) -> str:
    return f"sldb://anchor/{symbol}"


def build_typed_snapshot(
    store: str | Path,
    pythonpath: str | None = None,
    exclude_tags: Iterable[str] = DEFAULT_EXCLUDED_TAGS,
) -> tuple[GraphSnapshot, dict[str, Any]]:
    """Assemble and validate the typed graph of the store. Raises TypedIngestError."""
    builder = _Builder(store, pythonpath, set(exclude_tags))
    return builder.build()


class _Builder:
    def __init__(self, store: str | Path, pythonpath: str | None, exclude_tags: set[str]):
        self.sp, self.root = get_store_context(str(store))
        self.pythonpath = pythonpath
        self.exclude_tags = exclude_tags
        self.errors: list[str] = []
        self.nodes: dict[str, KnowledgeNode] = {}
        self.models: dict[str, dict] = {}
        self.model_types: dict[str, type] = {}
        self.relation_types: dict[str, dict] = {}
        self.report: dict[str, Any] = {}

    # -- assembly -----------------------------------------------------------

    def build(self) -> tuple[GraphSnapshot, dict[str, Any]]:
        payload = export_kgdb_semantic_payload(self.sp, self.root, resolve_model_ref, self.pythonpath, rebuild=True)
        base = sldb_semantic_export_to_snapshot(payload)
        self.nodes = {n.identity.node_id: n for n in base.nodes}
        self.models = {m["name"]: m for m in payload["models"]}
        self._resolve_model_types()
        docs = load_runtime_documents(self.sp, resolve_model_ref, self.pythonpath)
        by_kind = self._classify(docs)
        for export_id in by_kind["dropped"]:
            self._drop_document(export_id)
        self._mark_structural_edges()
        self._retype_documents()
        self._add_fields_and_extends()
        self._add_relation_types(by_kind["relation_types"])
        self._add_anchors(by_kind["anchors"])
        self._add_relation_docs(by_kind["relations"])
        self._validate()
        if self.errors:
            raise TypedIngestError(self.errors)
        self._finish_report(payload, by_kind)
        snapshot = GraphSnapshot(version="1.0", nodes=list(self.nodes.values()), metadata=self.report)
        return snapshot, self.report

    def _resolve_model_types(self) -> None:
        for name, m in self.models.items():
            try:
                self.model_types[name] = resolve_model_ref(m["model_ref"], self.pythonpath)
            except Exception:  # noqa: BLE001 - a linked model may not import here
                continue

    def _classify(self, docs) -> dict[str, list]:
        out: dict[str, list] = {"relation_types": [], "relations": [], "anchors": [], "dropped": []}
        for d in docs:
            export_id = f"{d.model_name}:{d.name}"
            if self.exclude_tags & set(d.semantic_tags):
                out["dropped"].append(export_id)
            elif d.model_name == RELATION_TYPE_MODEL:
                out["relation_types"].append(d); out["dropped"].append(export_id)
            elif d.model_name == RELATION_MODEL:
                out["relations"].append(d); out["dropped"].append(export_id)
            elif ANCHOR_TAG in d.semantic_tags and "symbol" in d.payload and "ref" in d.payload:
                out["anchors"].append(d); out["dropped"].append(export_id)
        return out

    def _drop_document(self, export_id: str) -> None:
        gone = {doc_node_id(export_id)}
        gone |= {nid for nid in self.nodes if nid.startswith(f"sldb://section/{export_id}#")}
        for nid in gone:
            self.nodes.pop(nid, None)
        for node in self.nodes.values():
            node.edges = [e for e in node.edges if e.target_id not in gone]

    def _mark_structural_edges(self) -> None:
        for node in self.nodes.values():
            for e in node.edges:
                e.metadata.setdefault("origin", "structural")

    def _retype_documents(self) -> None:
        for node in self.nodes.values():
            if node.identity.node_type == "sldb_document":
                node.identity.node_type = node.semantics.model

    def _add_fields_and_extends(self) -> None:
        for name, model_type in self.model_types.items():
            mid = model_node_id(name)
            if mid not in self.nodes:
                continue
            for fname, finfo in model_type.model_fields.items():
                fid = field_node_id(name, fname)
                desc = field_descriptor(fname, finfo)
                desc.update({"model": name, "description": finfo.description or ""})
                self.nodes[fid] = KnowledgeNode(identity=SystemIdentity(node_id=fid, node_type="sldb_field"), semantics=desc)
                self._edge(mid, fid, "has_field", {"origin": "schema"})
            for base in self.models[name].get("base_models", []):
                if model_node_id(base) in self.nodes:
                    self._edge(mid, model_node_id(base), "extends", {"origin": "schema"})

    def _add_relation_types(self, docs) -> None:
        for d in docs:
            p = d.payload
            name = p["name"]
            self.relation_types[name] = {**p, "doc": d.name}
            rid = relation_type_node_id(name)
            self.nodes[rid] = KnowledgeNode(identity=SystemIdentity(node_id=rid, node_type="relation_type"), semantics={**p, "doc": d.name})
            for kind, key in (("applies_to_source", "source_types"), ("applies_to_target", "target_types")):
                for cls in p.get(key, []):
                    if model_node_id(cls) in self.nodes:
                        self._edge(rid, model_node_id(cls), kind, {"origin": "schema"})

    def _add_anchors(self, docs) -> None:
        for d in docs:
            p = d.payload
            aid = anchor_node_id(str(p["symbol"]))
            self.nodes[aid] = KnowledgeNode(identity=SystemIdentity(node_id=aid, node_type="anchor"), semantics={**p, "doc": d.name})
            for target in self._anchor_targets(p):
                if target in self.nodes:
                    self._edge(aid, target, "names", {"origin": "alias"})

    def _anchor_targets(self, p: dict) -> list[str]:
        ref = str(p.get("ref", ""))
        if ref.lstrip().startswith("("):
            return _form_targets(_read_form(ref))
        targets: list[str] = []
        head, _, rest = ref.partition(":")
        if head == "model":
            targets.append(model_node_id(rest))
        elif head == "field" and "." in rest:
            m, f = rest.split(".", 1); targets.append(field_node_id(m, f))
        elif head == "predicate":
            targets.append(model_node_id(rest.split(":", 1)[0]))
        elif head == "relation":
            targets.append(relation_type_node_id(rest))
        elif head == "doc":
            targets.append(doc_node_id(rest))
        elif head == "action":
            for m, f in re.findall(r"\b([A-Za-z_]\w*)\.([A-Za-z_]\w*)=", rest):
                targets.append(field_node_id(m, f))
        elif head == "compose":
            for step in p.get("steps") or []:
                if isinstance(step, dict):
                    if step.get("model"): targets.append(model_node_id(step["model"]))
                    if step.get("relation"): targets.append(relation_type_node_id(step["relation"]))
        return targets

    def _add_relation_docs(self, docs) -> None:
        for d in docs:
            p = d.payload
            rt = self.relation_types.get(p["relation_type"])
            src, tgt = doc_node_id(p["source_id"]), doc_node_id(p["target_id"])
            meta = {
                "origin": "relation_doc",
                "relation_doc": d.name,
                "condition": p.get("condition") or (rt or {}).get("condition", ""),
                "axis": (rt or {}).get("axis", ""),
            }
            if src not in self.nodes:
                self.errors.append(f"relation '{d.name}': source '{p['source_id']}' is not a tracked document")
                continue
            if tgt not in self.nodes:
                self.errors.append(f"relation '{d.name}': target '{p['target_id']}' is not a tracked document")
                continue
            self._edge(src, tgt, p["relation_type"], meta)
            if rt and rt.get("direction") == "undirected":
                self._edge(tgt, src, p["relation_type"], {**meta, "reverse": True})

    def _edge(self, src: str, tgt: str, relation: str, meta: dict) -> None:
        self.nodes[src].edges.append(Edge(target_id=tgt, relation_type=relation, metadata=meta))

    # -- validation ----------------------------------------------------------

    def _validate(self) -> None:
        out_count: Counter = Counter()
        in_count: Counter = Counter()
        for node in self.nodes.values():
            for e in node.edges:
                self._validate_edge(node, e)
                out_count[(node.identity.node_id, e.relation_type)] += 1
                in_count[(e.target_id, e.relation_type)] += 1
        self._validate_cardinality(out_count, in_count)

    def _validate_edge(self, node: KnowledgeNode, e: Edge) -> None:
        rt = self.relation_types.get(e.relation_type)
        where = f"edge {node.identity.node_id} -[{e.relation_type}]-> {e.target_id}"
        if rt is None:
            hint = " (run `kgdb init` to track the builtin relation types)" if e.metadata.get("origin") in ("structural", "schema", "alias") else ""
            self.errors.append(f"{where}: unknown relation type '{e.relation_type}'{hint}")
            return
        target = self.nodes.get(e.target_id)
        if target is None:
            self.errors.append(f"{where}: target does not exist")
            return
        if not self._class_ok(node, rt.get("source_types", [])):
            self.errors.append(f"{where}: source class '{self._class_of(node)}' not in source_types {rt.get('source_types')}")
        if not self._class_ok(target, rt.get("target_types", [])):
            self.errors.append(f"{where}: target class '{self._class_of(target)}' not in target_types {rt.get('target_types')}")

    def _validate_cardinality(self, out_count: Counter, in_count: Counter) -> None:
        for (src, rel), n in out_count.items():
            card = self.relation_types.get(rel, {}).get("cardinality", "many_to_many")
            if n > 1 and card in ("one_to_one", "many_to_one"):
                self.errors.append(f"{src} has {n} '{rel}' targets but cardinality is {card}")
        for (tgt, rel), n in in_count.items():
            card = self.relation_types.get(rel, {}).get("cardinality", "many_to_many")
            if n > 1 and card in ("one_to_one", "one_to_many"):
                self.errors.append(f"{tgt} has {n} '{rel}' sources but cardinality is {card}")

    def _class_of(self, node: KnowledgeNode) -> str:
        return node.identity.node_type

    def _class_ok(self, node: KnowledgeNode, allowed: list[str]) -> bool:
        if not allowed:
            return True
        cls = self._class_of(node)
        lineage = [cls] + list(self.models.get(cls, {}).get("base_models", []))
        if "sldb_document" in allowed and cls in self.models:
            return True
        return any(c in allowed for c in lineage)

    # -- report ---------------------------------------------------------------

    def _finish_report(self, payload: dict, by_kind: dict) -> None:
        self.report = {
            "generated_from": "kgdb.ingest.typed",
            "store": {"root": str(self.root), "store_path": str(self.sp), "hash_a": payload["store"]["hash_a"]},
            "models": {m["name"]: m["hash_b"] for m in payload["models"]},
            "relation_types": sorted(self.relation_types),
            "relation_docs": len(by_kind["relations"]),
            "anchors": len(by_kind["anchors"]),
            "excluded_tags": sorted(self.exclude_tags),
            "excluded_documents": len(by_kind["dropped"]) - len(by_kind["relations"]) - len(by_kind["relation_types"]) - len(by_kind["anchors"]),
            "nodes": len(self.nodes),
            "edges": sum(len(n.edges) for n in self.nodes.values()),
        }


_FORM_TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))')
_KERNEL_WRITES = ("change", "add", "remove", "clean", "forget")


class _Sym(str):
    """A bare symbol of a form."""


def _read_form(text: str):
    """The one s-expression of a pron ref (pron spec 13): lists, symbols and strings."""
    stack: list[list] = [[]]
    pos, text = 0, text.strip()
    while pos < len(text):
        m = _FORM_TOKEN.match(text, pos)
        if m is None or m.end() == pos:
            break
        pos = m.end()
        if m.group(1):
            stack.append([])
        elif m.group(2):
            done = stack.pop()
            stack[-1].append(done)
        elif m.group(3) is not None:
            stack[-1].append(re.sub(r"\\(.)", r"\1", m.group(3)))
        elif m.group(4) is not None:
            stack[-1].append(_Sym(m.group(4)))
    return stack[0][0] if stack[0] else []


def _form_targets(form) -> list[str]:
    """What a ref written as a form names: models, fields, relation types, documents."""
    if not isinstance(form, list) or not form or not isinstance(form[0], _Sym):
        return []
    head, args = str(form[0]), form[1:]
    if head == "model" and args:
        return [model_node_id(str(args[0]))]
    if head == "field" and len(args) >= 2:
        return [field_node_id(str(args[0]), str(args[1]))]
    if head in ("where", "value") and args:
        return [model_node_id(str(args[0]))]
    if head == "relation" and args:
        return [relation_type_node_id(str(args[0]))]
    if head == "doc" and args:
        return [doc_node_id(str(args[0]))]
    if head in _KERNEL_WRITES and len(args) >= 2:
        noun = args[0]
        if isinstance(noun, list) and len(noun) >= 3 and str(noun[0]) in ("it", "them"):
            return [field_node_id(str(noun[2]), str(args[1]))]
        return []
    if head == "move":
        return [t for step in args for t in _form_targets(step)]
    if head == "create" and args:
        return [model_node_id(str(args[0]))]
    if head == "assert" and args:
        return [relation_type_node_id(str(args[0]))]
    return []
