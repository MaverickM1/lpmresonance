import re
from typing import Any

_SAFE_RE = re.compile(r"[^A-Za-z0-9_]+")

def sanitizeName(name: Any) -> str:
    """
    Public sanitizer (primary). Matches TeX-side rules.
    - Replace non [A-Za-z0-9_] with '_'
    - Collapse consecutive '_'
    - Strip leading/trailing '_'
    - If empty, return 'anon'
    """
    if not isinstance(name, str):
        name = str(name)
    s = _SAFE_RE.sub("_", name)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "anon"

# Public snake_case alias.
def sanitize_name(name: Any) -> str:
    return sanitizeName(name)

# Private alias kept for compatibility with existing imports.
def _sanitize_name(name: Any) -> str:
    return sanitizeName(name)
