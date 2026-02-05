---
title: Cache internals
---

# Cache internals

All generated artifacts are written under the cache root managed by
`lpm_paths.cache.Cache` (defaults to `lp-cache/` in the working directory). This
document outlines the responsibilities and invariants around those files.

## Directory layout

```
lp-cache/
├── path-<safe>-<hash>.tex
├── path-<safe>-<hash>.json
├── between-<lname>-<uname>-<hash>.tex
└── .names/
    └── path/<safe>.json
```

- `<safe>` is the sanitized TeX identifier derived from the user-facing name.
- `<hash>` is `hashing.key_of(payload)` where `payload` includes the op, bits,
  names, version, and optional cache ID.
- `.names` stores metadata describing the original (unsanitized) name so we can
  warn when two declarations collide after sanitization.

## Cache guard

`Cache.guard_path(path)` ensures every generated file remains inside the cache
root. It resolves both the root and the target, compares `os.path.commonpath`,
and raises `CacheFenceError` if the file would escape. Always go through
`Cache.file(filename)` or `Cache.tex_path(path)` rather than joining paths
yourself.

## Atomic writes

`cache.atomic_write` writes data to `<file>.tmp` and renames it once the write
completes. This prevents partial files when LaTeX/PythonTeX is interrupted.

## TeX path resolution

`Cache.tex_path(path)` returns a TeX-friendly path that tries to be relative to
`os.getcwd()` when possible. That keeps `\input` statements short and ensures
the cache is portable across machines so long as the relative layout is the
same.

## Cleaning the cache

Use `./scripts/clean-cache.sh` to delete `lp-cache/`, PythonTeX temporaries, and
other derived artifacts. Manual deletion is fine too—cache entries are
recomputed automatically on the next run.

## Backwards compatibility

Never mutate cache files in place. Instead, bump `EMITTER_VERSION` (see
`python/lpm_paths/version.py`) and include the new format fields in the hashed
payload. This guarantees old files remain readable while new builds pick up the
latest schema.
