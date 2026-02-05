"""
Name sanitization utilities.
"""

import re
from typing import Any

_SAFE_RE = re.compile(r"[^A-Za-z0-9_]+")

def sanitize_name(name: Any) -> str:
    """
    Sanitize a name for TeX-safe identifiers.

    Parameters
    ----------
    name : Any
        Input name to sanitize; non-strings are coerced to strings.

    Returns
    -------
    str
        Sanitized name with only letters, digits, and underscores.
    """
    if not isinstance(name, str):
        name = str(name)
    s = _SAFE_RE.sub("_", name)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "anon"