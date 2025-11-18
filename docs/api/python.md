---
title: Python API
---

# Python API

These helpers live under `lpm_paths.api`. They are the functions the TeX layer
calls through PythonTeX, and they double as the public entry points if you need
to script against lattice paths directly from Python.

## `declare_path_from_json(spec_json: str) -> str`

Accepts a JSON document with keys:

- `bits` (`str`) — bit string made of `0` (East) and `1` (North) steps.
- `name` (`str`) — user-facing identifier (sanitized internally).
- `cache_id` (`str`, optional) — overrides the automatic cache-grouping key.

The function validates the payload, constructs a `TeXEmitter`, computes the
`LatticePath`, and writes both `.tex` (macros) and `.json` (manifest) files. It
returns TeX glue that defines `\lp@pathfile@<safe>` and related macros.

Example:

```python
import json
from lpm_paths import api

spec = {"bits": "01011010", "name": "demo"}
glue = api.declare_path_from_json(json.dumps(spec))
print(glue)
```

## `path_data(spec_json: str) -> Dict[str, Any]`

Takes a JSON document with a single `bits` key and returns:

- `coords`: list of `(x, y)` pairs describing the lattice path (length = steps + 1).
- `upmarks`: list of step indices where the path moved North.

Useful when you need the raw geometry without touching the TeX layer.

## `between_from_json(spec_json: str) -> str`

Payload keys:

- `L` / `U`: bit strings for the lower and upper paths (must share start/end).
- `lname` / `uname`: friendly names used for cache lookup (default `"L"` / `"U"`).

Returns TeX glue that points `\lp@lastdeclaredbetweenfile` at the generated
polygon file so `\shadeBetweenBits` can input it later.

## Supporting modules

- `lpm_paths.types.LatticePath` — immutable representation with coords, upmarks,
  corners, inside corners, and `ellmap`.
- `lpm_paths.emitters.tex.TeXEmitter` — generates hashed cache filenames and TeX
  macro bodies.
- `lpm_paths.cache.Cache` — ensures generated files stay under `lp-cache/`.
- `lpm_paths.errors` — `InputSpecError`, `InvariantError`, and `CacheFenceError`
  document the exception surface area.
