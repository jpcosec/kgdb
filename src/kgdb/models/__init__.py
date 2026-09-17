"""The relation models moved to sldb (fusion of kgdb into sldb): `sldb.models.relation_doc`,
`sldb.models.relation_type_doc`, `sldb.models.builtin_relation_types`. Re-exported here so a
store that registered them as `kgdb.models:RelationDoc` / `kgdb.models:RelationTypeDoc` still
imports them; `sldb.api.init_relations` re-points such a store to the sldb references."""

from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_doc_name, builtin_payload
from sldb.models.relation_doc import RelationDoc
from sldb.models.relation_type_doc import RelationTypeDoc

__all__ = [
    "BUILTIN_RELATION_TYPES",
    "RelationDoc",
    "RelationTypeDoc",
    "builtin_doc_name",
    "builtin_payload",
]
