# ST-entry-points: kgdb CLI entry points

**Basado en:** UC-01

## Script

```bash
# 1. Verify kgdb is installed as a console script
which kgdb 2>&1
kgdb --help 2>&1 | head -3

# 2. Check the entry point script
head -5 $(which kgdb)

# 3. Try python -m kgdb (should exist if __main__.py present)
python3 -m kgdb 2>&1 || echo "python -m kgdb: NOT available"

# 4. Check if there's a __main__.py
ls -la src/kgdb/__main__.py 2>&1 || echo "No __main__.py"

# 5. Check setup.py / pyproject.toml for console_scripts entry point
python3 -c "
try:
    import tomllib
    with open('pyproject.toml', 'rb') as f:
        data = tomllib.load(f)
    scripts = data.get('project', {}).get('scripts', {}) or data.get('project', {}).get('entry-points', {}).get('console_scripts', {})
    print(f'Console scripts: {scripts}')
except:
    import configparser
    cp = configparser.ConfigParser()
    cp.read('setup.cfg')
    if cp.has_option('options.entry_points', 'console_scripts'):
        print(f'Console scripts: {cp.get(\"options.entry_points\", \"console_scripts\")}')
    else:
        print('Checking setup.py...')
        import subprocess
        r = subprocess.run(['python3', 'setup.py', '--entry-points'], capture_output=True, text=True)
        print(r.stdout or 'No entry points found in setup.py')
"

# 6. Compare kgdb behavior via installed script vs python -m
echo "--- Installed kgdb ---"
kgdb --help 2>&1
echo ""
echo "--- python -m kgdb ---"
python3 -m kgdb 2>&1 || true

# 7. Test using the kgdb module directly from Python
python3 -c "
import kgdb
print(f'kgdb version: {kgdb.__version__}')
print(f'kgdb file: {kgdb.__file__}')
print(f'kgdb dir: {dir(kgdb)}')
" 2>&1

# 8. Check if there are alternative entry points or aliases
python3 -c "
from kgdb.main import main
print(f'main function: {main}')
print(f'main module: {main.__module__}')
"

# 9. Verify that running kgdb and python3 -m kgdb.main produce same result
python3 -m kgdb.main 2>&1 || true

# 10. Check if kgdb can be invoked via symlink or pipe
echo "desk/fixtures/substrate_v1.json" | xargs -I{} kgdb list --graph {} 2>&1 | head -2
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿kgdb está en PATH? |
| 2 | ¿El script de entry point es simple o tiene lógica extra? |
| 3 | ¿python -m kgdb funciona? |
| 4 | ¿__main__.py existe? |
| 5 | ¿Cómo se define el entry point en pyproject.toml? |
| 6 | ¿kgdb y python -m kgdb se comportan igual? |
| 7 | ¿kgdb.__version__ existe? |
| 8 | ¿main function es invocable? |
| 9 | ¿python -m kgdb.main es equivalente? |
| 10 | ¿Piping de arguments funciona? |

## Modos de fracaso

- No hay `__main__.py` (`python -m kgdb` no funciona)
- `kgdb.__version__` no existe o no está actualizado
- Entry point script tiene wrapper con lógica extra inesperada
- Diferencia de comportamiento entre `kgdb` y `python -m kgdb`
- No hay entry point alternativo para desarrollo (ej: `python -m kgdb.main`)
