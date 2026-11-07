"""The Quarto build's warning gate, tools/quarto_build.py (D-0033, phase 1).

Any Quarto warning line fails the build. Quarto prints its own warnings as
`WARN: ...` and Pandoc's as `[WARNING] ...`; the gate must catch both and
must not trip on the ordinary progress lines.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from quarto_build import WARNING            # noqa: E402


class WarningGate(unittest.TestCase):

    def test_quarto_warn_line(self):
        self.assertIsNotNone(WARNING.search("WARN: Unable to resolve link target: x.qmd"))

    def test_plain_warning_line(self):
        self.assertIsNotNone(WARNING.search("WARNING: something"))

    def test_pandoc_bracketed_warning_line(self):
        line = "[WARNING] Note with key '1' defined at line 11 column 1 but not used."
        self.assertIsNotNone(WARNING.search(line))

    def test_progress_line_is_not_a_warning(self):
        self.assertIsNone(WARNING.search("[1/6] index.qmd"))

    def test_found_inside_a_whole_log(self):
        clean = "[1/2] index.qmd\n\n[2/2] courses\\index.qmd\n\nOutput created: build\\quarto-site\\index.html\n"
        self.assertIsNone(WARNING.search(clean))
        self.assertIsNotNone(WARNING.search(clean + "[WARNING] a Pandoc note\n"))
        self.assertIsNotNone(WARNING.search(clean + "WARN: a Quarto note\n"))


class LabPages(unittest.TestCase):
    """The generated lab pages (D-0118): tools/filters/media.lua runs at
    pre-ast, before Quarto's own figures, which would caption a lone
    picture with its alt text and drop the alt attribute (probed
    2026-10-08). Reads the pages tools/quarto_build.py generated."""

    def test_media_filter_runs_before_quartos_figures(self):
        pages = sorted((ROOT / "labs").glob("*/modern/index.qmd"))
        self.assertTrue(pages, "run tools/quarto_build.py first")
        for page in pages:
            text = page.read_text(encoding="utf-8")
            with self.subTest(page=page.parent.parent.name):
                self.assertRegex(text, r'\{"path": "[./]+/tools/filters/media\.lua", "at": "pre-ast"\}')


    def test_no_quarto_figure_on_a_lab_page(self):
        # Measured 2026-10-08 on a made-up lab with a picture, a cropped
        # picture, a drawn figure and equations: against the HTML download,
        # img, svg and math take the same computed styles at 375 and 1440
        # px once Bootstrap's vertical-align is reverted, because Quarto
        # makes no figure of them. A figure or Bootstrap's image classes on
        # a lab page would mean that no longer holds.
        pages = sorted((ROOT / "build" / "quarto-site" / "labs").glob("*/modern/index.html"))
        self.assertTrue(pages, "run tools/quarto_build.py first")
        for page in pages:
            main = page.read_text(encoding="utf-8").split("<main id=\"content\">", 1)[1].split("</main>", 1)[0]
            with self.subTest(page=page.parent.parent.name):
                for found in ("<figure", "<figcaption", "img-fluid", "figure-img", "quarto-float"):
                    self.assertNotIn(found, main)


if __name__ == "__main__":
    unittest.main()
