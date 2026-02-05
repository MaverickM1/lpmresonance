from __future__ import annotations
from typing import Any, Dict
from .types import LatticePath

def to_json_obj(name: str, lp: LatticePath) -> Dict[str, Any]:
    """
    Convert a LatticePath object and its name into a JSON-serializable dictionary.

    Parameters:
        name (str): The name associated with the lattice path.
        lp (LatticePath): The LatticePath object to serialize.

    Returns:
        Dict[str, Any]: A dictionary containing the name, bits, coords, and upmarks of the lattice path.
    """
    return {"name": name, "bits": lp.bits, "coords": lp.coords, "upmarks": lp.upmarks}