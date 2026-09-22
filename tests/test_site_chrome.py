"""Checks on the built site (build/site/). CI runs this after "Site builds".

A missing build is an error, never a skip (LEDGER 53).
"""

import base64
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "site"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
from render import BANNER_MAIN            # noqa: E402
from test_assets import LOGOS, sha256     # noqa: E402

POLICY_LINKS = [
    "https://oregonstate.edu/accessibility-statement",
    "https://oregonstate.edu/official-web-disclaimer",
    "https://eoa.oregonstate.edu/about-us/policies-guidance-and-memos",
]


def setUpModule():
    if not SITE.is_dir():
        raise RuntimeError("build/site is missing: run tools/render.py --site first")


def pages():
    """Built pages that carry the full chrome: not redirect stubs, not sims."""
    for p in sorted(SITE.rglob("index.html")):
        rel = p.relative_to(SITE).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        if re.fullmatch(r"sims/[^/]+/index\.html", rel):
            continue
        yield rel, text


def img_attrs(tag):
    return dict(re.findall(r'(\w+)="([^"]*)"', tag))


def embedded_png_sha(src):
    prefix = "data:image/png;base64,"
    assert src.startswith(prefix), src[:40]
    return sha256(base64.b64decode(src[len(prefix):]))


class FullChrome(unittest.TestCase):

    def test_enough_pages(self):
        self.assertGreaterEqual(len(list(pages())), 6)

    def test_logo_unaltered_and_linked(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                m = re.search(r'<a class="osu-logo" href="https://oregonstate.edu">\s*(<img[^>]*>)', text)
                self.assertIsNotNone(m, "no linked logo")
                attrs = img_attrs(m.group(1))
                self.assertEqual(attrs.get("alt"), "Oregon State University")
                self.assertEqual(embedded_png_sha(attrs["src"]), LOGOS["OSU_horizontal_2C_W_over_B.png"])

    def test_top_strip_links_department(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                self.assertIn('<a href="https://physics.oregonstate.edu">Department of Physics</a>', text)

    def test_draft_banner_and_noindex(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                # Pandoc wraps long metadata lines, so the sentence can break across lines.
                flat = " ".join(text.split())
                self.assertIn(BANNER_MAIN, flat)
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_footer_as_ruled(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                foot = re.search(r'<footer class="osu-foot">.*?</footer>', text, re.S)
                self.assertIsNotNone(foot)
                for url in POLICY_LINKS:
                    self.assertIn(url, foot.group(0))
                for banned in ("mailto:", "tel:", "&copy;", "©", "Copyright"):
                    self.assertNotIn(banned, text)


class DocumentBodies(unittest.TestCase):
    """D-0010: branding never changes a document's <main>."""

    def test_bodies_unchanged(self):
        want = json.loads((ROOT / "tests" / "fixtures" / "main-bodies.json").read_text(encoding="utf-8"))
        for rel, digest in want.items():
            with self.subTest(page=rel):
                text = (SITE / rel).read_text(encoding="utf-8")
                main = re.search(r"<main>.*?</main>", text, re.S).group(0)
                self.assertEqual(hashlib.sha256(main.encode()).hexdigest(), digest)


class SimBar(unittest.TestCase):
    """D-0005, D-0020, D-0022; LEDGER 51: source plus the bar, nothing else."""

    BAR = re.compile(r"<body[^>]*>(\n<style>\n\.lib-bar.*?</div>\n)", re.S)

    def sims(self):
        for src in sorted((ROOT / "sims").glob("*/index.html")):
            yield src, SITE / "sims" / src.parent.name / "index.html"

    def test_source_plus_bar_only(self):
        for src, pub in self.sims():
            with self.subTest(sim=src.parent.name):
                p = pub.read_text(encoding="utf-8")
                m = self.BAR.search(p)
                self.assertIsNotNone(m, "no bar after <body>")
                self.assertEqual(p.replace(m.group(1), "", 1), src.read_text(encoding="utf-8"))

    def test_bar_logo_and_banner(self):
        for src, pub in self.sims():
            with self.subTest(sim=src.parent.name):
                bar = self.BAR.search(pub.read_text(encoding="utf-8")).group(1)
                self.assertIn("background: #000", bar)
                self.assertIn('<span class="lib-draft">' + BANNER_MAIN + "</span>", bar)
                img = re.search(r'<a href="https://oregonstate.edu">(<img[^>]*>)</a>', bar)
                self.assertIsNotNone(img)
                attrs = img_attrs(img.group(1))
                self.assertEqual(attrs.get("alt"), "Oregon State University")
                self.assertEqual(embedded_png_sha(attrs["src"]), LOGOS["OSU_horizontal_2C_O_over_W.png"])


if __name__ == "__main__":
    unittest.main()
