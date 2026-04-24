"""kgdb contracts package."""

from importlib import import_module


_EXPORTS = {
    "Edge": "kgdb.contracts.base",
    "KnowledgeNode": "kgdb.contracts.node",
    "SystemIdentity": "kgdb.contracts.base",
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
