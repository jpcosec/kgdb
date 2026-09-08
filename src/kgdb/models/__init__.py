"""kgdb's document models: relations are typed by sldb documents kgdb owns."""

from kgdb.models.builtin import BUILTIN_RELATION_TYPES, builtin_doc_name, builtin_payload
from kgdb.models.relation_doc import RelationDoc
from kgdb.models.relation_type_doc import RelationTypeDoc

__all__ = [
    "BUILTIN_RELATION_TYPES",
    "RelationDoc",
    "RelationTypeDoc",
    "builtin_doc_name",
    "builtin_payload",
]
