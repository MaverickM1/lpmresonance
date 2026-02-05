---
title: TeX macro reference
---

# TeX macro reference

Quick lookup for the macros defined by `lpmresonance.sty` and the `.code.tex`
files under `tex/latex/lpmres`. See the user-guide pages for detailed
walkthroughs.

## Declaration macros

| Macro | Description |
|-------|-------------|
| `\lpDeclarePath{<name>}{<bits>}` | Calls PythonTeX to generate a lattice path, then registers the cache files. |
| `\shadeBetweenBits{<L bits>}{<U bits>}{<lname>}{<uname>}` | Computes the polygon between two bit strings and stores it under `<lname>/<uname>`. |

Both macros must run before you attempt to draw the corresponding data. They
print TeX glue produced by `lpm_paths.api` and immediately input the generated
files via `\lp@inputifready`.

## Drawing helpers

| Macro | Description |
|-------|-------------|
| `\drawLatticePath[<tikz opts>]{<name>}` | Draws the cached coordinates using the `lp/lpath` style plus any extra TikZ options. |
| `\drawGrid[<tikz opts>]{<name>}` | Draws a grid from `(0,0)` to the cached `(num_zeros,num_ones)` bounds. |
| `\shadeBetween[<tikz opts>]{<lname>}{<uname>}` | Fills the polygon between two previously declared paths. |
| `\drawBetween[<tikz opts>]{<lname>}{<uname>}` | Draws the polygon outline. |
| `\highlightInsideCorner[<style>]{<name>}{<index>}` | Highlights a specific inside corner by its 1-based index. |

### Option keys

`\drawLatticePath` installs a local `lplpath` key family:

- `lplpath/label upmarks` — label North steps with their index.
- `lplpath/show inside corners` — draw disks and coordinate labels on every
  East→North corner.
- `lplpath/show step marks` — place dots at each lattice point along the path.
- `lplpath/show endpoints` — mark the start and end points of the path.
- `lplpath/step mark style={<opts>}` — customize step mark appearance.
- `lplpath/upmark label style={<opts>}` — customize upmark label appearance.
- `lplpath/inside corner label style={<opts>}` — customize inside corner label appearance.

Standard TikZ options (e.g. `densely dashed`, `line width=1pt`) can be mixed in.

## Environment

| Environment | Description |
|-------------|-------------|
| `schubertpic` | Convenience wrapper around `tikzpicture` with pre-set scaling, a light grid, and axes. Pass normal TikZ options via the optional argument. |

Example:

```tex
\begin{schubertpic}[x=0.5cm,y=0.5cm,baseline=-0.5cm]
  \drawGrid{demo}
  \drawLatticePath[
    lplpath/label upmarks,
    lplpath/show inside corners,
  ]{demo}
\end{schubertpic}
```

## Low-level accessors

| Macro | Description |
|-------|-------------|
| `\lpBetweenCoords{<lname>}{<uname>}` | Expands to the stored coordinate list, or `(0,0)` when not ready. |
| `\lp@ensurebetweenplaceholder{<lname>}{<uname>}` | Pre-seeds the placeholder macros so TikZ has safe defaults on the first pass. |

These are primarily useful when you want to feed the coordinates into custom
TikZ/PGFPlots pipelines.
