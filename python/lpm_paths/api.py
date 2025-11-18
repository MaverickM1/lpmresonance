from __future__ import annotations
import json
from typing import Any, Dict
from .errors import InputSpecError
from .cache import Cache
from .emitters.tex import TeXEmitter
from .geometry import makeLatticePath

def declare_path_from_json(spec_json: str) -> str:
    try: spec = json.loads(spec_json)
    except Exception as e: raise InputSpecError(f"Invalid JSON: {e}")
    bits = spec.get("bits"); name = spec.get("name"); cache_id = spec.get("cache_id")
    if not isinstance(bits, str) or not isinstance(name, str): raise InputSpecError("'bits' and 'name' must be strings.")
    emitter = TeXEmitter(Cache.make())
    g1, g2, g3 = emitter.write_path(bits=bits, name=name, cache_id=cache_id)
    return "\n".join([g1, g2, g3])

def path_data(spec_json: str) -> Dict[str, Any]:
    try: spec = json.loads(spec_json)
    except Exception as e: raise InputSpecError(f"Invalid JSON: {e}")
    bits = spec.get("bits")
    if not isinstance(bits, str): raise InputSpecError("'bits' must be a string.")
    lp = makeLatticePath(bits)
    return {"coords": lp.coords, "upmarks": lp.upmarks}

def between_from_json(spec_json: str) -> str:
    try: spec = json.loads(spec_json)
    except Exception as e: raise InputSpecError(f"Invalid JSON: {e}")
    L = spec.get("L"); U = spec.get("U"); lname = spec.get("lname") or "L"; uname = spec.get("uname") or "U"
    if not isinstance(L, str) or not isinstance(U, str): raise InputSpecError("'L' and 'U' must be bit-strings.")
    emitter = TeXEmitter(Cache.make())
    return emitter.write_between(L_bits=L, U_bits=U, lname=lname, uname=uname)