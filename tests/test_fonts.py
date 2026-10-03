"""Open Sans, subset to Latin and Greek (D-0006, D-0025, D-0027)."""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "site" / "fonts"
sys.path.insert(0, str(ROOT / "tools"))
from subset_fonts import STYLES, covers   # noqa: E402

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
        for md in list(ROOT.glob("curriculum/**/*.md")) + list(ROOT.glob("site/*.md")):
            chars |= set(md.read_text(encoding="utf-8"))
        missing = sorted(c for c in chars if not c.isspace() and not covers(c))
        self.assertEqual([f"U+{ord(c):04X}" for c in missing], [])


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
