# ST-persistence: PersistenceEntry and TransactionManifest

**Basado en:** UC-05

## Script

```bash
# 1. Verify the persistence module exists and models are importable
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry, TransactionManifest
print('PersistenceEntry fields:', list(PersistenceEntry.model_fields.keys()))
print('TransactionManifest fields:', list(TransactionManifest.model_fields.keys()))
" 2>&1

# 2. Create a PersistenceEntry manually
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry
import hashlib, json
entry = PersistenceEntry(
    action='create',
    node_id='test://node-1',
    entry_hash=hashlib.sha256(b'test').hexdigest()
)
print(f'Entry: {entry.action} {entry.node_id}')
print(f'Hash: {entry.entry_hash[:16]}...')
print(f'Timestamp: {entry.timestamp}')
"

# 3. Create a PersistenceEntry with a KnowledgeNode payload
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry
from kgdb.contracts.node import KnowledgeNode
from kgdb.contracts.base import SystemIdentity
import hashlib

node = KnowledgeNode(identity=SystemIdentity(node_id='test://node-1', node_type='test'))
entry = PersistenceEntry(
    action='update',
    node_id='test://node-1',
    payload=node,
    entry_hash=hashlib.sha256(b'test').hexdigest()
)
print(f'Entry with payload: {entry.payload.identity.node_id}')
"

# 4. Create a TransactionManifest
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry, TransactionManifest
from kgdb.contracts.node import KnowledgeNode
from kgdb.contracts.base import SystemIdentity
import hashlib

entries = [
    PersistenceEntry(action='create', node_id='test://a', entry_hash=hashlib.sha256(b'a').hexdigest()),
    PersistenceEntry(action='create', node_id='test://b', entry_hash=hashlib.sha256(b'b').hexdigest()),
]
manifest = TransactionManifest(
    transaction_id='tx-001',
    entries=entries,
    hash_chain=hashlib.sha256(b'tx-001').hexdigest()
)
print(f'Manifest: {manifest.transaction_id}')
print(f'Entries: {len(manifest.entries)}')
print(f'Hash chain: {manifest.hash_chain[:16]}...')
print(f'Previous hash: {manifest.previous_hash}')
"

# 5. TransactionManifest with previous_hash (chain)
python3 -c "
from kgdb.contracts.persistence import TransactionManifest
import hashlib

manifest2 = TransactionManifest(
    transaction_id='tx-002',
    previous_hash=hashlib.sha256(b'tx-001').hexdigest(),
    hash_chain=hashlib.sha256(b'tx-001tx-002').hexdigest(),
    metadata={'author': 'test', 'reason': 'integration test'}
)
print(f'Chained manifest: {manifest2.transaction_id}')
print(f'Previous: {manifest2.previous_hash[:16]}...')
print(f'Metadata: {manifest2.metadata}')
"

# 6. Serialize/deserialize roundtrip
python3 -c "
from kgdb.contracts.persistence import TransactionManifest, PersistenceEntry
from kgdb.contracts.node import KnowledgeNode
from kgdb.contracts.base import SystemIdentity
import hashlib, json

node = KnowledgeNode(identity=SystemIdentity(node_id='test://roundtrip', node_type='test'))
entry = PersistenceEntry(action='create', node_id='test://roundtrip', payload=node, entry_hash=hashlib.sha256(b'r').hexdigest())
manifest = TransactionManifest(
    transaction_id='tx-roundtrip',
    entries=[entry],
    hash_chain=hashlib.sha256(b'r').hexdigest()
)

raw = manifest.model_dump(mode='json')
print(f'JSON: {json.dumps(raw)[:200]}')

reloaded = TransactionManifest.model_validate(raw)
print(f'Roundtrip OK: {reloaded.transaction_id}, {len(reloaded.entries)} entries')
"

# 7. Empty entries list
python3 -c "
from kgdb.contracts.persistence import TransactionManifest
import hashlib
manifest = TransactionManifest(
    transaction_id='tx-empty',
    hash_chain=hashlib.sha256(b'e').hexdigest()
)
print(f'Empty manifest: {manifest.transaction_id}, entries={len(manifest.entries)}')
"

# 8. Invalid action value (should fail validation)
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry
try:
    entry = PersistenceEntry(action='invalid_action', node_id='test://x', entry_hash='x')
    print('Invalid action accepted (unexpected)')
except Exception as e:
    print(f'Validation error: {type(e).__name__}: {e}')
"

# 9. Entry hash mismatch — is it validated?
python3 -c "
from kgdb.contracts.persistence import PersistenceEntry
entry = PersistenceEntry(action='create', node_id='test://x', entry_hash='not-a-real-hash')
print(f'Hash: {entry.entry_hash}')
print('Entry created with arbitrary hash (no validation at construction)')
"

# 10. TransactionManifest as dict (for possible CLI use)
python3 -c "
from kgdb.contracts.persistence import TransactionManifest
import hashlib
m = TransactionManifest(
    transaction_id='tx-dict-test',
    hash_chain=hashlib.sha256(b'd').hexdigest()
)
d = m.model_dump()
print(f'Dict keys: {list(d.keys())}')
print(f'Can be JSON-serialized: OK')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Los modelos se importan sin error? |
| 2 | ¿PersistenceEntry se puede crear con campos mínimos? |
| 3 | ¿KnowledgeNode como payload funciona? |
| 4 | ¿TransactionManifest funciona con múltiples entries? |
| 5 | ¿Chaining con previous_hash funciona? |
| 6 | ¿Roundtrip JSON serialization mantiene integridad? |
| 7 | ¿Empty entries list permitida? |
| 8 | ¿Validación de action (solo create/update/delete)? |
| 9 | ¿entry_hash no validado contra contenido? |
| 10 | ¿Se puede serializar a dict/JSON? |

## Modos de fracaso

- Persistence models no conectados a ningún comando CLI
- entry_hash no se valida contra contenido (solo string field)
- No hay manera de firmar/verificar hashes
- No hay CLI command para crear/persistir transacciones
- previous_hash no se verifica al cargar (solo metadata)
- No hay CLI para persistence (dead code)
