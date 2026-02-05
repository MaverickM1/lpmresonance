#!/usr/bin/env bash
set -euo pipefail

# NOTE: This script runs latexmk in the file's directory.
# Ensure PythonTeX is configured in ~/.latexmkrc (the installer does this automatically).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../" && pwd)"
EXAMPLE="${1:-examples/example.tex}"

if [[ ! -f "$ROOT/$EXAMPLE" ]]; then
  echo "TeX file '$EXAMPLE' not found. Pass a relative path (e.g. scripts/check-tex.sh examples/test-features.tex)." >&2
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "latexmk is not installed or not on PATH." >&2
  exit 1
fi

echo "Running latexmk on $EXAMPLE"
cd "$ROOT/$(dirname "$EXAMPLE")"
latexmk -pdf -shell-escape -interaction=nonstopmode "$(basename "$EXAMPLE")"
