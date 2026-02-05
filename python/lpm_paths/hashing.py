from __future__ import annotations

"""
Canonical JSON hashing utilities.
"""

import json
from hashlib import blake2b
from typing import Any

def canon_json(obj: Any) -> bytes:
    """
    Serialize an object to a canonical JSON byte string.

    Parameters
    ----------
    obj : Any
        Object to serialize.

    Returns
    -------
    bytes
        Canonical JSON representation encoded as UTF-8 bytes.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def key_of(obj: Any) -> str:
    """
    Compute a stable 32-byte BLAKE2b hex digest for an object.

    Parameters
    ----------
    obj : Any
        Object to hash via canonical JSON.

    Returns
    -------
    str
        Hexadecimal digest string.
    """
    return blake2b(canon_json(obj), digest_size=32).hexdigest()