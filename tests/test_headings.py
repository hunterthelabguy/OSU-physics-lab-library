"""Heading levels never skip (D-0166; WCAG 1.3.1, from the NVDA test of
2026-11-05), and each question's label is a heading one level below its
section (D-0176). Reads each source as the lab page renders it: through
tools/filters/questions.lua, so the labels are there.

KNOWN_SKIPS is a ratchet: the labs not yet fixed. A lab leaves the list
when its headings are fixed, and a lab on the list that no longer skips
fails, so the list only shrinks.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_numbers  # noqa: E402

KNOWN_SKIPS = {
    "ph211-capstone-handout",
    "ph211-uncertainty-handout",
    "ph213-data-analysis-handout",
}
LABELS = ("question-label", "checkpoint-label")


def headings(path):
    """[(level, kind, box)] in document order: kind "label" for a
    question's or checkpoint's label, "box" for a heading inside a question
    (box: its label's level), "section" otherwise."""
    doc = json.loads(subprocess.run(
        [check_numbers.PANDOC, str(path), "-f", check_numbers.FROM, "-t", "json",
         "--lua-filter", check_numbers.FILTER, "-M", "theme-name=modern"],
        capture_output=True, check=True, encoding="utf-8").stdout)
    found = []

    def walk(blocks, box):
        for b in blocks:
            if b["t"] == "Header":
                found.append((b["c"][0], "box" if box is not None else "section", box))
            elif b["t"] == "Div":
                (_, classes, _), content = b["c"]
                if any(k in classes for k in ("question", "checkpoint")):
                    label = content[0]
                    if label["t"] == "Div" and label["c"][0] == ["", [], []]:
                        label = label["c"][1][0]
                    if label["t"] != "Header" or not set(label["c"][1][1]) & set(LABELS):
                        raise AssertionError("{}: a question's label is not a heading".format(path.name))
                    found.append((label["c"][0], "label", None))
                    walk(content[1:], label["c"][0])
                else:
                    walk(content, box)
            elif b["t"] == "BlockQuote":
                walk(b["c"], box)
            elif b["t"] in ("BulletList", "OrderedList"):
                for item in (b["c"] if b["t"] == "BulletList" else b["c"][1]):
                    walk(item, box)

    walk(doc["blocks"], None)
    return found


def skips(levels):
    """Each (index, level, previous level) where a heading goes down by
    more than one level."""
    return [(i, b, a) for i, (a, b) in enumerate(zip(levels, levels[1:]), 1) if b > a + 1]


class HeadingLevels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.labs = {p.stem: headings(p) for p in sorted((ROOT / "curriculum").glob("*/*.md"))}

    def test_no_lab_skips_a_level(self):
        for lab, found in self.labs.items():
            with self.subTest(lab=lab):
                found = skips([level for level, _, _ in found])
                if lab in KNOWN_SKIPS:
                    self.assertNotEqual(found, [], "fixed: remove it from KNOWN_SKIPS")
                else:
                    self.assertEqual(found, [])

    def test_label_is_one_below_its_section(self):
        for lab, found in self.labs.items():
            with self.subTest(lab=lab):
                section = 1
                for level, kind, _ in found:
                    if kind == "section":
                        section = level
                    elif kind == "label":
                        self.assertEqual(level, section + 1)

    def test_box_heading_is_below_its_label(self):
        # D-0176: a heading inside a question's box sits under its label.
        for lab, found in self.labs.items():
            for level, kind, box in found:
                if kind == "box":
                    with self.subTest(lab=lab, level=level):
                        self.assertGreater(level, box)


if __name__ == "__main__":
    unittest.main()
