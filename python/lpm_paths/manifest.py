from __future__ import annotations
import json
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

def read_json(path: str) -> Dict[str, Any]:
    """
    Read a JSON file from the given path and return its contents as a dictionary.

    Parameters:
        path (str): The file path to the JSON file.

    Returns:
        Dict[str, Any]: The contents of the JSON file as a dictionary.
    """
    with open(path, "r", encoding="utf-8") as f: return json.load(f)