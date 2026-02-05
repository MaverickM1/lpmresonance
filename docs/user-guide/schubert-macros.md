---
title: Schubert macros
---

# Schubert macros

The package ships with a lightweight drawing environment tailored to the
Schubert calculus diagrams common in lattice-path proofs. Use it whenever you
need consistent axes, grids, and scaling without retyping boilerplate TikZ code.

## `schubertpic` environment

Defined in `tex/latex/lpmres/lpmres-pic.code.tex`:

```tex
\newenvironment{schubertpic}[1][]{
  \begin{tikzpicture}[x=0.6cm,y=0.6cm,#1]
  \draw[gray!30] (0,0) grid +(20,20);
  \draw[->] (0,0)--+(21,0); \draw[->] (0,0)--+(0,21);
}{
  \end{tikzpicture}
}
```

- Optional argument `[#1]` is forwarded to `tikzpicture`, so you can override
  the scale, baseline, or add TikZ libraries.
- The default grid covers a 20×20 box and includes axes with arrow tips.

Example:

```tex
\begin{schubertpic}[x=0.5cm,y=0.5cm]
  \drawGrid{demo}
  \drawLatticePath[
    lplpath/label upmarks,
    lplpath/show inside corners,
  ]{demo}
\end{schubertpic}
```

## Customizing the background

Because the environment is a thin wrapper, you can copy it and adjust the grid
size, colors, or decorations:

```tex
\newenvironment{smallschubert}[1][]{
  \begin{tikzpicture}[x=0.4cm,y=0.4cm,#1]
  \draw[gray!20] (0,0) grid +(12,12);
  \draw[->] (0,0)--+(13,0); \draw[->] (0,0)--+(0,13);
}{
  \end{tikzpicture}
}
```

Pair `\drawGrid{<name>}` with these environments so the lattice path matches the
bounding box implied by the bit string.

## Combining with between regions

`schubertpic` works equally well for between-region visualizations:

```tex
\shadeBetweenBits{00110101}{01011001}{L}{U}
\begin{schubertpic}[x=0.5cm,y=0.5cm]
  \shadeBetween[gray!15]{L}{U}
  \drawBetween[lp/path]{L}{U}
\end{schubertpic}
```

Use TikZ layering (`\begin{scope}[on background layer]`) if you need to mix
multiple regions or additional annotations inside the same environment.
