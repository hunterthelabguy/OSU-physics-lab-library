"""Which link forms the plan's bad_links() (revision 2.3) flags, and what
media.lua does with each: the revision's DOC_TARGET widening, plus forms
it does not reach.

- auto: a link to a heading's generated identifier (no `{#...}` on it).
  Spec 4.4 says the test fails on "an address that is not one of that
  document's explicit identifiers"; parsed() reads Pandoc's tree, where a
  generated identifier looks like an explicit one.
- md / dirmd / slash / bare: a link aimed at another document in a form an
  author might type (a file name, a path, the page's own folder, no
  fragment). DOC_TARGET's comment says "any link aimed at another document".
- web / local / mail: must be left alone.

Run from the scratch tree's root after T2, with PANDOC set:
python -X utf8 link_forms_probe.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import test_lab_handbook as t  # noqa: E402

LINKS = {
    "explicit": "a#x",
    "auto": "a#plain-heading",
    "auto-en-dash": "a#appendix-reference-information",
    "md": "a.md#x",
    "dirmd": "../ph21x/a.md#x",
    "slash": "a/#x",
    "bare": "a",
    "colon": "a#a:q1",
    "web": "https://e.org/a#x",
    "local": "#x",
    "mail": "mailto:someone@example.org",
}
with tempfile.TemporaryDirectory() as d:
    a, b = Path(d) / "a.md", Path(d) / "b.md"
    a.write_text("## Heading {#x}\n\n## Plain Heading\n\n## Appendix – Reference Information\n\n"
                 "::: {.question #a:q1}\nWords.\n:::\n", encoding="utf-8")
    text = " ".join("[{}]({})".format(k, v) for k, v in LINKS.items()) + "\n"
    b.write_text(text, encoding="utf-8")
    bad = {target for _, target in t.bad_links(t.sources({"a": {"path": a}, "b": {"path": b}}))}
    _, idents = t.parsed(a)
html = subprocess.run([t.PANDOC, "-f", t.render.FROM, "--lua-filter", str(t.MEDIA),
                       "-M", "library-url=" + t.render.LIBRARY_URL, "-t", "html"],
                      input=text, capture_output=True, encoding="utf-8").stdout
print("identifiers parsed() reads on a.md:", sorted(idents))
for k, v in LINKS.items():
    rewritten = ('href="' + v + '"') not in html
    print("{:13} {:34} flagged={!s:5} rewritten={}".format(k, v, v in bad, rewritten))
