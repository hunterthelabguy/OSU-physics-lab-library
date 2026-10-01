"""Phase 2 chrome on the Quarto build (D-0036 to D-0039, D-0042).

Needs both builds: build/site/ (the old build, the chrome's source) and
build/quarto-site/. A missing build is an error, never a skip (LEDGER 53).
"""

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


class Navigation(unittest.TestCase):
    """D-0037: one nav, no search."""

    def test_no_quarto_navbar_or_search(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertNotIn('id="quarto-header"', text)
                self.assertNotIn("quarto-search", text)

    def test_no_search_index(self):
        self.assertFalse((QSITE / "search.json").exists())


class Published(unittest.TestCase):
    """D-0039: only the fonts and their license go out."""

    def test_fonts_and_license_only(self):
        names = sorted(p.name for p in (QSITE / "site" / "fonts").iterdir())
        self.assertEqual(names, ["OFL.txt", "OpenSans-Bold.woff2", "OpenSans-BoldItalic.woff2",
                                 "OpenSans-Italic.woff2", "OpenSans-Regular.woff2"])
        self.assertFalse((QSITE / "site" / "brand").exists())

    def test_no_markdown_published(self):
        self.assertEqual([p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.md")], [])


if __name__ == "__main__":
    unittest.main()
