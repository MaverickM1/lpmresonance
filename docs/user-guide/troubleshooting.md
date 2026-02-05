---
title: Troubleshooting
---

# Troubleshooting

Compilation problems almost always fall into one of the cases below. If you are
still stuck after walking through the checklist, please open an issue with your
`.log` file and the steps you already tried.

## "Data 'lp@path@coords@<name>' not ready"

This warning means the cached data file was not created. Common causes:

1. **PythonTeX did not run.** Make sure you ran all three commands:
   ```bash
   pdflatex -shell-escape demo.tex
   pythontex demo
   pdflatex -shell-escape demo.tex
   ```
   Running `pythontex demo` manually is a quick sanity check.

2. **Python crashed.** Inspect `pythontex-files-<jobname>/py_default_default.err` for
   tracebacks (e.g., syntax errors, missing packages).

3. **The cache directory is read-only.** Make sure `lp-cache/` is writable by
   the user running LaTeX.

Once the cause is fixed, re-run the 3-step compilation.

## "pythontex: command not found"

PythonTeX must be installed and in your PATH:

```bash
# Check if pythontex is available
pythontex --version

# If not found, check if it's installed but not in PATH
kpsewhich pythontex.py
```

On some systems, the command is `pythontex3` instead of `pythontex`.

## "-shell-escape" errors

The `-shell-escape` flag is required for PythonTeX:

```bash
# Correct:
pdflatex -shell-escape demo.tex

# Wrong (will fail):
pdflatex demo.tex
```

Some editors disable shell-escape by default for security. Check your editor settings.

## "ModuleNotFoundError: No module named 'lpm_paths'"

PythonTeX executes in a bare interpreter. Either install the package into that
environment (`pip install -e .`) or prepend the repository to `PYTHONPATH`
inside your TeX toolchain, e.g.

```perl
$ENV{"PYTHONPATH"} = join(':', "$ENV{PWD}/..", $ENV{"PYTHONPATH"} // '');
```

## Sanitized name collisions

If you reuse two TeX names that sanitize to the same identifier (e.g.,
`"demo-path"` and `"demo_path"`), the package prints:

```
Package lpmresonance Warning: Sanitized path name 'demo_path' collides...
```

Either change the user-facing name or pass more descriptive prefixes so the
sanitized strings become unique.

## Undefined control sequence `\shadeBetween`

TeX could not locate `lpmresonance.sty`. Verify that `tex/latex/lpmres` is part
of `TEXINPUTS` or installed in your personal TEXMF tree. `kpsewhich
lpmresonance.sty` should resolve to a path inside the repository (or inside your
texmf directory) before you attempt to compile.

## Grid or between-region commands draw nothing

`\drawGrid`, `\shadeBetween`, and `\drawBetween` are silent when the
corresponding cache entries do not exist. Confirm you called either
`\lpDeclarePath` or `\shadeBetweenBits` _earlier in the document_ and that those
commands executed during the latest PythonTeX run.

## Python version warnings

The supported interpreter range is Python **3.9–3.13**. Running inside newer
versions emits the policy reminder described in
[`developer-guide/upgrade-notes.md`](../developer-guide/upgrade-notes.md). Update
your virtual environment or follow the checklist in the upgrade notes before
attempting to drop `from __future__ import annotations`.
