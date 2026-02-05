---
title: Architecture
---

# Architecture

`lpmresonance` has two halves that cooperate through PythonTeX:

1. **Python backend (`python/lpm_paths/`)** — parses bit strings, computes lattice
   path metadata, and writes cache artifacts to disk.
2. **TeX frontend (`tex/latex/lpmres/`)** — loads the cached data and renders it
   with TikZ.

The interaction model is a two-pass LaTeX build:

1. `pdflatex` encounters `\lpDeclarePath` / `\shadeBetweenBits`. PythonTeX stores
   the embedded Python code into `.pytxcode`.
2. `pythontex` executes those snippets, which call into `lpm_paths.api` to
   generate cache files under `lp-cache/`.
3. A subsequent `pdflatex` run inputs the generated `.tex` files via
   `\lp@inputifready` and draws the paths.

## Python modules

- `lpm_paths.types` — represents a lattice path (`LatticePath.from_bits`).
- `lpm_paths.emitters.tex` — owns the cache layout, hashing, and TeX macro
  generation for both paths and between regions.
- `lpm_paths.cache` — fences writes to `lp-cache/` and provides helper methods
  for computing TeX-friendly paths (`tex_path`).
- `lpm_paths.api` — user-facing JSON helpers invoked from TeX.
- `lpm_paths.between` — constructs polygons between two lattice paths.

## Cache layout

All generated artifacts live below `lp-cache/`:

- `path-<safe>-<hash>.tex` — TeX macros holding coordinates, upmarks, inside
  corners, and grid sizes.
- `path-<safe>-<hash>.json` — manifest used by tools/tests.
- `between-<lname>-<uname>-<hash>.tex` — polygon coordinate macros.
- `.names/` — metadata used to detect sanitized-name collisions.

The file names are content-addressed via `hashing.key_of(payload)`, so any change
to the inputs produces a fresh cache file.

## TeX packages

`lpmresonance.sty` loads several `.code.tex` modules:

- `lpmres-base.code.tex` — warnings, `\lp@inputifready`, and default TikZ styles.
- `lpmres-python.code.tex` — bridges TeX ↔ Python via PythonTeX.
- `lpmres-lpath.code.tex` — drawing helpers, upmark and inside-corner support.
- `lpmres-between.code.tex` — shading/drawing for between regions.
- `lpmres-grid.code.tex` — grid helper that consumes cached sizes.
- `lpmres-pic.code.tex` — `schubertpic` environment for consistent diagrams.

Each module confines its state to TeX macros so everything survives the usual
LaTeX reruns without re-executing Python unless inputs change.
