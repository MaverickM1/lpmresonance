import json
from pathlib import Path
from lpm_paths.cache import Cache
from lpm_paths.emitters.tex import TeXEmitter


def make_emitter(tmp_path):
    cache = Cache.make(str(tmp_path / "cache"))
    return cache, TeXEmitter(cache)


def test_write_path_creates_files_and_macros(tmp_path):
    cache, emitter = make_emitter(tmp_path)
    g1, g2, g3 = emitter.write_path("0101", " Demo Name ")
    tex_file = next((tmp_path / "cache").rglob("path-*.tex"))
    json_file = next((tmp_path / "cache").rglob("path-*.json"))
    safe = "Demo_Name"
    expected_tex = cache.tex_path(str(tex_file))
    expected_json = cache.tex_path(str(json_file))
    assert g1 == f"\\gdef\\lp@pathfile@{safe}{{{expected_tex}}}"
    assert g2 == f"\\gdef\\lp@pathjson@{safe}{{{expected_json}}}"
    assert g3 == f"\\gdef\\lp@lastdeclaredpathfile{{{expected_tex}}}"
    tex_body = tex_file.read_text()
    assert f"\\csname lp@path@coords@{safe}" in tex_body
    assert f"\\gdef\\lp@path@ready@{safe}{{1}}" in tex_body
    data = json.loads(json_file.read_text())
    assert data["name"] == " Demo Name "
    assert data["bits"] == "0101"
    assert data["coords"][0] == [0, 0]


def test_write_between_records_polygon(tmp_path):
    cache, emitter = make_emitter(tmp_path)
    gdef = emitter.write_between("0011", "0101", " L ", " U ")
    between_file = next((tmp_path / "cache").rglob("between-*.tex"))
    expected = cache.tex_path(str(between_file))
    assert gdef == f"\\gdef\\lp@lastdeclaredbetweenfile{{{expected}}}"
    body = between_file.read_text()
    assert "\\gdef\\lp@between@coords" in body
    assert "\\gdef\\lp@between@ready@L@U{1}" in body
