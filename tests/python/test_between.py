from __future__ import annotations

import pytest
from lpm_paths.between import between_polygon
from lpm_paths.errors import InputSpecError


def test_between_polygon_closed_loop():
    poly = between_polygon("0011", "0101")
    assert poly[0] == poly[-1]
    assert len(poly) > 4
    # Ensure no consecutive duplicates
    for a, b in zip(poly, poly[1:]):
        assert a != b


def test_between_polygon_requires_matching_endpoints():
    with pytest.raises(InputSpecError):
        between_polygon("0", "11")
