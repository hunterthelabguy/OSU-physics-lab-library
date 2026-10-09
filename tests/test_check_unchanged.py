"""The word check's equations, pictures, figures, SYMBOL field and text boxes.

Four-items call 4.2's and 4.3's cases, as amended by D-0113, D-0117 and
D-0118. Each original is a docx Pandoc makes at test time from known
Markdown, with XML added where Pandoc cannot write the structure (a text
box, a SYMBOL field, a drawn figure, an anchored picture; the last two from
tests/figure_fixture.py).
"""

import hashlib
import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import check_unchanged  # noqa: E402
import figure_fixture as fx  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
PH211 = ROOT / "curriculum" / "ph211" / "ph211-team-building-handout.md"

MATH = (r"Inline $v_{0} = \frac{d}{t}$ and $\vec{F}$, then"
        "\n\n$$x(t) = x_{0} + v_{0}t + \\frac{1}{2}at^{2}$$\n\n"
        r"and $\left| E \right|$ last.")

W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
M_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
TEXT_BOX = (
    '<w:p ' + W_NS + '><w:r><w:drawing>'
    '<wp:anchor xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
    '<wp:docPr id="90" name="Text Box 90"/>'
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
    '<wps:wsp xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
    '<wps:txbx><w:txbxContent><w:p><w:r><w:t xml:space="preserve">Boxed words </w:t></w:r>'
    '<m:oMath ' + M_NS + '><m:r><m:t>q</m:t></m:r></m:oMath></w:p></w:txbxContent></wps:txbx>'
    '</wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing></w:r>'
    '<w:r><w:t xml:space="preserve"> after the box.</w:t></w:r></w:p>')


def symbol_field(code):
    run = '<w:r><w:{}/></w:r>'
    return ('<w:p ' + W_NS + '><w:r><w:t xml:space="preserve">Ohm (</w:t></w:r>'
            + run.format('fldChar w:fldCharType="begin"')
            + '<w:r><w:instrText xml:space="preserve">symbol ' + code
            + ' \\f "Symbol" \\s 12</w:instrText></w:r>'
            + run.format('fldChar w:fldCharType="separate"')
            + '<w:r><w:t>W</w:t></w:r>'
            + run.format('fldChar w:fldCharType="end"')
            + '<w:r><w:t>) = 1 V/A</w:t></w:r></w:p>')


def symbol_run(text):
    return ('<w:p ' + W_NS + '><w:r><w:t xml:space="preserve">Select “A” </w:t></w:r>'
            '<w:r><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr><w:t>' + text
            + '</w:t></w:r><w:r><w:t xml:space="preserve"> “B”.</w:t></w:r></w:p>')


def png():
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00")) + chunk(b"IEND", b""))


class WordCheck(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "dot.png").write_bytes(png())

    def tearDown(self):
        self.tmp.cleanup()

    def original(self, body, extra_xml=""):
        src = self.root / "original-src.md"
        src.write_text(body, encoding="utf-8", newline="\n")
        out = self.root / "original.docx"
        subprocess.run([PANDOC, str(src), "-f", check_unchanged.FROM, "-o", str(out),
                        "--resource-path", str(self.root)], check=True)
        if extra_xml:
            with zipfile.ZipFile(out) as z:
                parts = {n: z.read(n) for n in z.namelist()}
            doc = parts["word/document.xml"].decode("utf-8")
            at = doc.rindex("<w:sectPr")
            parts["word/document.xml"] = (doc[:at] + extra_xml + doc[at:]).encode("utf-8")
            with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
                for n, data in parts.items():
                    z.writestr(n, data)
        return hashlib.sha256(out.read_bytes()).hexdigest()

    def check(self, original, converted, extra_xml="", front=""):
        digest = self.original(original, extra_xml)
        md = self.root / "lab.md"
        md.write_text('---\nsource_file: "original.docx"\nsource_sha256: "' + digest
                      + '"\n' + front + '---\n\n' + converted, encoding="utf-8", newline="\n")
        return check_unchanged.check(str(md), str(self.root))

    def assertFails(self, original, converted, words, extra_xml="", front=""):
        _, problems = self.check(original, converted, extra_xml, front)
        self.assertTrue(any(w in p for p in problems for w in [words]), problems)

    def test_ph211_unchanged(self):
        # D-0082's test: 989 words identical, bold on 943, and no equations.
        n, problems = check_unchanged.check(str(PH211), str(ROOT))
        self.assertEqual(problems, [])
        self.assertEqual((n["words"], n["bold"], n["equations"], n["pictures"]),
                         (989, 943, 0, 0))

    def test_equations_identical_pass(self):
        n, problems = self.check(MATH, MATH)
        self.assertEqual(problems, [])
        self.assertEqual(n["equations"], 4)

    def test_equation_dropped_fails(self):
        self.assertFails(MATH, MATH.replace(r"and $\vec{F}$, then", "and , then"),
                         "equations: original 4, converted 3")

    def test_equations_swapped_fail(self):
        swapped = MATH.replace(r"$v_{0} = \frac{d}{t}$ and $\vec{F}$",
                               r"$\vec{F}$ and $v_{0} = \frac{d}{t}$")
        self.assertFails(MATH, swapped, "equation 1")

    def test_subscript_changed_fails(self):
        self.assertFails(MATH, MATH.replace("v_{0} = ", "v_{1} = "), "equation 1")

    def test_display_made_inline_fails(self):
        inline = MATH.replace("$$x(t)", "$x(t)").replace("at^{2}$$", "at^{2}$")
        self.assertFails(MATH, inline, "original display, converted inline")

    def test_delimiter_written_as_bars_fails(self):
        # D-0113: Word's delimiter must stay a delimiter.
        self.assertFails(MATH, MATH.replace(r"\left| E \right|", "|E|"), "structure differs")

    def test_empty_root_for_a_typed_root_fails(self):
        # D-0113: Pandoc reads a typed "√" as an empty \sqrt{}.
        self.assertFails("$r = \u221aR^{2}$", r"$r = \sqrt{}R^{2}$", "equation 1")
        self.assertEqual(self.check("$r = \u221aR^{2}$", "$r = \u221aR^{2}$")[1], [])

    def test_hyphen_and_minus_are_one_sign(self):
        # D-0113's normalization: Word's typed "-" against the writer's U+2212.
        _, problems = self.check("$a - b$", "$a - b$")
        self.assertEqual(problems, [])

    def test_equation_bold_is_exempt(self):
        _, problems = self.check("Text $x$.", r"Text $\mathbf{x}$.")
        self.assertEqual(problems, [])

    def test_equation_in_a_text_box_missing_from_markdown_fails(self):
        self.assertFails("Before.", "Before.\n\nBoxed words after the box.",
                         "equations: original 1, converted 0", TEXT_BOX)

    def test_text_box_words_are_read_once(self):
        # Anchored at its paragraph's start, read after the paragraph's
        # words, where Word shows it (D-0118).
        _, problems = self.check("Before.", "Before.\n\nafter the box.\n\nBoxed words $q$\n",
                                 TEXT_BOX)
        self.assertEqual(problems, [])
        self.assertFails("Before.", "Before.\n\nBoxed words $q$ after the box.", "insert", TEXT_BOX)

    def test_symbol_field_reads_as_words_display(self):
        _, problems = self.check("Units.", "Units.\n\nOhm (\u03a9) = 1 V/A\n", symbol_field("87"))
        self.assertEqual(problems, [])
        self.assertFails("Units.", "Units.\n\nOhm (W) = 1 V/A\n", "replace",
                         symbol_field("87"))

    def test_unknown_symbol_character_stops(self):
        with self.assertRaises(SystemExit):
            self.check("Units.", "Units.\n\nOhm (?) = 1 V/A\n", symbol_field("88"))

    def test_symbol_font_run_reads_as_words_display(self):
        # D-0123: PH 211 Lab 3 types "®" in the Symbol font; Word draws →.
        for stored in ("\u00ae", "\uf0ae"):
            with self.subTest(stored=hex(ord(stored))):
                _, problems = self.check("Steps.", "Steps.\n\nSelect “A” → “B”.\n", symbol_run(stored))
                self.assertEqual(problems, [])
                self.assertFails("Steps.", "Steps.\n\nSelect “A” ® “B”.\n", "replace", symbol_run(stored))

    def test_unknown_symbol_font_character_stops(self):
        with self.assertRaises(SystemExit):
            self.check("Steps.", "Steps.\n\nSelect “A” ? “B”.\n", symbol_run("\u00a5"))


LONG = "words " * 16


def table(dashes, row=LONG):
    """A made-up pipe table whose dash counts set its column shares."""
    return ("| Task | One | Two |\n|" + "|".join("-" * d for d in dashes) + "|\n"
            "| Describe the model | " + row + "| Short |\n")


class TableWidths(unittest.TestCase):
    """Pass 4: a table's column shares are Word's (PH 212 Lab 6's rubric)."""

    setUp, tearDown = WordCheck.setUp, WordCheck.tearDown
    original, check, assertFails = WordCheck.original, WordCheck.check, WordCheck.assertFails

    def test_shares_as_word_pass(self):
        _, problems = self.check(table([10, 45, 45]), table([10, 45, 45]))
        self.assertEqual(problems, [])

    def test_shares_within_tolerance_pass(self):
        _, problems = self.check(table([10, 45, 45]), table([12, 44, 44]))
        self.assertEqual(problems, [])

    def test_narrow_first_column_fails(self):
        self.assertFails(table([10, 45, 45]), table([4, 48, 48]), "table 1: column shares 4/48/48")

    def test_default_widths_fail(self):
        # No line, the dashes included, past 72 characters: Pandoc ignores the dashes.
        self.assertFails(table([10, 45, 45], row="Short "), table([3, 3, 3], row="Short "),
                         "table 1: default column widths")

    def test_a_table_left_out_fails(self):
        self.assertFails(table([10, 45, 45]), "Describe the model " + LONG + "Short",
                         "tables of more than one column: original 1, converted 0")

    def test_one_cell_boxes_are_not_counted(self):
        self.assertEqual(check_unchanged.markdown_table_shares(
            [{"t": "Table", "c": [None, None, [[{"t": "AlignDefault"}, {"t": "ColWidthDefault"}]]]}]), [])


class FiguresAndFiles(unittest.TestCase):
    """D-0117 and D-0118 on a made-up original (tests/figure_fixture.py):
    a drawn figure read from its SVG, a picture's file, size and crop, an
    anchored drawing read after its paragraph's words, a lone text box."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, xml, converted, front=""):
        digest, _ = fx.original(self.root, PANDOC, "Before.\n", xml)
        md = self.root / "lab.md"
        md.write_text('---\nsource_file: "original.docx"\nsource_sha256: "' + digest
                      + '"\n' + front + '---\n\n' + converted, encoding="utf-8", newline="\n")
        return check_unchanged.check(str(md), str(self.root))

    def assertFails(self, xml, converted, words, front=""):
        _, problems = self.check(xml, converted, front)
        self.assertTrue(any(words in p for p in problems), problems)

    FIGURE = '![{}](lab-media/panel.svg){{.drawn drawings="501"}}\n'.format(fx.FIGURE_ALT)

    def test_figure_read_from_its_svg(self):
        n, problems = self.check(fx.paragraph("Words.", fx.figure()), "Before.\n\nWords.\n\n" + self.FIGURE)
        self.assertEqual(problems, [])
        self.assertEqual((n["figures"], n["equations"], n["pictures"]), (1, 1, 1))

    def test_figure_left_out_fails(self):
        self.assertFails(fx.paragraph("Words.", fx.figure()), "Before.\n\nWords.\n",
                         "drawing 501 ('A grey panel with two labels') is in no figure")

    def test_figure_before_its_paragraph_fails(self):
        # Anchored at the paragraph's start, shown below its words (D-0118).
        _, problems = self.check(fx.paragraph("Words.", fx.figure()), "Before.\n\n" + self.FIGURE + "\nWords.\n")
        self.assertTrue(problems)

    def test_figure_alt_text_is_words(self):
        self.assertFails(fx.paragraph("Words.", fx.figure()),
                         "Before.\n\nWords.\n\n" + self.FIGURE.replace("two labels", "labels"),
                         "figure 1: alt text")

    def test_figure_label_changed_in_the_original_fails(self):
        # The SVG is made from the original, so a word that differs is the
        # Markdown's: here the original's label says something else.
        self.assertFails(fx.paragraph("Words.", fx.figure(label="Accelerating voltage knob")),
                         "Before.\n\nWords.\n\n" + self.FIGURE.replace("panel", "panel") + "\nAccelerating voltage control\n",
                         "knob")

    def test_lone_text_box_is_words(self):
        box = fx.anchor("801", 200 * fx.PT, 30 * fx.PT, "", fx.SHAPE_URI,
                        fx.text_box("801", 0, 0, 200 * fx.PT, 30 * fx.PT, fx.run("Boxed sentence.")))
        _, problems = self.check(fx.paragraph("Words.", box), "Before.\n\nWords.\n\n::: box\nBoxed sentence.\n:::\n")
        self.assertEqual(problems, [])

    PICTURE = '![{}](lab-media/square.png){{width="1.0000in" height="0.5000in" crop="10000 20000 5000 0"}}\n'.format(
        fx.PICTURE_ALT)

    def front(self, data=None, part=fx.PART):
        (self.root / "lab-media").mkdir(exist_ok=True)
        (self.root / "lab-media" / "square.png").write_bytes(data or fx.png())
        return ('images:\n  - file: "lab-media/square.png"\n    source_part: "{}"\n    sha256: "{}"\n'
                .format(part, hashlib.sha256(data or fx.png()).hexdigest()))

    def picture(self, converted, front=None):
        return self.check(fx.paragraph("Caption words.", fx.anchored_picture()),
                          "Before.\n\nCaption words.\n\n" + converted, self.front() if front is None else front)

    def test_picture_file_size_and_crop_pass(self):
        n, problems = self.picture(self.PICTURE)
        self.assertEqual(problems, [])
        self.assertEqual(n["pictures"], 1)

    def test_picture_not_in_front_matter_fails(self):
        _, problems = self.picture(self.PICTURE, front="")
        self.assertTrue(any("not listed in front matter images" in p for p in problems), problems)

    def test_picture_alt_text_is_words(self):
        _, problems = self.picture(self.PICTURE.replace("A grey square", "A square"))
        self.assertTrue(any("picture 1: alt text 'A square', Word's is 'A grey square'" in p
                            for p in problems), problems)

    def test_picture_left_out_fails(self):
        _, problems = self.picture("", front="")
        self.assertTrue(any("pictures: original 1, converted 0" in p for p in problems), problems)

    def test_picture_bytes_differ_fails(self):
        _, problems = self.picture(self.PICTURE, front=self.front(data=fx.png(5, 3)))
        self.assertTrue(any("is not word/media/fixture.png byte for byte" in p for p in problems), problems)

    def test_picture_size_differs_fails(self):
        _, problems = self.picture(self.PICTURE.replace("1.0000in", "1.2000in"))
        self.assertTrue(any("width 1.2000in, Word's is 1.0000in" in p for p in problems), problems)

    def test_picture_crop_left_out_fails(self):
        _, problems = self.picture(self.PICTURE.replace(' crop="10000 20000 5000 0"', ""))
        self.assertTrue(any("crop None, Word's is '10000 20000 5000 0'" in p for p in problems), problems)

    def test_picture_before_its_paragraph_fails(self):
        _, problems = self.check(fx.paragraph("Caption words.", fx.anchored_picture()),
                                 "Before.\n\n" + self.PICTURE + "\nCaption words.\n", self.front())
        self.assertTrue(any("[picture]" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
