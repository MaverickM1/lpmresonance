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

## Remote Install from GitHub

The installer downloads the package, sets up the Python package, copies the TeX
files into your TEXMF tree, and runs a verification build. TeX Live and Python
3.9+ must already be installed.

One-line install:

```bash
curl -fsSL https://raw.githubusercontent.com/MaverickM1/lpmresonance/main/scripts/install-from-github.sh | bash
```

Two-step install:

```bash
curl -fsSL https://raw.githubusercontent.com/MaverickM1/lpmresonance/main/scripts/install-from-github.sh -o install-lpm.sh
bash install-lpm.sh
```

Installing a specific version or branch:

```bash
bash install-lpm.sh v0.0.1  # tagged release
bash install-lpm.sh dev     # development branch
```

The installer will:

1. Download the specified version (default: `main` branch)
2. Extract to a temporary directory
3. Run the platform-specific install script
4. Clean up all temporary files on exit

**Security note**: This method downloads and executes a shell script. Review the
script before running if you have security concerns:

```bash
curl -fsSL https://raw.githubusercontent.com/MaverickM1/lpmresonance/main/scripts/install-from-github.sh
```

## Compilation

This is a PythonTeX package. After installation, compile with the standard 3-step workflow:

```bash
pdflatex -shell-escape demo.tex
pythontex demo
pdflatex -shell-escape demo.tex
```

**What happens:**
1. First `pdflatex` extracts Python code into `demo.pytxcode`
2. `pythontex` executes the Python, writes results to `lp-cache/`
3. Second `pdflatex` reads the cached data and renders the diagrams

This is the standard PythonTeX workflow used by all PythonTeX packages.

## latexmk Setup (Optional) {#latexmk-setup}

For automated compilation, configure latexmk to run pythontex automatically.

### Global Configuration (Recommended)

Add the PythonTeX rule to your `~/.latexmkrc`:

```perl
# PythonTeX support
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex { return system("pythontex", $_[0]); }
```

Then compile with:

```bash
latexmk -pdf -shell-escape demo.tex
```

This configures latexmk once for all projects.

### Installer-Configured latexmkrc

The `scripts/install.sh` installer automatically appends the PythonTeX rule to
`~/.latexmkrc`. On macOS systems where `python` is not available (only `python3`),
the installer configures the rule with explicit interpreter paths:

```perl
# PythonTeX support (added by lpmresonance installer)
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex {
    system("python3 /path/to/pythontex --interpreter 'python:python3' \"\$_[0]\"");
}
```

The `--interpreter` flag tells PythonTeX to use `python3` for executing Python
code blocks, avoiding the "python: No such file or directory" error that occurs
when the `pythontex` script's shebang (`#!/usr/bin/env python`) fails.

### Per-Project Configuration

For project-specific settings that override the global configuration, create a
`latexmkrc` in your document directory:

```perl
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -shell-escape %O %S';

add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex { return system("pythontex", $_[0]); }

$clean_ext .= ' %R.pytxcode pythontex-files-%R';
```

This is only necessary if you need settings different from the global `~/.latexmkrc`.

## Local Install from Clone

If you have already cloned the repository, run the install script:

```bash
# macOS / Linux
./scripts/install.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-windows.ps1
```

For manual installation steps, see below.

## Manual Wiring

### Install the Python package

From a clone of this repository:

```bash
pip install -e .
```

Editable installs keep the `lpm_paths` module in sync with your working tree.
Replace `-e` with `--user` for a user-level install, or omit both flags when
installing inside a virtual environment.

### Make the LaTeX files discoverable

The TeX layer lives under `tex/latex/lpmres`. Options:

1. **Copy into a personal TEXMF tree** (TeX Live):
   ```bash
   mkdir -p ~/texmf/tex/latex/lpmres
   cp -R tex/latex/lpmres/* ~/texmf/tex/latex/lpmres/
   mktexlsr ~/texmf
   ```

2. **Extend `TEXINPUTS`** for a specific project:
   ```bash
   export TEXINPUTS="./tex/latex/lpmres:$TEXINPUTS"
   ```

Either approach works so long as `\usepackage{lpmresonance}` can find the
`.sty` and `.code.tex` files.

### Cache directory

The Python back-end writes into `lp-cache/` (relative to the working directory).
Ensure the user running LaTeX has write access there. You can remove the
directory at any time; the data is recreated automatically on the next build.
