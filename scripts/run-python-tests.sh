#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v pytest >/dev/null 2>&1; then
  echo "pytest is not installed. Install dev dependencies with 'pip install -e .[dev]'." >&2
  exit 1
fi

echo "Running Python test suite..."
pytest tests/python "$@"
