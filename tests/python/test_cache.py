from __future__ import annotations

import pytest
from pathlib import Path
from lpm_paths.cache import Cache, CacheFenceError, atomic_write


def test_guard_path_rejects_escape(tmp_path: Path) -> None:
    cache = Cache.make(str(tmp_path / "cache"))
    outside = tmp_path.parent / "elsewhere"
    outside.mkdir(exist_ok=True)
    with pytest.raises(CacheFenceError):
        cache.guard_path(str(outside))


def test_guard_path_allows_cache_child(tmp_path: Path) -> None:
    cache = Cache.make(str(tmp_path / "cache"))
    child = cache.file("nested/data.txt")
    assert Path(child).is_absolute()
    assert str(tmp_path / "cache") in child


def test_tex_path_prefers_relative(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    workdir = tmp_path / "work"
    workdir.mkdir()
    monkeypatch.chdir(workdir)
    cache = Cache.make(str(workdir / "cache"))
    target = cache.file("foo/bar.tex")
    atomic_write(target, "content")
    tex_path = cache.tex_path(target)
    assert tex_path == "cache/foo/bar.tex"


def test_atomic_write_replaces_file(tmp_path: Path) -> None:
    path = tmp_path / "value.txt"
    atomic_write(str(path), "first")
    assert path.read_text() == "first"
    atomic_write(str(path), "second")
    assert path.read_text() == "second"
    assert not path.with_suffix(".txt.tmp").exists()
