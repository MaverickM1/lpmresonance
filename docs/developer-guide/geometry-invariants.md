---
title: Geometry invariants
---

# Geometry invariants

`lpm_paths.types.LatticePath` enforces several invariants to keep downstream
code simple and to catch malformed bit strings early.

## Coordinate construction

- The path starts at `(0, 0)` and includes **len(bits)+1** coordinates.
- `bits[i] == "0"` increments `x`; `"1"` increments `y`. No other characters are
  allowed.
- The final coordinate equals `(count("0"), count("1"))`. Any mismatch raises
  `InvariantError`.

## Upmarks and corners

- **Upmarks** record the 1-based index of every step where the path moves North.
- **Corners** record indices where the direction changes (either `N→E` or
  `E→N`).
- **Inside corners** record only `E→N` transitions. They are used to highlight
  North steps that start immediately after an East step.

The indices align with the step that ends at the corner. Example:

```
bits = 0101
coords = [(0,0), (1,0), (1,1), (2,1), (2,2)]
insideCorners = [1, 3]
```

## Ell-map (`ellmap`)

`ellmap[y]` records the maximum `x` observed the first time the path reaches
height `y`. It is computed by scanning coordinates once and filling any missing
levels down to zero. Consumers rely on this map to reason about Schubert cells
without reprocessing the entire coordinate list.

## Between polygons

`lpm_paths.between.between_polygon(L_bits, U_bits)` requires:

- Both paths start at `(0,0)` and end at the same coordinate.
- Inputs are valid bit strings (delegated to `LatticePath.from_bits`).
- The output polygon includes the upper path, the reversed lower path, and
  loops back to the starting point with adjacent duplicates removed.

These invariants guarantee the polygon is well-formed for TikZ plotting.
