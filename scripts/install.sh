#!/usr/bin/env bash
set -euo pipefail

# Detect UTF-8 support for progress markers
if [[ "${LANG:-}" =~ UTF-8 ]] || [[ "${LC_ALL:-}" =~ UTF-8 ]]; then
  ARROW="→"
  CHECK="✓"
else
  ARROW=">"
  CHECK="[OK]"
fi

# Auto-detect OS
case "$(uname -s)" in
  Darwin*) OS_NAME="macOS" ;;
  Linux*)  OS_NAME="Linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS_NAME="Windows" ;;
  *)       OS_NAME="$(uname -s)" ;;
esac

# Allow override via --os flag
if [[ "${1:-}" == "--os" ]]; then
  OS_NAME="${2:-$OS_NAME}"
  shift 2
fi

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [--os <linux|macos>]

Installs the Python package in editable mode, installs TeX files into TEXMFHOME,
and compiles a temporary test document to verify the toolchain.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

if command -v python >/dev/null 2>&1; then
  PYTHON_BIN=$(command -v python)
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=$(command -v python3)
else
  echo "Error: Python 3 (python or python3) is required but was not found." >&2
  echo "Install Python 3.9+ from https://www.python.org/downloads/" >&2
  exit 1
fi

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 9):
    sys.stderr.write(f"Error: Python 3.9+ is required. Found: {sys.version_info.major}.{sys.version_info.minor}\n")
    sys.exit(1)
PY

if ! command -v pdflatex >/dev/null 2>&1; then
  echo "Error: pdflatex not found." >&2
  echo "Install TeX Live 2022+ from https://tug.org/texlive/" >&2
  exit 1
fi

if ! command -v pythontex >/dev/null 2>&1; then
  echo "Error: pythontex not found." >&2
  echo "Install PythonTeX via: tlmgr install pythontex" >&2
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "Error: latexmk not found." >&2
  echo "Install latexmk via: tlmgr install latexmk" >&2
  exit 1
fi

if ! command -v kpsewhich >/dev/null 2>&1; then
  echo "Error: kpsewhich not found. TeX Live installation may be incomplete." >&2
  exit 1
fi

echo "$ARROW Installing TeX files to TEXMFHOME..."
TEXMFHOME=$(kpsewhich -var-value TEXMFHOME)
if [[ -z "${TEXMFHOME}" ]]; then
  echo "Error: TEXMFHOME is empty. TeX Live does not appear configured." >&2
  exit 1
fi
if [[ "${TEXMFHOME}" == "~"* ]]; then
  TEXMFHOME="${TEXMFHOME/#\~/$HOME}"
fi

TARGET_DIR="${TEXMFHOME}/tex/latex/lpmres"
mkdir -p "$TARGET_DIR"
cp -a "$REPO_ROOT/tex/latex/lpmres/"* "$TARGET_DIR/"

if command -v mktexlsr >/dev/null 2>&1; then
  echo "$ARROW Refreshing TeX database..."
  if ! mktexlsr "$TEXMFHOME" >/dev/null 2>&1; then
    echo "Warning: Failed to refresh TeX database. You may need to run 'mktexlsr' manually." >&2
  fi
fi

echo "$ARROW Installing Python package..."
if ! "$PYTHON_BIN" -m pip install -e "$REPO_ROOT"; then
  echo "Error: pip install failed. Check your Python environment." >&2
  exit 1
fi

# Configure global ~/.latexmkrc with PythonTeX support
LATEXMKRC="$HOME/.latexmkrc"
PYTHONTEX_MARKER="# PythonTeX support"

if [[ -f "$LATEXMKRC" ]] && grep -q "$PYTHONTEX_MARKER" "$LATEXMKRC"; then
  echo "$ARROW PythonTeX already configured in ~/.latexmkrc"
else
  echo "$ARROW Configuring PythonTeX in ~/.latexmkrc..."
  
  # Determine the python command and pythontex path
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
  else
    PYTHON_CMD="python"
  fi
  PYTHONTEX_PATH=$(which pythontex)
  
  # Append PythonTeX configuration
  cat >> "$LATEXMKRC" <<LATEXMKRC_EOF

$PYTHONTEX_MARKER (added by lpmresonance installer)
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex {
    system("$PYTHON_CMD $PYTHONTEX_PATH --interpreter 'python:$PYTHON_CMD' \"\$_[0]\"");
}
LATEXMKRC_EOF
  echo "  Added PythonTeX rule using '$PYTHON_CMD'"
fi

if ! kpsewhich lpmresonance.sty >/dev/null 2>&1; then
  echo "Error: lpmresonance.sty not found in TeX search path after install." >&2
  exit 1
fi

TMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t lpmresonance)
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cat > "$TMP_DIR/lpmresonance-test.tex" <<'EOF'
\documentclass{article}
\usepackage{lpmresonance}
\begin{document}
\lpDeclarePath{demo}{0101}
\begin{schubertpic}
  \drawGrid{demo}
  \drawLatticePath{demo}
\end{schubertpic}
\end{document}
EOF

# Don't copy local latexmkrc - verification should use the global ~/.latexmkrc we just configured
# This ensures the global config actually works

echo "$ARROW Running verification build..."
(
  cd "$TMP_DIR"
  if ! latexmk -pdf -shell-escape lpmresonance-test.tex >"$TMP_DIR/build.log" 2>&1; then
    echo "Error: Test compilation failed. Last 30 lines of log:" >&2
    tail -n 30 "$TMP_DIR/build.log" >&2
    exit 1
  fi
)

if [[ ! -f "$TMP_DIR/lpmresonance-test.pdf" ]]; then
  echo "Error: Test compilation failed. PDF not generated." >&2
  exit 1
fi

if [[ ! -d "$TMP_DIR/lp-cache" ]] || [[ -z "$(ls -A "$TMP_DIR/lp-cache"/path-demo-*.tex 2>/dev/null)" ]]; then
  echo "Error: Cache files not generated. Python bridge may be broken." >&2
  exit 1
fi

trap - EXIT
cleanup

echo "$CHECK Installer completed successfully for ${OS_NAME}."
echo ""
echo "You can now use lpmresonance in your LaTeX documents:"
echo "  \\usepackage{lpmresonance}"
echo ""
echo "Compile with: latexmk -pdf -shell-escape yourfile.tex"
