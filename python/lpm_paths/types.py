from __future__ import annotations

"""
Core types for lattice path combinatorics.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

Coord = Tuple[int, int]
Upmark = int

@dataclass(frozen=True)
class LatticePath:
    """
    Immutable lattice path with derived geometric annotations.

    Attributes
    ----------
    bits : str
        Binary string encoding east (0) and north (1) steps.
    coords : list[Coord]
        Lattice coordinates along the path.
    upmarks : list[Upmark]
        Indices of north steps (1-based).
    corners : list[int]
        Indices where direction changes.
    insideCorners : list[int]
        Indices of east-to-north transitions.
    ellmap : dict[int, int]
        Mapping from y-level to max x at that level.
    """

    bits: str
    coords: List[Coord]
    upmarks: List[Upmark]
    corners: List[int]
    insideCorners: List[int]
    ellmap: Dict[int, int]

    @staticmethod
    def from_bits(bits: str) -> "LatticePath":
        """
        Create a lattice path from a bitstring.

        Parameters
        ----------
        bits : str
            Binary string encoding east (0) and north (1) steps.

        Returns
        -------
        LatticePath
            Parsed lattice path with derived annotations.

        Raises
        ------
        InputSpecError
            If the string contains characters other than 0 or 1.
        InvariantError
            If derived path invariants do not hold.
        """
        from .errors import InputSpecError, InvariantError

        if any(b not in "01" for b in bits):
            raise InputSpecError("bits must be a binary string of '0' and '1'.")
        x = y = 0
        coords: List[Coord] = [(0, 0)]
        upmarks: List[Upmark] = []
        corners: List[int] = []
        insideCorners: List[int] = []
        prev = None
        step_index = 0
        for b in bits:
            step_index += 1
            if b == "0":
                x += 1
                cur = "E"
            else:
                y += 1
                cur = "N"
                upmarks.append(step_index)
            coords.append((x, y))
            if prev is not None and prev != cur:
                corners.append(step_index - 1)
            if prev == "E" and cur == "N":
                insideCorners.append(step_index - 1)
            prev = cur
        ellmap: Dict[int, int] = {}
        seenY: Dict[int, int] = {}
        for (cx, cy) in coords:
            if cy > 0 and cy not in seenY:
                seenY[cy] = cx
        if y > 0:
            for level in range(1, y + 1):
                ellmap[level] = seenY.get(level, 0)
        if coords[0] != (0, 0):
            raise InvariantError("coords[0] must be (0,0).")
        if len(coords) != len(bits) + 1:
            raise InvariantError("len(coords) must equal len(bits)+1.")
        ex, ny = bits.count("0"), bits.count("1")
        if coords[-1] != (ex, ny):
            raise InvariantError("Endpoint mismatch with bit counts.")
        return LatticePath(bits, coords, upmarks, corners, insideCorners, ellmap)
