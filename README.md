# lpmresonance

[![Test](https://github.com/MaverickM1/lpmresonance/actions/workflows/test.yml/badge.svg)](https://github.com/MaverickM1/lpmresonance/actions/workflows/test.yml)
![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This is a package to draw lattice path diagrams using bitstrings.

![Lattice path example](https://maverickm1.github.io/lpmresonance/assets/basic-example.jpg)

**What it does:** The TeX side provides macros and drawing environments; the Python side generates coordinates and polygon data, caching them as `.tex` files that LaTeX includes on subsequent passes.

## Requirements
- Python 3.9–3.13 (uses `from __future__ import annotations` for forward refs)
- TeX Live 2022+ with PythonTeX

> Roadmap note: When the minimum Python version becomes 3.14+, we will remove the future import and adopt `annotationlib` for any annotation introspection. See `docs/developer-guide/upgrade-notes.md`.

## Installation

TeX Live 2022+ and Python 3.9+ must be installed first.

### One-line Install

```bash
curl -fsSL https://raw.githubusercontent.com/MaverickM1/lpmresonance/main/scripts/install-from-github.sh | bash
```

Or download and run:

```bash
curl -fsSL https://raw.githubusercontent.com/MaverickM1/lpmresonance/main/scripts/install-from-github.sh -o install-lpm.sh
bash install-lpm.sh
```

To install a specific version or branch:

```bash
bash install-lpm.sh v0.0.1  # tagged release
bash install-lpm.sh dev     # development branch
```

The installer:
- Downloads the package from GitHub
- Installs the Python package (`lpm_paths`)
- Copies TeX files to your `TEXMFHOME` directory
- Configures `~/.latexmkrc` with the PythonTeX rule
- Verifies the installation with a test compilation
- Removes temporary files on completion

> **Security Note**: This package uses PythonTeX to execute Python code during LaTeX compilation. The `-shell-escape` flag is required, which allows LaTeX to run external programs. Only compile documents from trusted sources.

## Compilation

This is a PythonTeX package. Compile with the standard 3-step workflow:

```bash
pdflatex -shell-escape demo.tex
pythontex demo
pdflatex -shell-escape demo.tex
```

**What happens:**
1. First `pdflatex` extracts Python code into `demo.pytxcode`
2. `pythontex` executes the Python, writes results to `lp-cache/`
3. Second `pdflatex` reads the cached data and renders the diagrams

### Automated Builds with latexmk (Optional)

For automated compilation, add the PythonTeX rule to your `~/.latexmkrc`:

```perl
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex { return system("pythontex", $_[0]); }
```

Then compile with:

```bash
latexmk -pdf -shell-escape demo.tex
```

The installer configures this automatically. For manual setup or customization, see [latexmk Setup](docs/user-guide/installation.md#latexmk-setup).

### Verify Installation

After installation, run the diagnostic tool to verify everything is working:

```bash
lpmresonance-doctor
```

This checks that PythonTeX, latexmk, and the package are correctly installed.

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

Compile:

```bash
pdflatex -shell-escape hello.tex
pythontex hello
pdflatex -shell-escape hello.tex
```

The cached files persist across compilations—changing a bit string triggers regeneration automatically.

> **Note**: `-shell-escape` is required for PythonTeX execution. See the security note in the Installation section.

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

### Troubleshooting Cache Issues

**Problem: Coordinates not updating after code changes**
```bash
# Force regeneration by cleaning cache
rm -rf lp-cache/
latexmk -pdf -shell-escape yourfile.tex
```

**Problem: "Cache file not found" errors**
- Ensure PythonTeX ran successfully (check for `pythontex-files-*/` directory)
- Verify Python package is installed: `python -c "import lpm_paths; print('OK')"`
- Check `latexmkrc` is present (handles automatic PythonTeX execution)

**Problem: Build fails with "shell-escape disabled"**
```bash
# Must use -shell-escape flag
latexmk -pdf -shell-escape yourfile.tex
```

**Custom cache location** (for build systems):
The cache directory defaults to `lp-cache/` relative to your `.tex` file. To override, set the working directory or adjust `latexmkrc` configuration.

## Advanced Installation (Manual)

For developers or custom setups, you can install manually:

```bash
pip install -e .
```

Then configure TeX to find the package files:
- **Option 1**: Copy `tex/latex/lpmres/*` to your `TEXMFHOME/tex/latex/lpmres/` directory
- **Option 2**: Set `TEXINPUTS` environment variable to include `tex/latex/lpmres`

For automated builds with latexmk, add the PythonTeX rule to `~/.latexmkrc`:

```perl
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex { return system("pythontex", $_[0]); }
```

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
