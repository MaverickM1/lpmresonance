---
title: Quickstart
---

# Quickstart

This guide walks through a minimal lattice-path figure end-to-end: declare a
path in Python, draw it with TikZ, and shade the region between two paths.
Make sure you followed the [installation guide](installation.md) first.

## 1. Create a document

Save the following snippet as `hello.tex`:

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

## 2. Compile

Use the standard PythonTeX 3-step workflow:

```bash
pdflatex -shell-escape hello.tex
pythontex hello
pdflatex -shell-escape hello.tex
```

**What happens:**
1. First `pdflatex` extracts Python code into `hello.pytxcode`
2. `pythontex` executes the Python, writes results to `lp-cache/`
3. Second `pdflatex` reads the cached data and renders the diagrams

You should see output like:

```
This is PythonTeX 0.18
...
PythonTeX:  hello - 0 error(s), 0 warning(s)
```

**Expected output:**
- A PDF file (`hello.pdf`) containing your lattice path diagrams
- The first diagram shows a grid with the path for `01011010`
- The second diagram shows the shaded region between two paths

**Expected generated files:**
- `lp-cache/path-demo-*.tex` — TeX coordinate macros for your path
- `lp-cache/path-demo-*.json` — machine-readable path data
- `lp-cache/between-L-U-*.tex` — polygon coordinates for the between region
- `pythontex-files-hello/` — PythonTeX working directory

If you see warnings like "not ready; run pythontex and recompile", verify that:
- You ran all three commands in order
- The `-shell-escape` flag is enabled
- Python 3.9+ is in your PATH

### Automated builds with latexmk (optional)

For automated compilation, add the PythonTeX rule to `~/.latexmkrc`:

```perl
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex { return system("pythontex", $_[0]); }
```

Then compile with a single command:

```bash
latexmk -pdf -shell-escape hello.tex
```

See [Installation: latexmk setup](installation.md#latexmk-setup) for details.

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
