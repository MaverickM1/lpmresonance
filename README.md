## Requirements
- Python 3.9–3.13 (uses `from __future__ import annotations` for forward refs)
- TeX Live 2022+ with PythonTeX

> Roadmap note: When the minimum Python version becomes 3.14+, we will remove the future import and adopt `annotationlib` for any annotation introspection. See `docs/developer-guide/upgrade-notes.md`.

## Installation

```bash
pip install -e .
```

Editable installs keep the `lpm_paths` module in sync with your working tree while
you iterate on the package or compile the bundled examples. Pair this with either
a `TEXINPUTS` entry pointing at `tex/latex/lpmres` or copy the `.sty`/`.code.tex`
files into your personal TEXMF tree so `\usepackage{lpmresonance}` can find them.
Ensure `latexmk` (or your preferred driver) runs `pdflatex` with `-shell-escape`
and registers `pythontex` as a custom dependency, mirroring `examples/latexmkrc`.

## Quickstart

Compile the trimmed example below (it matches the walkthrough in
`docs/user-guide/quickstart.md`) from inside `examples/`:

```tex
\documentclass{article}
\usepackage{lpmresonance}
\begin{document}
\lpDeclarePath{demo}{01011010}
\begin{schubertpic}
  \drawGrid{demo}
  \drawLatticePath{demo}
\end{schubertpic}
\shadeBetweenBits{00110101}{01011001}{L}{U}
\begin{schubertpic}
  \shadeBetween[gray!20]{L}{U}
  \drawBetween{L}{U}
\end{schubertpic}
\end{document}
```

```bash
latexmk -pdf -shell-escape hello.tex
```

The first pass invokes PythonTeX, which writes `lp-cache/path-*.tex/json` (path
data) and `lp-cache/between-*.tex` (between regions). Re-running `latexmk`
reuses the cached coordinates until the bit strings or names change.

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

## Documentation

See `docs/user-guide/` for installation details, macro reference pages, shading
guides, and troubleshooting tips. Developer internals (cache format, manifest
schema, upgrade plans) live under `docs/developer-guide/`. The MkDocs config
(`mkdocs.yml`) builds the entire site when you need a rendered version.

## Release workflow

1. **Update docs and changelog.** Summarize user-facing changes in
   `docs/changelog.md` (and regenerate any screenshots/assets if needed).
2. **Run automated tests.**
   ```bash
   pytest tests/python
   ```
   Then compile a representative TeX document (for example `examples/example.tex`
   via `latexmk -pdf -shell-escape example.tex`) to confirm the PythonTeX bridge
   still works end-to-end.
3. **Clean caches and build artifacts.**
   ```bash
   ./scripts/clean-cache.sh
   ```
   Ensure `lp-cache/` and `pythontex-files-*` directories are gone before
   packaging.
4. **Tag and publish.** Bump the version, create a signed git tag, and push both
   the branch and the tag. Upload the distribution to PyPI/CTAN as appropriate,
   then create a GitHub release that references the changelog entry.
