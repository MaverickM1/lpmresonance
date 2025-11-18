# Upgrade Notes

## PEP 649/749 transition: annotations and `annotationlib` (Python ≥ 3.14)

**Status for this repo:** We keep `from __future__ import annotations` across all modules for compatibility with Python ≤ 3.13. No runtime depends on evaluated annotations.

### What changes upstream
- Python 3.14+ adopts deferred evaluation by default (PEP 649 semantics).  
- `from __future__ import annotations` (PEP 563) is supported through Python 3.13; post-3.13 it enters deprecation and removal.  
- New stdlib: `annotationlib` for reading annotations (formats: `STRING`, `FORWARDREF`, `VALUE`, `VALUE_WITH_FAKE_GLOBALS`).  
- REPL and partially-executed modules follow lazy execution rules; deleting `__annotations__` also clears `__annotate__`.

### Our policy
- **Current target:** Python 3.9–3.13 inclusive. Keep the future import in all modules that declare annotations.
- **Future target:** When we drop ≤3.13, remove the future import and migrate any annotation readers to `annotationlib`.

### Action checklist when moving to Python ≥ 3.14 only
1. **Delete** `from __future__ import annotations` in all modules.
2. **Dequote** forward refs (no strings needed under 3.14+):
   ```python
   # before
   from __future__ import annotations
   def f(x: "LatticePath") -> "LatticePath | None": ...
   # after
   def f(x: LatticePath) -> LatticePath | None: ...
