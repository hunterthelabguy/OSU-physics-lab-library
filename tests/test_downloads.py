"""The lab downloads in the built Quarto site (D-0052, D-0053).

A missing build or tool is an error, never a skip (LEDGER 53). Reads
build/quarto-site/; run tools/quarto_build.py first.
"""

import html
import os
import re
import subprocess
import sys
import tempfile
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
                    self.assertIn('<a class="download-button" href="../{0}.{1}" download="{0}.{1}">{2}</a>'.format(
                        doc_id, ext, LABELS[ext]), nav)

    def test_approved_wording(self):
        # D-0059: the label and the four names as D-0053 approved them; the
        # buttons' gaps replace the middots.
        for doc_id, _ in converted():
            row = re.search(r'<span class="download-row">.*?</a></span>',
                            self.site_nav(page(doc_id, "modern")), re.S)
            with self.subTest(doc=doc_id):
                self.assertIsNotNone(row, "no download-row")
                text = flat(re.sub(r"<[^>]+>", " ", row.group(0)))
                self.assertEqual(text, "Download: Word HTML PDF Markdown")
                self.assertNotIn("&middot;", row.group(0))
                self.assertIn('<span class="download-label">Download:</span>', row.group(0))

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

    # These read the Word file's XML. What Word shows on the page is checked
    # by the owner in Word, never by these tests (D-0057).

    def part(self, doc_id, name):
        with zipfile.ZipFile(self.docx(doc_id)) as z:
            return z.read(name).decode("utf-8")

    def parts(self, doc_id, pattern):
        with zipfile.ZipFile(self.docx(doc_id)) as z:
            return [z.read(n).decode("utf-8") for n in z.namelist() if re.fullmatch(pattern, n)]

    def style(self, doc_id, style_id):
        m = re.search(r'<w:style\b[^>]*\bw:styleId="{}".*?</w:style>'.format(style_id),
                      self.part(doc_id, "word/styles.xml"), re.S)
        self.assertIsNotNone(m, "no style " + style_id)
        return m.group(0)

    def test_word_body_is_the_modern_words(self):
        # D-0057: the draft notice moved to the page header, so the body is
        # the modern words alone (the body's banner paragraphs are gone).
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                got = words(plain(str(self.docx(doc_id))))
                want = words(plain(str(source), "-f", "markdown-smart",
                                   "--lua-filter", str(FILTER), "-M", "theme=modern"))
                self.assertEqual(got, want)
                self.assertIn("Question", got)
                self.assertNotIn(flat(BANNER_DETAIL), flat(" ".join(got)))

    def test_word_header_is_the_draft_notice(self):
        # D-0057: BANNER_MAIN, the approved words, on every page, [9] pt
        # bold and centered, the size and weight of the PDF's banner box.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                body = self.part(doc_id, "word/document.xml")
                self.assertRegex(body, r'<w:headerReference\b[^>]*\bw:type="default"')
                headers = self.parts(doc_id, r"word/header\d*\.xml")
                self.assertEqual(len(headers), 1)
                text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", headers[0]))
                self.assertEqual(text, BANNER_MAIN)
                self.assertIn('<w:pStyle w:val="Header"', headers[0])
                self.assertNotIn("<w:rPr>", headers[0], "formatting belongs on the Header style")
                header = self.style(doc_id, "Header")
                for want in (r'<w:jc w:val="center"', r"<w:b\s*/>", r'<w:sz w:val="18"'):
                    self.assertRegex(header, want)

    def test_word_footer_names_the_department_and_counts_pages(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                body = self.part(doc_id, "word/document.xml")
                self.assertRegex(body, r'<w:footerReference\b[^>]*\bw:type="default"')
                footers = self.parts(doc_id, r"word/footer\d*\.xml")
                self.assertEqual(len(footers), 1)
                text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", footers[0]))
                self.assertIn(PHYSICS, text)
                self.assertRegex(footers[0], r'w:instr=" PAGE "')
                self.assertRegex(footers[0], r'w:instr=" NUMPAGES "')

    def test_word_footer_size_is_on_the_style(self):
        # D-0057: Word rebuilds the PAGE and NUMPAGES results and dropped the
        # 8 pt set on their cached runs, so the [8] pt lives on the footer
        # paragraph's style and no run in the footer sets a size.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                footer = self.parts(doc_id, r"word/footer\d*\.xml")[0]
                self.assertIn('<w:pStyle w:val="Footer"', footer)
                self.assertNotIn("<w:sz", footer)
                self.assertIn('<w:sz w:val="16"', self.style(doc_id, "Footer"))

    def test_word_page_is_letter_with_the_print_margins(self):
        # D-0057: the PDF's page, from site/site.css's @page: Letter,
        # [12240] by [15840] twips, margins [1080] twips (0.75 in) each side.
        css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
        page_rule = re.search(r"@page\s*\{(.*?)\n\}", css, re.S).group(1)
        self.assertRegex(page_rule, r"size:\s*letter;")
        inches = float(re.search(r"margin:\s*([\d.]+)in;", page_rule).group(1))
        twips = str(round(inches * 1440))
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                sect = re.search(r"<w:sectPr>.*?</w:sectPr>", self.part(doc_id, "word/document.xml"), re.S).group(0)
                self.assertRegex(sect, r'<w:pgSz\b(?=[^>]*\bw:w="12240")(?=[^>]*\bw:h="15840")')
                for side in ("top", "right", "bottom", "left"):
                    self.assertRegex(sect, r'<w:pgMar\b[^>]*\bw:{}="{}"'.format(side, twips))

    def test_word_questions_have_their_own_styles(self):
        # D-0057: each question is a Question Label paragraph ("Question N")
        # then its text in the Question style, in document order.
        for doc_id, source in converted():
            count = len(re.findall(r"^:::+ *\{\.question\b", source.read_text(encoding="utf-8"), re.M))
            with self.subTest(doc=doc_id, questions=count):
                paras = re.findall(r"<w:p\b.*?</w:p>", self.part(doc_id, "word/document.xml"), re.S)
                styled = [(re.search(r'<w:pStyle w:val="([^"]+)"', p) or [None, None])[1] for p in paras]
                labels = [i for i, s in enumerate(styled) if s == "QuestionLabel"]
                self.assertEqual(len(labels), count)
                self.assertGreater(count, 0)
                for n, i in enumerate(labels, 1):
                    text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", paras[i]))
                    self.assertEqual(text, "Question {}".format(n))
                    self.assertEqual(styled[i + 1], "Question")

    def test_word_question_styles_keep_whole_and_rule_left(self):
        # D-0057: the PDF's print look; both styles keep with the next
        # paragraph and keep their lines, share one left rule so Word draws
        # it as one, and Enter after a question starts plain Body Text.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                label, question = self.style(doc_id, "QuestionLabel"), self.style(doc_id, "Question")
                for s in (label, question):
                    self.assertIn("<w:keepNext", s)
                    self.assertIn("<w:keepLines", s)
                rule = lambda s: re.search(r"<w:pBdr>.*?</w:pBdr>", s, re.S).group(0)
                self.assertIn("<w:left ", rule(question))
                self.assertEqual(rule(label), rule(question))
                indent = lambda s: re.search(r"<w:ind\b[^>]*/>", s).group(0)
                self.assertEqual(indent(label), indent(question))
                self.assertIn('<w:next w:val="BodyText"', question)
                self.assertIn("<w:caps", label)
                self.assertNotRegex(question, r"<w:b\s*/>")

    def test_word_headings_keep_with_next(self):
        # A pin, not a change: Pandoc's default Heading 1 to 3 already keep
        # with the next paragraph; a Pandoc upgrade that dropped it fails here.
        for doc_id, _ in converted():
            for level in (1, 2, 3):
                with self.subTest(doc=doc_id, level=level):
                    self.assertIn("<w:keepNext", self.style(doc_id, "Heading{}".format(level)))


# Measured 2026-10-01: 161,024 bytes (Lab 1), times 1.10, rounded up to the
# next 10,000. Never a guess; remeasure when a lab is added.
HTML_CAP_BYTES = 180_000


class Html(unittest.TestCase):
    """A plain render of the source: banner, department line, modern theme,
    no site chrome, everything embedded (owner's ruling, chat 2026-10-01)."""

    def path(self, doc_id):
        return QSITE / "labs" / doc_id / (doc_id + ".html")

    def download(self, doc_id):
        return self.path(doc_id).read_text(encoding="utf-8")

    def test_self_contained(self):
        for doc_id, _ in converted():
            text = self.download(doc_id)
            with self.subTest(doc=doc_id):
                self.assertNotIn("<script", text)
                self.assertNotIn("<link", text)
                for url in re.findall(r'\b(?:src|href)="([^"]*)"', text):
                    self.assertFalse(downloads.is_relative(url), url)
                self.assertIn("data:font/woff2;base64,", text)

    def test_no_site_chrome(self):
        for doc_id, _ in converted():
            text = self.download(doc_id)
            with self.subTest(doc=doc_id):
                for chrome in ('class="osu-header"', 'class="site-nav"', 'class="osu-foot"'):
                    self.assertNotIn(chrome, text)

    def test_banner_department_and_noindex(self):
        for doc_id, _ in converted():
            text = self.download(doc_id)
            with self.subTest(doc=doc_id):
                self.assertIn(BANNER_MAIN, flat(text))
                self.assertIn(PHYSICS, flat(text))
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_main_is_the_line_then_the_modern_pages(self):
        for doc_id, _ in converted():
            want = re.search(r"<main>\n(.*?)</main>", page(doc_id, "modern"), re.S).group(1)
            got = re.search(r"<main>\n(.*?)</main>", self.download(doc_id), re.S).group(1)
            with self.subTest(doc=doc_id):
                self.assertEqual(got, "<p>{}</p>\n{}".format(PHYSICS, want))

    def test_size_capped(self):
        self.assertIsNotNone(HTML_CAP_BYTES, "set HTML_CAP_BYTES from the measurement")
        for doc_id, _ in converted():
            size = self.path(doc_id).stat().st_size
            with self.subTest(doc=doc_id, size=size):
                self.assertLessEqual(size, HTML_CAP_BYTES)


def pdf_text(path):
    return subprocess.run([PDFTOTEXT, "-layout", str(path), "-"], check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


class Pdf(unittest.TestCase):
    """The modern page printed with the site's print rules (D-0053)."""

    def path(self, doc_id):
        return QSITE / "labs" / doc_id / (doc_id + ".pdf")

    def text(self, doc_id):
        return pdf_text(self.path(doc_id))

    def test_is_a_pdf(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                self.assertEqual(self.path(doc_id).read_bytes()[:5], b"%PDF-")

    def test_banner_running_header_title_and_footer(self):
        for doc_id, source in converted():
            title = re.search(r"^# (.+)$", source.read_text(encoding="utf-8"), re.M).group(1)
            raw = self.text(doc_id)
            text = flat(raw)
            # The footer's own line, so the phrase in a lab's text cannot count.
            footers = re.findall(re.escape(PHYSICS) + r"[ \t]+Page (\d+) of (\d+)", raw)
            with self.subTest(doc=doc_id):
                self.assertIn(BANNER_MAIN, text)
                self.assertIn("DRAFT: license pending", text)
                self.assertIn(flat(title), text)
                self.assertTrue(footers, "no department footer beside 'Page N of M'")
                total = int(footers[0][1])
                self.assertEqual(footers, [(str(k), str(total)) for k in range(1, total + 1)],
                                 "the department beside the page count on every page")


class PrintKeeps(unittest.TestCase):
    """D-0058: in print, a question block stays whole and a heading never
    ends a page. The rules are the theme's (themes/modern.css, @media print)
    and site/site.css's; this pins that Chrome honors them.

    Lab 1 as printed puts no heading or question near a page break, so the
    built modern page is printed again from a temporary copy (a <base> points
    it at the build, so nothing is written into the folder that deploys) with
    a spacer at the top of <main> that pushes content across the breaks. With
    the keep rules switched off, the same offsets must split something, which
    proves they still cross a break here; with the rules on, nothing splits.
    Offsets measured 2026-10-01: with the rules off, 50 splits over 40
    offsets from 0 to 975 px; with them on, none."""

    OFFSETS = (100, 450, 575, 800, 950)
    RULES_OFF = ("<style>@media print { .question, .box { break-inside: auto !important; }"
                 " h1, h2, h3 { break-after: auto !important; } }</style>")

    def printed(self, doc_id, spacer, rules_off):
        folder = QSITE / "labs" / doc_id / "modern"
        text = (folder / "index.html").read_text(encoding="utf-8")
        text = text.replace("<head>", '<head><base href="{}">'.format(folder.as_uri() + "/"), 1)
        extra = (self.RULES_OFF if rules_off else "") + '<div style="height:{}px"></div>'.format(spacer)
        self.assertEqual(text.count("<main>"), 1)
        text = text.replace("<main>", "<main>" + extra, 1)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "page.html"
            src.write_text(text, encoding="utf-8")
            pdf = Path(tmp) / "page.pdf"
            subprocess.run([downloads.CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            "--print-to-pdf=" + str(pdf), src.as_uri()], check=True, capture_output=True)
            return pdf_text(pdf)

    def splits(self, doc_id, raw):
        """Headings that end a page and question blocks broken over two."""
        built = page(doc_id, "modern")
        main = re.search(r"<main>(.*?)</main>", built, re.S).group(1)
        headings = [flat(html.unescape(re.sub(r"<[^>]+>", "", h))) for h in re.findall(r"<h[123]\b[^>]*>(.*?)</h[123]>", main, re.S)]
        found = []
        pages = raw.split("\f")[:-1]
        for i, pg in enumerate(pages, 1):
            lines = [flat(l) for l in pg.split("\n") if l.strip()]
            body = [l for l in lines if not l.startswith(PHYSICS) and l != "DRAFT: license pending"]
            if body and any(h.endswith(body[-1]) for h in headings):
                found.append("page {} ends with a heading: {}".format(i, body[-1]))
        text = "\f".join(" ".join(words(p)) for p in pages)
        for n, rest in re.findall(r'<div class="question-label">\s*<p>Question (\d+)</p>\s*</div>(.*?)</div>', main, re.S):
            end = " ".join(words(re.sub(r"<[^>]+>", " ", rest))[-3:])
            start = text.find("QUESTION " + n)
            stop = text.find(end, start)
            if start < 0 or stop < 0:
                found.append("question {} not found in the print".format(n))
            elif "\f" in text[start:stop]:
                found.append("question {} broken over a page".format(n))
        return found

    def test_offsets_still_cross_a_break(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                found = [s for px in self.OFFSETS for s in self.splits(doc_id, self.printed(doc_id, px, True))]
                self.assertTrue(found, "no offset splits anything with the rules off: "
                                       "re-pick OFFSETS against this Chrome")

    def test_nothing_splits_with_the_rules_on(self):
        for doc_id, _ in converted():
            for px in (0,) + self.OFFSETS:
                with self.subTest(doc=doc_id, spacer=px):
                    raw = self.printed(doc_id, px, False)
                    self.assertEqual(self.splits(doc_id, raw), [])
                    if px == 0:
                        # The copy prints as the download does, fonts and all.
                        shipped = pdf_text(QSITE / "labs" / doc_id / (doc_id + ".pdf"))
                        self.assertEqual(raw.count("\f"), shipped.count("\f"))


if __name__ == "__main__":
    unittest.main()
