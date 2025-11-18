#!/usr/bin/env python3
"""
Regenerate TeX golden files used by tests/tex/.

This script invokes latexmk for each fixture listed in the GOLDEN_SOURCES table
and copies the relevant cache outputs into tests/tex/golden/.

It is intentionally conservative: review the generated files in git diff before
committing to ensure changes are expected.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
GOLDEN_DIR = REPO_ROOT / "tests" / "tex" / "golden"
GOLDEN_SOURCES = {
    "between-L-U.tex": ("test-between-golden.tex", "lp-cache/between-L-U"),
    "path-01011010.tex": ("test-path-golden.tex", "lp-cache/path-demo"),
}


def run_latexmk(tex_name: str) -> None:
    cmd = [
        "latexmk",
        "-pdf",
        "-shell-escape",
        "-interaction=nonstopmode",
        tex_name,
    ]
    subprocess.run(cmd, cwd=EXAMPLES_DIR, check=True)


def main() -> int:
    missing = [name for name in GOLDEN_SOURCES.values() if not (EXAMPLES_DIR / name[0]).exists()]
    if missing:
        print("Missing source TeX files:", ", ".join(missing), file=sys.stderr)
        return 1

    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    for output_name, (tex_source, cache_prefix) in GOLDEN_SOURCES.items():
        print(f"Compiling {tex_source}...")
        run_latexmk(tex_source)
        cache_path = next((EXAMPLES_DIR / cache_prefix).parent.glob(f"{Path(cache_prefix).name}*.tex"), None)
        if cache_path is None:
            print(f"Could not find cache output for prefix {cache_prefix}", file=sys.stderr)
            return 1
        target = GOLDEN_DIR / output_name
        shutil.copy2(cache_path, target)
        print(f"Updated {target.relative_to(REPO_ROOT)}")

    print("Done. Review changes under tests/tex/golden/ before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
