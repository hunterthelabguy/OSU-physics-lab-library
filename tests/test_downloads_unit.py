"""tools/downloads.py: standalone() on small fixtures (D-0052, D-0053).

The HTML download is the built modern page made to open from disk:
stylesheets inlined with their fonts, scripts and both navs removed,
relative links reduced to their words. Anything it cannot place is an
error, never a silent drop (LEDGER 53). Needs no build.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import downloads                          # noqa: E402

PAGE = """<!DOCTYPE html>
<html><head>
<meta name="robots" content="noindex, nofollow">
<link href="lib/bootstrap.min.css" rel="stylesheet" id="quarto-bootstrap">
<link href="lib/bootstrap-icons.css" rel="stylesheet">
<link rel="stylesheet" href="site/site.css">
<script src="lib/quarto.js"></script>
</head>
<body class="theme-modern">
<div class="draft-banner">Draft</div>
<header class="osu-header">
<a class="osu-logo" href="https://oregonstate.edu"><img src="data:image/png;base64,AAAA" alt="Oregon State University"></a>
<a class="osu-sitename" href="../../../">Physics Lab Library</a>
<nav class="osu-nav" aria-label="Library"><div class="osu-inner">
<a href="../../../">Library home</a>
</div></nav>
</header><nav class="site-nav">
<a href="../../../courses/">Course index</a>
</nav>
<main>
<h1>Lab</h1>
<p>See <a href="#part-1">part 1</a>.</p>
</main>
<script>window.x = 1;</script>
<footer class="osu-foot"><p>License: see <a href="../../../how-this-was-made/">How this was made</a>.</p>
<p><a href="https://oregonstate.edu/accessibility-statement">Accessibility Statement</a></p></footer>
</body></html>
"""


class Standalone(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "lib").mkdir()
        (root / "site" / "fonts").mkdir(parents=True)
        (root / "lib" / "bootstrap.min.css").write_text("body{margin:0}\n", encoding="utf-8")
        (root / "lib" / "bootstrap-icons.css").write_text(".bi{x:1}\n", encoding="utf-8")
        (root / "site" / "site.css").write_text(
            '@font-face { src: url("fonts/Sans.woff2") format("woff2"); }\n', encoding="utf-8")
        (root / "site" / "fonts" / "Sans.woff2").write_bytes(b"\x00\x01font")
        self.page_dir = str(root)

    def tearDown(self):
        self.tmp.cleanup()

    def out(self, page=PAGE):
        return downloads.standalone(page, self.page_dir)

    def test_both_navs_removed(self):
        text = self.out()
        self.assertNotIn('class="osu-nav"', text)
        self.assertNotIn('class="site-nav"', text)
        self.assertNotIn("Course index", text)

    def test_missing_nav_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace('<nav class="site-nav">', '<nav class="other">'))

    def test_scripts_removed(self):
        self.assertNotIn("<script", self.out())

    def test_stylesheets_inlined_with_fonts(self):
        text = self.out()
        self.assertNotIn("<link", text)
        self.assertIn("body{margin:0}", text)
        self.assertIn('url("data:font/woff2;base64,AAFmb250")', text)

    def test_icon_stylesheet_dropped(self):
        self.assertNotIn(".bi{x:1}", self.out())

    def test_icons_in_use_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace("<h1>Lab</h1>", '<h1 class="bi-star">Lab</h1>'))

    def test_relative_links_become_words(self):
        text = self.out()
        self.assertIn('<a href="#part-1">part 1</a>', text)
        self.assertIn("Physics Lab Library", text)
        self.assertNotIn('href="../../../"', text)
        self.assertIn("see How this was made.", text)

    def test_absolute_links_kept(self):
        text = self.out()
        self.assertIn('<a href="https://oregonstate.edu/accessibility-statement">', text)
        self.assertIn('<a class="osu-logo" href="https://oregonstate.edu">', text)

    def test_missing_font_is_an_error(self):
        (Path(self.page_dir) / "site" / "fonts" / "Sans.woff2").unlink()
        with self.assertRaises(FileNotFoundError):
            self.out()

    def test_relative_reference_left_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace('src="data:image/png;base64,AAAA"', 'src="logo.png"'))

    def test_nothing_relative_left(self):
        import re
        for url in re.findall(r'\b(?:src|href)="([^"]*)"', self.out()):
            with self.subTest(url=url):
                self.assertFalse(downloads.is_relative(url), url)


if __name__ == "__main__":
    unittest.main()
