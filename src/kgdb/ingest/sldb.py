"""Projecting an sldb semantic export into a graph snapshot moved to sldb itself:
`sldb.store.graph.ingest_sldb` (and `sldb.api.graph.ingest_sldb`).

Re-exported here for callers of `kgdb.ingest.sldb`. This was always sldb's own export being
read back; after the fusion it lives where the export is produced.
"""

from sldb.store.graph import sldb_semantic_export_to_snapshot

__all__ = ["sldb_semantic_export_to_snapshot"]
