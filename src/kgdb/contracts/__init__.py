"""kgdb contracts package."""

from importlib import import_module


_EXPORTS = {
    "Edge": "kgdb.contracts.base",
    "GraphSnapshot": "kgdb.contracts.io",
    "KnowledgeNode": "kgdb.contracts.node",
    "PersistenceEntry": "kgdb.contracts.persistence",
    "QueryResult": "kgdb.contracts.io",
    "SystemIdentity": "kgdb.contracts.base",
    "TransactionManifest": "kgdb.contracts.persistence",
    "VocabularyTerm": "kgdb.contracts.base",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str):
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value
