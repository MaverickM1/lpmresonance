from __future__ import annotations
from typing import List, Tuple
from .types import Coord
from .geometry import makeLatticePath
from .errors import InputSpecError

def between_polygon(L_bits: str, U_bits: str) -> List[Coord]:
    L = makeLatticePath(L_bits); U = makeLatticePath(U_bits)
    if L.coords[-1] != U.coords[-1]: raise InputSpecError("Paths must share the same endpoint.")
    if L.coords[0] != (0,0) or U.coords[0] != (0,0): raise InputSpecError("Paths must start at (0,0).")
    upper = U.coords[:]
    lower = list(reversed(L.coords))[1:-1]
    polygon = upper + lower + [upper[0]]
    dedup: List[Coord] = []
    for c in polygon:
        if not dedup or dedup[-1] != c: dedup.append(c)
    return dedup