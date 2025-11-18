import pytest
from lpm_paths.geometry import makeLatticePath
from lpm_paths.errors import InputSpecError


def test_make_lattice_path_parses_bits():
    lp = makeLatticePath("0101")
    assert lp.coords[-1] == (2, 2)
    assert lp.upmarks == [2, 4]
    assert lp.corners == [1, 2, 3]
    assert lp.ellmap == {1: 1, 2: 2}


def test_make_lattice_path_validates_bits():
    with pytest.raises(InputSpecError):
        makeLatticePath("10a1")
