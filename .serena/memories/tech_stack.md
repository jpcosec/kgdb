# Tech Stack

- Python package using `src/` layout with setuptools backend (`pyproject.toml`).
- Requires Python `>=3.10`.
- Runtime deps: `pydantic>=2.0.0`, `networkx>=3.0`.
- Console script: `kgdb = kgdb.main:main`.
- Pytest config in `pyproject.toml`: `pythonpath = ["src"]`, `testpaths = ["tests"]`; plain `pytest` from repo root is expected to work.