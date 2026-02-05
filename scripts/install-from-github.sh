#!/usr/bin/env bash
set -euo pipefail

# Self-extracting installer for lpmresonance
# Downloads from GitHub and runs the installation script

VERSION="${1:-main}"
REPO_URL="https://github.com/MaverickM1/lpmresonance"

# Detect UTF-8 support for progress markers
if [[ "${LANG:-}" =~ UTF-8 ]] || [[ "${LC_ALL:-}" =~ UTF-8 ]]; then
  ARROW="→"
  CHECK="✓"
else
  ARROW=">"
  CHECK="[OK]"
fi

usage() {
  cat <<'EOF'
Usage: install-from-github.sh [VERSION]

Downloads and installs lpmresonance from GitHub.

Arguments:
  VERSION    Git tag, branch, or commit (default: main)

Examples:
  install-from-github.sh              # Install from main branch
  install-from-github.sh v0.0.1       # Install specific version
  install-from-github.sh develop      # Install from develop branch

Requirements:
  - curl or wget
  - tar
  - Python 3.9+
  - TeX Live 2022+

EOF
}

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

# Check for download tools
if command -v curl >/dev/null 2>&1; then
  DOWNLOAD_CMD="curl -fsSL"
elif command -v wget >/dev/null 2>&1; then
  DOWNLOAD_CMD="wget -qO-"
else
  echo "Error: Neither curl nor wget found. Install one of them first." >&2
  exit 1
fi

# Check for tar
if ! command -v tar >/dev/null 2>&1; then
  echo "Error: tar not found." >&2
  exit 1
fi

echo "$ARROW Creating temporary directory..."
TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t lpmresonance)
trap "rm -rf '$TMPDIR'" EXIT

ARCHIVE_URL="${REPO_URL}/archive/${VERSION}.tar.gz"
echo "$ARROW Downloading lpmresonance ${VERSION} from GitHub..."
echo "   $ARCHIVE_URL"

if ! $DOWNLOAD_CMD "$ARCHIVE_URL" > "$TMPDIR/lpmresonance.tar.gz"; then
  echo "Error: Failed to download from $ARCHIVE_URL" >&2
  echo "Check that the version/branch exists and you have internet access." >&2
  exit 1
fi

echo "$ARROW Extracting archive..."
if ! tar -xzf "$TMPDIR/lpmresonance.tar.gz" -C "$TMPDIR"; then
  echo "Error: Failed to extract archive." >&2
  exit 1
fi

# Find the extracted directory (handles version tags with 'v' prefix)
EXTRACT_DIR=$(find "$TMPDIR" -maxdepth 1 -type d -name "lpmresonance-*" | head -n 1)
if [[ -z "$EXTRACT_DIR" ]]; then
  echo "Error: Could not find extracted directory." >&2
  exit 1
fi

echo "$ARROW Running installation script..."
cd "$EXTRACT_DIR"

if [[ ! -f "scripts/install.sh" ]]; then
  echo "Error: install.sh not found in archive." >&2
  echo "The archive may be corrupted or incomplete." >&2
  exit 1
fi

# Detect OS for install script
OS_FLAG=""
if [[ "$(uname -s)" == "Darwin" ]]; then
  OS_FLAG="--os macos"
elif [[ "$(uname -s)" == "Linux" ]]; then
  OS_FLAG="--os linux"
fi

if ! bash scripts/install.sh $OS_FLAG; then
  echo "" >&2
  echo "Installation failed. Check the errors above." >&2
  exit 1
fi

echo ""
echo "$CHECK Installation complete!"
echo ""
echo "To verify installation, run:"
echo "  lpmresonance-doctor"
