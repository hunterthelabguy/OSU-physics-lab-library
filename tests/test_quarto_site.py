"""Checks on the Quarto build (build/quarto-site/), migration phase 1 (D-0033).

A missing build is an error, never a skip (LEDGER 53). The chrome suite,
test_site_chrome.py, is phase 2's contract and is not asserted here.
"""

import html
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
PANDOC = os.environ.get("PANDOC", "pandoc")
FILTER = ROOT / "tools" / "filters" / "questions.lua"
sys.path.insert(0, str(ROOT / "tests"))
import test_site_chrome as chrome         # noqa: E402  (for SimBar.BAR only)


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("build/quarto-site is missing: run tools/quarto_build.py first")


def converted():
    """(id, path) of every converted curriculum document."""
    for p in sorted((ROOT / "curriculum").rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        if text.startswith("---") and re.search(r"^source_file:", text, re.M):
            yield re.search(r"^id:\s*(\S+)", text, re.M).group(1), p


def is_redirect(text):
    return 'http-equiv="refresh"' in text


def is_sim(rel):
    return re.fullmatch(r"sims/[^/]+/index\.html", rel) is not None


def html_pages():
    for p in sorted(QSITE.rglob("*.html")):
        rel = p.relative_to(QSITE).as_posix()
        if rel.startswith("site_libs/"):
            continue
        yield rel, p, p.read_text(encoding="utf-8")


def words(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split()


class Pages(unittest.TestCase):

    def test_expected_pages(self):
        want = ["index.html", "404.html", "courses/index.html",
                "how-this-was-made/index.html", "sims/index.html"]
        for doc_id, _ in converted():
            want += [f"labs/{doc_id}/modern/index.html",
                     f"labs/{doc_id}/faithful/index.html"]
        for rel in want:
            with self.subTest(page=rel):
                self.assertTrue((QSITE / rel).is_file())

    def test_404_page_resolves_links_from_the_root(self):
        # Pages serves 404.html at whatever path was asked for, so the
        # chrome's relative nav links need a base (D-0049).
        text = (QSITE / "404.html").read_text(encoding="utf-8")
        self.assertEqual(text.count("<base "), 1)
        head = text.split("</head>", 1)[0]
        self.assertIn('<base href="/">', head)
        self.assertLess(head.index("<base "), head.index("<link "))

    def test_noindex_on_every_page(self):
        for rel, _, text in html_pages():
            if is_sim(rel):
                continue
            with self.subTest(page=rel):
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_one_h1_per_page(self):
        for rel, _, text in html_pages():
            if is_sim(rel) or is_redirect(text):
                continue
            with self.subTest(page=rel):
                self.assertEqual(len(re.findall(r"<h1\b", text)), 1)

    def test_source_front_matter_not_rendered(self):
        for rel, _, text in html_pages():
            with self.subTest(page=rel):
                self.assertNotIn("source_sha256", text)

    def test_stylesheets_resolve(self):
        for rel, path, text in html_pages():
            # Every <link> tag, whatever order its attributes come in: Quarto
            # writes its own as href-then-rel and ours as rel-then-href.
            for tag in re.findall(r"<link\b[^>]*>", text):
                found = re.search(r'href="([^"]+)"', tag)
                if 'rel="stylesheet"' not in tag or not found:
                    continue
                href = found.group(1)
                if href.startswith("data:"):
                    continue
                # Quarto writes a 404 page's links from the site root.
                base = QSITE if href.startswith("/") else path.parent
                with self.subTest(page=rel, href=href):
                    self.assertTrue((base / href.split("?")[0].lstrip("/")).resolve().is_file())


class NoThirdParty(unittest.TestCase):
    """D-0033: no theme or setting that loads a third-party resource."""

    TAG = re.compile(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', re.I)
    CSS = re.compile(r'(?:@import\s*(?:url\()?|url\()\s*["\']?(?:https?:)?//', re.I)

    def test_pages(self):
        for rel, _, text in html_pages():
            with self.subTest(page=rel):
                self.assertIsNone(self.TAG.search(text))

    def test_stylesheets(self):
        for css in QSITE.rglob("*.css"):
            with self.subTest(css=css.relative_to(QSITE).as_posix()):
                self.assertIsNone(self.CSS.search(css.read_text(encoding="utf-8")))


class Documents(unittest.TestCase):
    """LEDGER 28 and the question filter, as Quarto renders them."""

    def reference_words(self, source, theme):
        out = subprocess.run(
            [PANDOC, str(source), "-f", "markdown-smart", "-t", "html",
             "--lua-filter", str(FILTER), "-M", "theme-name=" + theme],
            check=True, capture_output=True, text=True, encoding="utf-8").stdout
        return words(out)

    def test_words_match_a_plain_pandoc_render(self):
        # The document's words, in order, appear unbroken inside Quarto's <main>.
        for doc_id, source in converted():
            for theme in ("modern", "faithful"):
                with self.subTest(doc=doc_id, theme=theme):
                    page = (QSITE / "labs" / doc_id / theme / "index.html").read_text(encoding="utf-8")
                    main = re.search(r"<main\b.*?</main>", page, re.S).group(0)
                    want = "\x00".join(self.reference_words(source, theme))
                    self.assertIn(want, "\x00".join(words(main)))

    def test_questions_numbered(self):
        for doc_id, source in converted():
            n = len(re.findall(r"\{\.question\b", source.read_text(encoding="utf-8")))
            self.assertGreater(n, 0)
            base = QSITE / "labs" / doc_id
            modern = (base / "modern" / "index.html").read_text(encoding="utf-8")
            faithful = (base / "faithful" / "index.html").read_text(encoding="utf-8")
            with self.subTest(doc=doc_id):
                for k in range(1, n + 1):
                    self.assertIn(f"Question {k}<", modern)
                    self.assertIn(f"<strong>{k})", faithful)
                self.assertNotIn(f"Question {n + 1}<", modern)


class SimsAndStubs(unittest.TestCase):
    """LEDGER 51 (sims), LEDGER 37 (robots), and the trimmed-URL stubs."""

    def test_sim_is_source_plus_bar_only(self):
        for src in sorted((ROOT / "sims").glob("*/index.html")):
            with self.subTest(sim=src.parent.name):
                pub = (QSITE / "sims" / src.parent.name / "index.html").read_text(encoding="utf-8")
                m = chrome.SimBar.BAR.search(pub)
                self.assertIsNotNone(m, "no bar after <body>")
                self.assertEqual(pub.replace(m.group(1), "", 1), src.read_text(encoding="utf-8"))

    def test_robots_disallows_everything(self):
        text = (QSITE / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *\nDisallow: /\n", text)
        self.assertNotIn("Sitemap", text)

    def test_trimmed_lab_url_redirects_to_modern(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                text = (QSITE / "labs" / doc_id / "index.html").read_text(encoding="utf-8")
                self.assertTrue(is_redirect(text))
                self.assertIn('url=modern/', text)


if __name__ == "__main__":
    unittest.main()
