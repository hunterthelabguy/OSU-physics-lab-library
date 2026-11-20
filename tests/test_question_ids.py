"""The ordered-ids pin (D-0077) and the em-dash scan's converted-file rule (D-0103).

Each converted lab's question and checkpoint ids, in order, equal its entry
in tests/question-ids.json. Adding, removing or reordering one fails here
until the pin is updated in the same PR with an entry naming the numbers that
moved: the owner's cue to edit the rubrics, and the Gradescope outline
maintainers' notice. That the order agrees with the original is the number
check's job (tools/check_numbers.py); the pin freezes it once ruled content
changes begin.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_em_dash  # noqa: E402
import check_unchanged  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
PIN = json.loads((ROOT / "tests" / "question-ids.json").read_text(encoding="utf-8"))["labs"]
PH211 = ROOT / "curriculum" / "ph211" / "ph211-team-building-handout.md"


def read(md):
    doc = json.loads(subprocess.run([PANDOC, str(md), "-f", "markdown-smart", "-t", "json"],
                                    capture_output=True, check=True, encoding="utf-8").stdout)
    ids = []

    def walk(blocks):
        for b in blocks:
            if b["t"] == "Div":
                (ident, classes, _), content = b["c"]
                kind = next((k for k in ("question", "checkpoint") if k in classes), None)
                if kind:
                    ids.append([kind, ident])
                else:
                    walk(content)
    walk(doc["blocks"])
    lab = doc["meta"]["id"]
    lab = lab["c"] if lab["t"] == "MetaString" else "".join(
        x.get("c", "") if x["t"] == "Str" else "" for x in lab["c"])
    return lab, ids


def converted_labs():
    for md in sorted((ROOT / "curriculum").rglob("*.md")):
        if check_em_dash.converted(md):
            yield md


class Pin(unittest.TestCase):

    def test_every_converted_lab_matches_its_pin(self):
        seen = set()
        for md in converted_labs():
            lab, ids = read(md)
            seen.add(lab)
            with self.subTest(lab=lab):
                self.assertIn(lab, PIN, "a converted lab has no pin")
                self.assertEqual(ids, PIN[lab])
                self.assertTrue(all(ident for _, ident in ids), "a block without an id")
        self.assertEqual(seen, set(PIN), "the pin names a lab that is not converted")

    def test_reordering_a_question_fails_the_pin(self):
        # D-0077's test: two questions swapped in a copy of PH 211 Lab 1.
        text = PH211.read_text(encoding="utf-8")
        a = text.index("::: {.question #ph211-team-building:good-lab-partner}")
        b = text.index("::: {.question #ph211-team-building:sketches}")
        end = text.index(":::\n", b) + 4
        first_end = text.index(":::\n", a) + 4
        swapped = text[:a] + text[b:end] + text[first_end:b] + text[a:first_end] + text[end:]
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "lab.md"
            md.write_text(swapped, encoding="utf-8", newline="\n")
            lab, ids = read(md)
        self.assertEqual(sorted(ids), sorted(PIN[lab]))
        self.assertNotEqual(ids, PIN[lab])

    def test_reordering_a_ruled_change_file_fails_the_pin(self):
        # D-0195: re-baselining skips the Word checks, never the pin.
        text = PH211.read_text(encoding="utf-8")
        self.assertIn("\nstatus: converted\n", text)
        text = text.replace("\nstatus: converted\n", "\nstatus: ruled-change\n", 1)
        a = text.index("::: {.question #ph211-team-building:good-lab-partner}")
        b = text.index("::: {.question #ph211-team-building:sketches}")
        end = text.index(":::\n", b) + 4
        first_end = text.index(":::\n", a) + 4
        swapped = text[:a] + text[b:end] + text[first_end:b] + text[a:first_end] + text[end:]
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "lab.md"
            md.write_text(swapped, encoding="utf-8", newline="\n")
            self.assertTrue(check_unchanged.rebaselined(md))
            lab, ids = read(md)
        self.assertEqual(sorted(ids), sorted(PIN[lab]))
        self.assertNotEqual(ids, PIN[lab])


class EmDashScan(unittest.TestCase):

    def test_converted_file_keeps_its_originals_em_dash(self):
        # D-0103's test.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "curriculum").mkdir()
            (root / "site").mkdir()
            (root / "curriculum" / "lab.md").write_text(
                '---\nsource_file: "originals/x.docx"\n---\n\na model\u2014a representation\n',
                encoding="utf-8")
            (root / "curriculum" / "notes.md").write_text(
                "---\ntitle: x\n---\n\nwritten here\u2014not converted\n", encoding="utf-8")
            (root / "site" / "page.md").write_text("one\u2014two\n", encoding="utf-8")
            (root / "site" / "font.woff2").write_bytes(b"\0" + "\u2014".encode("utf-8"))
            found = check_em_dash.scan(str(root), ("curriculum", "site"))
        self.assertEqual(found, ["curriculum/notes.md", "site/page.md"])

    def test_published_sources_have_none(self):
        self.assertEqual(check_em_dash.scan(), [])

    def test_ruled_change_is_scanned(self):
        # D-0195: a ruled-change file is the site's own wording.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "curriculum").mkdir()
            (root / "curriculum" / "lab.md").write_text(
                '---\nsource_file: "originals/x.docx"\nstatus: ruled-change\n---\n\n'
                'new words\u2014here\n', encoding="utf-8")
            found = check_em_dash.scan(str(root), ("curriculum",))
        self.assertEqual(found, ["curriculum/lab.md"])


if __name__ == "__main__":
    unittest.main()
