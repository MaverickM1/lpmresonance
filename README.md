## Requirements
- Python 3.9–3.13 (uses `from __future__ import annotations` for forward refs)
- TeX Live 2022+ with PythonTeX

> Roadmap note: When the minimum Python version becomes 3.14+, we will remove the future import and adopt `annotationlib` for any annotation introspection. See `docs/developer-guide/upgrade-notes.md`.

## Cache Management

The package uses a `lp-cache/` directory to store pre-computed path coordinates and between-region polygons. These cache files are automatically created during compilation and persist across builds to improve performance.

### Automatic Cache Behavior
- **Created**: When `\lpDeclarePath` or `\shadeBetweenBits` is called
- **Named**: By SHA256 hash of input (e.g., `path-0011-abc123.tex`)
- **Reused**: Automatically on subsequent compilations
- **Updated**: Only when input changes (new hash = new file)

### Manual Cache Cleanup

**Clean all build artifacts** (recommended):
```bash
./scripts/clean-cache.sh
```

**Selective cleanup**:
```bash
# Remove all cache files
rm -rf examples/lp-cache/

# Remove cache for specific path
rm -rf examples/lp-cache/path-MyPath*

# Remove all between-region cache
rm -rf examples/lp-cache/between-*
```

**When to clean cache:**
- After modifying the Python backend code
- Before creating a clean distribution
- When debugging suspected cache corruption
- To reclaim disk space

> **Note**: Deleting cache files is safe. They will be regenerated on the next compilation (adds one extra LaTeX pass).