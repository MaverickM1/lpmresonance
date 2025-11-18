
## Upgrade watchlist
- See **Developer Guide → Upgrade Notes → PEP 649/749 transition** for the annotations plan and removal of `from __future__ import annotations` when we target Python ≥ 3.14.

## Between-region helpers
- `\shadeBetweenBits{<Lbits>}{<Ubits>}{<lname>}{<uname>}` now records multiple filled regions at once.
- Use the new `\lpBetweenCoords{<lname>}{<uname>}` macro instead of the internal `\lp@between@coords` alias so you can draw any previously declared region without re-running Python.
- The helper falls back to the most recent region (matching the prior behavior) and emits a package warning if the requested pair has not been declared yet.
