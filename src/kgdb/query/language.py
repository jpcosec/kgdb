"""The structured query language moved to sldb: `sldb.store.graph.language`.

Re-exported here so a query built against `kgdb.query.language` is the same object sldb's own
executor accepts. Note that only the *language* is shared: `kgdb.query.executor` runs it over a
networkx graph, `sldb.store.graph.executor` runs it over the store's edge index.
"""

from sldb.store.graph import FacetFilter, FieldCondition, GraphScope, RelationFilter, StructuredQuery

__all__ = ["FacetFilter", "FieldCondition", "GraphScope", "RelationFilter", "StructuredQuery"]
