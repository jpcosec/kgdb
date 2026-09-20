"""The IO contracts moved to sldb: `sldb.store.graph.snapshot` / `query_result`.

Re-exported here for callers of `kgdb.contracts.io`. See `kgdb.contracts.base`.
"""

from sldb.store.graph import GraphSnapshot, QueryResult

__all__ = ["GraphSnapshot", "QueryResult"]
