"""The lab downloads in the built Quarto site (D-0052, D-0053).

A missing build or tool is an error, never a skip (LEDGER 53). Reads
build/quarto-site/; run tools/quarto_build.py first.
"""

import os
import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
PANDOC = os.environ.get("PANDOC", "pandoc")
PDFTOTEXT = os.environ.get("PDFTOTEXT", "pdftotext")
FILTER = ROOT / "tools" / "filters" / "questions.lua"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import downloads                          # noqa: E402
from render import BANNER_MAIN, BANNER_DETAIL  # noqa: E402
from test_quarto_site import converted    # noqa: E402

LABELS = {"docx": "Word", "html": "HTML", "pdf": "PDF", "md": "Markdown"}
FOOTER_NEW = "Downloads carry the same draft notice as these pages."
FOOTER_OLD = "are not wired up in this draft"
# The owner's words for every download, in place of the logo (chat, 2026-10-01).
PHYSICS = "Department of Physics, Oregon State University"


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("build/quarto-site is missing: run tools/quarto_build.py first")


def page(doc_id, theme):
    return (QSITE / "labs" / doc_id / theme / "index.html").read_text(encoding="utf-8")


def flat(text):
    return " ".join(text.split())


class Links(unittest.TestCase):
    """D-0053: the approved links on modern pages only, outside <main>."""

    def site_nav(self, text):
        m = re.search(r'<nav class="site-nav">.*?</nav>', text, re.S)
        self.assertIsNotNone(m, "no site-nav")
        return m.group(0)

    def test_modern_page_links_every_download(self):
        for doc_id, _ in converted():
            nav = self.site_nav(page(doc_id, "modern"))
            for ext in downloads.EXTENSIONS:
                with self.subTest(doc=doc_id, ext=ext):
                    self.assertIn('<a href="../{0}.{1}" download="{0}.{1}">{2}</a>'.format(
                        doc_id, ext, LABELS[ext]), nav)

    def test_approved_wording(self):
        for doc_id, _ in converted():
            nav = flat(re.sub(r"<[^>]+>", "", self.site_nav(page(doc_id, "modern"))))
            with self.subTest(doc=doc_id):
                self.assertIn("Download: Word · HTML · PDF · Markdown", nav.replace("&middot;", "·"))

    def test_faithful_page_offers_none(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                self.assertNotIn(" download=", page(doc_id, "faithful"))

    def test_links_outside_main(self):
        for doc_id, _ in converted():
            main = re.search(r"<main>.*?</main>", page(doc_id, "modern"), re.S).group(0)
            with self.subTest(doc=doc_id):
                self.assertNotIn(" download=", main)

    def test_footer_sentence(self):
        for doc_id, _ in converted():
            for theme in ("modern", "faithful"):
                text = flat(page(doc_id, theme))
                with self.subTest(doc=doc_id, theme=theme):
                    self.assertIn(FOOTER_NEW, text)
                    self.assertNotIn(FOOTER_OLD, text)


def words(text):
    """Letters and digits only, so bullets and list marks cannot differ."""
    return re.findall(r"[\w’']+", text)


def plain(*args, input=None):
    return subprocess.run([PANDOC, *args, "-t", "plain"], input=input, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


class MarkdownAndWord(unittest.TestCase):

    def docx(self, doc_id):
        return QSITE / "labs" / doc_id / (doc_id + ".docx")

    def test_markdown_is_the_source_byte_for_byte(self):
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                got = (QSITE / "labs" / doc_id / (doc_id + ".md")).read_bytes()
                self.assertEqual(got, source.read_bytes())

    def test_word_is_banner_then_the_modern_words(self):
        banner = words(BANNER_MAIN + " " + BANNER_DETAIL)
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                got = words(plain(str(self.docx(doc_id))))
                want = words(plain(str(source), "-f", "markdown-smart",
                                   "--lua-filter", str(FILTER), "-M", "theme=modern"))
                self.assertEqual(got[:len(banner)], banner)
                self.assertEqual(got[len(banner):], want)
                self.assertIn("Question", got)

    def test_word_footer_names_the_department_and_counts_pages(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id), zipfile.ZipFile(self.docx(doc_id)) as z:
                body = z.read("word/document.xml").decode("utf-8")
                self.assertRegex(body, r'<w:footerReference\b[^>]*\bw:type="default"')
                footers = [z.read(n).decode("utf-8") for n in z.namelist()
                           if re.fullmatch(r"word/footer\d*\.xml", n)]
                self.assertEqual(len(footers), 1)
                text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", footers[0]))
                self.assertIn(PHYSICS, text)
                self.assertRegex(footers[0], r'w:instr=" PAGE "')
                self.assertRegex(footers[0], r'w:instr=" NUMPAGES "')


if __name__ == "__main__":
    unittest.main()
