---
title: Changelog
---

# Changelog

## Unreleased

- Added installation, quickstart, macro reference, shading, options, and troubleshooting guides under `docs/user-guide/`.
- Expanded the README with install instructions, a quickstart example, and the release workflow.
- Documented the release workflow for contributors (tests + cache cleanup + tagging).
- Updated `mkdocs.yml` navigation to expose the full documentation set.
- Improved `lpm_paths.emitters.tex` to emit grid size metadata, upmark labels, and inside-corner helpers for TikZ.

## 0.3.0 – 2025-11-11

- Initial public preview of the PythonTeX-backed lattice-path package.
- Introduced `\lpDeclarePath`, `\shadeBetweenBits`, `\drawLatticePath`, and the base grid helpers.
- Shipped `lpmresonance.sty` with `pythontex` integration and cache management.
