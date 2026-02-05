---
title: API Stability Contract
---

# API Stability Contract

This document defines which macros and Python APIs are **stable** (guaranteed backwards compatibility) versus **experimental** (may change without notice).

## Version Policy

lpmresonance follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Breaking changes to stable APIs
- **MINOR** version: New features, experimental API changes, non-breaking enhancements
- **PATCH** version: Bug fixes, documentation updates

**Current version**: 0.0.1 (pre-release)

> **Note**: During the 0.x series, minor version bumps may include breaking changes. Stability guarantees apply starting from version 1.0.0.

## Stable TeX Macros

These macros will maintain backwards compatibility across minor versions (once 1.0.0 is released):

### Path Declaration

| Macro | Since | Status |
|-------|-------|--------|
| `\lpDeclarePath{<name>}{<bits>}` | 0.0.1 | **Stable** |
| `\shadeBetweenBits{<L>}{<U>}{<lname>}{<uname>}` | 0.0.1 | **Stable** |

### Drawing Commands

| Macro | Since | Status |
|-------|-------|--------|
| `\drawLatticePath[<opts>]{<name>}` | 0.0.1 | **Stable** |
| `\drawGrid[<opts>]{<name>}` | 0.0.1 | **Stable** |
| `\shadeBetween[<opts>]{<lname>}{<uname>}` | 0.0.1 | **Stable** |
| `\drawBetween[<opts>]{<lname>}{<uname>}` | 0.0.1 | **Stable** |

### Feature Options

| Option Key | Since | Status |
|------------|-------|--------|
| `lplpath/label upmarks` | 0.0.1 | **Stable** |
| `lplpath/show inside corners` | 0.0.1 | **Stable** |
| `lplpath/show endpoints` | 0.0.1 | **Stable** |

### Environments

| Environment | Since | Status |
|-------------|-------|--------|
| `schubertpic` | 0.0.1 | **Stable** |

## Stable Python APIs

These Python functions and classes maintain backwards compatibility:

### Core Types

```python
from lpm_paths.types import LatticePath, Coordinate
```

| Class/Function | Since | Status |
|----------------|-------|--------|
| `LatticePath.from_bits(bits: str)` | 0.0.1 | **Stable** |
| `LatticePath.coords` property | 0.0.1 | **Stable** |
| `LatticePath.bits` property | 0.0.1 | **Stable** |

### Cache Management

```python
from lpm_paths.cache import resolve_cache_path, cleanup_cache
```

| Function | Since | Status |
|----------|-------|--------|
| `resolve_cache_path(...)` | 0.0.1 | **Stable** |
| `cleanup_cache(directory)` | 0.0.1 | **Stable** |

### API Entry Points

```python
from lpm_paths.api import declare_path_from_json, between_from_json
```

| Function | Since | Status |
|----------|-------|--------|
| `declare_path_from_json(json_str)` | 0.0.1 | **Stable** |
| `between_from_json(json_str)` | 0.0.1 | **Stable** |

## Experimental Features

These features may change in minor versions without a major version bump:

### TeX Macros

| Macro | Since | Status | Notes |
|-------|-------|--------|-------|
| `\highlightInsideCorner[<opts>]{<name>}{<idx>}` | 0.0.1 | **Experimental** | API may change for multi-corner selection |

### Python APIs

| API | Since | Status | Notes |
|-----|-------|--------|-------|
| `lpm_paths.emitters.TeXEmitter` internals | 0.0.1 | **Experimental** | Emitter implementation details not guaranteed |

### CLI Tools

| Command | Since | Status | Notes |
|---------|-------|--------|-------|
| `lpmresonance-doctor` | 0.0.1 | **Experimental** | Output format may change |

## Cache File Format

The cache file format (SHA256-based naming, `.tex` and `.json` files) is **stable**. Changes to the format will trigger a major version bump and migration tools will be provided.

## Deprecation Policy

When deprecating a stable API:

1. **Deprecation warning** added in MINOR version
2. **Deprecation period** of at least 2 MINOR versions
3. **Removal** only in MAJOR version

Example:
- Version 1.2.0: Feature X deprecated, warning added
- Version 1.3.0: Warning continues
- Version 1.4.0: Warning continues
- Version 2.0.0: Feature X removed

## Migration Guides

Migration guides for breaking changes will be provided in:
- `CHANGELOG.md` - Summary of breaking changes
- `docs/developer-guide/upgrade-notes.md` - Detailed migration instructions

## Reporting API Issues

If you encounter unexpected API changes or have questions about stability:

1. Check `CHANGELOG.md` for documented changes
2. Open an issue on [GitHub](https://github.com/MaverickM1/lpmresonance/issues)
3. Reference this stability contract in your report

## Future Stable APIs (Planned)

These features are planned for stabilization in future versions:

### Version 1.0.0 Candidates

- `\lpDeclareSchubert{<name>}{<permutation>}` - Schubert variety paths
- `\drawSchubert[<opts>]{<name>}` - Schubert path rendering
- Multi-corner highlighting syntax
- Path transformation macros (rotation, reflection)

### Version 1.1.0+ Candidates

- Path algebra operations (concatenation, reversal)
- Custom coordinate systems
- Export to other formats (SVG, TikZ standalone)
- Advanced caching strategies

## Version History

| Version | Release Date | Stability Status |
|---------|--------------|------------------|
| 0.0.1 | TBD | Pre-release, all APIs experimental |
| 1.0.0 | TBD | First stable release |

---

**Last updated**: January 21, 2026  
**Applies to**: lpmresonance 0.0.1
