"""Which `<id>#<x>` link forms media.lua leaves alone and bad_links() passes.

A link to a real document whose fragment has a character outside
`[A-Za-z0-9_-]` (a question id has a colon) is neither rewritten nor
validated, so it ships as a relative link that 404s on the site.

Run from the scratch tree's root after T2, with PANDOC set:
python -X utf8 link_gap_probe.py
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import test_lab_handbook as t  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    a, b = Path(d) / "a.md", Path(d) / "b.md"
    a.write_text("::: {.question #a:q1}\nWords.\n:::\n\n## H {#x}\n", encoding="utf-8")
    text = "[colon](a#a:q1) [dot](a#x.y) [slash](a/#x) [ok](a#x)\n"
    b.write_text(text, encoding="utf-8")
    print("bad_links:", t.bad_links(t.sources({"a": {"path": a}, "b": {"path": b}})))
out = subprocess.run([t.PANDOC, "-f", t.render.FROM, "--lua-filter", str(t.MEDIA),
                      "-M", "library-url=" + t.render.LIBRARY_URL, "-t", "html"],
                     input=text, capture_output=True, encoding="utf-8").stdout
print("html:", out.strip())
