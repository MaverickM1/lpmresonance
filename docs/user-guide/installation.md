---
title: Installation
---

# Installation

The project ships as a hybrid LaTeX/Python package. You need TeX to find the `.sty`
files **and** you need Python to execute the back-end that emits coordinates. Make
sure both halves are ready before compiling any document.

## Requirements

- Python **3.9–3.13** with `pip`. We test under Linux and macOS, but the code is
  pure Python and works everywhere PythonTeX runs.
- TeX Live **2022 or newer** (or an equivalent distribution) with the
  `pythontex` package installed.
- Ability to invoke LaTeX with `-shell-escape` (PythonTeX fails without it).

You can double-check your toolchain with:

```bash
python3 -V
pythontex --version
kpsewhich pythontex.sty
```

## Install the Python package

From a clone of this repository:

```bash
pip install -e .
```

Editable installs keep the CLI entry points (if any) and the `lpm_paths`
module in sync with your working tree, which is ideal while editing the
package or running the examples. Replace `-e` with `--user` for a user-level
install, or omit both flags when installing inside a virtual environment.

## Make the LaTeX files discoverable

The TeX layer lives under `tex/latex/lpmres`. You have two easy options:

1. **Copy into a personal TEXMF tree**. For example on TeX Live:
   ```bash
   mkdir -p ~/texmf/tex/latex/lpmres
   cp -R tex/latex/lpmres/* ~/texmf/tex/latex/lpmres/
   mktexlsr ~/texmf
   ```
2. **Extend `TEXINPUTS`** inside your project or `latexmkrc`. The examples in
   this repo prepend the repo-local directory so you can compile in-place:
   ```perl
   # examples/latexmkrc
   $ENV{"TEXINPUTS"} = join(':', '../tex/latex/lpmres', $ENV{"TEXINPUTS"} // '');
   ```

Either approach works so long as `\usepackage{lpmresonance}` can find the
`.sty` and `.code.tex` files.

## Configure latexmk / PythonTeX

Enable shell escape and register PythonTeX as a custom dependency. The snippet
below is the minimal set we ship in `examples/latexmkrc`:

```perl
$force_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -shell-escape %O %S';
add_cus_dep('pytxcode','tex',0,'pythontex');
sub pythontex { return system("pythontex \"$_[0]\""); }
$clean_ext .= ' %R.pytxcode %R.pytxmcr pythontex-files-%R';
```

Point `pythontex` at whatever interpreter hosts the `lpm_paths` package. When
latexmk runs it will call:

1. `pdflatex` to produce `.pytxcode`.
2. `pythontex` to execute the snippets embedded in your document.
3. `pdflatex` again to include the cache files emitted by Python.

## Cache directory

By default the Python back-end writes into `lp-cache/` (relative to the working
directory). Ensure the user running LaTeX has write access there. You can remove
the directory at any time; the data is recreated automatically on the next build.
