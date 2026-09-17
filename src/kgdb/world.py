"""``kgdb init``: make an sldb store able to hold typed relations.

Registers kgdb's two models in the store, writes the builtin relation types as
tracked documents, and registers each relation name as an sldb predicate with
its axis. Idempotent: running it twice changes nothing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sldb.api import add_model, load_registered_model, open_store, resolve_model_ref
from sldb.core.exceptions import SLDBModelError
from sldb.runtime.validation import render_model_markdown
from sldb.store.io import load_documents_index, load_models_index, load_store_index, save_store_index
from sldb.store.models import PredicateEntry
from sldb.store.ops import track_document

from kgdb.models import BUILTIN_RELATION_TYPES, RelationTypeDoc, builtin_doc_name, builtin_payload

MODEL_REFS = ("kgdb.models:RelationTypeDoc", "kgdb.models:RelationDoc")
BUILTIN_DIR = Path("kgdb") / "relation_types"


@dataclass
class InitReport:
    models_added: list[str] = field(default_factory=list)
    types_written: list[str] = field(default_factory=list)
    predicates_added: list[str] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"models added: {len(self.models_added)} · builtin relation types written: "
            f"{len(self.types_written)} · predicates added: {len(self.predicates_added)}"
        )


def init_world(store: str | Path, pythonpath: str | None = None) -> InitReport:
    """Prepare the store at ``store`` for typed relations."""
    location = open_store(store)
    sp, root = location.store_path, location.project_root
    report = InitReport()
    for ref in MODEL_REFS:
        if _add_model(sp, ref, pythonpath):
            report.models_added.append(ref)
    _write_builtin_types(sp, root, pythonpath, report)
    _register_predicates(sp, report)
    return report


def _add_model(sp: Path, ref: str, pythonpath: str | None) -> bool:
    try:
        registration = add_model(sp, ref, pythonpath)
    except SLDBModelError:
        return False
    print(f"Registered '{registration.name}'")
    return True


def _write_builtin_types(sp: Path, root: Path, pythonpath: str | None, report: InitReport) -> None:
    registered = load_registered_model(sp, "RelationTypeDoc", pythonpath)
    model_type, entry, idx = registered.model_type, registered.entry, registered.store_index
    tracked = _tracked_names(root, entry)
    for spec in BUILTIN_RELATION_TYPES:
        name = builtin_doc_name(spec)
        if name in tracked:
            continue
        path = root / BUILTIN_DIR / f"{spec['name']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_model_markdown(RelationTypeDoc, builtin_payload(spec)) + "\n", encoding="utf-8")
        track_document(sp, root, idx, model_type, entry, path, name, resolve_model_ref, pythonpath)
        idx = load_store_index(sp)
        report.types_written.append(spec["name"])


def _tracked_names(root: Path, entry) -> set[str]:
    m_idx = load_models_index(root / entry.models_index)
    return {d.name for d in load_documents_index(root / m_idx.documents_index).documents}


def _register_predicates(sp: Path, report: InitReport) -> None:
    idx = load_store_index(sp)
    known = {p.name for p in idx.predicates}
    for spec in BUILTIN_RELATION_TYPES:
        if spec["name"] in known:
            continue
        idx.predicates.append(PredicateEntry(name=spec["name"], axis=spec["axis"], description=spec["description"]))
        report.predicates_added.append(spec["name"])
    if report.predicates_added:
        save_store_index(sp, idx)
