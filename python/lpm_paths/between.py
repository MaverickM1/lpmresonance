from __future__ import annotations

"""
Geometry helpers for between-region polygons.
"""

from typing import List

from .errors import InputSpecError
from .types import Coord, LatticePath

def between_polygon(L_bits: str, U_bits: str) -> List[Coord]:
    """
    Build a polygon for the region between two lattice paths.

    Parameters
    ----------
    L_bits : str
        Lower path bitstring.
    U_bits : str
        Upper path bitstring.

    Returns
    -------
    list[Coord]
        Polygon coordinates, closed and de-duplicated.

    Raises
    ------
    InputSpecError
        If paths do not share the same start or end points.
    """
    L = LatticePath.from_bits(L_bits)
    U = LatticePath.from_bits(U_bits)
    if L.coords[-1] != U.coords[-1]:
        raise InputSpecError("Paths must share the same endpoint.")
    if L.coords[0] != (0, 0) or U.coords[0] != (0, 0):
        raise InputSpecError("Paths must start at (0,0).")
    upper = U.coords[:]
    lower = list(reversed(L.coords))[1:-1]
    polygon = upper + lower + [upper[0]]
    dedup: List[Coord] = []
    for c in polygon:
        if not dedup or dedup[-1] != c:
            dedup.append(c)
    return dedup
