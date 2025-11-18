from __future__ import annotations #to continue calling classes that aren't yet defined.
from dataclasses import dataclass #dataclass decorator to create immutable data classes
from typing import List, Tuple, Dict #constructs for type hinting

Coord = Tuple[int, int] #coodinates as (x,y) tuples
Upmark = int #up-steps as integers (step indices)

@dataclass(frozen=True) #frozen makes instances immutable. Why? Because lattice paths shouldn't change after creation.
class LatticePath: #main class representing a lattice path
    bits: str #binary string of '0's and '1's representing east and north steps
    coords: List[Coord] #list of (x,y) coordinates along the path
    upmarks: List[Upmark] #list of step indices where north steps occur
    corners: List[int] #indices with corners (where direction changes)
    insideCorners: List[int] #indices with inside corners (East -> North transitions)
    ellmap: Dict[int, int] #ell map as a dictionary: y-level to max x at that level

    @staticmethod
    def from_bits(bits: str) -> "LatticePath": #static method to create LatticePath from binary string
        from .errors import InputSpecError, InvariantError #error classes to ensure clean input and invariants
        if any(b not in "01" for b in bits):
            raise InputSpecError("bits must be a binary string of '0' and '1'.")
        x = y = 0 #start at origin
        coords: List[Coord] = [(0, 0)] #same.
        upmarks: List[Upmark] = [] #none up-marked yet.
        corners: List[int] = [] #obviously none yet.
        insideCorners: List[int] = [] #none yet.
        prev = None #previous direction (None at start)
        stepIndex = 0 #step counter
        for b in bits: #bit-by-bit processing
            stepIndex += 1 #increment step index
            if b == "0": #east step
                x += 1; cur = "E" #move east
            else: #else north step
                y += 1; cur = "N"; upmarks.append(stepIndex) #move north and mark up-step
            coords.append((x, y)) #record new coordinate
            if prev is not None and prev != cur: #counts outer corners as well: the transition North->East is also counter. We only require inside corners: East->North transitions.
                corners.append(stepIndex - 1)
            if prev == "E" and cur == "N": #inside corner detected
                insideCorners.append(stepIndex - 1)
            prev = cur #update previous direction
        ellmap: Dict[int, int] = {} #initialize ell map
        seenY: Dict[int, int] = {} #track max x for each y-level
        for (cx, cy) in coords: #build seenY map
            if cy > 0 and cy not in seenY: #for each new y-level
                seenY[cy] = cx #record max x at that level
        if y > 0:
            for level in range(1, y + 1):
                ellmap[level] = seenY.get(level, 0)
        if coords[0] != (0, 0): raise InvariantError("coords[0] must be (0,0).")
        if len(coords) != len(bits) + 1: raise InvariantError("len(coords) must equal len(bits)+1.")
        ex, ny = bits.count("0"), bits.count("1") #better names?
        if coords[-1] != (ex, ny): raise InvariantError("Endpoint mismatch with bit counts.")
        return LatticePath(bits, coords, upmarks, corners, insideCorners, ellmap)