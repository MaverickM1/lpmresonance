---
title: Emitter contracts
---

# Emitter contracts

`lpm_paths.emitters.tex.TeXEmitter` is responsible for turning lattice-path data
into TeX macros and JSON manifests. This document spells out the expected
outputs and invariants so other emitters (or future refactors) can conform.

## `write_path(bits, name, cache_id=None)`

### Inputs

- `bits`: string of `0`/`1`.
- `name`: original identifier (not sanitized).
- `cache_id`: optional string to separate cache namespaces (defaults to empty).

### Outputs

Returns a tuple `(g1, g2, g3)` of TeX glue strings:

1. `g1`: defines `\lp@pathfile@<safe>` and includes any sanitized-name warnings.
2. `g2`: defines `\lp@pathjson@<safe>`.
3. `g3`: sets `\lp@lastdeclaredpathfile`.

### Side effects

- Writes `lp-cache/path-<safe>-<hash>.tex` with macros:
  - `\lp@path@coords@<safe>` — formatted coordinate list.
  - `\lp@path@upmarks@<safe>` and `\lp@path@upmarklabels@<safe>` (when upmarks exist).
  - `\lp@path@insidecorners@<safe>`, `\lp@path@insidecornerlabels@<safe>`,
    `\lp@path@insidecornercoord@<safe>@<i>`.
  - `\lp@path@gridsize@<safe>` — `(num_zeros,num_ones)`.
  - `\lp@path@ready@<safe>` — flag set to `1`.
- Writes `lp-cache/path-<safe>-<hash>.json` via `manifest.to_json_obj`.
- Updates `.names/path/<safe>.json` with the original name and emits a
  `\PackageWarning` when the sanitized name collides with a different original.

### Failure modes

- Raises `InputSpecError` if `bits` contains characters other than `0`/`1`.
- Raises `InvariantError` if the computed coordinates do not match the implied
  bounding box.
- Raises `CacheFenceError` if the cache root is misconfigured.

## `write_between(L_bits, U_bits, lname, uname)`

### Inputs

- `L_bits`, `U_bits`: bit strings for lower/upper paths (must share endpoints).
- `lname`, `uname`: identifiers used to build cache filenames and TeX macros.

### Outputs

Returns TeX glue defining `\lp@lastdeclaredbetweenfile`.

### Side effects

- Writes `lp-cache/between-<Ls>-<Us>-<hash>.tex` containing:
  - `\lp@between@coords@<Ls>@<Us>` — formatted polygon.
  - `\lp@between@coords` — legacy alias for the most recent polygon.
  - `\lp@between@ready@<Ls>@<Us>` — readiness flag set to `1`.

### Failure modes

- Raises `InputSpecError` if the two paths do not share both start and end
  coordinates.

## Versioning

`EMITTER_VERSION` (in `python/lpm_paths/version.py`) must be bumped whenever the
output format changes. Include the version in the hashed payload so new files
are distinct from old ones.
