from lpm_paths.hashing import key32


def test_key32_deterministic_for_equivalent_objects():
    a = {"name": "demo", "coords": [(0, 0), (1, 0)], "flags": [1, 2]}
    b = {"flags": [1, 2], "coords": [(0, 0), (1, 0)], "name": "demo"}
    assert key32(a) == key32(b)
    assert len(key32(a)) == 64
