"""Make tools/reference.docx, the Word downloads' page and styles (D-0052,
D-0053, D-0057).

One-time tool, run by hand; builds read the committed file. Rerun it when
the header, the footer, the styles below, the banner wording or the Pandoc
that builds the downloads changes. Needs PANDOC set to Quarto's bundled
Pandoc (D-0044).

Usage: python tools/make_reference_docx.py

Starts from Pandoc's own default reference document and adds:
- a page header on every page, the draft notice (render.BANNER_MAIN, ledger
  37) in the Header style, 9 pt bold and centered like the PDF's banner box;
  it goes when the license settles;
- a page footer, the department line then "Page N of M" from Word's PAGE and
  NUMPAGES fields, in the Footer style at 8 pt like the PDF's. The size is
  on the style, never on the runs: Word rebuilds a field's result and drops
  the formatting of the cached one;
- the PDF's page: Letter with site/site.css's 0.75 in margins;
- the Question Label style that tools/filters/questions.lua names for a
  question's label in Word: the modern page's label, in capitals and its
  --quiet colour, kept with what follows. The box around the question is a
  one-cell table the filter draws (D-0082), not a style;
- the modern page's spacing in Pandoc's Body Text and Compact styles: lines
  at least 1.6 times the body size, and the paragraph and list item gaps in
  the page's proportions (the owner found the first build's spacing tighter
  than the page, 2026-10-01).
Every other part is copied byte for byte, so the Word file otherwise keeps
Pandoc's default styles.
"""

import io
import os
import re
import subprocess
import zipfile
from xml.sax.saxutils import escape

import downloads
import render

OUT = os.path.join(render.ROOT, "tools", "reference.docx")
HEADER_ID = "rIdLabHeader"
FOOTER_ID = "rIdLabFooter"
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
TWIPS_PER_INCH = 1440
LETTER = (8.5, 11)    # inches, site/site.css @page size: letter
MARGIN = 0.75         # inches, site/site.css @page margin

# The modern page's values (themes/modern.css), carried into Word's 12 pt
# body: a length in rem is taken over the body's 1.0625rem, so it keeps its
# proportion to the text.
BODY_REM = 1.0625
BODY_PT = 12
LINE_HEIGHT = 1.6


def pt(rem):
    return rem / BODY_REM * BODY_PT


def twips(points):
    return round(points * 20)


def spacing(after_rem):
    """Lines at least 1.6 times the body (an exact proportion, whatever the
    font's own metrics), nothing before, the page's gap after."""
    return '<w:spacing w:before="0" w:after="{}" w:line="{}" w:lineRule="atLeast" />'.format(
        twips(pt(after_rem)), twips(LINE_HEIGHT * BODY_PT))


BODY_SPACING = spacing(1)      # p { margin: 0 0 1rem; }
ITEM_SPACING = spacing(.5)     # li { margin: 0 0 .5rem; }


STYLES = (
    '<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header" />'
    '<w:basedOn w:val="Normal" /><w:uiPriority w:val="99" /><w:unhideWhenUsed />'
    '<w:pPr><w:spacing w:after="0" /><w:jc w:val="center" /></w:pPr>'
    '<w:rPr><w:b /><w:bCs /><w:sz w:val="18" /><w:szCs w:val="18" /></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer" />'
    '<w:basedOn w:val="Normal" /><w:uiPriority w:val="99" /><w:unhideWhenUsed />'
    '<w:pPr><w:spacing w:after="0" /></w:pPr>'
    '<w:rPr><w:sz w:val="16" /><w:szCs w:val="16" /></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="QuestionLabel">'
    '<w:name w:val="Question Label" /><w:basedOn w:val="BodyText" /><w:next w:val="BodyText" /><w:qFormat />'
    '<w:pPr><w:keepNext /><w:keepLines />'
    + '<w:spacing w:before="0" w:after="{}" w:line="240" w:lineRule="auto" />'.format(twips(pt(.35)))
    + '</w:pPr>'
    # .question-label p: .8rem (9 pt), letter-spacing .08em, --quiet.
    '<w:rPr><w:caps /><w:color w:val="0D5257" /><w:spacing w:val="14" /><w:sz w:val="18" /><w:szCs w:val="18" /></w:rPr>'
    '</w:style>')


def paragraph(style, runs):
    return '<w:p><w:pPr><w:pStyle w:val="{}" /></w:pPr>{}</w:p>'.format(style, runs)


def run(text):
    return '<w:r><w:t xml:space="preserve">{}</w:t></w:r>'.format(escape(text))


def field(instr):
    return '<w:fldSimple w:instr=" {} ">{}</w:fldSimple>'.format(instr, run("1"))


XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
HEADER = XML + '<w:hdr {}>'.format(W) + paragraph("Header", run(render.BANNER_MAIN)) + '</w:hdr>\n'
FOOTER = XML + '<w:ftr {}>'.format(W) + paragraph(
    "Footer", run(downloads.PHYSICS + " · Page ") + field("PAGE") + run(" of ")
    + field("NUMPAGES")) + '</w:ftr>\n'
PAGE = ('<w:pgSz w:w="{}" w:h="{}" />'.format(*(round(i * TWIPS_PER_INCH) for i in LETTER))
        + '<w:pgMar w:top="{0}" w:right="{0}" w:bottom="{0}" w:left="{0}" w:header="720" '
          'w:footer="720" w:gutter="0" />'.format(round(MARGIN * TWIPS_PER_INCH)))
PARTS = {"word/header1.xml": ("header", HEADER_ID, HEADER), "word/footer1.xml": ("footer", FOOTER_ID, FOOTER)}


def once(pattern, text, repl):
    new, n = re.subn(pattern, lambda m: repl, text, count=1)
    if n != 1:
        raise SystemExit("reference.docx: expected " + pattern)
    return new


def respace(text, style_id, new):
    """Replace the one spacing element of one of Pandoc's default styles."""
    pattern = r'<w:style\b[^>]*\bw:styleId="{}".*?</w:style>'.format(style_id)
    block = re.findall(pattern, text, re.S)
    if len(block) != 1:
        raise SystemExit("reference.docx: expected one {} style".format(style_id))
    changed, n = re.subn(r"<w:spacing\b[^>]*/>", lambda m: new, block[0])
    if n != 1:
        raise SystemExit("reference.docx: expected one spacing in the {} style".format(style_id))
    return text.replace(block[0], changed)


def edit(name, data):
    text = data.decode("utf-8")
    if name == "word/document.xml":
        if 'xmlns:r="' not in text:
            raise SystemExit("document.xml declares no r: namespace")
        # Section children keep the schema's order: references, the
        # footnote settings Pandoc's default carries, then the page.
        refs = ''.join('<w:{}Reference w:type="default" r:id="{}" />'.format(kind, rid)
                       for kind, rid, _ in PARTS.values())
        text = once(r"<w:sectPr>", text, "<w:sectPr>" + refs)
        text = once(r"</w:footnotePr>", text, "</w:footnotePr>" + PAGE)
    elif name == "word/styles.xml":
        for style_id in ("Header", "Footer", "QuestionLabel"):
            if 'w:styleId="{}"'.format(style_id) in text:
                raise SystemExit("Pandoc's default already has the {} style; review this tool".format(style_id))
        for style_id, new in (("BodyText", BODY_SPACING), ("Compact", ITEM_SPACING)):
            text = respace(text, style_id, new)
        text = once(r"</w:styles>", text, STYLES + "</w:styles>")
    elif name == "word/_rels/document.xml.rels":
        rels = ''.join('<Relationship Type="http://schemas.openxmlformats.org/officeDocument/'
                       '2006/relationships/{}" Id="{}" Target="{}" />'.format(kind, rid, part[len("word/"):])
                       for part, (kind, rid, _) in PARTS.items())
        text = once(r"</Relationships>", text, rels + "</Relationships>")
    elif name == "[Content_Types].xml":
        types = ''.join('<Override PartName="/{}" ContentType="application/vnd.openxmlformats-'
                        'officedocument.wordprocessingml.{}+xml" />'.format(part, kind)
                        for part, (kind, _, _) in PARTS.items())
        text = once(r"</Types>", text, types + "</Types>")
    return text.encode("utf-8")


def main():
    default = subprocess.run([render.PANDOC, "--print-default-data-file", "reference.docx"],
                             capture_output=True, check=True).stdout
    src = zipfile.ZipFile(io.BytesIO(default))
    if any(re.fullmatch(r"word/(header|footer)\d*\.xml", n) for n in src.namelist()):
        raise SystemExit("Pandoc's default already has a header or footer; review this tool")
    with zipfile.ZipFile(OUT, "w") as out:
        for info in src.infolist():
            out.writestr(info, edit(info.filename, src.read(info)))
        for part, (_, _, xml) in PARTS.items():
            entry = zipfile.ZipInfo(part, src.getinfo("word/document.xml").date_time)
            entry.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(entry, xml.encode("utf-8"))
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
