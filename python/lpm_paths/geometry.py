from __future__ import annotations
from .types import LatticePath #importing LatticePath class from local types module
def makeLatticePath(bits: str) -> LatticePath:
    """
    Create a LatticePath object from a string of bits.

    Args:
        bits (str): A string representing the lattice path in bits.

    Returns:
        LatticePath: The corresponding LatticePath object.
    """
    return LatticePath.from_bits(bits)