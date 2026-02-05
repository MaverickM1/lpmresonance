import pytest
from lpm_paths.errors import InputSpecError
from lpm_paths.types import LatticePath


def test_make_lattice_path_parses_bits():
    lp = LatticePath.from_bits("0101")
    assert lp.coords[-1] == (2, 2)
    assert lp.upmarks == [2, 4]
    assert lp.corners == [1, 2, 3]
    assert lp.ellmap == {1: 1, 2: 2}


def test_make_lattice_path_validates_bits():
    with pytest.raises(InputSpecError):
        LatticePath.from_bits("10a1")
