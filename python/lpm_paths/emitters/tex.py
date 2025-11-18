from __future__ import annotations
import json
import os
from typing import List, Tuple
from ..cache import Cache, atomic_write
from ..manifest import to_json_obj
from ..sanitize import _sanitize_name
from ..hashing import key_of
from ..version import EMITTER_VERSION
from ..types import LatticePath

def _formatCoords(coords: List[Tuple[int, int]]) -> str:
    return " ".join(f"({x},{y})" for (x, y) in coords)

def _gdef(name: str, value: str) -> str:
    return f"\\gdef\\{name}{{{value}}}"

class TeXEmitter:
    def __init__(self, cache: Cache) -> None:
        self.cache = cache

    def _tex_path(self, path: str) -> str:
        return self.cache.tex_path(path)

    def _safe_name_warning(self, kind: str, safe: str, original: str | None) -> str:
        prior = self._record_safe_name(kind, safe, original or "")
        if prior is None or prior == (original or ""):
            return ""
        return f"\\PackageWarning{{lpmresonance}}{{Sanitized {kind} name '{safe}' collides with another declaration; later data overwrites earlier results.}}\n"

    def _record_safe_name(self, kind: str, safe: str, original: str) -> str | None:
        rel_path = os.path.join(".names", kind, f"{safe}.json")
        meta_path = self.cache.file(rel_path)
        prior: str | None = None
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                prior = data.get("original")
            except Exception:
                prior = None
        if prior == original:
            return None
        payload = {"original": original}
        atomic_write(meta_path, json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return prior

    def write_path(self, bits: str, name: str, cache_id: str | None = None) -> tuple[str, str, str]:
        safe = _sanitize_name(name)
        payload = {"op": "declare_path", "bits": bits, "name": name, "ver": EMITTER_VERSION, "cache_id": cache_id or ""}
        key = key_of(payload)
        texname = f"path-{safe}-{key}.tex"
        jsonname = f"path-{safe}-{key}.json"
        texpath = self.cache.file(texname)
        jsonpath = self.cache.file(jsonname)
        lp = LatticePath.from_bits(bits)
        
        # Compute grid dimensions: (num_zeros, num_ones)
        num_ones = bits.count('1')
        num_zeros = bits.count('0')
        
        body = ["\\makeatletter"]
        body.append(f"\\expandafter\\gdef\\csname lp@path@coords@{safe}\\endcsname{{{_formatCoords(lp.coords)}}}")
        if lp.upmarks:
            upstr = ",".join(str(i) for i in lp.upmarks)
            body.append(f"\\expandafter\\gdef\\csname lp@path@upmarks@{safe}\\endcsname{{{upstr}}}")
            # Generate node commands for upmark labels with clean rational coordinates
            label_cmds = []
            for idx in lp.upmarks:
                prev_coord = lp.coords[idx - 1]
                curr_coord = lp.coords[idx]
                mid_x = (prev_coord[0] + curr_coord[0]) / 2.0
                mid_y = (prev_coord[1] + curr_coord[1]) / 2.0
                # Format with :g to remove trailing zeros (2.0 -> 2, 0.5 -> 0.5)
                label_cmds.append(f"\\node[anchor=west,scale=0.85,font=\\scriptsize] at ({mid_x:g},{mid_y:g}) {{{idx}}};%\n")
            labels_str = "".join(label_cmds)
            body.append(f"\\expandafter\\gdef\\csname lp@path@upmarklabels@{safe}\\endcsname{{{labels_str}}}")
        
        # Inside corners: emit indices and generate visualization commands
        if lp.insideCorners:
            cornerstr = ",".join(str(i) for i in lp.insideCorners)
            body.append(f"\\expandafter\\gdef\\csname lp@path@insidecorners@{safe}\\endcsname{{{cornerstr}}}")
            body.append(f"\\expandafter\\gdef\\csname lp@path@insidecornercount@{safe}\\endcsname{{{len(lp.insideCorners)}}}")
            
            # Generate fill and node commands for ALL inside corners (for batch display)
            corner_cmds = []
            for idx in lp.insideCorners:
                coord = lp.coords[idx]
                x, y = coord[0], coord[1]
                corner_cmds.append(f"\\fill[red] ({x},{y}) circle (2pt);%\n")
                corner_cmds.append(f"\\node[anchor=south east,scale=0.85,font=\\scriptsize] at ({x},{y}) {{\\scriptsize ({x},{y})}};%\n")
            corners_str = "".join(corner_cmds)
            body.append(f"\\expandafter\\gdef\\csname lp@path@insidecornerlabels@{safe}\\endcsname{{{corners_str}}}")
            
            # Generate individual coordinate macros for EACH inside corner (1-based indexing for users)
            # Store just the coordinate so TeX can apply custom styling
            for corner_num, idx in enumerate(lp.insideCorners, start=1):
                coord = lp.coords[idx]
                x, y = coord[0], coord[1]
                body.append(f"\\expandafter\\gdef\\csname lp@path@insidecornercoord@{safe}@{corner_num}\\endcsname{{({x},{y})}}")
        
        body.append(f"\\expandafter\\gdef\\csname lp@path@gridsize@{safe}\\endcsname{{({num_zeros},{num_ones})}}")
        body.append(f"\\expandafter\\gdef\\csname lp@path@ready@{safe}\\endcsname{{1}}")
        body.append("\\makeatother")
        atomic_write(texpath, "\n".join(body) + "\n")
        atomic_write(
            jsonpath,
            json.dumps(to_json_obj(name, lp), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False),
        )
        warn = self._safe_name_warning("path", safe, name)
        g1 = "\\makeatletter\n" + _gdef(f"lp@pathfile@{safe}", self._tex_path(texpath)) + "\n\\makeatother"
        if warn:
            g1 = f"{warn}{g1}"
        return (
            g1,
            "\\makeatletter\n" + _gdef(f"lp@pathjson@{safe}", self._tex_path(jsonpath)) + "\n\\makeatother",
            "\\makeatletter\n" + _gdef("lp@lastdeclaredpathfile", self._tex_path(texpath)) + "\n\\makeatother",
        )

    def write_between(self, L_bits: str, U_bits: str, lname: str, uname: str) -> str:
        from ..between import between_polygon
        Ls, Us = _sanitize_name(lname), _sanitize_name(uname)
        payload = {"op": "between", "L": L_bits, "U": U_bits, "ver": EMITTER_VERSION}
        key = key_of(payload)
        texname = f"between-{Ls}-{Us}-{key}.tex"
        texpath = self.cache.file(texname)
        poly = between_polygon(L_bits, U_bits)
        coords_str = _formatCoords(poly)
        body = [
            "\\makeatletter",
            f"\\expandafter\\gdef\\csname lp@between@coords@{Ls}@{Us}\\endcsname{{{coords_str}}}",
            f"\\gdef\\lp@between@coords{{{coords_str}}}",
            f"\\expandafter\\gdef\\csname lp@between@ready@{Ls}@{Us}\\endcsname{{1}}",
            "\\makeatother",
        ]
        atomic_write(texpath, "\n".join(body) + "\n")
        return "\\makeatletter\n" + _gdef("lp@lastdeclaredbetweenfile", self._tex_path(texpath)) + "\n\\makeatother"
