from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional
from .errors import CacheFenceError

DEFAULT_CACHE_DIR = "lp-cache"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


@dataclass(frozen=True)
class Cache:
    root: str

    @staticmethod
    def make(root: Optional[str] = None) -> "Cache":
        r = root or DEFAULT_CACHE_DIR
        ensure_dir(r)
        return Cache(root=r)

    def guardPath(self, path: str) -> str:
        root_real = os.path.realpath(self.root)
        path_real = os.path.realpath(path)
        try:
            common = os.path.commonpath([root_real, path_real])
        except ValueError as exc:
            raise CacheFenceError(f"Path escapes fence: {path}") from exc
        if common != root_real:
            raise CacheFenceError(f"Path escapes fence: {path}")
        return path_real

    def file(self, filename: str) -> str:
        p = os.path.join(self.root, filename)
        ensure_dir(os.path.dirname(p))
        return self.guardPath(p)

    def tex_path(self, path: str) -> str:
        path_real = self.guardPath(path)
        try:
            rel = os.path.relpath(path_real, os.getcwd())
        except ValueError:
            rel = None
        upward = os.pardir
        if rel is not None and rel not in (upward,) and not rel.startswith(upward + os.sep):
            display = rel
        else:
            display = path_real
        return display.replace(os.sep, "/")


def _atomic_write(path: str, data: str) -> None:
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp, path)


atomic_write = _atomic_write
