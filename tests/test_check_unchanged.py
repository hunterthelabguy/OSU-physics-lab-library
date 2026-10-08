"""The word check's equations, pictures, SYMBOL field and text boxes.

Four-items call 4.2's and 4.3's cases, as amended by D-0113. Each original is
a docx Pandoc makes at test time from known Markdown, with XML added where
Pandoc cannot write the structure (a text box, a SYMBOL field).
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
import check_unchanged  # noqa: E402

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
        subprocess.run([PANDOC, str(src), "-f", "markdown-smart", "-o", str(out),
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

    def check(self, original, converted, extra_xml=""):
        digest = self.original(original, extra_xml)
        md = self.root / "lab.md"
        md.write_text('---\nsource_file: "original.docx"\nsource_sha256: "' + digest
                      + '"\n---\n\n' + converted, encoding="utf-8", newline="\n")
        return check_unchanged.check(str(md), str(self.root))

    def assertFails(self, original, converted, words, extra_xml=""):
        _, problems = self.check(original, converted, extra_xml)
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
        _, problems = self.check("Before.", "Before.\n\nBoxed words $q$ after the box.",
                                 TEXT_BOX)
        self.assertEqual(problems, [])

    def test_picture_alt_text_compared(self):
        doc = "![A dot on white](dot.png)\n\nAfter.\n"
        n, problems = self.check(doc, doc)
        self.assertEqual(problems, [])
        self.assertEqual(n["pictures"], 1)
        self.assertFails(doc, doc.replace("A dot on white", "A dot"), "picture 1")
        self.assertFails(doc, "After.\n", "pictures: original 1, converted 0")

    def test_symbol_field_reads_as_words_display(self):
        _, problems = self.check("Units.", "Units.\n\nOhm (\u03a9) = 1 V/A\n", symbol_field("87"))
        self.assertEqual(problems, [])
        self.assertFails("Units.", "Units.\n\nOhm (W) = 1 V/A\n", "replace",
                         symbol_field("87"))

    def test_unknown_symbol_character_stops(self):
        with self.assertRaises(SystemExit):
            self.check("Units.", "Units.\n\nOhm (?) = 1 V/A\n", symbol_field("88"))


if __name__ == "__main__":
    unittest.main()
