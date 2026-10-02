"""Phase 2 chrome on the Quarto build (D-0036 to D-0039, D-0042).

Needs both builds: build/site/ (the old build, the chrome's source) and
build/quarto-site/. A missing build is an error, never a skip (LEDGER 53).
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from test_quarto_site import converted    # noqa: E402
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

    def test_only_markdown_downloads_published(self):
        # D-0053: each lab's source is a download; no other Markdown goes out.
        want = sorted("labs/{0}/{0}.md".format(doc_id) for doc_id, _ in converted())
        self.assertEqual(sorted(p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.md")), want)


class PageShell(unittest.TestCase):
    """What the quarto-only CSS in site/site.css depends on in the markup."""

    def test_one_content_opener_around_main(self):
        # Every selector in the block names #quarto-content; D-0036's dressing
        # anchors on the closing comment only, so the opener is guarded here.
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count('<div id="quarto-content"'), 1)
                opener = text.index('<div id="quarto-content"')
                self.assertLess(opener, text.index("<main>"))
                self.assertLess(text.index("</main>"), text.index("</div> <!-- /content -->"))

    def test_load_order_bootstrap_site_theme(self):
        # The reverts in the block sit at Bootstrap's specificity and work by
        # coming after it; a bare-element rule above the block in site.css is
        # cancelled the same way. So site.css must load after Bootstrap and
        # before the document theme (CLAUDE.md, Keeping the measured match).
        for rel, text in chrome_pages():
            hrefs = re.findall(r'<link [^>]*href="([^"]+)"[^>]*rel="stylesheet"|'
                               r'<link [^>]*rel="stylesheet"[^>]*href="([^"]+)"', text)
            hrefs = [a or b for a, b in hrefs]
            idx = lambda pat: [i for i, h in enumerate(hrefs) if re.search(pat, h)]
            with self.subTest(page=rel):
                boot, site = idx(r"bootstrap/bootstrap-[0-9a-f]+\.min\.css"), idx(r"site/site\.css")
                self.assertEqual(len(boot), 1)
                self.assertEqual(len(site), 1)
                self.assertLess(boot[0], site[0])
                for theme in idx(r"themes/"):
                    self.assertLess(site[0], theme)


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

    def block(self):
        css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
        return re.search(r"/\* quarto-only: start \(D-0036\) \*/(.*?)/\* quarto-only: end \*/", css, re.S).group(1)

    def test_load_order_is_noted_where_the_rules_live(self):
        self.assertIn("themes/*.css", self.block())
        self.assertIn("after", self.block())

    def test_dd_margins_reverted(self):
        # Measured 2026-10-01 against the old build: Bootstrap gives dd
        # margin-left 0 (browser default 40px) and margin-bottom .5rem.
        body = re.sub(r"/\*.*?\*/", "", self.block(), flags=re.S)
        m = re.search(r"dd\s*\{([^}]*)\}", body)
        self.assertIsNotNone(m, "no dd revert")
        self.assertIn("margin-left: revert", m.group(1))
        self.assertIn("margin-bottom: revert", m.group(1))


if __name__ == "__main__":
    unittest.main()
