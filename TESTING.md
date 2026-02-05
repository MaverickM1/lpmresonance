# Testing

The test suite uses `pytest` for Python unit tests and `latexmk` for TeX compilation tests.

## Setup

Install development dependencies:

```bash
pip install -e ".[dev]"
```

This installs:
- `pytest` - test framework
- `pytest-cov` - coverage reporting

## Running Tests

Run all Python tests:

```bash
pytest tests/python
```

Run with coverage:

```bash
pytest --cov=lpm_paths --cov-report=term-missing tests/python
```

Run specific test file:

```bash
pytest tests/python/test_cache.py
```

Run specific test:

```bash
pytest tests/python/test_cache.py::test_guard_path_rejects_escape
```

## Test Structure

- `tests/python/` - Python unit tests for the `lpm_paths` package
  - `test_cache.py` - Cache system and file operations
  - `test_api.py` - JSON API and PythonTeX integration
  - `test_between.py` - Between-path polygon computation
  - `test_geometry.py` - Lattice path geometry
  - `test_emitters_tex.py` - TeX macro generation
  - `test_hashing.py` - Content hashing and cache keys
  - `conftest.py` - Shared fixtures

- `tests/tex/` - TeX compilation tests (run via `latexmk`)

## Type Checking

The project uses Pylance/Pyright for type checking. Configuration is in `pyproject.toml`:

```toml
[tool.pyright]
pythonVersion = "3.9"
typeCheckingMode = "basic"
```

To run type checking manually:

```bash
pyright python tests
```
