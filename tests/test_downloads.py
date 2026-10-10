"""The lab downloads in the built Quarto site (D-0052, D-0053).

A missing build or tool is an error, never a skip (LEDGER 53). Reads
build/quarto-site/; run tools/quarto_build.py first.
"""

import hashlib
import html
import json
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
import check_unchanged                    # noqa: E402
import downloads                          # noqa: E402
import figure_fixture as fx               # noqa: E402
import media                              # noqa: E402
import render                             # noqa: E402
from render import BANNER_MAIN, BANNER_DETAIL  # noqa: E402
from test_quarto_site import converted, question_numbers, split_figures  # noqa: E402
import test_quarto_site                   # noqa: E402

LABELS = {"docx": "Word", "html": "HTML", "pdf": "PDF", "md": "Markdown"}

# The modern page's values that the Word file follows (D-0057): the light
# scheme's colors, the body's size and line height, and the paragraph and
# list item gaps, all in rem except the unitless line height.
_MODERN = (ROOT / "themes" / "modern.css").read_text(encoding="utf-8")
MODERN_ROOT = dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})", re.search(r":root\s*\{(.*?)\}", _MODERN, re.S).group(1)))
_BODY = re.search(r"\nbody\s*\{(.*?)\}", _MODERN, re.S).group(1)
MODERN_BODY = {"font-size": float(re.search(r"font-size:\s*([\d.]+)rem", _BODY).group(1)),
               "line-height": float(re.search(r"line-height:\s*([\d.]+);", _BODY).group(1))}
MODERN_P_GAP = float(re.search(r"\np\s*\{\s*margin:\s*0 0 ([\d.]+)rem;", _MODERN).group(1))
MODERN_LI_GAP = float(re.search(r"\nli\s*\{\s*margin:\s*0 0 ([\d.]+)rem;", _MODERN).group(1))
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

    def test_links_outside_main(self):
        for doc_id, _ in converted():
            main = re.search(r"<main>.*?</main>", page(doc_id, "modern"), re.S).group(0)
            with self.subTest(doc=doc_id):
                self.assertNotIn(" download=", main)

    def test_footer_sentence(self):
        for doc_id, _ in converted():
            for theme in ("modern",):
                text = flat(page(doc_id, theme))
                with self.subTest(doc=doc_id, theme=theme):
                    self.assertIn(FOOTER_NEW, text)
                    self.assertNotIn(FOOTER_OLD, text)
                    # D-0116: the one-source point lives on "How this site works" only.
                    self.assertNotIn("drift apart", text)


def words(text):
    """Letters and digits only, so bullets and list marks cannot differ."""
    return re.findall(r"[\w’']+", text)


def read_words(*args):
    """Words and equations of a document, read through Pandoc's syntax tree
    as the word check reads them: an equation is left out of the words and
    compared apart (D-0113), since Pandoc's plain writer warns on TeX math.
    Returns (words, [(kind, tex)])."""
    doc = json.loads(subprocess.run([PANDOC, *args, "-t", "json"], check=True,
                                    capture_output=True, encoding="utf-8").stdout)
    buf, found = [], {"math": [], "images": [], "figures": [], "figure": lambda ids: []}
    check_unchanged.ast_chars(doc["blocks"], buf, found=found)
    return words("".join(c for c, _ in buf)), found["math"], doc["pandoc-api-version"]


def word_equations(path):
    """The Word file's equations as the word check reads Word's (D-0113)."""
    with zipfile.ZipFile(path) as z:
        return check_unchanged.omml_equations(z.read("word/document.xml"))


def same_equations(test, source_math, api, docx):
    want = check_unchanged.tex_equations(source_math, api)
    got = word_equations(docx)
    test.assertEqual([(e["kind"], e["norm"], e["shape"]) for e in got],
                     [(e["kind"], e["norm"], e["shape"]) for e in want])


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
        # Equations are compared apart (D-0113).
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                got, _, _ = read_words(str(self.docx(doc_id)))
                want, math, api = read_words(str(source), "-f", render.FROM,
                                             "--lua-filter", str(FILTER), "-M", "theme=modern")
                self.assertEqual(got, want)
                self.assertIn("Question", got)
                self.assertNotIn(flat(BANNER_DETAIL), flat(" ".join(got)))
                same_equations(self, math, api, self.docx(doc_id))

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

    def boxes(self, doc_id):
        """Each one-cell table in the body: (its XML, its paragraphs' styles, its text)."""
        out = []
        for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", self.part(doc_id, "word/document.xml"), re.S):
            paras = re.findall(r"<w:p\b.*?</w:p>", tbl, re.S)
            styles = [(re.search(r'<w:pStyle w:val="([^"]+)"', p) or [None, None])[1] for p in paras]
            texts = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras]
            out.append((tbl, styles, texts))
        return out

    def test_word_questions_are_one_cell_tables(self):
        # D-0082 (amends D-0057): each question is one table of one cell,
        # its Question Label paragraph ("Question N") first, in document
        # order, so a list or a bullet between parts sits inside the box.
        for doc_id, source in converted():
            numbers = question_numbers(source.read_text(encoding="utf-8"))
            count = len(numbers)
            with self.subTest(doc=doc_id, questions=count):
                boxes = [b for b in self.boxes(doc_id) if "QuestionLabel" in b[1]]
                self.assertEqual(len(boxes), count)
                self.assertGreater(count, 0)
                for n, (tbl, styles, texts) in zip(numbers, boxes):
                    self.assertEqual(len(re.findall(r"<w:tc>", tbl)), 1)
                    self.assertEqual(styles[0], "QuestionLabel")
                    self.assertEqual(texts[0], "Question {}".format(n))
                    self.assertTrue(any(texts[1:]), "the question's words are in the box")
                self.assertNotIn('w:val="QuestionLabel"', re.sub(
                    r"<w:tbl>.*?</w:tbl>", "", self.part(doc_id, "word/document.xml"), flags=re.S))

    def test_word_box_is_the_modern_block(self):
        # D-0057, D-0082: the modern page's question block, from
        # themes/modern.css: its --accent rule down the left, [3] pt (sz 24),
        # its --tint behind, kept on one page, across the text column of the
        # Letter page; the label in capitals, kept with the question.
        accent, tint = (MODERN_ROOT[k].lstrip("#").upper() for k in ("--accent", "--tint"))
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                sect = re.search(r"<w:sectPr>.*?</w:sectPr>", self.part(doc_id, "word/document.xml"), re.S).group(0)
                page = int(re.search(r'<w:pgSz\b[^>]*\bw:w="(\d+)"', sect).group(1))
                left = int(re.search(r'<w:pgMar\b[^>]*\bw:left="(\d+)"', sect).group(1))
                right = int(re.search(r'<w:pgMar\b[^>]*\bw:right="(\d+)"', sect).group(1))
                for tbl, styles, _ in self.boxes(doc_id):
                    if "QuestionLabel" not in styles:
                        continue
                    self.assertRegex(tbl, r'<w:left w:val="single" w:sz="24" w:space="0" w:color="{}"/>'.format(accent))
                    self.assertRegex(tbl, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(tint))
                    self.assertIn("<w:cantSplit/>", tbl)
                    self.assertIn('<w:tblW w:w="{}" w:type="dxa"/>'.format(page - left - right), tbl)
                label = self.style(doc_id, "QuestionLabel")
                self.assertIn("<w:caps", label)
                self.assertIn("<w:keepNext", label)
                self.assertNotIn("<w:pBdr>", label)
                self.assertNotIn("<w:shd", label)

    def test_word_box_holds_a_list_between_parts(self):
        # D-0082 (finding 3, F14(b)): a stem, lettered parts and a round-bullet
        # action between them draw as one box, which custom-style could not.
        body = ("::: {.question #probe:parts}\n**Make a plot.**\n\na.  **Slope?**\nb.  **Units?**\n\n"
                "::: action\n- An action between parts.\n:::\n\nc.  **Agree?**\n:::\n\nAfter.\n")
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "probe.docx"
            subprocess.run([PANDOC, "-f", "markdown-smart", "-t", "docx", "--lua-filter", str(FILTER),
                            "-M", "theme=modern", *downloads.box_colours(),
                            "--reference-doc", downloads.REFERENCE_DOCX, "-o", str(out)],
                           input=body, check=True, capture_output=True, encoding="utf-8")
            with zipfile.ZipFile(out) as z:
                doc = z.read("word/document.xml").decode("utf-8")
        tables = re.findall(r"<w:tbl>.*?</w:tbl>", doc, re.S)
        self.assertEqual(len(tables), 1)
        inside = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tables[0]))
        for words in ("Make a plot.", "Slope?", "Units?", "An action between parts.", "Agree?"):
            self.assertIn(words, inside)
        self.assertNotIn("After.", inside)

    def test_word_checkpoint_is_its_own_box(self):
        # D-0110, D-0115: "Checkpoint 1" in a one-cell table with the light
        # page's Candela fill and Luminance rule, then "Question 1" in the
        # question's own colours.
        body = "::: {.checkpoint #c}\nExchange contacts.\n:::\n\n::: {.question #a}\n**Why?**\n:::\n"
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "probe.docx"
            subprocess.run([PANDOC, "-f", "markdown-smart", "-t", "docx", "--lua-filter", str(FILTER),
                            "-M", "theme=modern", *downloads.box_colours(),
                            "--reference-doc", downloads.REFERENCE_DOCX, "-o", str(out)],
                           input=body, check=True, capture_output=True, encoding="utf-8")
            with zipfile.ZipFile(out) as z:
                doc = z.read("word/document.xml").decode("utf-8")
        checkpoint, question = re.findall(r"<w:tbl>.*?</w:tbl>", doc, re.S)
        fill, rule = (MODERN_ROOT[k].lstrip("#").upper() for k in ("--checkpoint-fill", "--checkpoint-rule"))
        self.assertIn("Checkpoint 1", checkpoint)
        self.assertRegex(checkpoint, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(fill))
        self.assertRegex(checkpoint, r'<w:left\b(?=[^>]*\bw:color="{}")'.format(rule))
        self.assertIn("Question 1", question)
        self.assertRegex(question, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(MODERN_ROOT["--tint"].lstrip("#").upper()))

    def test_word_box_without_its_colours_fails(self):
        # The filter never guesses a colour: a Word render without them stops.
        r = subprocess.run([PANDOC, "-f", "markdown-smart", "-t", "docx", "--lua-filter", str(FILTER),
                            "-o", os.devnull],
                           input="::: {.question #a}\nText.\n:::\n", capture_output=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("needs its colours", r.stderr)

    def test_word_spacing_follows_the_modern_page(self):
        # D-0057, amended after the owner's Word check: the body's line
        # spacing at least [1.6] times the body size, and the gaps after a
        # paragraph and a list item in the modern page's proportions
        # (themes/modern.css: line-height, p and li margins over the body's
        # font size), in twips of Word's 12 pt body.
        body_pt = 12
        line = round(MODERN_BODY["line-height"] * body_pt * 20)
        para = round(MODERN_P_GAP / MODERN_BODY["font-size"] * body_pt * 20)
        item = round(MODERN_LI_GAP / MODERN_BODY["font-size"] * body_pt * 20)
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                styles = self.part(doc_id, "word/styles.xml")
                self.assertRegex(styles, r'(?s)<w:rPrDefault>.*?<w:sz w:val="{}"'.format(body_pt * 2))
                for style_id, after in (("BodyText", para), ("Compact", item)):
                    spacing = re.search(r"<w:spacing\b[^>]*/>", self.style(doc_id, style_id)).group(0)
                    for attr, want in (("before", 0), ("after", after), ("line", line)):
                        self.assertRegex(spacing, r'\bw:{}="{}"'.format(attr, want), style_id)
                    self.assertIn('w:lineRule="atLeast"', spacing, style_id)

    def test_tables_draw_a_thin_grid(self):
        # D-0130: the theme's cells and Word's Table style draw the same thin
        # full grid in --quiet; the question and checkpoint boxes name their
        # own borders, so the style does not reach them.
        cells = re.search(r"\nth, td \{(.*?)\}", _MODERN, re.S).group(1)
        self.assertIn("border: 1px solid var(--quiet);", cells)
        quiet = MODERN_ROOT["--quiet"].lstrip("#").upper()
        for doc_id, _ in converted():
            table = self.style(doc_id, "Table")
            with self.subTest(doc=doc_id):
                for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
                    rule = re.search(r'<w:{} ([^>]*)/>'.format(edge), table.split("<w:tblBorders>")[1])
                    self.assertIsNotNone(rule, edge)
                    self.assertEqual(dict(re.findall(r'w:(\w+)="([^"]*)"', rule.group(1))),
                                     {"val": "single", "sz": "4", "space": "0", "color": quiet}, edge)

    def test_word_headings_keep_with_next(self):
        # A pin, not a change: Pandoc's default Heading 1 to 4 already keep
        # with the next paragraph; a Pandoc upgrade that dropped it fails here.
        # Heading 4 is a box title where Word's outline has Heading 1 (D-0120).
        for doc_id, _ in converted():
            for level in (1, 2, 3, 4):
                with self.subTest(doc=doc_id, level=level):
                    self.assertIn("<w:keepNext", self.style(doc_id, "Heading{}".format(level)))


# Each lab's HTML download, measured, times 1.10, rounded up to the next
# 10,000; never a guess. A lab without its own cap fails, so a lab is
# measured when it is added: its pictures and figures are embedded in it
# (four-items call 4.3). PH 211 Lab 1: 161,024 bytes (2026-10-01), 168,938
# remeasured in pass 2b (2026-10-08).
HTML_CAPS = {
    "ph211-capstone-handout": 210_000,  # 187,181 bytes, pass 3
    "ph211-data-analysis-handout": 230_000,  # 201,354 bytes, pass 3
    "ph211-describing-an-experiment-handout": 210_000,  # 189,015 bytes, pass 3
    "ph211-designing-an-experiment-handout": 370_000,  # 335,643 bytes, pass 3
    "ph211-hypothesis-testing-handout": 330_000,  # 295,331 bytes, pass 3
    "ph211-team-building-handout": 190_000,
    "ph211-uncertainty-handout": 320_000,  # 284,044 bytes, pass 3
    "ph212-data-analysis-handout": 210_000,  # 188,615 bytes, pass 4
    "ph212-designing-experiments-handout": 380_000,  # 343,116 bytes, pass 3
    "ph212-extending-a-model-handout": 210_000,  # 185,980 bytes, pass 4
    "ph212-hypothesis-testing-handout": 200_000,  # 179,126 bytes, pass 4
    "ph212-sharing-and-comparing-handout": 360_000,  # 324,578 bytes, pass 4
    "ph213-hypothesis-testing-handout": 1_820_000,  # 1,650,026 bytes, its photograph embedded (D-0092)
}


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
        # A picture's address differs: the page's is the published file,
        # the download's the file itself, embedded, where Pandoc also
        # writes role="img" and an aria-label repeating the alt text. Quarto
        # writes a drawn figure's inline SVG again (attribute case, empty
        # elements, xml:space), so figures are compared by their words.
        def src(text):
            text = re.sub(r'<img role="img" aria-label="[^"]*" ', "<img ", text)
            text = re.sub(r'(<img\b[^>]*\salt)(?=[\s>])', r'\1=""', text)
            # Quarto rewrites a table's own attributes (Bootstrap's `table`
            # class for Pandoc's width) and gives rows odd/even classes; the
            # theme draws both alike (D-0130, measured). Quarto also writes
            # void elements as HTML5 does (<br>, <col ...>).
            text = re.sub(r"<table\b[^>]*>", "<table>", text)
            text = re.sub(r"<tr\b[^>]*>", "<tr>", text)
            text = text.replace('<blockquote class="blockquote">', "<blockquote>")
            # Quarto's serializer writes characters, Pandoc's some entities
            # (&#39;, &nbsp;): the same text either way.
            text = html.unescape(text)
            text = re.sub(r"\s*/>", ">", text)
            return re.sub(r'\bsrc="[^"]*"', 'src=""', text)
        for doc_id, _ in converted():
            want, want_figures = split_figures(
                re.search(r"<main>\n(.*?)</main>", page(doc_id, "modern"), re.S).group(1))
            got, got_figures = split_figures(
                re.search(r"<main>\n(.*?)</main>", self.download(doc_id), re.S).group(1))
            with self.subTest(doc=doc_id):
                self.assertEqual(src(got), src("<p>{}</p>\n{}".format(PHYSICS, want)))
                self.assertEqual([test_quarto_site.words(f) for f in got_figures],
                                 [test_quarto_site.words(f) for f in want_figures])

    def test_size_capped(self):
        for doc_id, _ in converted():
            size = self.path(doc_id).stat().st_size
            with self.subTest(doc=doc_id, size=size):
                self.assertIn(doc_id, HTML_CAPS, "measure this lab's HTML download and add its cap")
                self.assertLessEqual(size, HTML_CAPS[doc_id])


class MediaDownloads(unittest.TestCase):
    """A made-up lab with a cropped picture, a drawn figure and an equation
    (tests/figure_fixture.py) through the Word and HTML downloads
    (four-items call 4.3; D-0117, D-0118)."""

    ID = "fixture-lab"
    SOURCE = ('---\nid: "fixture-lab"\ntitle: "Fixture"\nsource_file: "{original}"\n'
              'source_sha256: "{digest}"\nimages:\n  - file: "fixture-lab-media/square.png"\n'
              '    source_part: "word/media/fixture.png"\n    sha256: "{sha}"\n---\n\n'
              "# Fixture\n\nBefore $v_{{0}} = \\frac{{d}}{{t}}$.\n\nWords.\n\n"
              '![{figure}](fixture-lab-media/panel.svg){{.drawn drawings="501"}}\n\n'
              "Caption words.\n\n"
              '![{picture}](fixture-lab-media/square.png){{width="1.0000in" height="0.5000in"'
              ' crop="10000 20000 5000 0"}}\n')

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        xml = fx.paragraph("Words.", fx.figure()) + fx.paragraph("Caption words.", fx.anchored_picture())
        digest, image = fx.original(root, PANDOC, "# Fixture\n\nBefore $v_{0} = \\frac{d}{t}$.\n", xml)
        (root / "fixture-lab-media").mkdir()
        (root / "fixture-lab-media" / "square.png").write_bytes(image)
        source = root / "fixture-lab.md"
        source.write_text(cls.SOURCE.format(
            original=(root / "original.docx").as_posix(), digest=digest,
            sha=hashlib.sha256(image).hexdigest(), figure=fx.FIGURE_ALT, picture=fx.PICTURE_ALT),
            encoding="utf-8", newline="\n")
        cls.source = source
        cls.doc = {"path": str(source), "meta": render.pandoc_meta(str(source)),
                   "lab_dir": str(root / "labs" / cls.ID)}
        cls.published = media.build(cls.doc, downloads.media_dir(cls.doc), downloads.CHROME)
        cls.docx = root / "fixture-lab.docx"
        cls.html = root / "fixture-lab.html"
        downloads.word(cls.doc, str(cls.docx))
        downloads.html(cls.doc, str(cls.html))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_the_fixture_passes_the_word_check(self):
        _, problems = check_unchanged.check(str(self.source), str(ROOT))
        self.assertEqual(problems, [])

    def test_published_media(self):
        # The picture and the figure's SVG; the PNG is for Word only.
        self.assertEqual(self.published, ["square.png", "panel.svg"])
        self.assertEqual(media.published(self.doc), self.published)
        folder = Path(downloads.media_dir(self.doc))
        self.assertTrue((folder / "panel.png").is_file())

    def word_pictures(self):
        with zipfile.ZipFile(self.docx) as z:
            doc = z.read("word/document.xml").decode("utf-8")
        return re.findall(r"<w:drawing>.*?</w:drawing>", doc, re.S)

    def test_word_has_the_figure_as_png_at_its_size(self):
        figure, picture = self.word_pictures()
        self.assertRegex(figure, r'descr="{}'.format(re.escape(fx.FIGURE_ALT)))
        cx = int(re.search(r'<wp:extent cx="(\d+)"', figure).group(1))
        self.assertAlmostEqual(cx, fx.WIDTH, delta=9525)
        with zipfile.ZipFile(self.docx) as z:
            pngs = [n for n in z.namelist() if n.startswith("word/media/")]
            self.assertTrue(any(z.read(n)[:8] == b"\x89PNG\r\n\x1a\n" and len(z.read(n)) > 1000 for n in pngs))

    def test_word_picture_has_words_size_and_crop(self):
        _, picture = self.word_pictures()
        self.assertIn('descr="{}"'.format(fx.PICTURE_ALT), picture)
        self.assertRegex(picture, r'<wp:extent cx="914400" cy="457200"')
        self.assertIn('<a:srcRect l="10000" t="20000" r="5000" b="0"/>', picture)

    def test_word_equations_and_words(self):
        got, _, _ = read_words(str(self.docx))
        want, math, api = read_words(str(self.source), "-f", render.FROM, "--lua-filter", str(FILTER),
                                     "-M", "theme=modern")
        self.assertEqual(got, want)
        self.assertEqual(len(math), 1)
        same_equations(self, math, api, self.docx)

    def test_html_figure_is_inline_svg_text(self):
        text = self.html.read_text(encoding="utf-8")
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg" class="drawn-figure"', text)
        self.assertRegex(text, r'<text class="figure-label"[^>]*>.*?Accelerating')
        self.assertNotIn("<figure", text)
        self.assertNotIn("<figcaption", text)

    def test_html_equation_is_mathml(self):
        text = self.html.read_text(encoding="utf-8")
        self.assertIn("<math", text)
        self.assertIn("<mfrac>", text)

    def test_html_picture_embedded_at_words_size_and_crop(self):
        text = self.html.read_text(encoding="utf-8")
        span = re.search(r'<span class="picture-crop" style="([^"]*)">(<img [^>]*>)</span>', text)
        self.assertIsNotNone(span)
        self.assertIn("width:96.00px", span.group(1))
        img = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', span.group(2)))
        self.assertTrue(img["src"].startswith("data:image/png;base64,"))
        self.assertEqual(img["alt"], fx.PICTURE_ALT)
        # Word shows 85 % of the width from 10 % in, 80 % of the height
        # from 20 % down.
        self.assertEqual(img["style"], "width:117.6471%;height:125.0000%;left:-11.7647%;top:-25.0000%")

    def test_page_picture_prefix(self):
        # The lab page sits one folder below the media (labs/<id>/modern/).
        out = subprocess.run([PANDOC, str(self.source), "-f", render.FROM, "-t", "html",
                              "--lua-filter", str(downloads.MEDIA_FILTER), "-M", "media-prefix=../",
                              "-M", "media-dir=" + downloads.media_dir(self.doc).replace(os.sep, "/")],
                             check=True, capture_output=True, encoding="utf-8").stdout
        self.assertIn('src="../fixture-lab-media/square.png"', out)


def pdf_text(path):
    return subprocess.run([PDFTOTEXT, "-layout", str(path), "-"], check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


class LandscapePages(unittest.TestCase):
    """Pass 4: a `::: landscape` block is a landscape page of its own in
    Word and in print, the draft header and the footer on it (a made-up
    lab and page, D-0119 call 4)."""

    SOURCE = ('---\nid: "landscape-lab"\ntitle: "Landscape"\n---\n\n# Landscape\n\n'
              "Portrait words before.\n\n::: landscape\n| Task | One |\n|---|------------|\n"
              "| Describe the model | " + "words " * 16 + "|\n:::\n\nPortrait words after.\n")

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        source = root / "landscape-lab.md"
        source.write_text(cls.SOURCE, encoding="utf-8", newline="\n")
        doc = {"path": str(source), "meta": render.pandoc_meta(str(source)),
               "lab_dir": str(root / "labs" / "landscape-lab")}
        cls.docx = root / "landscape-lab.docx"
        downloads.word(doc, str(cls.docx))
        with zipfile.ZipFile(cls.docx) as z:
            cls.xml = z.read("word/document.xml").decode("utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_word_turns_the_block_and_only_it(self):
        sections = re.findall(r"<w:sectPr\b.*?</w:sectPr>", self.xml, re.S)
        self.assertEqual(len(sections), 3)
        self.assertNotIn("<!--section:", self.xml)
        before, block, own = sections
        self.assertEqual(before, own)
        self.assertIn('<w:pgSz w:w="15840" w:h="12240" w:orient="landscape" />', block)
        self.assertNotIn("landscape", own)
        for s in sections:
            self.assertIn("<w:headerReference", s)
            self.assertIn("<w:footerReference", s)
        # The table, and only it, lies in the landscape section.
        at = [m.start() for m in re.finditer(r"<w:sectPr\b", self.xml)]
        table = self.xml.index("<w:tbl>")
        self.assertTrue(at[0] < table < at[1])
        self.assertLess(self.xml.index("Portrait words before"), at[0])
        self.assertGreater(self.xml.index("Portrait words after"), at[1])

    def test_print_turns_the_block_and_keeps_the_page_furniture(self):
        css = [(ROOT / "site" / "site.css").as_uri(), (ROOT / "themes" / "modern.css").as_uri()]
        page = ("<!doctype html><html><head><meta charset=\"utf-8\">"
                + "".join('<link rel="stylesheet" href="{}">'.format(c) for c in css)
                + "</head><body><main><p>Portrait words before.</p><div class=\"landscape\"><table>"
                "<tr><td>Task</td><td>Wide words</td></tr></table></div><p>Portrait words after.</p>"
                "</main></body></html>")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "page.html"
            src.write_text(page, encoding="utf-8")
            pdf = Path(tmp) / "page.pdf"
            subprocess.run([downloads.CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            "--print-to-pdf=" + str(pdf), src.as_uri()], check=True, capture_output=True)
            boxes = re.findall(rb"/MediaBox\s*\[([^\]]*)\]", pdf.read_bytes())
            pages = pdf_text(pdf).split("\f")[:-1]
        self.assertEqual([b.split()[2:] for b in boxes], [[b"612", b"792"], [b"792", b"612"], [b"612", b"792"]])
        self.assertIn("Wide words", pages[1])
        for i, pg in enumerate(pages, 1):
            self.assertIn(PHYSICS, flat(pg))
            self.assertIn("Page {} of 3".format(i), flat(pg))
            self.assertIn("DRAFT: license pending", flat(pg))


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


class DecorativePictures(unittest.TestCase):
    """D-0132 call 6: a picture with Word's empty alt text stays decorative
    in the HTML download (made-up markup, D-0119 call 4)."""

    def test_empty_alt_loses_role_and_label(self):
        got = downloads.without_empty_image_role(
            '<p><img role="img" aria-label src="data:x" alt width="31"></p>')
        self.assertEqual(got, '<p><img src="data:x" alt="" width="31"></p>')
        got = downloads.without_empty_image_role('<img role="img" aria-label="" src="a" alt="">')
        self.assertEqual(got, '<img src="a" alt="">')

    def test_named_picture_unchanged(self):
        tag = '<img role="img" aria-label="A cart on a ramp" src="a" alt="A cart on a ramp">'
        self.assertEqual(downloads.without_empty_image_role(tag), tag)


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
    # A question block taller than a printed page cannot stay whole, and
    # Chrome breaks it (break-inside: avoid yields). Each entry is proved
    # taller by test_taller_than_a_page_is_true; a lab's PR adds its own
    # as it adds its HTML cap: (doc id, the question's label number).
    TALLER_THAN_A_PAGE = {
        # The "What is Uncertainty?" box sits inside it, between stem and parts (S14).
        ("ph212-data-analysis-handout", "4"),
    }
    HEADER = words("DRAFT: license pending")
    RULES_OFF = ("<style>@media print { .question, .box { break-inside: auto !important; }"
                 " h1, h2, h3, h4 { break-after: auto !important; } }</style>")

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
        headings = [flat(html.unescape(re.sub(r"<[^>]+>", "", h))) for h in re.findall(r"<h[1-4]\b[^>]*>(.*?)</h[1-4]>", main, re.S)]
        pages = raw.split("\f")[:-1]
        found = self.page_endings(pages, headings, main)
        text = "\f".join(" ".join(words(p)) for p in pages)
        start = -1
        tall = {n for d, n in self.TALLER_THAN_A_PAGE if d == doc_id}
        for n, rest in re.findall(r'<div class="question-label">\s*<p>Question (\d+)</p>\s*</div>(.*?)</div>', main, re.S):
            end = " ".join(self.last_words(rest))
            # In order: after a restart (S9), "Question 1" comes again.
            start = text.find("QUESTION " + n, start + 1)
            stop = text.find(end, start)
            if start < 0 or stop < 0:
                found.append("question {} not found in the print".format(n))
            elif "\f" in text[start:stop] and n not in tall:
                found.append("question {} broken over a page".format(n))
        return found

    @classmethod
    def page_endings(cls, pages, headings, main):
        """Pages whose last lines are a heading. Where a paragraph or list
        item has the same words as a heading (PH 212 Lab 6's "Week 1"
        label above its list, and its Week 1 heading), the print's whole
        lines with those words are matched in order to the page's blocks
        with them, and only a heading's counts."""
        blocks = [(tag.startswith("h"), flat(html.unescape(re.sub(r"<[^>]+>", "", body))))
                  for tag, body in re.findall(r"<(h[1-4]|p|li)\b[^>]*>(.*?)</\1>", main, re.S)]
        found, seen = [], {}
        for i, pg in enumerate(pages, 1):
            lines = [flat(l) for l in pg.split("\n") if l.strip()]
            body = [l for l in lines if not l.startswith(PHYSICS) and l != "DRAFT: license pending"]
            for l in body:
                seen[l] = seen.get(l, 0) + 1
            ending = cls.ends_with_heading("\n".join(body), headings)
            if ending and body and body[-1] == ending:
                kinds = [is_h for is_h, t in blocks if t == ending]
                n = seen[ending]
                if n <= len(kinds) and not kinds[n - 1]:
                    ending = None
            if ending:
                found.append("page {} ends with a heading: {}".format(i, ending))
        return found

    def starts_a_page_and_breaks(self, raw, n):
        """Question n prints first on its page, under the running header,
        and still crosses a page break: it is taller than a page."""
        pages = raw.split("\f")[:-1]
        for i, pg in enumerate(pages):
            got = words(pg)
            if got[:len(self.HEADER) + 2] == self.HEADER + ["QUESTION", n]:
                rest = " ".join(words(" ".join(pages[i + 1:i + 2])))
                return bool(rest) and not rest.startswith(" ".join(self.HEADER) + " QUESTION")
        return False

    @staticmethod
    def ends_with_heading(page_text, headings):
        """The heading a printed page ends with, or None. A heading may wrap,
        so the page's last one to three lines, joined, must be a whole
        heading; lines that merely end with one are not (a table cell's
        "Experiment" against "Week 2 – Perform the Experiment", PH 211
        Lab 7; a contents item "4. Linearization", PH 212 Lab 4)."""
        body = [flat(l) for l in page_text.split("\n") if l.strip()]
        tails = [" ".join(body[-k:]) for k in (1, 2, 3) if len(body) >= k]
        return next((h for h in headings if h in tails), None)

    @staticmethod
    def last_words(block):
        """Up to three words that end a question block as pdftotext prints
        them: after its last equation if words follow it, else before it,
        since MathML's text and its TeX annotation print otherwise or not at
        all; a drawn figure's labels are left out (their order in the PDF is
        the figure's)."""
        block, _ = split_figures(block)
        parts = re.split(r"<math\b.*?</math>", block, flags=re.S)
        tail = words(re.sub(r"<[^>]+>", " ", parts[-1]))
        if not tail and len(parts) > 1:
            tail = words(re.sub(r"<[^>]+>", " ", parts[-2]))
        return tail[-3:]

    def test_a_page_ending_in_a_heading_is_found_whole(self):
        heads = ["Week 2 – Perform the Experiment"]
        page = "Title\nSome text above\nWeek 2 – Perform the\nExperiment\n"
        cell = "Title\nLab 06 – Describing an\nExperiment\n"
        self.assertEqual(self.ends_with_heading(page, heads), "Week 2 – Perform the Experiment")
        self.assertIsNone(self.ends_with_heading(cell, heads))
        contents = "Appendix\n1. Required Plot Elements\n4. Linearization\n"
        self.assertIsNone(self.ends_with_heading(contents, ["Linearization"]))
        self.assertEqual(self.ends_with_heading("Text\nLinearization\n", ["Linearization"]),
                         "Linearization")

    def test_a_paragraph_with_a_headings_words_is_not_a_heading(self):
        main = ("<p>The project:</p><p>Week 1</p><ol><li>Choose</li></ol>"
                "<h2>Week 1</h2><p>Text.</p>")
        label_ends = ["DRAFT: license pending\nThe project:\nWeek 1\n", "1. Choose\nWeek 1\nText.\n"]
        heading_ends = ["DRAFT: license pending\nThe project:\nWeek 1\n1. Choose\nWeek 1\n", "Text.\n"]
        self.assertEqual(self.page_endings(label_ends, ["Week 1"], main), [])
        self.assertEqual(self.page_endings(heading_ends, ["Week 1"], main),
                         ["page 1 ends with a heading: Week 1"])

    def test_a_question_starting_a_page_and_breaking_is_taller(self):
        top = "DRAFT: license pending\nQUESTION 4\nRead the box.\n\f"
        mid = "DRAFT: license pending\nSome words.\nQUESTION 4\nRead the box.\n\f"
        rest = "DRAFT: license pending\na. List the sources.\n\f"
        after = "DRAFT: license pending\nQUESTION 5\nNext.\n\f"
        self.assertTrue(self.starts_a_page_and_breaks(top + rest, "4"))
        self.assertFalse(self.starts_a_page_and_breaks(mid + rest, "4"))
        self.assertFalse(self.starts_a_page_and_breaks(top + after, "4"))

    def test_taller_than_a_page_is_true(self):
        ids = {d for d, _ in converted()}
        for doc_id, n in sorted(self.TALLER_THAN_A_PAGE):
            with self.subTest(doc=doc_id, question=n):
                self.assertIn(doc_id, ids)
                self.assertTrue(self.starts_a_page_and_breaks(self.printed(doc_id, 0, False), n),
                                "fits on a page now: remove it from TALLER_THAN_A_PAGE")

    def test_last_words_skip_math_and_figures(self):
        last = self.last_words
        self.assertEqual(last("<p>in the <math><mi>A</mi><annotation>A</annotation></math> format.</p>"),
                         ["format"])
        self.assertEqual(last("<p>one two three four <math><mi>x</mi></math></p>"), ["two", "three", "four"])
        self.assertEqual(last('<p>the words end here</p><svg class="drawn-figure"><text>Label</text></svg>'),
                         ["words", "end", "here"])

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
