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
python -V  # or python3 -V
pythontex --version
kpsewhich pythontex.sty
```

## Scripted install (recommended)

The installer scripts set up the Python package, copy the TeX files into your
TEXMF tree, and run a small verification build. TeX Live and Python 3.9+ must
already be installed.

```bash
# macOS
./scripts/install-macos.sh

# Linux
./scripts/install-linux.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-windows.ps1
```

If you need manual wiring (deprecated), follow the steps below.

## Manual wiring (deprecated)

### Install the Python package

From a clone of this repository:

```bash
pip install -e .
```

Editable installs keep the CLI entry points (if any) and the `lpm_paths`
module in sync with your working tree, which is ideal while editing the
package or running the examples. Replace `-e` with `--user` for a user-level
install, or omit both flags when installing inside a virtual environment.

### Make the LaTeX files discoverable

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

### Configure latexmk for PythonTeX

The package includes a pre-configured `latexmkrc` that automatically handles the
PythonTeX build process. You can either **copy it** or **write your own**.

### Option 1: Use the included configuration (recommended)

Copy `examples/latexmkrc` to your document directory and adjust `TEXINPUTS` if
needed:

```bash
cp examples/latexmkrc .
```

This configuration:
- Sets `TEXINPUTS` to find the package files
- Enables `-shell-escape` for PythonTeX and minted
- Automatically runs PythonTeX when `.pytxcode` files are generated
- Uses `python`, falling back to `python3` if needed (ensure it resolves to Python 3)
- Cleans up auxiliary files properly

With this in place, you can simply run:

```bash
latexmk -pdf yourfile.tex
```

The build process is fully automated:
1. First `pdflatex` run generates `.pytxcode` files
2. `pythontex` executes Python code and creates cache files
3. Subsequent `pdflatex` runs incorporate the cached coordinates
4. Cross-references are resolved automatically

### Option 2: Custom configuration

If you need custom settings, here's the minimal configuration:

```perl
# Set TEXINPUTS to find lpmresonance package (adjust path as needed)
$ENV{"TEXINPUTS"} = "path/to/tex/latex/lpmres:" . ($ENV{"TEXINPUTS"} // "");

# Enable shell-escape and register PythonTeX
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -shell-escape %O %S';

add_cus_dep('pytxcode', 'tex', 0, 'run_pythontex');
sub run_pythontex {
    return system("python /Library/TeX/texbin/pythontex --interpreter python:python \"$_[0]\"");
}

$clean_ext .= ' %R.pytxcode pythontex-files-%R';
$max_repeat = 5;
```

Adjust the `pythontex` path and interpreter to match your system.

### Cache directory

By default the Python back-end writes into `lp-cache/` (relative to the working
directory). Ensure the user running LaTeX has write access there. You can remove
the directory at any time; the data is recreated automatically on the next build.
