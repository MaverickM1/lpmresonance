from __future__ import annotations

"""
Public JSON-driven API helpers for lattice paths.
"""

import json
from typing import Any, Dict

from .cache import Cache
from .emitters.tex import TeXEmitter
from .errors import InputSpecError
from .types import LatticePath

def declare_path_from_json(spec_json: str) -> str:
    """
    Declare a lattice path from a JSON specification.

    Parameters
    ----------
    spec_json : str
        JSON string with keys "bits", "name", and optional "cache_id".

    Returns
    -------
    str
        TeX macro definitions for the path and its cached artifacts.

    Raises
    ------
    InputSpecError
        If the JSON is invalid or required fields are missing.
    """
    try:
        spec = json.loads(spec_json)
    except Exception as exc:
        raise InputSpecError(f"Invalid JSON: {exc}") from exc
    bits = spec.get("bits")
    name = spec.get("name")
    cache_id = spec.get("cache_id")
    if not isinstance(bits, str) or not isinstance(name, str):
        raise InputSpecError("'bits' and 'name' must be strings.")
    emitter = TeXEmitter(Cache.make())
    g1, g2, g3 = emitter.write_path(bits=bits, name=name, cache_id=cache_id)
    return "\n".join([g1, g2, g3])

def path_data(spec_json: str) -> Dict[str, Any]:
    """
    Return decoded path data from a JSON specification.

    Parameters
    ----------
    spec_json : str
        JSON string with key "bits".

    Returns
    -------
    dict[str, Any]
        Path coordinates and upmark indices.

    Raises
    ------
    InputSpecError
        If the JSON is invalid or required fields are missing.
    """
    try:
        spec = json.loads(spec_json)
    except Exception as exc:
        raise InputSpecError(f"Invalid JSON: {exc}") from exc
    bits = spec.get("bits")
    if not isinstance(bits, str):
        raise InputSpecError("'bits' must be a string.")
    lp = LatticePath.from_bits(bits)
    return {"coords": lp.coords, "upmarks": lp.upmarks}

def between_from_json(spec_json: str) -> str:
    """
    Declare a between-region from a JSON specification.

    Parameters
    ----------
    spec_json : str
        JSON string with keys "L", "U", and optional "lname", "uname".

    Returns
    -------
    str
        TeX macro definition for the between-region.

    Raises
    ------
    InputSpecError
        If the JSON is invalid or required fields are missing.
    """
    try:
        spec = json.loads(spec_json)
    except Exception as exc:
        raise InputSpecError(f"Invalid JSON: {exc}") from exc
    L = spec.get("L")
    U = spec.get("U")
    lname = spec.get("lname") or "L"
    uname = spec.get("uname") or "U"
    if not isinstance(L, str) or not isinstance(U, str):
        raise InputSpecError("'L' and 'U' must be bit-strings.")
    emitter = TeXEmitter(Cache.make())
    return emitter.write_between(L_bits=L, U_bits=U, lname=lname, uname=uname)
