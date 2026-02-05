---
title: Shading between paths
---

# Shading between paths

Two lattice paths with the same endpoints bound a region. The package computes
that polygon in Python (so you do not have to) and makes it available as TikZ
coordinates.

## Declare the region in Python

```tex
\shadeBetweenBits{<L bits>}{<U bits>}{<lname>}{<uname>}
```

- `<L bits>` / `<U bits>` are East/North bit strings for the lower (L) and upper
  (U) paths. They must share both the starting point `(0,0)` and the final point.
- `<lname>` / `<uname>` become sanitized TeX identifiers, just like
  `\lpDeclarePath`. Reusing the same name pair reuses the cache entry.

When this macro runs, PythonTeX writes a file such as
`lp-cache/between-L-U-<hash>.tex` holding the polygon coordinates. The helper
also records the latest file path in `\lp@lastdeclaredbetweenfile`.

## Draw or shade the saved region

```tex
\shadeBetween[<tikz opts>]{<lname>}{<uname>}
\drawBetween[<tikz opts>]{<lname>}{<uname>}
```

Both commands check whether the requested name pair is ready. If not, you get a
package warning instead of a TikZ error. Once ready, each command calls
`\fill` or `\draw` with the stored coordinates.

Example:

```tex
\shadeBetweenBits{00110101}{01011001}{L}{U}
\begin{schubertpic}
  \shadeBetween[gray!20]{L}{U}
  \drawBetween[thick]{L}{U}
\end{schubertpic}
```

## Reusing coordinates elsewhere

Use the low-level accessor when you need to plug the polygon into custom TikZ
code or PGFPlots:

```tex
\path plot coordinates \lpBetweenCoords{L}{U};
```

- When the polygon is ready, `\lpBetweenCoords{L}{U}` expands to the cached
  coordinate list.
- Otherwise it expands to the placeholder `(0,0)` so TikZ still receives valid
  syntax during the first LaTeX pass.

Call `\lp@ensurebetweenplaceholder{<lname>}{<uname>}` if you need to reserve a
pair before Python runs (the macro is defined in `lpmres-base.code.tex` and is
already used internally by `\shadeBetweenBits`).
