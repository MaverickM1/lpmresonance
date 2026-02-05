"""
Custom error types for lpmresonance.
"""

class InputSpecError(ValueError):
    """Invalid input specification."""

    pass


class InvariantError(RuntimeError):
    """Invariant violation."""

    pass


class CacheFenceError(PermissionError):
    """Cache fence violation."""

    pass


class PathFormatError(ValueError):
    """Invalid path format."""

    pass


__all__ = [
    "InputSpecError",
    "InvariantError",
    "CacheFenceError",
    "PathFormatError",
]
