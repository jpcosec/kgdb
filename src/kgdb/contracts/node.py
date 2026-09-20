"""`KnowledgeNode` and its facet payload moved to sldb: `sldb.store.graph.node`.

Re-exported here for callers of `kgdb.contracts.node`, together with the two names the old
module happened to expose through its own imports (`Edge`, `SystemIdentity`), which callers
import from here. See `kgdb.contracts.base`.
"""

from sldb.store.graph import Edge, FacetPayload, KnowledgeNode, SystemIdentity

__all__ = ["Edge", "FacetPayload", "KnowledgeNode", "SystemIdentity"]
