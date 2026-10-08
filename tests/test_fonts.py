"""Open Sans, subset to Latin and Greek (D-0006, D-0025, D-0027)."""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "site" / "fonts"
PANDOC = os.environ.get("PANDOC", "pandoc")
sys.path.insert(0, str(ROOT / "tools"))
from subset_fonts import STYLES, covers   # noqa: E402
import render                             # noqa: E402

# Typed as text in an original's math font, Cambria Math, not as an
# equation: PH 213 Lab 2's "∆𝑦" and "𝛥𝑉A", PH 211 Lab 4's "d ∝ h". Open
# Sans's Latin and Greek subset holds neither Mathematical Alphanumeric
# Symbols nor Mathematical Operators, so the reader's own math font sets
# them, as Word sets them in Cambria Math (D-0120). An equation's
# characters are MathML, set by the math font, and are not read here.
MATH_FONT = ((0x1D400, 0x1D7FF), (0x2200, 0x22FF))


def set_in_math_font(ch):
    return any(a <= ord(ch) <= b for a, b in MATH_FONT)


def text_outside_math(md):
    """The characters a converted source shows as text: Pandoc's syntax tree
    read as the build reads it, without equations."""
    tree = json.loads(subprocess.run([PANDOC, "-f", render.FROM, "-t", "json", str(md)],
                                     check=True, capture_output=True, encoding="utf-8").stdout)
    out = []

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            if node.get("t") == "Math":
                return
            if node.get("t") == "Str":
                out.append(node["c"])
            walk(node.get("c"))

    walk([tree["meta"], tree["blocks"]])
    return "".join(out)

STRIP = re.compile(r"/\*.*?\*/", re.S)


class FontFiles(unittest.TestCase):

    def test_files_and_license_present(self):
        for style in STYLES:
            self.assertTrue((FONTS / f"OpenSans-{style}.woff2").is_file(), style)
        self.assertIn("SIL OPEN FONT LICENSE", (FONTS / "OFL.txt").read_text(encoding="utf-8").upper())

    def test_subset_covers_our_text(self):
        # Every character in the converted documents and site copy must be in
        # the subset, or a reader sees a fallback glyph mid-word.
        chars = set()
        for md in ROOT.glob("curriculum/**/*.md"):
            chars |= set(text_outside_math(md))
        for md in ROOT.glob("site/*.md"):
            chars |= set(md.read_text(encoding="utf-8"))
        missing = sorted(c for c in chars if not c.isspace() and not covers(c) and not set_in_math_font(c))
        self.assertEqual([f"U+{ord(c):04X}" for c in missing], [])

    def test_equations_and_math_font_text_are_not_read_as_open_sans(self):
        self.assertTrue(set_in_math_font("𝑦") and set_in_math_font("∆") and set_in_math_font("∝"))
        self.assertFalse(set_in_math_font("Δ"))  # Greek, in the subset
        self.assertFalse(set_in_math_font("ж"))


class Weights(unittest.TestCase):
    """D-0027: two weights only, 400 and 700."""

    def test_only_two_weights(self):
        for css in ("site/site.css", "themes/modern.css"):
            text = STRIP.sub("", (ROOT / css).read_text(encoding="utf-8"))
            found = set(re.findall(r"font-weight\s*:\s*(\d+)", text))
            found |= set(re.findall(r"font\s*:\s*(\d{3})\s", text))
            with self.subTest(css=css):
                self.assertTrue(found <= {"400", "700"}, found)


if __name__ == "__main__":
    unittest.main()
