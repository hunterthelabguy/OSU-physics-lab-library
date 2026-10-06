"""tools/quarto_chrome.py: the old chrome lifted, and a Quarto page dressed
(D-0036, D-0038). Needs Pandoc (PANDOC), not a build.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import quarto_chrome                      # noqa: E402
import render                             # noqa: E402

# The shape Quarto 1.10.18 writes, cut down (real lines from build/quarto-site).
SKELETON = (
    '<!DOCTYPE html>\n<html><head><title>t</title></head>\n'
    '<body class="fullcontent quarto-light">\n\n'
    '<div id="quarto-content" class="quarto-container page-columns">\n'
    '<main class="content" id="quarto-document-content">'
    '<header id="title-block-header" class="quarto-title-block"></header>\n\n\n'
    '<h1 id="x">X</h1>\n<p>Body.</p>\n\n'
    '</main> <!-- /main -->\n<script>var mailtoRegex;</script>\n'
    '</div> <!-- /content -->\n\n</body></html>\n')
TOP = '<div class="top">T</div>\n'
BOTTOM = '<footer class="b">B</footer>\n'


def dressed(page=SKELETON):
    return quarto_chrome.dress(page, "site-page", TOP, BOTTOM)


class Dress(unittest.TestCase):

    def test_main_made_bare(self):
        out = dressed()
        self.assertIn('<main>\n<h1 id="x">X</h1>\n<p>Body.</p>\n</main>', out)
        self.assertNotIn("title-block-header", out)
        self.assertNotIn("quarto-document-content", out)

    def test_top_right_after_body(self):
        self.assertIn('<body class="site-page fullcontent quarto-light">\n<div class="top">T</div>\n',
                      dressed())

    def test_bottom_right_after_content_div(self):
        out = dressed()
        self.assertIn('</div> <!-- /content -->\n<footer class="b">B</footer>\n', out)
        self.assertGreater(out.index("<footer"), out.index("</main>"))

    def test_anchor_missing_or_doubled_fails(self):
        broken = {
            "no main shape": SKELETON.replace('<main class="content"', "<main"),
            "no body class": SKELETON.replace('<body class="fullcontent quarto-light">', "<body>"),
            "two content ends": SKELETON.replace(quarto_chrome.QCONTENT_END,
                                                 quarto_chrome.QCONTENT_END * 2),
        }
        for what, page in broken.items():
            with self.subTest(case=what):
                with self.assertRaises(ValueError):
                    dressed(page)


class OldChrome(unittest.TestCase):

    def test_document_page(self):
        body_class, top, bottom = quarto_chrome.old_chrome(
            {"html": "labs/x/modern/index.html", "kind": "doc", "depth": 3,
             "theme": "modern", "footnote": ""})
        self.assertEqual(body_class, "theme-modern")
        for piece in ('<div class="draft-banner">', '<header class="osu-header">',
                      '<nav class="site-nav">', '<a class="switch" href="../faithful/">',
                      'src="../../../site/brand/OSU_horizontal_2C_W_over_B.png"'):
            self.assertIn(piece, top)
        self.assertIn(render.BANNER_MAIN, " ".join(top.split()))
        self.assertIn('<footer class="doc-footer">', bottom)
        self.assertIn('<footer class="osu-foot">', bottom)

    def test_site_page_with_footnote(self):
        body_class, top, bottom = quarto_chrome.old_chrome(
            {"html": "how-this-site-works/index.html", "kind": "site", "depth": 1,
             "theme": None, "footnote": render.METHOD_FOOTNOTE})
        self.assertEqual(body_class, "site-page")
        self.assertNotIn("site-nav", top)
        self.assertIn('<div class="site-foot">', bottom)
        self.assertIn("site/how-this-site-works.md", bottom)

    def test_site_page_without_footnote(self):
        _, _, bottom = quarto_chrome.old_chrome(
            {"html": "index.html", "kind": "site", "depth": 0, "theme": None, "footnote": ""})
        self.assertNotIn("site-foot", bottom)
        self.assertIn('<footer class="osu-foot">', bottom)


if __name__ == "__main__":
    unittest.main()
