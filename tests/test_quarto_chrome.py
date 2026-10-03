"""The chrome on the Quarto build (D-0036 to D-0039, D-0042, D-0061).

Reads build/quarto-site/. A missing build is an error, never a skip
(LEDGER 53).
"""

import html
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))
from test_quarto_site import converted    # noqa: E402
import render                             # noqa: E402
QSITE = ROOT / "build" / "quarto-site"


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("{} is missing: run tools/quarto_build.py first".format(QSITE))


def chrome_pages():
    """Quarto pages that carry the full chrome: not redirect stubs, not sims."""
    for p in sorted(QSITE.rglob("index.html")):
        rel = p.relative_to(QSITE).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text or re.fullmatch(r"sims/[^/]+/index\.html", rel):
            continue
        yield rel, text


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


def template(name):
    return (ROOT / "tools" / name).read_text(encoding="utf-8")


def from_template(name, pattern):
    """The one match of pattern in a template: the words come from there."""
    found = re.findall(pattern, template(name), re.S)
    if len(found) != 1:
        raise AssertionError("{}: expected one match of {!r}, found {}".format(name, pattern, len(found)))
    return found[0]


def meta(args):
    """{key: value} of render.py's -M arguments."""
    return dict(a.split("=", 1) for a in args[1::2])


def lab_theme(rel):
    """The theme of a lab page's path, or None for a site page."""
    m = re.fullmatch(r"labs/[^/]+/([^/]+)/index\.html", rel)
    return m.group(1) if m else None


def one_line(text):
    return " ".join(text.split())


class ChromePieces(unittest.TestCase):
    """D-0038, D-0061: each piece of chrome pinned by its words.

    Replaced ChromeParity's comparisons with the old build. Every expected
    string is read from tools/render.py or the templates, never retyped, so
    a dress that drops or alters a piece fails. Whitespace is compared as
    single spaces, because the templates break the paragraph across lines.
    """

    def pages(self):
        pages = list(chrome_pages())
        labs = [rel for rel, _ in pages if lab_theme(rel)]
        self.assertEqual(len(labs), 2 * len(list(converted())), labs)
        self.assertEqual(sorted(rel for rel, _ in pages if not lab_theme(rel)),
                         ["courses/index.html", "how-this-was-made/index.html",
                          "index.html", "sims/index.html"])
        return pages

    def test_body_class(self):
        # site/site.css scopes its rules to body.site-page and the themes to
        # body.theme-<name>; the dress puts the template's class first.
        site = from_template("template-site.html", r'<body class="([^"$]+)">')
        doc = from_template("template.html", r'<body class="([^"]+)">')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            want = doc.replace("$theme$", theme) if theme else site
            with self.subTest(page=rel):
                classes = re.search(r'<body class="([^"]*)">', text).group(1).split()
                self.assertEqual(classes[0], want)
                self.assertGreater(len(classes), 1, "Quarto's own classes are kept")

    def test_document_nav(self):
        home = from_template("template.html", r'<a href="\$homehref\$">([^<$]+)</a>')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            if not theme:
                continue
            m = meta(render.document_extras(theme))
            nav = re.findall(r'<nav class="site-nav">.*?</nav>', text, re.S)
            with self.subTest(page=rel):
                self.assertEqual(len(nav), 1)
                links = [(html.unescape(a), one_line(html.unescape(t)))
                         for a, t in re.findall(r"<a ([^>]*)>(.*?)</a>", nav[0], re.S)]
                for piece in (('href="{}"'.format(render.up(3)), home),
                              ('href="{}"'.format(m["uphref"]), m["uplabel"]),
                              ('class="switch" href="{}"'.format(m["switchhref"]), m["switchlabel"])):
                    self.assertEqual(links.count(piece), 1, (piece, links))

    def test_no_document_nav_on_site_pages(self):
        for rel, text in self.pages():
            if not lab_theme(rel):
                with self.subTest(page=rel):
                    self.assertNotIn('<nav class="site-nav">', text)

    def test_presentation_note_and_both_presentations(self):
        both = from_template(
            "template.html",
            r'<footer class="doc-footer">\n<p>\$presentationnote\$</p>\n'
            r'\$if\(homehref\)\$\n<p>([^<$]+)</p>\n\$endif\$\n</footer>')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            footer = re.findall(r'<footer class="doc-footer">\n(.*?)</footer>', text, re.S)
            with self.subTest(page=rel):
                if not theme:
                    self.assertEqual(footer, [])
                    continue
                self.assertEqual(len(footer), 1)
                paras = [one_line(html.unescape(p)) for p in re.findall(r"<p>(.*?)</p>", footer[0], re.S)]
                self.assertEqual(paras, [one_line(render.THEME_NOTE[theme]), one_line(both)])

    def test_method_footnote_only_on_its_page(self):
        shape = from_template(
            "template-site.html",
            r'(<div class="site-foot">\n<p class="print-hide">)\$footnote\$(</p>\n</div>)')
        for rel, text in self.pages():
            found = re.findall(re.escape(shape[0]) + "(.*?)" + re.escape(shape[1]), text, re.S)
            with self.subTest(page=rel):
                if rel == "how-this-was-made/index.html":
                    self.assertEqual([one_line(html.unescape(f)) for f in found],
                                     [one_line(render.METHOD_FOOTNOTE)])
                else:
                    self.assertNotIn('<div class="site-foot">', text)


    def test_landing_footnote_not_carried(self):
        # D-0038: it said the site is built with Pandoc and one build script.
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
    """D-0039 amended: the fonts, their license and the header logo go out."""

    def test_fonts_license_and_header_logo_only(self):
        names = sorted(p.name for p in (QSITE / "site" / "fonts").iterdir())
        self.assertEqual(names, ["OFL.txt", "OpenSans-Bold.woff2", "OpenSans-BoldItalic.woff2",
                                 "OpenSans-Italic.woff2", "OpenSans-Regular.woff2"])
        brand = sorted(p.name for p in (QSITE / "site" / "brand").iterdir())
        self.assertEqual(brand, ["OSU_horizontal_2C_W_over_B.png"])

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
        # before the document theme (docs/agent-reference.md, Measuring and keeping the measured match).
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
    """Rules added for Quarto must not reach the HTML download, which embeds
    site/site.css through tools/template.html without Quarto's markup
    (D-0054, D-0061)."""

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

    def test_download_buttons(self):
        # D-0059: the landing hero's primary button (D-0031) at nav scale,
        # [44] px tall; measured 2026-10-01 on the mockups at 375 px.
        body = re.sub(r"/\*.*?\*/", "", self.block(), flags=re.S)
        m = re.search(r"\.quarto-light \.site-nav a\.download-button\s*\{([^}]*)\}", body)
        self.assertIsNotNone(m, "no download-button rule")
        for decl in ("min-height: 44px", "background: var(--chrome-accent)", "color: #fff", "font-weight: 700"):
            with self.subTest(decl=decl):
                self.assertIn(decl, m.group(1))


if __name__ == "__main__":
    unittest.main()
