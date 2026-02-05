from lpm_paths.hashing import key_of


def test_key_of_deterministic_for_equivalent_objects():
    a = {"name": "demo", "coords": [(0, 0), (1, 0)], "flags": [1, 2]}
    b = {"flags": [1, 2], "coords": [(0, 0), (1, 0)], "name": "demo"}
    assert key_of(a) == key_of(b)
    assert len(key_of(a)) == 64