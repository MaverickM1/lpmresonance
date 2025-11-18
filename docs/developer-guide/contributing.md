---
title: Contributing
---

# Contributing

We welcome patches! This guide covers the repo workflow and expectations.

## Environment setup

1. Clone the repository and install the Python package in editable mode:
   ```bash
   pip install -e .[dev]
   ```
2. Install the TeX files by either copying them to your TEXMF tree or by
   extending `TEXINPUTS` (see `docs/user-guide/installation.md`).
3. Verify your toolchain with `pytest tests/python` and `latexmk -pdf -shell-escape examples/example.tex`.

## Coding guidelines

- Python 3.9–3.13 compatibility is required until we bump the minimum version.
- Keep `from __future__ import annotations` in any module that uses annotations.
- Run `pytest` before sending a patch; add regression tests where reasonable.
- For TeX changes, include a sample in `examples/` or extend the TeX regression
  tests under `tests/tex/`.
- Document new features in the relevant user-guide or API page and add an entry
  to `docs/changelog.md`.

## Git workflow

- Work on a feature branch.
- Keep commits focused and descriptive.
- If you modify generated files (e.g., cached outputs), mention why in the
  commit message or avoid committing them altogether.

## Pull requests

When you open a PR:

1. Summarize the change and why it is needed.
2. List the tests you ran (pytest, latexmk, etc.).
3. Highlight any follow-up work (e.g., documentation improvements, TODOs).

CI runs the Python tests and builds a sample TeX document using the CI-specific
`ci/latexmk/latexmkrc`. Ensure the PR keeps CI green.
