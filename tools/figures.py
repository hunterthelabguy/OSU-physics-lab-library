"""Drawn figures (S13): a drawing in a Word original as SVG (D-0101, D-0117).

Usage: python tools/figures.py ORIGINAL.docx OUT.svg DOCPR_ID [DOCPR_ID ...]

A figure is one or more drawings anchored in one paragraph, named by their
`wp:docPr` ids, drawn at Word's offsets in one SVG: PH 213 Lab 2's labelled
photograph is one group, PH 212 Lab 3's figure is two screenshots and the
two arrows laid over them (D-0117, call 4). Labels stay SVG text, so the
word check (tools/check_unchanged.py) reads them and a screen reader reads
them on the page; a picture keeps the original's bytes, embedded.

It draws only what the three figures use: groups (scaled, not rotated),
rectangles, parallelograms, cubes, straight connectors with arrowheads,
pictures (cropped or not), picture fills (stretched or tiled), text boxes
whose paragraphs hold runs, fields and equations of runs, subscripts and
superscripts. Anything else stops with its name, so a new drawing is looked
at before it is drawn wrong.

Word stores no line breaks, so a label that holds more than one word is
broken by the advance widths in tools/font-metrics.json (Liberation Serif,
metric-compatible with Times New Roman; D-0117, call 2). A label in a face
with no widths, or a break within BREAK_MARGIN of the box's edge, stops.

Every length here is in EMU (914400 per inch) until written; the SVG's user
unit is the point (12700 EMU) and its width and height are CSS pixels at
96 per inch, Word's own size. figures.png() renders an SVG to PNG with
headless Chrome for the Word download (D-0117, call 3).
"""

import base64
import colorsys
import html
import json
import math
import os
import pathlib
import re
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS = os.path.join(ROOT, "tools", "font-metrics.json")

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
W, WP, A, PIC, WPS, WPG, M, R = ("{%s}" % NS[k] for k in ("w", "wp", "a", "pic", "wps", "wpg", "m", "r"))
FALLBACK = "{%s}Fallback" % NS["mc"]
EMU_PT, EMU_PX = 12700, 9525
# Word lays text out in twips, so each glyph's advance may round by half a
# twip: a break whose line comes within that, per glyph, of the box's inner
# width is too close to call from widths alone (points per glyph).
BREAK_MARGIN = 0.025
# The OMML kinds a label's equation may hold, drawn as nested tspans; their
# names are the word check's (check_unchanged.OMML_KINDS).
MATH_KINDS = ("r", "sSub", "sSup", "sSubSup")
# Subscript and superscript: size and baseline shift, fractions of the em.
# The subscript's shift, 0.2 em, is measured on Word's PDF of PH 213 Lab 2.
SCRIPT_SIZE, SUB_SHIFT, SUP_SHIFT = 0.7, 0.2, 0.35
# Faces whose line Word sets by their hhea metrics (Fonts.vertical).
MATH_FACES = ("Cambria Math",)
# CSS fallbacks after Word's face, for a reader without it.
FALLBACKS = {
    "Times New Roman": "'Times New Roman', 'Liberation Serif', serif",
    "Calibri": "Calibri, Carlito, sans-serif",
    "Cambria Math": "'Cambria Math', 'STIX Two Math', serif",
    "Script MT Bold": "'Script MT Bold', 'Script MT', cursive",
}
# DrawingML's line-end sizes, as multiples of the line's width, which Word
# takes as at least 2 pt: a medium head is 6 pt by 6 pt on PH 213 Lab 2's
# 0.5 pt pointers and on PH 212 Lab 3's 2 pt arrows (Word's PDFs).
END_SIZE = {"sm": 2, "med": 3, "lg": 5}
END_MIN_WIDTH = 25400


class Unsupported(SystemExit):
    pass


def stop(what):
    raise Unsupported("tools/figures.py does not draw {}; look at it before adding it".format(what))


def q(name):
    prefix, local = name.split(":")
    return "{%s}%s" % (NS[prefix], local)


def num(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") if v != int(v) else str(int(v))


def pt(emu):
    return num(emu / EMU_PT)


# ---------------------------------------------------------------- the package

class Package:
    """The parts of a docx a figure reads: document, styles, theme, media."""

    def __init__(self, path):
        self.zip = zipfile.ZipFile(path)
        self.document = without_fallbacks(self.zip.read("word/document.xml"))
        self.styles = ET.fromstring(self.zip.read("word/styles.xml"))
        rels = ET.fromstring(self.zip.read("word/_rels/document.xml.rels"))
        self.rels = {r.get("Id"): r.get("Target") for r in rels}
        theme = "word/theme/theme1.xml"
        self.theme = ET.fromstring(self.zip.read(theme)) if theme in self.zip.namelist() else None
        self.style_index = {s.get(W + "styleId"): s for s in self.styles.iter(W + "style")}

    def media(self, rid):
        target = self.rels[rid]
        part = "word/" + target if not target.startswith("/") else target[1:]
        return part, self.zip.read(part)


def without_fallbacks(data):
    root = ET.fromstring(data)
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == FALLBACK:
                parent.remove(child)
    return root


def drawings(pkg, ids):
    """The w:drawing elements with these docPr ids, in document order, and
    the paragraph that holds them (they must share one)."""
    found, para = [], None
    for p in pkg.document.iter(W + "p"):
        for d in p.iter(W + "drawing"):
            if d[0].find(WP + "docPr").get("id") in ids and d not in [x for x, _ in found]:
                found.append((d, p))
    missing = set(ids) - {d[0].find(WP + "docPr").get("id") for d, _ in found}
    if missing:
        raise SystemExit("no drawing with docPr id {} in the original".format(", ".join(sorted(missing))))
    paras = {id(p) for _, p in found}
    if len(paras) != 1:
        stop("a figure whose drawings sit in more than one paragraph")
    return [d for d, _ in found]


# ---------------------------------------------------------------- colours

def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def srgb(c):
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


PRESET = {"white": "FFFFFF", "black": "000000"}


def colour(pkg, el, placeholder=None):
    """An a:*Clr element as #rrggbb, its transforms applied (ECMA-376 20.1.2.3)."""
    tag = el.tag[len(A):]
    if tag == "srgbClr":
        rgb = hex_rgb(el.get("val"))
    elif tag == "prstClr":
        if el.get("val") not in PRESET:
            stop("preset colour " + el.get("val"))
        rgb = hex_rgb(PRESET[el.get("val")])
    elif tag == "sysClr":
        rgb = hex_rgb(el.get("lastClr"))
    elif tag == "scrgbClr":
        # Linear RGB in thousandths of a percent.
        rgb = tuple(srgb(int(el.get(k)) / 100000) for k in ("r", "g", "b"))
    elif tag == "schemeClr":
        name = el.get("val")
        if name == "phClr":
            if placeholder is None:
                stop("a placeholder colour outside a style")
            rgb = hex_rgb(placeholder.lstrip("#"))
        else:
            name = {"tx1": "dk1", "tx2": "dk2", "bg1": "lt1", "bg2": "lt2"}.get(name, name)
            scheme = pkg.theme.find(".//a:clrScheme/a:" + name, NS)
            if scheme is None:
                stop("scheme colour " + name)
            rgb = hex_rgb(colour(pkg, scheme[0])[1:])
    else:
        stop("colour " + tag)
    for mod in el:
        k, v = mod.tag[len(A):], int(mod.get("val")) / 100000
        if k == "shade":
            rgb = tuple(srgb(lin(c) * v) for c in rgb)
        elif k == "tint":
            rgb = tuple(srgb(lin(c) * v + 1 - v) for c in rgb)
        elif k in ("lumMod", "lumOff"):
            h, l, s = colorsys.rgb_to_hls(*rgb)
            l = l * v if k == "lumMod" else l + v
            rgb = colorsys.hls_to_rgb(h, max(0, min(1, l)), s)
        else:
            stop("colour transform " + k)
    return "#" + "".join("%02x" % round(c * 255) for c in rgb)


def fill_colour(pkg, el, placeholder=None):
    return colour(pkg, el[0], placeholder)


# ---------------------------------------------------------------- pictures

def image_size(data):
    """Pixel size and dots per inch of a PNG or JPEG."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        dpi = (96, 96)
        i = 8
        while i < len(data):
            n, kind = struct.unpack(">I4s", data[i:i + 8])
            if kind == b"pHYs":
                x, y, unit = struct.unpack(">IIB", data[i + 8:i + 17])
                if unit == 1:
                    dpi = (x * 0.0254, y * 0.0254)
            if kind == b"IDAT":
                break
            i += 12 + n
        return (w, h), dpi
    if data[:2] == b"\xff\xd8":
        dpi, i = (96, 96), 2
        while i < len(data):
            marker = data[i + 1]
            size = struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker == 0xE0 and data[i + 4:i + 9] == b"JFIF\x00":
                unit, x, y = struct.unpack(">BHH", data[i + 11:i + 16])
                if unit == 1 and x and y:
                    dpi = (x, y)
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h), dpi
            i += 2 + size
    stop("a picture that is neither PNG nor JPEG")


def data_uri(part, data):
    kind = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(
        os.path.splitext(part)[1].lower())
    if kind is None:
        stop("picture type " + part)
    return "data:{};base64,{}".format(kind, base64.b64encode(data).decode("ascii"))


# ---------------------------------------------------------------- text

class Fonts:
    def __init__(self):
        with open(METRICS, encoding="utf-8") as fh:
            self.faces = json.load(fh)["faces"]

    def face(self, family, bold, italic):
        return (self.faces.get("{}|{}|{}".format(family, int(bold), int(italic)))
                or self.faces.get("{}|0|0".format(family)))

    def vertical(self, family, bold, italic):
        """(above, below) the baseline, in ems, of a single-spaced line.

        Measured on Word's PDFs of PH 213 Labs 2 and 4 (2026-10-08): the
        line is the larger of the Windows ascent and descent and the hhea
        ascent, descent and line gap; the baseline sits the Windows descent
        above the line's foot. Cambria Math is the exception: Word sets its
        line by the hhea numbers alone."""
        f = self.face(family, bold, italic)
        if f is None:
            stop("text in the face {!r}, which tools/font-metrics.json lacks".format(family))
        u = f["units_per_em"]
        hhea = (f["hhea_ascent"] + f["hhea_line_gap"]) / u, f["hhea_descent"] / u
        if family in MATH_FACES:
            return hhea
        line = max(f["win_ascent"] + f["win_descent"],
                   f["hhea_ascent"] + f["hhea_descent"] + f["hhea_line_gap"]) / u
        return line - f["win_descent"] / u, f["win_descent"] / u

    def width(self, family, bold, italic, text):
        f = self.face(family, bold, italic)
        if f is None or "widths" not in f:
            return None
        try:
            return sum(f["widths"][c] for c in text) / f["units_per_em"]
        except KeyError as e:
            stop("the character {!r} in {!r}, which has no width in tools/font-metrics.json".format(e.args[0], family))


def on(el):
    if el is None:
        return None
    return el.get(W + "val", "true").lower() not in ("0", "false", "off")


class Style:
    """Run and paragraph properties resolved through docDefaults and styles."""

    def __init__(self, pkg):
        self.pkg = pkg
        minor = pkg.theme.find(".//a:minorFont/a:latin", NS) if pkg.theme is not None else None
        major = pkg.theme.find(".//a:majorFont/a:latin", NS) if pkg.theme is not None else None
        self.theme_fonts = {"minorHAnsi": minor.get("typeface") if minor is not None else None,
                            "majorHAnsi": major.get("typeface") if major is not None else None}
        self.theme_fonts["minorAscii"] = self.theme_fonts["minorHAnsi"]
        self.theme_fonts["majorAscii"] = self.theme_fonts["majorHAnsi"]
        self.default_para = next((s.get(W + "styleId") for s in pkg.styles.iter(W + "style")
                                  if s.get(W + "type") == "paragraph" and s.get(W + "default") in ("1", "true")), None)

    def chain(self, sid):
        out, seen = [], set()
        while sid and sid in self.pkg.style_index and sid not in seen:
            seen.add(sid)
            s = self.pkg.style_index[sid]
            out.append(s)
            based = s.find(W + "basedOn")
            sid = based.get(W + "val") if based is not None else None
        return list(reversed(out))

    def rpr(self, props, rpr):
        if rpr is None:
            return
        fonts = rpr.find(W + "rFonts")
        if fonts is not None:
            font = fonts.get(W + "hAnsi") or fonts.get(W + "ascii")
            theme = fonts.get(W + "hAnsiTheme") or fonts.get(W + "asciiTheme")
            if font:
                props["font"] = font
            elif theme:
                props["font"] = self.theme_fonts.get(theme)
        for key in ("b", "i"):
            v = on(rpr.find(W + key))
            if v is not None:
                props[key] = v
        sz = rpr.find(W + "sz")
        if sz is not None:
            props["size"] = int(sz.get(W + "val")) / 2
        col = rpr.find(W + "color")
        if col is not None:
            theme = col.get(W + "themeColor")
            if theme:
                el = ET.Element(A + "schemeClr", val={"text1": "tx1", "text2": "tx2", "background1": "bg1",
                                                      "background2": "bg2"}.get(theme, theme))
                props["color"] = colour(self.pkg, el)
            elif col.get(W + "val") == "auto":
                props["color"] = "#000000"
            else:
                props["color"] = "#" + col.get(W + "val").lower()
        for key in ("caps", "smallCaps", "strike", "vertAlign", "u"):
            el = rpr.find(W + key)
            if el is not None and (key != "u" or el.get(W + "val") not in (None, "none")) \
                    and (key != "vertAlign" or el.get(W + "val") != "baseline") and on(el) is not False:
                stop("run property " + key)

    def ppr(self, props, ppr):
        if ppr is None:
            return
        jc = ppr.find(W + "jc")
        if jc is not None:
            props["jc"] = jc.get(W + "val")
        sp = ppr.find(W + "spacing")
        if sp is not None:
            for key in ("before", "after", "line"):
                if sp.get(W + key) is not None:
                    props[key] = int(sp.get(W + key))
            if sp.get(W + "lineRule"):
                props["lineRule"] = sp.get(W + "lineRule")
        for key in ("ind", "numPr"):
            if ppr.find(W + key) is not None:
                stop("paragraph property " + key + " in a label")

    def paragraph(self, p):
        """(paragraph props, base run props) for a w:p."""
        para = {"jc": "left", "before": 0, "after": 0, "line": 240, "lineRule": "auto"}
        run = {"font": None, "b": False, "i": False, "size": 10.0, "color": "#000000"}
        defaults = self.pkg.styles.find(W + "docDefaults")
        if defaults is not None:
            self.rpr(run, defaults.find(f"{W}rPrDefault/{W}rPr"))
            self.ppr(para, defaults.find(f"{W}pPrDefault/{W}pPr"))
        ps = p.find(f"{W}pPr/{W}pStyle")
        for s in self.chain(ps.get(W + "val") if ps is not None else self.default_para):
            self.ppr(para, s.find(W + "pPr"))
            self.rpr(run, s.find(W + "rPr"))
        self.ppr(para, p.find(W + "pPr"))
        return para, run

    def run(self, base, r):
        props = dict(base)
        rs = r.find(f"{W}rPr/{W}rStyle")
        if rs is not None:
            for s in self.chain(rs.get(W + "val")):
                self.rpr(props, s.find(W + "rPr"))
        self.rpr(props, r.find(W + "rPr"))
        return props


def label_runs(style, p):
    """A paragraph as a list of pieces: ("text", props, str) and
    ("math", [(kind, depth, props, str)])."""
    para, base = style.paragraph(p)
    pieces, fields = [], []

    def run(r):
        props = style.run(base, r)
        for el in r:
            if el.tag == W + "fldChar":
                kind = el.get(W + "fldCharType")
                if kind == "begin":
                    fields.append("instr")
                elif kind == "separate" and fields:
                    fields[-1] = "result"
                elif kind == "end" and fields:
                    fields.pop()
            elif el.tag == W + "instrText":
                instr = (el.text or "").split()
                if instr and instr[0].upper() != "SEQ":
                    stop("the field " + instr[0])
            elif el.tag == W + "t":
                if "instr" not in fields:
                    pieces.append(("text", props, el.text or ""))
            elif el.tag in (W + "rPr", W + "lastRenderedPageBreak", W + "noBreakHyphen"):
                pass
            elif el.tag in (W + "tab", W + "br", W + "cr"):
                stop("a tab or break in a label")
            else:
                stop("the run element " + el.tag.split("}")[1])

    def math(om):
        """An equation as a tree that mirrors its OMML: a run is
        ("r", props, text, depth); a script is (kind, [(part, [nodes])])."""

        def walk(el, depth):
            tag = el.tag[len(M):] if el.tag.startswith(M) else None
            if tag == "r":
                props = style.run(base, el)
                props["font"] = "Cambria Math"
                sty = el.find(f"{M}rPr/{M}sty")
                text = "".join(t.text or "" for t in el.iter(M + "t"))
                plain = sty is not None and sty.get(M + "val") == "p"
                props["i"] = not plain and text.isalpha()
                return [("r", props, text, depth)]
            if tag in ("sSub", "sSup", "sSubSup"):
                parts = []
                for child in el:
                    ct = child.tag[len(M):]
                    if ct.endswith("Pr"):
                        continue
                    if ct not in ("e", "sub", "sup"):
                        stop("the equation part " + ct)
                    inner = depth + ((-1 if ct == "sub" else 1,) if ct != "e" else ())
                    parts.append((ct, [n for c in child for n in walk(c, inner)]))
                return [(tag, parts)]
            if tag and tag.endswith("Pr"):
                return []
            stop("the equation element " + el.tag.split("}")[1])

        pieces.append(("math", [n for child in om for n in walk(child, ())]))

    for el in p:
        if el.tag == W + "r":
            run(el)
        elif el.tag == M + "oMath":
            math(el)
        elif el.tag == M + "oMathPara":
            stop("a display equation in a label")
        elif el.tag in (W + "pPr", W + "proofErr", W + "bookmarkStart", W + "bookmarkEnd"):
            pass
        else:
            stop("the paragraph element " + el.tag.split("}")[1])
    return para, base, pieces


def math_runs(nodes):
    """An equation tree's runs in order: (props, text, depth)."""
    for node in nodes:
        if node[0] == "r":
            yield node[1], node[2], node[3]
        else:
            for _, inner in node[1]:
                yield from math_runs(inner)


def words(pieces):
    """Pieces split at spaces into words, each a list of segments; an
    equation is one word of its own, as Word sets it here."""
    out, cur = [], []
    for piece in pieces:
        if piece[0] == "math":
            if cur:
                out.append(cur)
                cur = []
            out.append([piece])
            continue
        _, props, text = piece
        for i, chunk in enumerate(text.split(" ")):
            if i:
                if cur:
                    out.append(cur)
                cur = []
            if chunk:
                cur.append(("text", props, chunk))
    if cur:
        out.append(cur)
    return out


def seg_width(fonts, seg):
    """(width in points, exact) of one segment."""
    if seg[0] == "text":
        _, p, text = seg
        w = fonts.width(p["font"], p["b"], p["i"], text)
        return (None, False) if w is None else (w * p["size"], True)
    total = 0
    for p, text, depth in math_runs(seg[1]):
        size = p["size"] * (SCRIPT_SIZE ** len(depth))
        # Word spaces an equation's runs by its own rules, so its width is an
        # estimate and a line holding one is never a close call (BREAK_MARGIN).
        w = fonts.width(p["font"], False, False, text)
        if w is None:
            return None, False
        total += w * size
    return total, False


def lines_of(fonts, para_words, space_props, avail):
    """Greedy breaks, as Word makes them for a left-to-right label."""
    if len(para_words) <= 1:
        return [para_words]
    space = fonts.width(space_props["font"], space_props["b"], space_props["i"], " ")
    if space is None:
        stop("a label of more than one word in the face {!r}, which has no widths".format(space_props["font"]))
    space *= space_props["size"]
    lines, cur = [], []
    cur_w = cur_glyphs = cur_rough = 0.0
    for word in para_words:
        widths = [seg_width(fonts, s) for s in word]
        if any(w is None for w, _ in widths):
            stop("a label of more than one word in the face {!r}, which has no widths".format(
                word[0][1]["font"] if word[0][0] == "text" else "Cambria Math"))
        ww = sum(w for w, _ in widths)
        glyphs = sum(len(s[2]) if s[0] == "text" else sum(len(t) for _, t, _ in math_runs(s[1])) for s in word)
        # An equation's width is estimated (seg_width), so its whole width
        # counts as doubt.
        rough = sum(w for w, exact in widths if not exact)
        trial = cur_w + (space if cur else 0) + ww
        if cur:
            doubt = BREAK_MARGIN * (cur_glyphs + 1 + glyphs) + cur_rough + rough
            if abs(trial - avail) <= doubt:
                stop("a line break too close to call: {:.2f} pt of words in {:.2f} pt, give or take {:.2f}".format(
                    trial, avail, doubt))
        if cur and trial > avail:
            lines.append(cur)
            cur, cur_w, cur_glyphs, cur_rough = [word], ww, glyphs, rough
        else:
            cur.append(word)
            cur_w, cur_glyphs, cur_rough = trial, cur_glyphs + (1 if cur_glyphs else 0) + glyphs, cur_rough + rough
    lines.append(cur)
    return lines


# ---------------------------------------------------------------- geometry

class Frame:
    """Maps a group's child coordinates to the figure's (EMU)."""

    def __init__(self, sx=1.0, dx=0.0, sy=1.0, dy=0.0):
        self.sx, self.dx, self.sy, self.dy = sx, dx, sy, dy

    def point(self, x, y):
        return self.sx * x + self.dx, self.sy * y + self.dy

    def inner(self, xfrm):
        """The frame a group's children live in."""
        off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
        choff, chext = xfrm.find("a:chOff", NS), xfrm.find("a:chExt", NS)
        if xfrm.get("rot", "0") != "0" or xfrm.get("flipH") == "1" or xfrm.get("flipV") == "1":
            stop("a rotated or flipped group")
        ox, oy, cx, cy = (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")))
        chx, chy, chcx, chcy = (int(choff.get("x")), int(choff.get("y")),
                                int(chext.get("cx")), int(chext.get("cy")))
        sx = cx / chcx if chcx else 1.0
        sy = cy / chcy if chcy else 1.0
        x0, y0 = self.point(ox, oy)
        return Frame(self.sx * sx, x0 - self.sx * sx * chx, self.sy * sy, y0 - self.sy * sy * chy)


def box(frame, xfrm):
    """(x, y, w, h, rot degrees, flipH, flipV) of a shape in figure EMU."""
    off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
    x, y = frame.point(int(off.get("x")), int(off.get("y")))
    w, h = int(ext.get("cx")) * frame.sx, int(ext.get("cy")) * frame.sy
    rot = int(xfrm.get("rot", "0")) / 60000
    if rot and abs(frame.sx - frame.sy) > 0.005 * frame.sx:
        stop("a rotated shape in a group scaled unevenly")
    return x, y, w, h, rot, xfrm.get("flipH") == "1", xfrm.get("flipV") == "1"


def transform(x, y, w, h, rot, fh, fv, mirror=False):
    parts = ["translate({} {})".format(pt(x), pt(y))]
    cx, cy = w / 2, h / 2
    if mirror:
        parts.append("translate({0} {1}) scale(-1 1) translate(-{0} -{1})".format(pt(cx), pt(cy)))
    if rot:
        parts.append("rotate({} {} {})".format(num(rot), pt(cx), pt(cy)))
    if fh or fv:
        parts.append("translate({0} {1}) scale({2} {3}) translate(-{0} -{1})".format(
            pt(cx), pt(cy), -1 if fh else 1, -1 if fv else 1))
    return " ".join(parts)


def adj(geom, default):
    gd = geom.find("a:avLst/a:gd", NS)
    if gd is None:
        return default
    m = re.fullmatch(r"val (-?\d+)", gd.get("fmla"))
    if not m:
        stop("the adjustment " + gd.get("fmla"))
    return int(m.group(1))


def outline(prst, geom, w, h):
    """Preset geometry (ECMA-376 presetShapeDefinitions) as path data, in
    the shape's own box; for a cube, its faces and edges."""
    ss = min(w, h)
    if prst == "rect":
        return [("M0 0H{0}V{1}H0Z".format(pt(w), pt(h)), "norm")]
    if prst == "parallelogram":
        a = max(0, min(adj(geom, 25000), 100000 * w / ss if ss else 0))
        x2 = ss * a / 100000
        return [("M0 {1}L{0} 0L{2} 0L{3} {1}Z".format(pt(x2), pt(h), pt(w), pt(w - x2)), "norm")]
    if prst == "cube":
        a = max(0, min(adj(geom, 25000), 100000))
        y1 = ss * a / 100000
        x4, y4 = w - y1, h - y1
        P = lambda *xy: " ".join("{} {}".format(pt(xy[i]), pt(xy[i + 1])) for i in range(0, len(xy), 2))
        return [("M{}L{}Z".format(P(0, y1), P(x4, y1, x4, h, 0, h)), "norm"),
                ("M{}L{}Z".format(P(x4, y1), P(w, 0, w, y4, x4, h)), "darkenLess"),
                ("M{}L{}Z".format(P(0, y1), P(y1, 0, w, 0, x4, y1)), "lightenLess"),
                ("M{}L{}ZM{}L{}M{}L{}".format(P(0, y1), P(y1, 0, w, 0, w, y4, x4, h, 0, h),
                                               P(0, y1), P(x4, y1, w, 0), P(x4, y1), P(x4, h)), "stroke")]
    stop("the preset shape " + prst)


# ---------------------------------------------------------------- the figure

class Figure:
    def __init__(self, pkg):
        self.pkg = pkg
        self.style = Style(pkg)
        self.fonts = Fonts()
        self.defs, self.body = [], []
        # Labels and pictures are numbered "drawing.item" in the original's
        # reading order, which the word check follows; they paint in
        # Word's stacking order.
        self.drawing, self.items = 0, 0
        self.patterns = {}
        # Text may run past its box, as Word draws it: the label's ink, in points.
        self.ink = [math.inf, -math.inf]

    # style references (wps:style) and the theme's style lists
    def style_ref(self, sp, name):
        ref = sp.find(f"{WPS}style/a:{name}", NS) if sp is not None else None
        if ref is None:
            return 0, None
        return int(ref.get("idx")), (colour(self.pkg, ref[0]) if len(ref) else None)

    def theme_line(self, idx, col):
        if not idx:
            return None
        lns = self.pkg.theme.findall(".//a:fmtScheme/a:lnStyleLst/a:ln", NS)
        ln = lns[idx - 1]
        fill = ln.find("a:solidFill", NS)
        return {"w": int(ln.get("w", "9525")), "color": fill_colour(self.pkg, fill, col) if fill is not None else col,
                "head": None, "tail": None}

    def line(self, sp, sppr):
        idx, col = self.style_ref(sp, "lnRef")
        base = self.theme_line(idx, col)
        ln = sppr.find("a:ln", NS)
        if ln is None:
            return base
        if ln.find("a:noFill", NS) is not None:
            return None
        out = dict(base or {"w": 9525, "color": "#000000"})
        if ln.get("w"):
            out["w"] = int(ln.get("w"))
        fill = ln.find("a:solidFill", NS)
        if fill is not None:
            out["color"] = fill_colour(self.pkg, fill, col)
        elif base is None:
            return None
        dash = ln.find("a:prstDash", NS)
        if dash is not None and dash.get("val") != "solid":
            stop("a dashed line")
        if ln.find("a:gradFill", NS) is not None or ln.find("a:pattFill", NS) is not None:
            stop("a gradient or patterned line")
        for end in ("head", "tail"):
            e = ln.find("a:{}End".format(end), NS)
            kind = e.get("type", "none") if e is not None else "none"
            out[end] = None if kind == "none" else (kind, e.get("w", "med"), e.get("len", "med"))
        return out

    def fill(self, sp, sppr, w, h):
        """An SVG fill for the shape's own box, or "none"."""
        for el in sppr:
            tag = el.tag[len(A):] if el.tag.startswith(A) else None
            if tag == "noFill":
                return "none"
            if tag == "solidFill":
                return fill_colour(self.pkg, el)
            if tag == "blipFill":
                return self.blip_fill(el, w, h)
            if tag in ("gradFill", "pattFill", "grpFill"):
                stop("a {} fill".format(tag))
        idx, col = self.style_ref(sp, "fillRef")
        if not idx:
            return "none"
        fills = self.pkg.theme.find(".//a:fmtScheme/a:fillStyleLst", NS)
        f = fills[idx - 1]
        if f.tag != A + "solidFill":
            stop("a theme fill other than solid")
        return fill_colour(self.pkg, f, col)

    def blip_fill(self, el, w, h):
        blip = el.find("a:blip", NS)
        part, data = self.pkg.media(blip.get(R + "embed"))
        tile, stretch = el.find("a:tile", NS), el.find("a:stretch", NS)
        pid = "f{}".format(len(self.patterns) + 1)
        if tile is not None:
            if tile.get("flip", "none") != "none" or tile.get("algn", "tl") != "tl":
                stop("a flipped or aligned tile")
            (px, py), (dx, dy) = image_size(data)
            tw = px / dx * 914400 * int(tile.get("sx", "100000")) / 100000
            th = py / dy * 914400 * int(tile.get("sy", "100000")) / 100000
            key = (part, tw, th, tile.get("tx", "0"), tile.get("ty", "0"))
            if key not in self.patterns:
                self.patterns[key] = pid
                self.defs.append(
                    '<pattern id="{}" patternUnits="userSpaceOnUse" x="{}" y="{}" width="{}" height="{}">'
                    '<image width="{}" height="{}" preserveAspectRatio="none" href="{}"/></pattern>'.format(
                        pid, pt(int(tile.get("tx", "0"))), pt(int(tile.get("ty", "0"))), pt(tw), pt(th),
                        pt(tw), pt(th), data_uri(part, data)))
            return "url(#{})".format(self.patterns[key])
        if stretch is not None:
            key = (part, w, h)
            if key not in self.patterns:
                self.patterns[key] = pid
                self.defs.append(
                    '<pattern id="{}" patternUnits="userSpaceOnUse" width="{}" height="{}">'
                    '<image width="{}" height="{}" preserveAspectRatio="none" href="{}"/></pattern>'.format(
                        pid, pt(w), pt(h), pt(w), pt(h), data_uri(part, data)))
            return "url(#{})".format(self.patterns[key])
        stop("a picture fill neither tiled nor stretched")

    # elements
    def walk(self, el, frame):
        tag = el.tag
        if tag in (WPG + "wgp", WPG + "grpSp"):
            xfrm = el.find(f"{WPG}grpSpPr/a:xfrm", NS)
            inner = frame.inner(xfrm) if xfrm is not None else frame
            for child in el:
                if child.tag in (WPG + "cNvGrpSpPr", WPG + "grpSpPr", WPG + "cNvPr"):
                    continue
                self.walk(child, inner)
        elif tag == WPS + "wsp":
            self.shape(el, frame)
        elif tag == PIC + "pic":
            self.picture(el, frame)
        else:
            stop("the drawing element " + tag.split("}")[1])

    def picture(self, el, frame):
        x, y, w, h, rot, fh, fv = box(frame, el.find(f"{PIC}spPr/a:xfrm", NS))
        if rot or fh or fv:
            stop("a rotated or flipped picture")
        blip = el.find(f"{PIC}blipFill/a:blip", NS)
        part, data = self.pkg.media(blip.get(R + "embed"))
        src = el.find(f"{PIC}blipFill/a:srcRect", NS)
        crop = [int(src.get(k, "0")) / 100000 if src is not None else 0 for k in ("l", "t", "r", "b")]
        descr = el.find(f"{PIC}nvPicPr/{PIC}cNvPr", NS).get("descr", "")
        label = ' role="img" aria-label="{}"'.format(html.escape(descr)) if descr else ' aria-hidden="true"'
        l, t, r, b = crop
        self.items += 1
        self.body.append(
            '<svg class="figure-picture" data-i="{d}.{i}" data-alt="{alt}"{label} x="{x}" y="{y}" width="{w}" height="{h}"'
            ' viewBox="{vx} {vy} {vw} {vh}" preserveAspectRatio="none">'
            '<image width="1" height="1" preserveAspectRatio="none" href="{uri}"/></svg>'.format(
                d=self.drawing, i=self.items, alt=html.escape(descr), label=label, x=pt(x), y=pt(y), w=pt(w), h=pt(h),
                vx=num(l), vy=num(t), vw=num(1 - l - r), vh=num(1 - t - b), uri=data_uri(part, data)))

    def shape(self, el, frame):
        sppr = el.find(WPS + "spPr")
        xfrm = sppr.find("a:xfrm", NS)
        x, y, w, h, rot, fh, fv = box(frame, xfrm)
        geom = sppr.find("a:prstGeom", NS)
        if geom is None:
            stop("a custom geometry")
        prst = geom.get("prst")
        mirror = False
        scene = sppr.find("a:scene3d", NS)
        if scene is not None:
            cam = scene.find("a:camera", NS)
            r = cam.find("a:rot", NS)
            if (cam.get("prst") != "orthographicFront" or r is None
                    or (r.get("lat"), r.get("lon"), r.get("rev")) != ("0", "10800000", "0")):
                stop("a 3-D scene other than a front camera turned half round")
            mirror = True
        for unsupported in ("a:effectLst/*", "a:sp3d/*"):
            if sppr.find(unsupported, NS) is not None:
                stop("an effect or 3-D shape")
        ln = self.line(el, sppr)
        g = transform(x, y, w, h, rot, fh, fv, mirror)
        if prst in ("straightConnector1", "line"):
            if ln:
                self.connector(g, w, h, ln)
        else:
            self.body.append('<g transform="{}">'.format(g))
            paint = self.fill(el, sppr, w, h)
            for d, kind in outline(prst, geom, w, h):
                if kind == "stroke":
                    if ln:
                        self.body.append('<path d="{}" fill="none"{}/>'.format(d, stroke(ln)))
                    continue
                face = paint if kind == "norm" or paint == "none" else shade_face(paint, kind)
                self.body.append('<path d="{}" fill="{}"{}/>'.format(
                    d, face, stroke(ln) if ln and prst != "cube" else ' stroke="none"'))
            self.body.append("</g>")
        text = el.find(f"{WPS}txbx/{W}txbxContent", NS)
        if text is not None:
            if rot or fh or fv or mirror:
                stop("a rotated or flipped text box")
            self.label(el.find(WPS + "bodyPr"), text, x, y, w, h, ln["w"] if ln else 0)

    def connector(self, g, w, h, ln):
        width = ln["w"]
        parts = ['<g transform="{}">'.format(g)]
        x1, y1, x2, y2 = 0.0, 0.0, w, h
        length = math.hypot(x2 - x1, y2 - y1)
        ends = []
        for end, (ax, ay, bx, by) in (("head", (x1, y1, x2, y2)), ("tail", (x2, y2, x1, y1))):
            spec = ln[end]
            if spec is None:
                continue
            kind, ew, el_ = spec
            if kind not in ("triangle", "arrow"):
                stop("the line end " + kind)
            unit = max(width, END_MIN_WIDTH)
            hw, hl = END_SIZE[ew] * unit / 2, END_SIZE[el_] * unit
            ux, uy = (bx - ax) / length, (by - ay) / length
            bx_, by_ = ax + ux * hl, ay + uy * hl
            left = (bx_ - uy * hw, by_ + ux * hw)
            right = (bx_ + uy * hw, by_ - ux * hw)
            ends.append((end, kind, (ax, ay), left, right, (bx_, by_)))
        sx, sy, ex, ey = x1, y1, x2, y2
        for end, kind, tip, left, right, base in ends:
            if kind == "triangle":
                if end == "head":
                    sx, sy = base
                else:
                    ex, ey = base
        parts.append('<path d="M{} {}L{} {}" fill="none"{}/>'.format(pt(sx), pt(sy), pt(ex), pt(ey), stroke(ln)))
        for end, kind, tip, left, right, base in ends:
            if kind == "triangle":
                parts.append('<path d="M{} {}L{} {}L{} {}Z" fill="{}" stroke="none"/>'.format(
                    pt(tip[0]), pt(tip[1]), pt(left[0]), pt(left[1]), pt(right[0]), pt(right[1]), ln["color"]))
            else:
                parts.append('<path d="M{} {}L{} {}L{} {}" fill="none"{}/>'.format(
                    pt(left[0]), pt(left[1]), pt(tip[0]), pt(tip[1]), pt(right[0]), pt(right[1]), stroke(ln)))
        parts.append("</g>")
        self.body.extend(parts)

    def label(self, body, content, x, y, w, h, lw):
        """A text box's paragraphs as SVG text: one <text> per paragraph, a
        tspan per line. Measured on Word's PDF of PH 213 Lab 2 (2026-10-08):
        the insets count from the outline's inner edge; a line's baseline
        sits its ascent and line gap below the line above's descent, the
        first's below the paragraph's space before; Word applies that space
        at the top of a text box too."""
        ins = {k: int(body.get(k + "Ins", d)) for k, d in (("l", 91440), ("t", 45720), ("r", 91440), ("b", 45720))}
        if body.get("vert", "horz") != "horz" or body.get("rot", "0") != "0":
            stop("vertical or rotated text")
        if body.get("wrap", "square") != "square":
            stop("a text box that does not wrap")
        pad = lw / 2
        left = (x + pad + ins["l"]) / EMU_PT
        avail = (w - lw - ins["l"] - ins["r"]) / EMU_PT
        inner_top = (y + pad + ins["t"]) / EMU_PT
        inner_h = (h - lw - ins["t"] - ins["b"]) / EMU_PT
        blocks = []
        for p in content:
            if p.tag != W + "p":
                stop("the text box element " + p.tag.split("}")[1])
            para, base, pieces = label_runs(self.style, p)
            if not pieces:
                stop("an empty paragraph in a label")
            if (para["line"], para["lineRule"]) != (240, "auto"):
                stop("line spacing other than single in a label")
            laid = []
            for line in lines_of(self.fonts, words(pieces), base, avail):
                above = below = 0.0
                for word in line:
                    for seg in word:
                        segs = [(seg[1], ())] if seg[0] == "text" else [(pp, d) for pp, _, d in math_runs(seg[1])]
                        for props, depth in segs:
                            a, d = self.fonts.vertical(props["font"], props["b"], props["i"])
                            s = props["size"] * (SCRIPT_SIZE ** len(depth))
                            above, below = max(above, a * s), max(below, d * s)
                laid.append((line, above, below))
            blocks.append((para, base, laid))
        total, prev = 0.0, None
        for para, _, laid in blocks:
            total += para["before"] / 20
            for _, above, below in laid:
                total += above + (prev or 0)
                prev = below
            total += prev + para["after"] / 20
            prev = 0
        anchor = body.get("anchor", "t")
        top = {"t": inner_top, "ctr": inner_top + (inner_h - total) / 2,
               "b": inner_top + inner_h - total}.get(anchor)
        if top is None:
            stop("the text anchor " + anchor)
        cursor = top
        for para, base, laid in blocks:
            cursor += para["before"] / 20
            self.items += 1
            out = ['<text class="figure-label" data-i="{}.{}" xml:space="preserve" font-family="{}" font-size="{}"'
                   ' fill="{}"{}{}>'.format(self.drawing, self.items, html.escape(family(base["font"])), num(base["size"]),
                                           base["color"], ' font-weight="bold"' if base["b"] else "",
                                           ' font-style="italic"' if base["i"] else "")]
            below_prev = 0.0
            for line, above, below in laid:
                cursor += below_prev + above
                jc = para["jc"]
                space = self.fonts.width(base["font"], base["b"], base["i"], " ")
                width = sum(seg_width(self.fonts, s)[0] for word in line for s in word) +                     (len(line) - 1) * space * base["size"]
                if width > avail:
                    # Word starts a word too wide for its box at the left
                    # inset (PH 213 Lab 4's "T", Word's PDF).
                    jc = "left"
                if jc == "center":
                    lx, anchor_ = left + avail / 2, "middle"
                elif jc in ("right", "end"):
                    lx, anchor_ = left + avail, "end"
                elif jc in ("left", "start", "both"):
                    lx, anchor_ = left, None
                else:
                    stop("the alignment " + jc)
                self.ink = [min(self.ink[0], cursor - above), max(self.ink[1], cursor + below)]
                out.append('<tspan class="figure-line" x="{}" y="{}"{}>'.format(
                    num(lx), num(cursor), ' text-anchor="{}"'.format(anchor_) if anchor_ else ""))
                for k, word in enumerate(line):
                    if k:
                        out.append(" ")
                    for seg in word:
                        out.append(self.segment(seg, base))
                out.append("</tspan>")
                below_prev = below
            cursor += below_prev + para["after"] / 20
            out.append("</text>")
            self.body.append("".join(out))

    def segment(self, seg, base):
        if seg[0] == "text":
            return run_tspan(seg[1], base, html.escape(seg[2]))
        def emit(node, size):
            if node[0] == "r":
                _, props, text, _ = node
                return '<tspan data-omml="r" font-family="{}" font-style="{}">{}</tspan>'.format(
                    html.escape(family(props["font"])), "italic" if props["i"] else "normal",
                    html.escape(text))
            out = ['<tspan data-omml="{}">'.format(node[0])]
            for part, inner in node[1]:
                if part == "e":
                    out.append('<tspan data-omml="e">' + "".join(emit(n, size) for n in inner) + "</tspan>")
                else:
                    shift = (SUP_SHIFT if part == "sup" else -SUB_SHIFT) * size
                    out.append('<tspan data-omml="{}" font-size="{}" baseline-shift="{}">{}</tspan>'.format(
                        part, num(size * SCRIPT_SIZE), num(shift),
                        "".join(emit(n, size * SCRIPT_SIZE) for n in inner)))
            out.append("</tspan>")
            return "".join(out)

        return ('<tspan class="figure-math" data-kind="inline">'
                + "".join(emit(n, base["size"]) for n in seg[1]) + "</tspan>")


def family(name):
    return FALLBACKS.get(name, "'{}'".format(name))


def run_tspan(props, base, text):
    attrs = ""
    if props["font"] != base["font"]:
        attrs += ' font-family="{}"'.format(html.escape(family(props["font"])))
    if props["size"] != base["size"]:
        attrs += ' font-size="{}"'.format(num(props["size"]))
    if props["b"] != base["b"]:
        attrs += ' font-weight="{}"'.format("bold" if props["b"] else "normal")
    if props["i"] != base["i"]:
        attrs += ' font-style="{}"'.format("italic" if props["i"] else "normal")
    if props["color"] != base["color"]:
        attrs += ' fill="{}"'.format(props["color"])
    return '<tspan{}>{}</tspan>'.format(attrs, text) if attrs else text


def stroke(ln):
    return ' stroke="{}" stroke-width="{}" stroke-linejoin="round"'.format(ln["color"], pt(ln["w"]))


def shade_face(paint, kind):
    """A cube's side faces: darkenLess and lightenLess of a solid fill."""
    if not paint.startswith("#"):
        stop("a shaded face of a picture fill")
    rgb = hex_rgb(paint[1:])
    factor = 0.8 if kind == "darkenLess" else 1.2
    return "#" + "".join("%02x" % round(max(0, min(1, c * factor)) * 255) for c in rgb)


# ---------------------------------------------------------------- the whole

def svg(original, ids, title=""):
    """The SVG of the drawings with these docPr ids, and Word's descr of
    each drawing that is not a picture."""
    pkg = Package(original)
    found = drawings(pkg, [str(i) for i in ids])
    fig = Figure(pkg)
    frames, descrs, frame_of = [], [], {}
    relative = set()
    for d in found:
        holder = d[0]
        ext = holder.find(WP + "extent")
        cx, cy = int(ext.get("cx")), int(ext.get("cy"))
        if holder.tag == WP + "anchor":
            ph, pv = holder.find(WP + "positionH"), holder.find(WP + "positionV")
            ox, oy = ph.find(WP + "posOffset"), pv.find(WP + "posOffset")
            if ox is None or oy is None:
                stop("a drawing placed by alignment rather than offset")
            relative.add((ph.get("relativeFrom"), pv.get("relativeFrom")))
            x0, y0 = int(ox.text), int(oy.text)
        elif len(found) == 1:
            x0 = y0 = 0
        else:
            stop("an inline drawing in a figure of several")
        eff = holder.find(WP + "effectExtent")
        e = {k: int(eff.get(k, "0")) if eff is not None else 0 for k in "ltrb"}
        frames.append((x0 - e["l"], y0 - e["t"], x0 + cx + e["r"], y0 + cy + e["b"]))
        frame_of[id(d)] = (x0, y0, cx, cy, int(holder.get("relativeHeight", "0")))
        data = holder.find("a:graphic/a:graphicData", NS)
        if data.get("uri") != NS["pic"]:
            descr = holder.find(WP + "docPr").get("descr", "")
            if descr:
                descrs.append(descr)
    if len(relative) > 1:
        stop("a figure whose drawings are placed from different frames")
    left, top = min(f[0] for f in frames), min(f[1] for f in frames)
    right, bottom = max(f[2] for f in frames), max(f[3] for f in frames)
    # Paint in Word's stacking order; the labels and pictures keep the
    # original's reading order in data-i.
    order = sorted(found, key=lambda d: frame_of[id(d)][4])
    reading = {id(d): i for i, d in enumerate(found)}
    chunks = {}
    for d in order:
        x0, y0, cx, cy, _ = frame_of[id(d)]
        data = d[0].find("a:graphic/a:graphicData", NS)
        start = len(fig.body)
        fig.drawing, fig.items = reading[id(d)], 0
        child = data[0]
        if child.tag == WPS + "wsp":
            sppr_xfrm = child.find(f"{WPS}spPr/a:xfrm", NS)
            off = sppr_xfrm.find("a:off", NS)
            frame = Frame(1.0, x0 - left - int(off.get("x")), 1.0, y0 - top - int(off.get("y")))
        elif child.tag == WPG + "wgp":
            frame = Frame(1.0, x0 - left, 1.0, y0 - top)
        elif child.tag == PIC + "pic":
            p_xfrm = child.find(f"{PIC}spPr/a:xfrm", NS)
            off, ext = p_xfrm.find("a:off", NS), p_xfrm.find("a:ext", NS)
            frame = Frame(cx / int(ext.get("cx")), x0 - left - int(off.get("x")),
                          cy / int(ext.get("cy")), y0 - top - int(off.get("y")))
        else:
            stop("the drawing " + child.tag.split("}")[1])
        if child.tag == WPG + "wgp":
            xfrm = child.find(f"{WPG}grpSpPr/a:xfrm", NS)
            ext = xfrm.find("a:ext", NS)
            if (int(ext.get("cx")), int(ext.get("cy"))) != (cx, cy):
                stop("a group whose size differs from its drawing's")
        fig.walk(child, frame)
    # The figure's box: Word's frames, and any label's ink beyond them.
    y0 = min(0.0, fig.ink[0] * EMU_PT) if fig.ink[0] < math.inf else 0.0
    y1 = max(bottom - top, fig.ink[1] * EMU_PT) if fig.ink[1] > -math.inf else bottom - top
    width, height = right - left, y1 - y0
    label = (' role="group" aria-label="{}"'.format(html.escape(" ".join(descrs)))
             if descrs else "")
    head = ('<svg xmlns="http://www.w3.org/2000/svg" class="drawn-figure" width="{}" height="{}"'
            ' viewBox="0 {} {} {}"{}>'.format(num(width / EMU_PX), num(height / EMU_PX),
                                               pt(y0), pt(width), pt(height), label))
    defs = "<defs>{}</defs>".format("".join(fig.defs)) if fig.defs else ""
    return head + defs + "".join(fig.body) + "</svg>\n", descrs


def png(svg_path, png_path, chrome, scale=2):
    """The SVG as PNG, drawn by headless Chrome at `scale` device pixels
    per CSS pixel, on a transparent ground (D-0117, call 3)."""
    text = pathlib.Path(svg_path).read_text(encoding="utf-8")
    m = re.match(r'<svg[^>]*\bwidth="([\d.]+)" height="([\d.]+)"', text)
    w, h = math.ceil(float(m.group(1))), math.ceil(float(m.group(2)))
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "figure.html"
        page.write_text('<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}'
                        'svg{display:block}</style></head><body>' + text + "</body></html>",
                        encoding="utf-8")
        out = pathlib.Path(tmp) / "figure.png"
        subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000",
                        "--force-device-scale-factor={}".format(scale),
                        "--window-size={},{}".format(w, h), "--screenshot=" + str(out), page.as_uri()],
                       check=True, capture_output=True, timeout=120)
        data = out.read_bytes()
    with open(png_path, "wb") as fh:
        fh.write(data)


def main(argv):
    original, out, *ids = argv
    text, _ = svg(original, ids)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote", out, len(text), "bytes")


if __name__ == "__main__":
    main(sys.argv[1:])
