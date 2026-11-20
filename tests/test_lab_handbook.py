"""The Lab Handbook (D-0188, D-0190): links to a converted document by id,
and the handbook's fixed section addresses."""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import render  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
MEDIA = ROOT / "tools" / "filters" / "media.lua"
HANDBOOK = "ph21x-lab-handbook"
ADDRESSES = ["plot-elements", "linearization", "what-is-uncertainty", "sources-of-uncertainty",
             "predictions-hypotheses-models", "graphical-analysis-tips", "variables-and-parameters"]
# media.lua's own pattern, `^([%w%-]+)#([%w%-_]+)$`, so every link it
# rewrites is one this test validates, whatever its case, title or brackets.
DOC_LINK = re.compile(r"^([A-Za-z0-9-]+)#([A-Za-z0-9_-]+)$")
DOC_TARGET = re.compile(r"^[A-Za-z0-9-]+#")   # an `<id>#...` target; a path form
# (`a.md#x`, `a/#x`) is neither rewritten nor checked, and no source has one (pass 4).


def sources(docs=None):
    """{id: path} of every converted document (render.converted_documents())."""
    docs = render.converted_documents() if docs is None else docs
    return {i: Path(d["path"]) for i, d in docs.items()}


def parsed(path):
    """(link targets, explicit identifiers) in a source. Generated heading
    identifiers are off: spec 4.4 links only to explicit ones."""
    doc = json.loads(subprocess.run([PANDOC, str(path), "-f", render.FROM + "-auto_identifiers", "-t", "json"],
                                    capture_output=True, check=True, encoding="utf-8").stdout)
    targets, idents = [], set()

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            if node.get("t") == "Link":
                targets.append(node["c"][2][0])
            elif node.get("t") in ("Header", "Div", "Span"):
                attr = node["c"][1] if node["t"] == "Header" else node["c"][0]
                if attr[0]:
                    idents.add(attr[0])
            walk(node.get("c"))

    walk(doc["blocks"])
    return targets, idents


def bad_links(sources):
    """(id, target) of each `<id>#<identifier>` link whose id is no such
    document or whose identifier is not one on that document."""
    read = {i: parsed(p) for i, p in sources.items()}
    bad = []
    for doc_id, (targets, _) in read.items():
        for target in targets:
            if not DOC_TARGET.match(target):
                continue
            # A fragment media.lua cannot rewrite (a colon, a dot) would ship
            # as a relative link that 404s (pass 3): bad, as D-0190 (3) says.
            m = DOC_LINK.match(target)
            if not m or m.group(1) not in read or m.group(2) not in read[m.group(1)][1]:
                bad.append((doc_id, target))
    return bad


class Links(unittest.TestCase):
    TEXT = "[Linearization](ph21x-lab-handbook#linearization) and [here](#local).\n"
    URL = render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#linearization"

    def run_filter(self, to, out=None):
        args = [PANDOC, "-f", render.FROM, "--lua-filter", str(MEDIA),
                "-M", "library-url=" + render.LIBRARY_URL]
        args += ["-o", str(out)] if out else ["-t", to]
        return subprocess.run(args, input=self.TEXT, capture_output=True, encoding="utf-8")

    def test_page_link_points_at_the_library(self):
        page = self.run_filter("html").stdout
        self.assertIn('href="' + self.URL + '"', page)
        self.assertIn('href="#local"', page)

    def test_word_link_points_at_the_library(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "links.docx"
            self.assertEqual(self.run_filter("docx", out).returncode, 0)
            with zipfile.ZipFile(out) as z:
                rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        self.assertIn('Target="' + self.URL + '"', rels)

    def test_every_document_link_resolves(self):
        self.assertEqual(bad_links(sources()), [])

    def test_bad_links_are_found(self):
        # Every form media.lua rewrites (pass 2, probes/link_forms.py): plain,
        # titled, angle-bracketed, upper case.
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.md", Path(d) / "b.md"
            a.write_text("## Heading {#x}\n\n## Plain Heading\n", encoding="utf-8")
            b.write_text('[ok](a#x) [no](a#y) [none](c#x) [titled](a#z "T")'
                         " [angle](<a#w>) [upper](A#x) [local](#x)"
                         " [colon](a#a:q1) [dot](a#x.y) [web](https://e.org/a#x) [auto](a#plain-heading)\n", encoding="utf-8")
            found = bad_links(sources({"a": {"path": a}, "b": {"path": b}}))
        self.assertEqual(sorted(found),
                         [("b", "A#x"), ("b", "a#a:q1"), ("b", "a#plain-heading"), ("b", "a#w"), ("b", "a#x.y"),
                          ("b", "a#y"), ("b", "a#z"), ("b", "c#x")])


class Addresses(unittest.TestCase):

    def test_seven_fixed_addresses(self):
        source = sources()[HANDBOOK].read_text(encoding="utf-8")
        found = re.findall(r"^## .*\{#([A-Za-z0-9_-]+)\}$", source, re.M)
        self.assertEqual(found, ADDRESSES)
