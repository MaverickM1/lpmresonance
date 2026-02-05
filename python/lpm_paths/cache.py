from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from .errors import CacheFenceError

DEFAULT_CACHE_DIR = "lp-cache"


def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists.

    Parameters
    ----------
    path : str
        Directory path to create if missing.
    """
    os.makedirs(path, exist_ok=True)


@dataclass(frozen=True)
class Cache:
    """
    Cache root and path-fencing utilities.

    Parameters
    ----------
    root : str
        Root directory for all cached artifacts.

    Notes
    -----
    All file paths are validated to stay within the cache root to avoid
    unintended reads or writes outside the cache fence.
    """

    root: str

    @staticmethod
    def make(root: Optional[str] = None) -> "Cache":
        """
        Create a cache rooted at the provided path or default location.

        Parameters
        ----------
        root : str or None, optional
            Cache root directory.

        Returns
        -------
        Cache
            Cache instance rooted at the resolved directory.
        """
        r = root or DEFAULT_CACHE_DIR
        ensure_dir(r)
        return Cache(root=r)

    def guard_path(self, path: str) -> str:
        """
        Validate that a resolved path stays within the cache root.

        Parameters
        ----------
        path : str
            Candidate path to validate.

        Returns
        -------
        str
            Resolved absolute path if it remains within the cache fence.

        Raises
        ------
        CacheFenceError
            If the path escapes the cache root.
        """
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
        """
        Return a fenced cache file path and create parent directories.

        Parameters
        ----------
        filename : str
            Cache-relative filename.

        Returns
        -------
        str
            Absolute, fenced path to the cache file.
        """
        p = os.path.join(self.root, filename)
        ensure_dir(os.path.dirname(p))
        return self.guard_path(p)

    def tex_path(self, path: str) -> str:
        """
        Convert a cache path to a TeX-friendly display path.

        Parameters
        ----------
        path : str
            Absolute or cache-relative path.

        Returns
        -------
        str
            TeX-friendly path with normalized separators.
        """
        path_real = self.guard_path(path)
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


def atomic_write(path: str, data: str) -> None:
    """
    Write data to a file atomically.

    Parameters
    ----------
    path : str
        Destination path.
    data : str
        File contents to write.
    """
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp, path)