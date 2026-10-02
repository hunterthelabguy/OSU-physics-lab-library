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
- the Question Label and Question styles that tools/filters/questions.lua
  names for Word: the PDF's print look, a black rule down the left that Word
  draws as one across both, the label in capitals, and both kept whole and
  with what follows.
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

# One left rule and one indent shared by both question styles, so Word joins
# the label and the question into one ruled block.
RULE = ('<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="000000" /></w:pBdr>')
INDENT = '<w:ind w:left="240" />'

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
    '<w:name w:val="Question Label" /><w:basedOn w:val="BodyText" /><w:next w:val="Question" /><w:qFormat />'
    '<w:pPr><w:keepNext /><w:keepLines />' + RULE + '<w:spacing w:before="360" w:after="60" />' + INDENT + '</w:pPr>'
    '<w:rPr><w:caps /><w:color w:val="0D5257" /><w:spacing w:val="14" /><w:sz w:val="18" /><w:szCs w:val="18" /></w:rPr>'
    '</w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Question">'
    '<w:name w:val="Question" /><w:basedOn w:val="BodyText" /><w:next w:val="BodyText" /><w:qFormat />'
    '<w:pPr><w:keepNext /><w:keepLines />' + RULE + '<w:spacing w:before="0" w:after="360" />' + INDENT + '</w:pPr>'
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
        for style_id in ("Header", "Footer", "QuestionLabel", "Question"):
            if 'w:styleId="{}"'.format(style_id) in text:
                raise SystemExit("Pandoc's default already has the {} style; review this tool".format(style_id))
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
