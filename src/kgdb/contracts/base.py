"""The base graph contracts moved to sldb (fusion of kgdb into sldb): `sldb.store.graph`.

Re-exported here so callers of `kgdb.contracts.base` keep working — and, more to the point,
so there is a single `Edge`/`SystemIdentity` class in the ecosystem instead of two that merely
look alike. A node built by sldb and a node built through kgdb are now the same type.
"""

from sldb.store.graph import Edge, SystemIdentity, VocabularyTerm

__all__ = ["Edge", "SystemIdentity", "VocabularyTerm"]
