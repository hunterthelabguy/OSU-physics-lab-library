"""Make tools/reference.docx, the Word downloads' page footer (D-0052, D-0053).

One-time tool, run by hand; builds read the committed file. Rerun it only
when the footer changes or the Pandoc that builds the downloads changes.
Needs PANDOC set to Quarto's bundled Pandoc (D-0044).

Usage: python tools/make_reference_docx.py

Starts from Pandoc's own default reference document and adds one thing: a
footer on every page, the department line then "Page N of M" from Word's
PAGE and NUMPAGES fields, at 8 pt like the PDF's. Every other part is
copied byte for byte, so the Word file keeps Pandoc's default styles.
"""

import io
import os
import re
import subprocess
import zipfile

import downloads
import render

OUT = os.path.join(render.ROOT, "tools", "reference.docx")
REL_ID = "rIdLabFooter"
SMALL = '<w:rPr><w:sz w:val="16" /></w:rPr>'


def run(text):
    return '<w:r>{}<w:t xml:space="preserve">{}</w:t></w:r>'.format(SMALL, text)


def field(instr):
    return '<w:fldSimple w:instr=" {} ">{}</w:fldSimple>'.format(instr, run("1"))


FOOTER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:p>' + run(downloads.PHYSICS + " &#183; Page ") + field("PAGE")
    + run(" of ") + field("NUMPAGES") + '</w:p></w:ftr>\n')


def once(pattern, text, repl):
    new, n = re.subn(pattern, repl, text, count=1)
    if n != 1:
        raise SystemExit("reference.docx: expected " + pattern)
    return new


def edit(name, data):
    text = data.decode("utf-8")
    if name == "word/document.xml":
        if 'xmlns:r="' not in text:
            raise SystemExit("document.xml declares no r: namespace")
        text = once(r"<w:sectPr>", text,
                    '<w:sectPr><w:footerReference w:type="default" r:id="{}" />'.format(REL_ID))
    elif name == "word/_rels/document.xml.rels":
        text = once(r"</Relationships>", text,
                    '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/'
                    '2006/relationships/footer" Id="{}" Target="footer1.xml" />'
                    '</Relationships>'.format(REL_ID))
    elif name == "[Content_Types].xml":
        text = once(r"</Types>", text,
                    '<Override PartName="/word/footer1.xml" ContentType="application/'
                    'vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
    return text.encode("utf-8")


def main():
    default = subprocess.run([render.PANDOC, "--print-default-data-file", "reference.docx"],
                             capture_output=True, check=True).stdout
    src = zipfile.ZipFile(io.BytesIO(default))
    if any(re.fullmatch(r"word/footer\d*\.xml", n) for n in src.namelist()):
        raise SystemExit("Pandoc's default already has a footer; review this tool")
    with zipfile.ZipFile(OUT, "w") as out:
        for info in src.infolist():
            out.writestr(info, edit(info.filename, src.read(info)))
        footer = zipfile.ZipInfo("word/footer1.xml", src.getinfo("word/document.xml").date_time)
        footer.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(footer, FOOTER.encode("utf-8"))
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
