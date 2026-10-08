"""Drawn figures as SVG (S13; D-0101, D-0117): tools/figures.py.

The original is made up (tests/figure_fixture.py). What Word draws for the
three real figures was measured against Word's own PDFs in pass 2b
(docs/superpowers/plans/2026-10-08-pass-2b-figures.md); these pin the
converter's rules: labels and equations stay SVG text, a label breaks where
the width table says, Word's line placement, a shape it does not know
stops, and the PNG for Word is made from the SVG.
"""

import base64
import math
import os
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import check_unchanged      # noqa: E402
import figures              # noqa: E402
import figure_fixture as fx  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
CHROME = os.environ.get("CHROME", "google-chrome")
SVG = "{http://www.w3.org/2000/svg}"


class Figure(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, xml):
        fx.original(self.root, PANDOC, "Before.\n", xml)
        return str(self.root / "original.docx")

    def svg(self, xml=None, ids=("501",)):
        original = self.make(xml or fx.paragraph("Words.", fx.figure()))
        text, descrs = figures.svg(original, list(ids))
        return text, descrs, ET.fromstring(text)

    def lines(self, root):
        return [("".join(t.itertext()), float(t.get("y")), float(t.get("x")))
                for t in root.iter(SVG + "tspan") if t.get("class") == "figure-line"]

    def test_labels_are_svg_text(self):
        text, descrs, root = self.svg()
        self.assertEqual(descrs, [fx.FIGURE_ALT])
        self.assertEqual(root.get("aria-label"), fx.FIGURE_ALT)
        self.assertEqual(root.get("role"), "group")
        labels = [t for t in root.iter(SVG + "text") if t.get("class") == "figure-label"]
        self.assertEqual(len(labels), 2)
        self.assertNotIn("<image", re.sub(r"<svg class=\"figure-picture\".*?</svg>", "", text))

    def test_label_breaks_where_the_widths_say(self):
        # Times New Roman 12 pt: "Accelerating voltage" is 99.61 pt, with
        # "control" 136.6 pt; the box's inner width is 110 pt.
        _, _, root = self.svg()
        lines = [t for t, _, _ in self.lines(root)]
        self.assertEqual(lines[:2], ["Accelerating voltage", "control"])

    def test_line_placement_is_words(self):
        # Measured on Word's PDF of PH 213 Lab 2 (2026-10-08): the first
        # baseline sits half the outline, the top inset, and the line's
        # ascent and gap below the box's top; the next line its descent
        # plus the next ascent and gap lower; the start half the outline
        # and the left inset in. Times New Roman 12 pt: (1825 + 87) / 2048
        # em above, 443 / 2048 below.
        _, _, root = self.svg()
        (_, y1, x1), (_, y2, _) = self.lines(root)[:2]
        top, left = 10 * fx.PT, 10 * fx.PT          # the box, at half scale
        above, below = 1912 / 2048 * 12, 443 / 2048 * 12
        self.assertAlmostEqual(y1, (top + fx.LINE / 2 + 45720) / fx.PT + above, places=1)
        self.assertAlmostEqual(y2 - y1, below + above, places=1)
        self.assertAlmostEqual(x1, (left + fx.LINE / 2 + fx.INSET) / fx.PT, places=1)

    def test_equation_mirrors_its_omml(self):
        _, _, root = self.svg()
        math = [t for t in root.iter(SVG + "tspan") if t.get("class") == "figure-math"]
        self.assertEqual(len(math), 1)
        self.assertEqual("".join(math[0].itertext()), "ΔVD")
        kinds = [t.get("data-omml") for t in math[0].iter(SVG + "tspan") if t.get("data-omml")]
        self.assertEqual(kinds, ["r", "sSub", "e", "r", "sub", "r"])
        sub = next(t for t in math[0].iter(SVG + "tspan") if t.get("data-omml") == "sub")
        self.assertLess(float(sub.get("baseline-shift")), 0)

    def test_word_check_reads_the_figure(self):
        text, _, _ = self.svg()
        tokens = check_unchanged.figure_tokens(text)
        words = " ".join("".join(v for k, v in tokens if k == "text").split())
        self.assertEqual(words, "Accelerating voltage control Turn")
        self.assertEqual([k for k, _ in tokens if k != "text"], ["picture", "math"])

    def test_picture_keeps_the_originals_bytes(self):
        _, _, root = self.svg()
        href = next(root.iter(SVG + "image")).get("href")
        self.assertTrue(href.startswith("data:image/png;base64,"))
        self.assertEqual(base64.b64decode(href.split(",", 1)[1]), fx.png())

    def test_size_is_words(self):
        _, _, root = self.svg()
        self.assertAlmostEqual(float(root.get("width")), fx.WIDTH / 9525, places=1)

    def test_unknown_shape_stops(self):
        ellipse = fx.text_box("605", 0, 0, 100 * fx.PT, 50 * fx.PT, fx.run("Odd"), prst="ellipse")
        with self.assertRaises(figures.Unsupported) as e:
            self.svg(fx.paragraph("Words.", fx.figure(extra_shape=ellipse)))
        self.assertIn("ellipse", str(e.exception))

    def test_close_break_stops(self):
        # "Accelerating voltage" is 99.61 pt; a label of exactly that much
        # room cannot be called from widths.
        # At the group's half scale, so twice Word's size inside it.
        tight = fx.text_box("605", 0, 0, 2 * (int(99.7 * fx.PT) + 2 * fx.INSET + fx.LINE), 100 * fx.PT,
                            fx.run("Accelerating voltage"))
        with self.assertRaises(figures.Unsupported) as e:
            self.svg(fx.paragraph("Words.", fx.figure(extra_shape=tight)))
        self.assertIn("too close to call", str(e.exception))

    def test_missing_drawing_stops(self):
        with self.assertRaises(SystemExit):
            self.svg(ids=("999",))

    def test_png_is_made_from_the_svg(self):
        text, _, _ = self.svg()
        svg_path = self.root / "figure.svg"
        svg_path.write_text(text, encoding="utf-8")
        figures.png(str(svg_path), str(self.root / "figure.png"), CHROME)
        data = (self.root / "figure.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        # Two device pixels to each CSS pixel of Word's size, rounded up.
        width = int.from_bytes(data[16:20], "big")
        self.assertEqual(width, 2 * math.ceil(float(re.search(r'width="([\d.]+)"', text).group(1))))


if __name__ == "__main__":
    unittest.main()
