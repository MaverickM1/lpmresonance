---
title: Examples Gallery
---

# Examples Gallery

The `examples/example-gallery.tex` file contains a collection of lpmresonance features. This page highlights key examples with minimal code snippets.

> **Tip**: Compile the full gallery with: `cd examples && latexmk -pdf -shell-escape example-gallery.tex`

## Basic Path Drawing

Declare and draw a simple lattice path:

```latex
\lpDeclarePath{S1}{0010011001}
\begin{tikzpicture}
  \drawGrid{S1}
  \drawLatticePath{S1}
\end{tikzpicture}
```

**Features shown:**
- Path declaration from bit string (0=East, 1=North)
- Grid drawing with automatic bounds
- Basic path rendering

## Styled Paths

Apply TikZ styling to paths:

```latex
\lpDeclarePath{RedPath}{0110}
\drawLatticePath[red, line width=2pt]{RedPath}

\lpDeclarePath{BluePath}{1001}
\drawLatticePath[blue, dashed, line width=1.5pt]{BluePath}
```

**Features shown:**
- Color customization
- Line width and style (dashed, dotted, solid)
- Multiple paths in one diagram

## Upmark Labels

Show step indices at each North step:

```latex
\lpDeclarePath{Path}{0010011001}
\drawLatticePath[lplpath/label upmarks]{Path}
```

**Features shown:**
- `lplpath/label upmarks` option
- Automatic step numbering
- Useful for identifying specific positions

## Inside Corners

Visualize and highlight inside corners (East→North transitions):

```latex
\lpDeclarePath{IC}{10010010}
\drawLatticePath[lplpath/show inside corners]{IC}

% Or highlight a specific corner
\highlightInsideCorner[orange]{IC}{1}  % 1st corner
```

**Features shown:**
- `lplpath/show inside corners` to show all corners
- `\highlightInsideCorner` for selective highlighting
- 1-based indexing for corners

## Shading Between Paths

Shade the region between two paths:

```latex
\lpDeclarePath{Lower}{000111}
\lpDeclarePath{Upper}{110001}

\shadeBetweenBits{000111}{110001}{Lower}{Upper}
\begin{tikzpicture}
  \shadeBetween[fill=yellow!30]{Lower}{Upper}
  \drawLatticePath[red, very thick]{Lower}
  \drawLatticePath[blue, very thick]{Upper}
  \drawGrid{Lower}
\end{tikzpicture}
```

**Features shown:**
- `\shadeBetweenBits` to compute region polygon
- `\shadeBetween` to fill the region
- Paths must share start and end points

## Multiple Shaded Regions

Stack multiple shaded regions with different colors:

```latex
\lpDeclarePath{P1}{00001111}
\lpDeclarePath{P2}{00110011}
\lpDeclarePath{P3}{01010101}

\shadeBetweenBits{00001111}{00110011}{P1}{P2}
\shadeBetweenBits{00110011}{01010101}{P2}{P3}

\begin{tikzpicture}
  \shadeBetween[fill=red!10]{P1}{P2}
  \shadeBetween[fill=blue!10]{P2}{P3}
  \drawLatticePath[red, very thick, lplpath/label upmarks]{P1}
  \drawLatticePath[green!60!black, very thick, lplpath/label upmarks]{P2}
  \drawLatticePath[blue, very thick, lplpath/label upmarks]{P3}
  \drawGrid{P1}
\end{tikzpicture}
```

**Features shown:**
- Multiple `\shadeBetweenBits` declarations
- Layered shading with transparency
- Combining labels, shading, and styling

## Full Example

Combining all features:

```latex
% Declare three paths
\lpDeclarePath{Lower}{0000000011111111}
\lpDeclarePath{Middle}{0001011001101101}
\lpDeclarePath{Upper}{1010101110001100}

% Generate between regions
\shadeBetweenBits{0000000011111111}{0001011001101101}{Lower}{Middle}
\shadeBetweenBits{0001011001101101}{1010101110001100}{Middle}{Upper}

\begin{tikzpicture}
  % Shade regions
  \shadeBetween[fill=blue!10]{Lower}{Middle}
  \shadeBetween[fill=red!10]{Middle}{Upper}
  
  % Draw paths with labels
  \drawLatticePath[blue, very thick, lplpath/label upmarks]{Lower}
  \drawLatticePath[purple, very thick, lplpath/label upmarks]{Middle}
  \drawLatticePath[red, very thick, lplpath/label upmarks]{Upper}
  
  % Highlight specific corners
  \highlightInsideCorner[red!70]{Upper}{1}
  \highlightInsideCorner[red!70]{Upper}{3}
\end{tikzpicture}
```

**Features shown:**
- Three-path system with two shaded regions
- Upmark labels on all paths
- Selective corner highlighting
- Color coordination

## Using Python Code

Generate paths programmatically with PythonTeX:

```latex
\begin{pycode}
from lpm_paths.types import LatticePath
from itertools import combinations

lower = LatticePath.from_bits("00010111")
upper = LatticePath.from_bits("10111000")

# Find all paths between bounds
paths = []
for ones_positions in combinations(range(8), 4):
    bits = ['0'] * 8
    for pos in ones_positions:
        bits[pos] = '1'
    curr_path = LatticePath.from_bits(''.join(bits))
    if all(lower.coords[i][1] <= curr_path.coords[i][1] <= upper.coords[i][1]
           for i in range(len(curr_path.coords))):
        paths.append(''.join(bits))

# Generate TeX code
print(r"\begin{tikzpicture}")
for i, bitstring in enumerate(paths[:10]):
    print(rf"\lpDeclarePath{{path{i}}}{{{bitstring}}}")
    print(rf"\drawLatticePath[opacity=0.5]{{path{i}}}")
print(r"\end{tikzpicture}")
\end{pycode}
```

**Features shown:**
- Direct Python computation with `lpm_paths` module
- Generating multiple paths algorithmically
- Emitting TeX code from Python

## See Also

- [Lattice Path Macros](lattice-path-macros.md) - Detailed macro reference
- [Shading Between Paths](shading-between-paths.md) - Region computation details
- [Options and Keys](options-and-keys.md) - All styling options
- `examples/example-gallery.tex` - Full compilable gallery with 40+ examples
