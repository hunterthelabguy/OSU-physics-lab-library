"""Do the rendered non-label headings equal the source's ATX headings, level for level, in every source?"""
import re, sys
from pathlib import Path
sys.path.insert(0, "tests")
import test_headings as th
bad = 0
for p in sorted(Path("curriculum").glob("*/*.md")):
    atx, fenced = [], False
    for line in p.read_text(encoding="utf-8").split("\n"):
        if line.startswith("```"): fenced = not fenced
        m = None if fenced else re.match(r"^(#{1,6}) ", line)
        if m: atx.append(len(m.group(1)))
    rendered = [lvl for lvl, kind, _ in th.headings(p) if kind != "label"]
    if atx != rendered: bad += 1; print("differs", p.stem, atx, rendered)
print("sources differing:", bad)
