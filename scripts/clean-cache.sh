#!/bin/bash
# Clean all build artifacts and cache files from lpmresonance package

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Cleaning lpmresonance build artifacts and cache..."

# Clean LaTeX auxiliary files
echo "  → Removing LaTeX auxiliary files..."
find "$PROJECT_ROOT" -type f \( \
    -name "*.aux" -o \
    -name "*.bbl" -o \
    -name "*.blg" -o \
    -name "*.fdb_latexmk" -o \
    -name "*.fls" -o \
    -name "*.log" -o \
    -name "*.out" -o \
    -name "*.synctex.gz" -o \
    -name "*.toc" -o \
    -name "*.pytxcode" -o \
    -name "*.pytxmcr" \
\) -delete 2>/dev/null || true

# Clean PythonTeX directories
echo "  → Removing PythonTeX directories..."
find "$PROJECT_ROOT" -type d -name "pythontex-files-*" -exec rm -rf {} + 2>/dev/null || true

# Clean minted directories
echo "  → Removing minted directories..."
find "$PROJECT_ROOT" -type d -name "_minted-*" -exec rm -rf {} + 2>/dev/null || true

# Clean lp-cache directories
echo "  → Removing lp-cache directories..."
find "$PROJECT_ROOT" -type d -name "lp-cache" -exec rm -rf {} + 2>/dev/null || true

# Clean .names directories
echo "  → Removing .names directories..."
find "$PROJECT_ROOT" -type d -name ".names" -exec rm -rf {} + 2>/dev/null || true

# Clean Python cache
echo "  → Removing Python cache..."
find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true

echo "✓ Cleanup complete!"
