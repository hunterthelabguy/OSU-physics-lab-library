"""Phase 2 chrome on the Quarto build (D-0036 to D-0039, D-0042).

Needs both builds: build/site/ (the old build, the chrome's source) and
build/quarto-site/. A missing build is an error, never a skip (LEDGER 53).
"""

import base64
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
OLD = ROOT / "build" / "site"


def setUpModule():
    for d, how in ((OLD, "tools/render.py --site"), (QSITE, "tools/quarto_build.py")):
        if not d.is_dir():
            raise RuntimeError("{} is missing: run {} first".format(d, how))


def chrome_pages():
    """Quarto pages that carry the full chrome: not redirect stubs, not sims."""
    for p in sorted(QSITE.rglob("index.html")):
        rel = p.relative_to(QSITE).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text or re.fullmatch(r"sims/[^/]+/index\.html", rel):
            continue
        yield rel, text


LOGO = re.compile(r'src="data:image/png;base64,([^"]+)"')


def logo_by_digest(fragment):
    """Compare embedded images by their decoded bytes, not their encoding."""
    return LOGO.sub(lambda m: 'src="sha256:{}"'.format(
        hashlib.sha256(base64.b64decode(m.group(1))).hexdigest()), fragment)


def old_parts(text):
    m = re.search(r'<body class="([^"]*)">\n(.*?)<main>.*?</main>\n(.*?)</body>', text, re.S)
    return m.group(1), m.group(2), m.group(3)


def new_parts(text):
    body = re.search(r'<body class="([^"]*)">\n', text)
    end = "</div> <!-- /content -->\n"
    after = text.index(end) + len(end)
    return body.group(1), text[body.end():text.index("<main>")], text[after:text.index("</body>")]


class Navigation(unittest.TestCase):
    """D-0037: one nav, no search."""

    def test_no_quarto_navbar_or_search(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertNotIn('id="quarto-header"', text)
                self.assertNotIn("quarto-search", text)

    def test_no_search_index(self):
        self.assertFalse((QSITE / "search.json").exists())

    def test_one_osu_nav(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count('<nav class="osu-nav"'), 1)


class ChromeParity(unittest.TestCase):
    """D-0036, D-0038: every Quarto page carries the old page's chrome."""

    def test_every_page_has_an_old_twin(self):
        rels = [rel for rel, _ in chrome_pages()]
        self.assertGreaterEqual(len(rels), 6)
        for rel in rels:
            with self.subTest(page=rel):
                self.assertTrue((OLD / rel).is_file())

    def test_body_class_carried(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[0]
                self.assertTrue(new_parts(text)[0].startswith(want + " "))

    def test_top_chrome_matches_old_build(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[1].rstrip("\n")
                got = new_parts(text)[1]
                self.assertTrue(logo_by_digest(got).startswith(logo_by_digest(want)))

    def test_bottom_chrome_matches_old_build(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[2]
                if rel == "index.html":
                    # D-0038: the landing footnote names the old build.
                    want = re.sub(r'<div class="site-foot">.*?</div>\n', "", want, flags=re.S)
                self.assertEqual(new_parts(text)[2].strip(), want.strip())

    def test_landing_footnote_not_carried(self):
        self.assertNotIn("one build script", (QSITE / "index.html").read_text(encoding="utf-8"))


class MainBare(unittest.TestCase):
    """D-0036: one bare <main>, no empty title block."""

    def test_main_is_bare(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count("<main>"), 1)
                self.assertNotIn("<main ", text)
                self.assertNotIn("title-block-header", text)


class Published(unittest.TestCase):
    """D-0039: only the fonts and their license go out."""

    def test_fonts_and_license_only(self):
        names = sorted(p.name for p in (QSITE / "site" / "fonts").iterdir())
        self.assertEqual(names, ["OFL.txt", "OpenSans-Bold.woff2", "OpenSans-BoldItalic.woff2",
                                 "OpenSans-Italic.woff2", "OpenSans-Regular.woff2"])
        self.assertFalse((QSITE / "site" / "brand").exists())

    def test_no_markdown_published(self):
        self.assertEqual([p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.md")], [])


class QuartoOnlyCss(unittest.TestCase):
    """Rules added for Quarto must not reach the old build, which shares
    site/site.css and is still production."""

    def test_block_present_and_scoped(self):
        css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
        m = re.search(r"/\* quarto-only: start \(D-0036\) \*/(.*?)/\* quarto-only: end \*/", css, re.S)
        self.assertIsNotNone(m, "no quarto-only block")
        body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        selectors = [s.strip() for sel in re.findall(r"([^{}]+)\{", body) for s in sel.split(",")]
        self.assertTrue(selectors)
        for s in selectors:
            if s.startswith("@media"):
                continue
            with self.subTest(selector=s):
                self.assertTrue("#quarto-content" in s or ".quarto-light" in s)


if __name__ == "__main__":
    unittest.main()
