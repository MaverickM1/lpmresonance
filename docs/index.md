---
title: Home
---

# lpmresonance

**LaTeX package for drawing lattice paths with a PythonTeX backend.**

`lpmresonance` couples TikZ drawing with Python computation to generate annotated lattice paths and between-region shadings from binary strings. The package handles coordinate generation, caching, and rendering automatically.

---

## Features

- **Bit string notation** — Declare paths with `0` (East) and `1` (North) steps
- **Automatic coordinates** — Python backend computes geometry
- **TikZ rendering** — Customizable styles with full TikZ integration
- **Step marks** — Visual markers at lattice points for easy step counting without grids
- **Upmark labels** — Automatic coordinate labels on North steps with customizable styling
- **Inside corner detection** — Highlight East→North transitions
- **Between-region shading** — Fill polygons between two paths
- **Smart caching** — SHA256-based cache for fast recompilation
- **PythonTeX integration** — Direct TeX↔Python workflow

---

## Quick Example

```tex
\documentclass{article}
\usepackage{lpmresonance}
\begin{document}

\lpDeclarePath{demo}{01011010}
\begin{schubertpic}
  \drawGrid{demo}
  \drawLatticePath[lplpath/label upmarks, lplpath/show step marks]{demo}
\end{schubertpic}

\end{document}
```

Compile with `latexmk -pdf -shell-escape` and the package generates cached coordinates automatically.

---

## Quick Links

### Getting Started
- [Installation Guide](user-guide/installation.md) — Python and LaTeX setup
- [Quickstart Tutorial](user-guide/quickstart.md) — Minimal working example
- [Troubleshooting](user-guide/troubleshooting.md) — Common issues and fixes

### Reference
- [TeX Macro Reference](api/tex-macro-reference.md) — Complete command documentation
- [Python API](api/python.md) — Backend functions and types
- [Lattice Path Macros](user-guide/lattice-path-macros.md) — Path declaration and drawing
- [Shading Between Paths](user-guide/shading-between-paths.md) — Between-region polygons
- [Options and Keys](user-guide/options-and-keys.md) — TikZ styles and customization

### Development
- [Architecture](developer-guide/architecture.md) — System design and workflow
- [Contributing Guide](developer-guide/contributing.md) — How to contribute
- [Changelog](changelog.md) — Version history
- [FAQ](faq.md) — Frequently asked questions

---

## Requirements

- Python 3.9–3.13
- TeX Live 2022+ with PythonTeX
- LaTeX compilation with `-shell-escape`

---

## Installation

```bash
# macOS / Linux
./scripts/install.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-windows.ps1
```

Manual wiring (deprecated):

```bash
pip install -e .
```

See the [Installation Guide](user-guide/installation.md) for complete setup
instructions including `TEXINPUTS` configuration and latexmk setup.

---

## What's New

### Recent Updates
- **Upmark labels** with `:g` formatting (removes trailing zeros)
- **Inside corner highlighting** for East→North transitions
- **Between-region shading** with automatic polygon generation
- **Complete documentation** with user and developer guides
- **CI/CD pipeline** with GitHub Actions
- **Academic citation** support with CITATION.cff

### Upgrade Notes

See [Developer Guide → Upgrade Notes](developer-guide/upgrade-notes.md) for the PEP 649/749 transition plan when targeting Python ≥ 3.14.

---

## License

MIT License — Copyright (c) 2025 Prajwal Dhondiram Udanshive

## Citation

If you use lpmresonance in academic work, please cite using the [CITATION.cff](https://github.com/MaverickM1/lpmresonance/blob/main/CITATION.cff) file in the repository.
