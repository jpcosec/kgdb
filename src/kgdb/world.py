"""``kgdb init``: make an sldb store able to hold typed relations.

The work moved to sldb (fusion of kgdb into sldb): `sldb.api.init_relations` registers the
two relation models (from `sldb.models`), writes the builtin relation types as tracked
documents under ``sldb/relation_types/``, and registers each relation name as an sldb
predicate with its axis. Idempotent: running it twice changes nothing. This module is what
is left for callers of ``kgdb.world.init_world``.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api import RelationsInitReport, init_relations

InitReport = RelationsInitReport


def init_world(store: str | Path, pythonpath: str | None = None) -> RelationsInitReport:
    """Prepare the store at ``store`` for typed relations."""
    report = init_relations(store, pythonpath)
    for ref in report.models_added:
        print(f"Registered '{ref.split(':', 1)[1]}'")
    return report
