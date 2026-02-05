# Asset files for documentation

This directory contains images and other assets for the MkDocs documentation site.

## Adding Images

1. Place PNG/SVG files in this directory
2. Reference in Markdown: `![Alt text](assets/filename.png)`
3. For README (after GitHub Pages is deployed):
   ```markdown
   ![Example](https://maverickm1.github.io/lpmresonance/assets/filename.png)
   ```

## Recommended Image Workflow

1. Compile `examples/example-gallery.tex`
2. Convert PDF pages to PNG:
   ```bash
   pdftoppm -png -r 150 examples/example-gallery.pdf docs/assets/gallery
   # Creates gallery-1.png, gallery-2.png, etc.
   ```
3. Or take screenshots of specific figures
4. Commit and push — images will be available at the GitHub Pages URL
