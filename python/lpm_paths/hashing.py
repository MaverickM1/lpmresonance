from __future__ import annotations
import json
from hashlib import blake2b #benefits of blake2b: fast, secure, built-in
from typing import Any #why Any? Because we want to hash arbitrary objects.

def canon_json(obj: Any) -> bytes:
    """
    Serialize an object to a canonical JSON byte string.

    Args:
        obj (Any): The object to serialize.

    Returns:
        bytes: The canonical JSON representation of the object as UTF-8 encoded bytes.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def key32_hex(obj: Any) -> str:
    """
    Returns a 32-byte BLAKE2b hash of the canonical JSON representation of the object as a hexadecimal string.
    """
    return blake2b(canon_json(obj), digest_size=32).hexdigest()

def object_hash(obj: Any) -> str:
    """
    Returns a 32-byte BLAKE2b hash of the canonical JSON representation of the given object as a hexadecimal string.

    Args:
        obj (Any): The object to hash.

    Returns:
        str: The hexadecimal hash string.
    """
    return key32_hex(obj)

# Backwards-compatible aliases
canonJson = canon_json
key32 = key32_hex
key_of = object_hash
