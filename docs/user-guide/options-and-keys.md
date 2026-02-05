---
title: Options and keys
---

# Options and keys

All drawing macros ultimately defer to TikZ. You can replace or extend every
style we ship by calling `\tikzset` in your document preamble.

## Built-in TikZ styles

`lpmres-base.code.tex` and `lpmres-lpath.code.tex` define the following styles:

| Style                | Default definition                              | Used by                     |
|----------------------|--------------------------------------------------|-----------------------------|
| `lp/path`            | `line cap=round, line join=round`                | Every lattice path          |
| `lp/lpath`           | `thick, red`                                     | `\drawLatticePath`          |
| `lp/named`           | `thick, red` (legacy alias)                      | Backwards compatibility     |
| `lp/schubert`        | `very thick, blue`                               | Reserved for Schubert pics  |
| `lp/step mark`       | `black, fill=white`                              | Step mark dots              |
| `lp/upmark label`    | `anchor=west, scale=0.85, font=\scriptsize`      | Upmark number labels        |

You can override them globally:

```tex
\tikzset{
  lp/lpath/.style = {ultra thick, teal},
  lp/path/.style = {line cap=butt},
  lp/step mark/.style = {orange, fill=orange!30},
  lp/upmark label/.style = {scale=1.2, font=\bfseries},
}
```

## `lplpath` option family

`\drawLatticePath` temporarily activates the local key family `lplpath`. The
following flags are available:

- `lplpath/label upmarks` — emit numbered labels halfway along each North step.
- `lplpath/show inside corners` — draw red disks + coordinate labels at every
  East→North transition.
- `lplpath/show endpoints` — mark the start and end points of the path.
- `lplpath/show step marks` — place dots at each lattice point (vertex) along the path, making step counting immediate when grids are not displayed.

Because the keys live inside a TeX group, the flags reset at the end of each
`\drawLatticePath` call. Mix them with normal TikZ keys:

```tex
\drawLatticePath[
  lplpath/label upmarks,
  lplpath/show step marks,
  densely dashed,
]{S}
```

### Customizing step marks and labels

The appearance of step marks and upmark labels can be customized using TikZ styles:

- `lplpath/step mark style={<tikz options>}` — customize the appearance of step mark dots (color, fill, size, etc.)
- `lplpath/upmark label style={<tikz options>}` — customize the appearance of upmark labels (font, scale, color, anchor, etc.)

Example:

```tex
\drawLatticePath[
  lplpath/show step marks,
  lplpath/step mark style={red, fill=yellow},
  lplpath/label upmarks,
  lplpath/upmark label style={scale=1.2, font=\bfseries},
]{MyPath}
```

## Grids and backgrounds

`lpmres-grid.code.tex` exposes `\drawGrid[<tikz opts>]{<safeName>}`. The grid is
computed from the cached path dimensions, so you never need to count bits by
hand. Combine it with the `schubertpic` environment (from
`lpmres-pic.code.tex`) to get a tidy plotting area:

```tex
\begin{schubertpic}[x=0.5cm,y=0.5cm,baseline=-0.5cm]
  \drawGrid[gray!40]{demo}
  \drawLatticePath{demo}
\end{schubertpic}
```

The optional argument is forwarded straight to TikZ, so you can adjust scaling,
baselines, or add extra options like `>=latex`.
