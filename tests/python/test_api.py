from __future__ import annotations

import json
import pytest
from pathlib import Path
from lpm_paths import api
from lpm_paths.cache import Cache
from lpm_paths.errors import InputSpecError


@pytest.fixture
def use_temp_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Cache:
    cache = Cache.make(str(tmp_path / "cache"))
    dummy = type("DummyCache", (), {"make": staticmethod(lambda root=None: cache)})
    monkeypatch.setattr(api, "Cache", dummy)
    return cache


def test_declare_path_from_json_writes_files(use_temp_cache: Cache, tmp_path: Path) -> None:
    resp = api.declare_path_from_json(json.dumps({"bits": "01", "name": "demo"}))
    tex_file = next((tmp_path / "cache").rglob("path-demo-*.tex"))
    assert "\\gdef\\lp@pathfile@demo{" in resp
    assert tex_file.exists()


def test_path_data_returns_coords():
    data = api.path_data(json.dumps({"bits": "010"}))
    assert data["coords"][-1] == (2, 1)
    assert data["upmarks"] == [2]


def test_between_from_json(use_temp_cache: Cache, tmp_path: Path) -> None:
    resp = api.between_from_json(json.dumps({"L": "0011", "U": "0101", "lname": "L", "uname": "U"}))
    between_file = next((tmp_path / "cache").rglob("between-L-U-*.tex"))
    assert between_file.exists()
    assert "\\gdef\\lp@lastdeclaredbetweenfile" in resp
