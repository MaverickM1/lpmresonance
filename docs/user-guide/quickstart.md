---
title: Quickstart
---

# Quickstart

This guide walks through a minimal lattice-path figure end-to-end: declare a
path in Python, draw it with TikZ, and shade the region between two paths.
Make sure you followed the [installation guide](installation.md) first.

## 1. Create a document

Save the following snippet as `examples/hello.tex`. It is the same file used in
`examples/example.tex`, trimmed down to the essentials:

```tex
\documentclass{article}
\usepackage{lpmresonance}

\begin{document}

\lpDeclarePath{demo}{01011010}
\begin{schubertpic}
  \drawGrid{demo}
  \drawLatticePath[lplpath/label upmarks]{demo}
\end{schubertpic}

\shadeBetweenBits{00110101}{01011001}{L}{U}
\begin{schubertpic}
  \shadeBetween[gray!20]{L}{U}
  \drawBetween[thick]{L}{U}
\end{schubertpic}

\end{document}
```

`\lpDeclarePath` (and `\shadeBetweenBits`) call into the Python package through
PythonTeX. They emit small `.tex` files holding coordinates and register them in
the `lp-cache/` directory.

## 2. Compile with latexmk

From the example directory run:

```bash
latexmk -pdf -shell-escape hello.tex
```

**That's it!** With the `latexmkrc` configuration from the installation guide,
latexmk automatically:
1. Runs `pdflatex` to generate `.pytxcode` files
2. Detects the `.pytxcode` and runs `pythontex` to execute Python code
3. Runs `pdflatex` again to incorporate the generated coordinates
4. Resolves cross-references with additional passes as needed

You should see output like:

```
This is PythonTeX 0.18
...
PythonTeX:  hello - 0 error(s), 0 warning(s)
...
Output written on hello.pdf (X pages, XXXXX bytes)
```

If you see warnings like "not ready; run pythontex and recompile", verify that:
- The `latexmkrc` file is in your document directory (or project root)
- The `-shell-escape` flag is enabled
- `python3` is in your PATH

## 3. Inspect the cache

After a successful build the working tree contains:

- `lp-cache/path-demo-*.tex` — TeX macros for your path.
- `lp-cache/path-demo-*.json` — machine-readable data (used by tooling/tests).
- `lp-cache/between-L-U-*.tex` — polygon coordinates for the between region.

These cache files are content-addressed. Editing the bit string or the path
name yields a new hash and therefore a new file. You can delete the entire
`lp-cache/` directory whenever you need a clean rebuild.

## 4. Iterate

Recompile the document after changing either the TeX markup or the Python
source. The renderer automatically reuses existing cache entries so subsequent
builds are much faster than the first run.
