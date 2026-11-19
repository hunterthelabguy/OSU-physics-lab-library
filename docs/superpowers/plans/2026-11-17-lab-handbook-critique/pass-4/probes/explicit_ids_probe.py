"""The fix for bad_links() accepting generated identifiers, tried in this
process only: parsed() reads with `-auto_identifiers`, so only an explicit
`{#...}` (or a div's or span's id) counts. Checks the fixture forms and
every real source (after T4, Lab 3's two links must still resolve).

Run from the scratch tree's root after T4, with PANDOC set:
python -X utf8 explicit_ids_probe.py
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import test_lab_handbook as t  # noqa: E402

base = t.render.FROM
for label, frm in (("as written", base), ("-auto_identifiers", base + "-auto_identifiers")):
    t.render.FROM = frm
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d) / "a.md", Path(d) / "b.md"
        a.write_text("## Heading {#x}\n\n## Plain Heading\n", encoding="utf-8")
        b.write_text("[ok](a#x) [auto](a#plain-heading)\n", encoding="utf-8")
        fixture = t.bad_links(t.sources({"a": {"path": a}, "b": {"path": b}}))
    real = t.bad_links(t.sources())
    print("{:18} fixture bad: {}   real tree bad: {}".format(label, fixture, real))
t.render.FROM = base
