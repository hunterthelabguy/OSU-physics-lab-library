"""Made-up Word originals with pictures and a drawn figure (D-0117, D-0118).

Pandoc writes the docx from Markdown; this adds the OOXML Pandoc cannot
write: an anchored group of a picture, two text boxes and a pointer, its
picture's part and relationship, and an anchored picture with a crop. The
words, sizes and ids are the tests' own. The labels name Times New Roman,
whose widths tools/font-metrics.json holds, so their breaks are measured.
"""

import hashlib
import struct
import subprocess
import zipfile
import zlib

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"')
REL = "rIdFixture"
PART = "word/media/fixture.png"
PT = 12700
# The label box's inner width: "Accelerating voltage" (99.61 pt in Times
# New Roman at 12 pt) fits, "control" goes to a second line (136.6 pt).
INNER = 110 * PT
INSET, LINE = 91440, 9525
BOX = INNER + 2 * INSET + LINE


def png(width=4, height=3):
    """A small grey PNG, `width` by `height` pixels."""
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))
    rows = b"".join(b"\x00" + b"\x80" * width for _ in range(height))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def run(text):
    return ('<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            '<w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{}</w:t></w:r>'.format(text))


def equation(base, script):
    return ('<m:oMath><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>Δ</m:t></m:r><m:sSub><m:e><m:r>'
            '<m:t>{}</m:t></m:r></m:e><m:sub><m:r><m:t>{}</m:t></m:r></m:sub></m:sSub></m:oMath>'
            .format(base, script))


def text_box(shape_id, x, y, cx, cy, paragraph, prst="rect"):
    return ('<wps:wsp><wps:cNvPr id="{0}" name="Text Box {0}"/><wps:cNvSpPr txBox="1"/><wps:spPr>'
            '<a:xfrm><a:off x="{1}" y="{2}"/><a:ext cx="{3}" cy="{4}"/></a:xfrm>'
            '<a:prstGeom prst="{6}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
            '<a:ln w="{7}"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln></wps:spPr>'
            '<wps:txbx><w:txbxContent><w:p>{5}</w:p></w:txbxContent></wps:txbx>'
            '<wps:bodyPr lIns="{8}" tIns="45720" rIns="{8}" bIns="45720" wrap="square" anchor="t"/></wps:wsp>'
            .format(shape_id, x, y, cx, cy, paragraph, prst, LINE, INSET))


def pointer(shape_id, x, y, cx, cy):
    return ('<wps:wsp><wps:cNvPr id="{0}" name="Pointer {0}"/><wps:cNvCnPr/><wps:spPr>'
            '<a:xfrm><a:off x="{1}" y="{2}"/><a:ext cx="{3}" cy="{4}"/></a:xfrm>'
            '<a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>'
            '<a:ln w="6350"><a:solidFill><a:srgbClr val="000000"/></a:solidFill><a:tailEnd type="triangle"/></a:ln>'
            '</wps:spPr><wps:bodyPr/></wps:wsp>'.format(shape_id, x, y, cx, cy))


def picture(pic_id, x, y, cx, cy, descr, crop=""):
    return ('<pic:pic><pic:nvPicPr><pic:cNvPr id="{0}" name="Picture {0}" descr="{5}"/><pic:cNvPicPr/>'
            '</pic:nvPicPr><pic:blipFill><a:blip r:embed="{6}"/>{7}<a:stretch><a:fillRect/></a:stretch>'
            '</pic:blipFill><pic:spPr><a:xfrm><a:off x="{1}" y="{2}"/><a:ext cx="{3}" cy="{4}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            .format(pic_id, x, y, cx, cy, descr, REL, crop))


def anchor(doc_pr_id, cx, cy, descr, uri, body, offset=PT * 30):
    return ('<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" '
            'relativeHeight="{6}" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">'
            '<wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="column"><wp:posOffset>0</wp:posOffset>'
            '</wp:positionH><wp:positionV relativeFrom="paragraph"><wp:posOffset>{7}</wp:posOffset></wp:positionV>'
            '<wp:extent cx="{1}" cy="{2}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapTopAndBottom/>'
            '<wp:docPr id="{0}" name="Drawing {0}" descr="{3}"/><a:graphic><a:graphicData uri="{4}">{5}'
            '</a:graphicData></a:graphic></wp:anchor></w:drawing></w:r>'
            .format(doc_pr_id, cx, cy, descr, uri, body, 251660000 + int(doc_pr_id), offset))


GROUP_URI = "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
SHAPE_URI = "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
PIC_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
FIGURE_ALT = "A grey panel with two labels"
PICTURE_ALT = "A grey square"
WIDTH, HEIGHT = 300 * PT, 200 * PT


def figure(extra_shape="", label="Accelerating voltage control", doc_pr_id="501"):
    """An anchored group: a picture, a two-line label, a label holding an
    equation, and a pointer; at half scale inside (chExt twice ext)."""
    s = 2
    children = (picture("601", 0, 0, WIDTH * s, HEIGHT * s, "")
                + text_box("602", 10 * PT * s, 10 * PT * s, BOX * s, 60 * PT * s, run(label))
                + text_box("603", 150 * PT * s, 120 * PT * s, BOX * s, 40 * PT * s,
                           run("Turn ") + equation("V", "D"))
                + pointer("604", 140 * PT * s, 30 * PT * s, 40 * PT * s, 20 * PT * s)
                + extra_shape)
    group = ('<wpg:wgp><wpg:cNvGrpSpPr/><wpg:grpSpPr><a:xfrm><a:off x="0" y="0"/>'
             '<a:ext cx="{0}" cy="{1}"/><a:chOff x="0" y="0"/><a:chExt cx="{2}" cy="{3}"/></a:xfrm>'
             '</wpg:grpSpPr>{4}</wpg:wgp>').format(WIDTH, HEIGHT, WIDTH * s, HEIGHT * s, children)
    return anchor(doc_pr_id, WIDTH, HEIGHT, FIGURE_ALT, GROUP_URI, group)


def anchored_picture(doc_pr_id="701", crop=(10000, 20000, 5000, 0)):
    """A picture of its own, anchored, cropped by Word."""
    rect = '<a:srcRect l="{}" t="{}" r="{}" b="{}"/>'.format(*crop) if crop else ""
    body = picture(doc_pr_id, 0, 0, 72 * PT, 36 * PT, PICTURE_ALT, rect)
    return anchor(doc_pr_id, 72 * PT, 36 * PT, PICTURE_ALT, PIC_URI, body)


def paragraph(text, *drawings):
    """A paragraph whose drawings sit at its start, as all 23 in the
    handouts do (D-0118), then its words."""
    return "<w:p {}>{}{}</w:p>".format(NS, "".join(drawings), run(text) if text else "")


def original(root, pandoc, markdown, xml):
    """original.docx in root: Pandoc's docx of `markdown` with `xml`
    paragraphs, the fixture picture's part and relationship added. Returns
    its SHA-256 and the picture's bytes."""
    src = root / "original-src.md"
    src.write_text(markdown, encoding="utf-8", newline="\n")
    out = root / "original.docx"
    subprocess.run([pandoc, str(src), "-f", "markdown-smart-implicit_figures", "-o", str(out)], check=True)
    with zipfile.ZipFile(out) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    doc = parts["word/document.xml"].decode("utf-8")
    at = doc.rindex("<w:sectPr")
    parts["word/document.xml"] = (doc[:at] + xml + doc[at:]).encode("utf-8")
    rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
    rels = rels.replace("</Relationships>", '<Relationship Id="{}" Type="http://schemas.openxmlformats.org/'
                        'officeDocument/2006/relationships/image" Target="media/fixture.png"/>'
                        "</Relationships>".format(REL))
    parts["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    image = png()
    parts[PART] = image
    types = parts["[Content_Types].xml"].decode("utf-8")
    if 'Extension="png"' not in types:
        types = types.replace("</Types>", '<Default Extension="png" ContentType="image/png"/></Types>')
    parts["[Content_Types].xml"] = types.encode("utf-8")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return hashlib.sha256(out.read_bytes()).hexdigest(), image
