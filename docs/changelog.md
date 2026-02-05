---
title: Changelog
---

# Changelog

## Unreleased

### New Features
- Added `lplpath/show step marks` option to place visual markers (dots) at each lattice point along a path, improving step counting when grids are not displayed.
- Added `lplpath/step mark style` option to customize the appearance of step mark dots (color, fill, size).
- Added `lplpath/upmark label style` option to customize the appearance of upmark number labels (font size, scale, color, anchor).
- Updated `lpm_paths.emitters.tex` to generate step mark coordinates and emit TikZ style-based rendering commands.

### Installation & Infrastructure
- Created `scripts/install-from-github.sh` for one-line remote installation from GitHub.
- Adopted standard PythonTeX 3-command workflow as primary compilation method.
- Installer automatically configures global `~/.latexmkrc` with PythonTeX rule.
- Installer handles macOS `python3` vs `python` shebang issue via `--interpreter` flag.

### Code Quality
- Added comprehensive NumPy-style docstrings to all 10 Python modules.
- Applied PEP 8 naming conventions: `guardPath` → `guard_path`, `_sanitize_name` → `sanitize_name`.
- Removed `geometry.py` module (functionality moved to `LatticePath.from_bits`).
- Added type annotations throughout test suite (6 test files).
- Enhanced `doctor.py` with colored output, better error handling, `--no-color` flag support.

### Testing & Development
- Added `[project.optional-dependencies]` with `dev = ["pytest>=7.0", "pytest-cov>=4.0"]`.
- Created `pyrightconfig.json` for Pylance/Pyright type checking configuration.
- Created `TESTING.md` with setup instructions, test commands, and structure documentation.
- All 14 Python tests passing with full type annotation coverage.

### Documentation
- Added installation, quickstart, macro reference, shading, options, and troubleshooting guides under `docs/user-guide/`.
- Expanded README with install instructions, quickstart checklist, and latexmkrc requirements.
- Documented release workflow for contributors (tests + cache cleanup + tagging).
- Updated `mkdocs.yml` navigation to expose the full documentation set.
- Improved `lpm_paths.emitters.tex` to emit grid size metadata, upmark labels, and inside-corner helpers for TikZ.

### Package Metadata
- Cleaned up `MANIFEST.in` with explicit includes/excludes, removing wildcards.

## 0.0.1 – 2026-02-04

- Initial public preview of the PythonTeX-backed lattice-path package.
- Introduced `\lpDeclarePath`, `\shadeBetweenBits`, `\drawLatticePath`, and the base grid helpers.
- Shipped `lpmresonance.sty` with `pythontex` integration and cache management.
