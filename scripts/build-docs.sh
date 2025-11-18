#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v mkdocs >/dev/null 2>&1; then
  echo "mkdocs is not installed. Install it via 'pip install mkdocs mkdocs-material'." >&2
  exit 1
fi

echo "Building documentation..."
mkdocs build --clean "$@"
echo "Docs available in site/ (serve with 'mkdocs serve' for live preview)."
