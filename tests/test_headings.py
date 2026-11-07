"""Heading levels never skip (D-0166; WCAG 1.3.1, from the NVDA test of
2026-11-05). Reads each converted source's ATX headings; a screen reader's
heading list is built from them.

KNOWN_SKIPS is a ratchet: the labs not yet fixed. A lab leaves the list
when its headings are fixed, and a lab on the list that no longer skips
fails, so the list only shrinks.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN_SKIPS = {
    "ph211-capstone-handout",
    "ph211-uncertainty-handout",
    "ph213-data-analysis-handout",
}


def skips(path):
    """Each (line, level, previous level) where a heading goes down by more
    than one level, fenced code ignored."""
    found, prev, fenced = [], None, False
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.startswith("```"):
            fenced = not fenced
        m = None if fenced else re.match(r"^(#{1,6}) ", line)
        if m:
            level = len(m.group(1))
            if prev is not None and level > prev + 1:
                found.append((n, level, prev))
            prev = level
    return found


class HeadingLevels(unittest.TestCase):

    def test_no_lab_skips_a_level(self):
        for path in sorted((ROOT / "curriculum").glob("*/*.md")):
            with self.subTest(lab=path.stem):
                if path.stem in KNOWN_SKIPS:
                    self.assertNotEqual(skips(path), [], "fixed: remove it from KNOWN_SKIPS")
                else:
                    self.assertEqual(skips(path), [])


if __name__ == "__main__":
    unittest.main()
