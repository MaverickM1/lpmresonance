---
title: FAQ
---

# Frequently Asked Questions

**Do I have to run Python manually?**  
No. `\lpDeclarePath` and `\shadeBetweenBits` embed small PythonTeX blocks in
your document. When you call `latexmk -pdf -shell-escape <file>`, latexmk
invokes `pythontex` on your behalf. The only time you run `pythontex` directly
is when debugging (e.g., to inspect `pythontex.log`).

**Where are the generated files stored?**  
Under `lp-cache/` in the directory where LaTeX runs. The files are
content-addressed and safe to delete. Use `./scripts/clean-cache.sh` for a full
reset or remove individual `path-*` / `between-*` files if you only want to
invalidate one declaration.

**Should I commit the cache to version control?**  
No. Add `lp-cache/` to `.gitignore`. The files speed up recompilation but are
fully reproducible from the source document.

**What happens if I declare the same path twice?**  
Reusing the same sanitized name overwrites the cached macros. The package emits
a warning so you can confirm whether the collision is intentional. Use distinct
names (or add prefixes) to keep data sets separate.

**Can I script against the JSON manifest?**  
Yes. Every path declaration writes `path-<safe>-<hash>.json` alongside the TeX
file. You can load it with `python -m json.tool lp-cache/path-*.json` or with
your own tooling. See `python/lpm_paths/api.py` for the schema.

**Where do I learn about upcoming compatibility changes?**  
Check [`docs/developer-guide/upgrade-notes.md`](developer-guide/upgrade-notes.md).
We mirror its highlights on the project README, but the upgrade notes are the
authoritative source for Python/TeX policy changes such as the move to
`annotationlib` once Python ≥3.14 becomes the baseline.
