---
title: Lattice path macros
---

# Lattice path macros

Everything starts with a named lattice path. The Python back-end converts a bit
string into coordinates and stores them in the cache. The TeX layer then draws
the cached data with TikZ.

## Declaring a path

```tex
\lpDeclarePath{<name>}{<bits>}
```

- `<bits>` is a string of `0`s (East steps) and `1`s (North steps). The final
  point is `(num_zeros, num_ones)`.
- `<name>` is any text. It is sanitized to `A-Za-z0-9_` before being turned into
  a control sequence. Reusing the same sanitized name overwrites the previous
  declaration and triggers a package warning.
- The macro calls PythonTeX during compilation. If `pythontex` did not run you
  will see “not ready; run pythontex and recompile” warnings.

Internally `\lpDeclarePath` defines three helper macros:

- `\lp@pathfile@<safe>` – path to the generated `.tex`.
- `\lp@pathjson@<safe>` – path to the JSON manifest.
- `\lp@lastdeclaredpathfile` – useful for debugging or input hooks.

You normally do not need to reference these directly; they exist for advanced
automation and for tests.

## Drawing a path

```tex
\drawLatticePath[<tikz opts>]{<safeName>}
```

- `<safeName>` must match the sanitized name returned by `\lpDeclarePath`.
  (In practice you pass the same literal string you used in `\lpDeclarePath`.)
- `<tikz opts>` are appended to the default `lp/path,lp/lpath` style.
- The command warns (instead of crashing) when the data has not been generated
  yet, which keeps the first LaTeX pass quiet.

We recommend wrapping drawings in the `schubertpic` environment provided by
`lpmres-pic.code.tex`. It applies a square grid and axes so you can focus on the
path itself:

```tex
\begin{schubertpic}[x=0.5cm,y=0.5cm]
  \drawGrid{demo}
  \drawLatticePath{demo}
\end{schubertpic}
```

## Grids and helper geometry

`\drawGrid[<tikz opts>]{<safeName>}` queries the cached grid size for the path
and draws a standard TikZ grid from `(0,0)` to `(num_zeros,num_ones)`. Supply a
custom style (e.g. `gray, very thin`) to match the rest of your document.

## Upmarks and inside corners

The Python back-end records two extra data sets:

- **Upmarks** – step indices where the path moves North.
- **Inside corners** – the East→North transitions.

Enable the annotations via scoped TikZ keys:

```tex
\drawLatticePath[
  lplpath/label upmarks,
  lplpath/show inside corners,
]{demo}
```

`lplpath/label upmarks` places small node labels halfway through every North
step. `lplpath/show inside corners` fills each inside corner in red and prints
its coordinates using the default styling from `lpmres-lpath.code.tex`.

You can customize the appearance of these labels:

```tex
\drawLatticePath[
  lplpath/label upmarks,
  lplpath/upmark label style={scale=1.2, font=\bfseries},
  lplpath/show inside corners,
  lplpath/inside corner label style={blue, scale=1.0},
]{demo}
```

Need a single corner? Use the explicit helper:

```tex
\highlightInsideCorner[blue]{demo}{2} % second inside corner
```

The style argument defaults to `red`. Corner indices start at 1 (matching the
order stored in the cache).
