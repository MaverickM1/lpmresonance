# LPM Resonance Examples

This directory contains example LaTeX documents demonstrating the `lpmresonance` package.

## Quick Start

If you ran the installer script, you can compile with latexmk directly:

```bash
latexmk -pdf -shell-escape example-gallery.tex
```

To compile any example manually:

```bash
# Set up environment
export PATH="$HOME/.local/bin:$PATH"

# Compile an example (3-step process)
TEXINPUTS=../tex/latex/lpmres: pdflatex example-gallery.tex
python /usr/local/texlive/2022/texmf-dist/scripts/pythontex/pythontex.py example-gallery.tex
TEXINPUTS=../tex/latex/lpmres: pdflatex example-gallery.tex
```

## Available Examples

### `example-gallery.tex`

Shows all package features:
- Generic lattice paths from bit strings and coordinates
- Styled paths with TikZ options
- Multiple paths on one diagram
- Between-path region shading
- Inside corners
- Python computation integration

### Other Examples
- `example-complete.tex` - Previous version (uses old API)
- `example-minimal.tex` - Minimal example
- `example-simple-test.tex` - Simple test
- `example-direct-test.tex` - Direct API test

## Compilation Notes

### Required Tools
1. **pdflatex** - TeX Live 2022 or later
2. **pythontex** - Comes with TeX Live
3. **Python 3** - With `lpm_paths` package installed (ensure `python` resolves to Python 3.9+)

### Important Setup Steps

1. **Install Python package** (from repo root):
   ```bash
   pip install -e .
   ```

2. **Create python symlink** (only if your system provides `python3` but not `python`):
   ```bash
   mkdir -p ~/.local/bin
   ln -sf /usr/local/bin/python3 ~/.local/bin/python
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Set TEXINPUTS** (so LaTeX finds the package files):
   ```bash
   export TEXINPUTS=../tex/latex/lpmres:
   ```

### Compilation Workflow

The compilation requires:

1. **First pdflatex run**: Extracts Python code blocks, creates placeholders
2. **pythontex run**: Executes Python code, generates coordinate data
3. **Second pdflatex run**: Incorporates generated data, renders final graphics

### Caching

- Coordinate data is cached in `lp-cache/` directory
- Cache files are named by content hash
- After first run, unchanged paths load instantly
- Changing a permutation triggers automatic recomputation

### Troubleshooting

**"No such file or directory: 'python'"**
- Use `python3` if available, or create the symlink: `ln -sf /usr/local/bin/python3 ~/.local/bin/python`
- Add to PATH: `export PATH="$HOME/.local/bin:$PATH"`

**"File `lpmresonance.sty' not found"**
- Set TEXINPUTS: `TEXINPUTS=../tex/latex/lpmres: pdflatex ...`

**"Coordinates not ready" warnings**
- Run pythontex between pdflatex passes
- Check `pythontex-files-*/` for error messages

**Python import errors**
- Install package: `pip install -e .` from repo root
- Verify: `python -c "import lpm_paths; print('OK')"`

## Package API Quick Reference

### Declare and Draw Schubert Paths

```latex
\pyc{lpDeclareSchubert('name', [permutation])}
\drawSchubert[tikz options]{name}
```

Example:
```latex
\pyc{lpDeclareSchubert('S', [3, 1, 4, 2])}
\drawSchubert[red, thick]{S}
```

### Declare and Draw Generic Lattice Paths

From bit string:
```latex
\pyc{lpDeclarePath('name', 'bitstring')}
\drawLatticePath[tikz options]{name}
```

From coordinates:
```latex
\pyc{lpDeclarePath('name', [(x1,y1), (x2,y2), ...])}
\drawLatticePath[tikz options]{name}
```

### Between-Path Regions

```latex
\pyc{lpDeclareSchubert('lower', [perm1])}
\pyc{lpDeclareSchubert('upper', [perm2])}
\pyc{lpDeclareBetweenBits('lower', 'upper')}

% Shade the region
\shadeBetween[fill=yellow!30]{lower}{upper}

% Or draw the boundary
\drawBetween[thick, dashed]{lower}{upper}
```

## Output Files

After compilation you'll see:

- `example-gallery.pdf` - The final output
- `example-gallery.aux`, `.log` - Standard LaTeX files
- `example-gallery.pytxcode` - Extracted Python code
- `pythontex-files-example-gallery/` - PythonTeX working directory
  - `*.py` - Generated Python scripts
  - `*.stdout` - Python output (TeX macros)
- `lp-cache/` - Cached coordinate data
  - `schubert-*.tex` - Coordinate macros for Schubert paths
  - `lpath-*.tex` - Coordinate macros for generic paths
  - `between-*.tex` - Between-region data
---
