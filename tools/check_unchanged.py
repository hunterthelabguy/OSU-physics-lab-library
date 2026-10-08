"""Content-unchanged check: original Word or Excel file vs converted Markdown.

Usage: python tools/check_unchanged.py FILE.md [FILE.md ...]

For each Markdown file, reads `source_file` and `source_sha256` from its front
matter, verifies the original's hash, extracts the original's words directly
from the Office XML (independent of Pandoc), extracts the Markdown's words
from Pandoc's syntax tree, and compares:

1. the word sequences, exactly; and
2. the bold state of every word (bold, not bold, or partly bold). Bold carries
   meaning in this curriculum: a bold item is one students must answer in the
   graded report (library ledger 23). Headings are exempt on both sides,
   since a heading's weight is presentation, not the graded-item signal.
3. equations (D-0113): each Word equation (`m:oMath`) and each `Math` node
   takes one place in the word sequence, so count and position are compared
   there; then, in order, display against inline, and the equation's text and
   structure, the converted side's read back from the OMML that Pandoc's own
   Word writer makes of its TeX ("Equation rule" in docs/conversion-spec.md).
4. pictures (four-items call 4.3): each picture (a `pic:pic`, in a drawing of
   its own or inside a drawn figure) and each `Image` node takes one place in
   the word sequence; then, in order, Word's alt text (`descr`) against the
   image's alt text, word for word. A picture of its own is also its file: the
   Markdown names it in front matter `images:` (`file`, `source_part`,
   `sha256`), its bytes are the original's part byte for byte, and its
   `width` and `height` (inches) and `crop` (Word's `srcRect`, l t r b) are
   Word's (D-0118).
5. drawn figures (S13; D-0101, D-0117): an `Image` with class `drawn` names
   the original's drawings in `drawings` (their `wp:docPr` ids); its words,
   equations and pictures are read in place from the SVG that
   tools/figures.py makes of those drawings, and its alt text is Word's
   `descr` of each that is not a picture. Every drawing that is not a
   picture belongs to a figure, except a lone text box, whose words are
   read as words (D-0117, call 4). A figure's words are exempt from the
   bold compare, as headings are.

A SYMBOL field counts as the character Word displays, not its stored result
(survey section 6), and so does a text run set in the Symbol font (D-0123).
A text box's words are read once. A drawing anchored to a paragraph (`wp:anchor`) is read after that paragraph's words, where Word
shows it: all 23 in the 19 handouts sit at their paragraph's start and are
placed below its first lines (D-0118); an inline one is read in place.
Markdown is read as the build reads it, with implicit figures off, so a
lone image is not given its alt text as a visible caption (D-0118).
List markers, block structure, italics, and underline are not compared.

Differences are allowed only when declared in front matter and ruled in a
ledger:

    ruled_omissions:     # passages in the original, absent from the Markdown
      - text: "..."
        ledger: "instructor 4"
    ruled_additions:     # passages in the Markdown, absent from the original
      - text: "..."
        ledger: "library 20"

Each declared passage must actually occur, so a stale declaration fails too.
Requires Python 3.9+ and Pandoc on PATH (or in the PANDOC environment
variable). Exit code 0 when every file passes.
"""

import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
PIC = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"
PIC_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
WPS = "{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
PANDOC = os.environ.get("PANDOC", "pandoc")
# How every step reads a converted source (render.FROM, _quarto.yml's from):
# no smart quotes, and no implicit figures (D-0118).
FROM = "markdown-smart-implicit_figures"
# Word's size in inches to four places is within this many EMU of its extent.
SIZE_TOLERANCE = 46
INLINE_CONTAINERS = {
    "Emph", "Underline", "Strikeout", "Superscript", "Subscript",
    "SmallCaps", "Span", "Link", "Cite",
}
HEADING_STYLE = re.compile(r"^(heading\s*\d|title|subtitle)$", re.I)

# One word each in the sequence; private-use characters, so no text has them.
EQUATION, PICTURE = "\ue000", "\ue001"
SHOWN = {EQUATION: "[equation]", PICTURE: "[picture]"}

# The Symbol font's slots that a SYMBOL field or a Symbol-font text run in the
# originals uses, and the character Word displays for each. 87 (0x57, "W")
# draws as capital omega: Word's PDF of PH 213 Lab 5 prints it as Ω (survey
# sections 3 and 6). 174 (0xAE, typed as "®") draws as a right arrow: Word's
# PDF of PH 211 Lab 3 prints → in its appendix's steps (D-0123). A slot not
# listed here fails the check until someone reads what Word displays.
SYMBOL_FONT = {0x57: "\u03a9", 0xAE: "\u2192"}
SYMBOL_FIELD = re.compile(r'^\s*symbol\s+(0x[0-9a-f]+|\d+)\s+\\f\s+"?symbol"?(\s|$)', re.I)

# The equation comparison (D-0113): structure kinds counted, and the default
# characters OMML stores as attributes.
OMML_KINDS = ("f", "sSub", "sSup", "sSubSup", "sPre", "rad", "acc", "bar", "d",
              "nary", "limLow", "limUpp", "groupChr", "eqArr", "m", "box",
              "borderBox", "phant")
OMML_CHR = {"nary": "\u222b", "acc": "\u0302", "groupChr": "\u23df"}

# Text is carried as a list of (character, bold) pairs. bold is True, False,
# or None (exempt: headings, equations, pictures).


def tokens(chars):
    """Split (char, bold) pairs into (word, state) tokens.

    state is "B" (bold), "N" (not bold), "M" (partly bold), or None (exempt).
    Only letters and digits decide the state, so a plain comma after a bold
    word does not make it partly bold.
    """
    out, cur = [], []

    def flush():
        if not cur:
            return
        word = unicodedata.normalize("NFC", "".join(c for c, _ in cur))
        decisive = [b for c, b in cur if c.isalnum()] or [b for _, b in cur]
        if any(b is None for b in decisive):
            state = None
        elif all(decisive):
            state = "B"
        elif not any(decisive):
            state = "N"
        else:
            state = "M"
        out.append((word, state))
        cur.clear()

    for c, b in chars:
        # A zero-width space separates words without showing; Pandoc's Word
        # writer puts one after inline math.
        if c.isspace() or c == "\u200b":
            flush()
        else:
            cur.append((c, b))
    flush()
    return out


def on(el):
    """Value of an OOXML boolean property element, or None when absent."""
    if el is None:
        return None
    return el.get(W + "val", el.get("val", "true")).lower() not in ("0", "false", "off")


def placeholder(out, mark):
    out.extend(((" ", None), (mark, None), (" ", None)))


def math_norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u2206", "\u0394").replace("-", "\u2212")
    return "".join(c for c in s
                    if not c.isspace() and c not in "\u200b\u2061\u2062\u2063\u2064")


def math_text(el):
    """An equation's m:t text in order, with OMML's attribute characters."""
    tag = el.tag[len(M):] if el.tag.startswith(M) else None
    if tag == "t":
        return el.text or ""
    if tag == "d":
        pr = el.find(M + "dPr")

        def chr_(name, default):
            x = pr.find(M + name) if pr is not None else None
            return default if x is None else x.get(M + "val", "")
        parts = ["".join(math_text(c) for c in e) for e in el.findall(M + "e")]
        return chr_("begChr", "(") + chr_("sepChr", "|").join(parts) + chr_("endChr", ")")
    if tag in OMML_CHR:
        pr = el.find(M + tag + "Pr")
        x = pr.find(M + "chr") if pr is not None else None
        mark = OMML_CHR[tag] if x is None else x.get(M + "val", "")
        return mark + "".join(math_text(c) for c in el if c.tag != M + tag + "Pr")
    return "".join(math_text(c) for c in el)


def equation(om, kind):
    text = math_text(om)
    return {
        "kind": kind,
        "text": text,
        "norm": math_norm(text),
        "shape": tuple(sum(1 for _ in om.iter(M + k)) for k in OMML_KINDS),
    }


def without_fallbacks(xml_bytes):
    """Parse a part; drawings carry a fallback copy of themselves, dropped here."""
    root = ET.fromstring(xml_bytes)
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == MC_FALLBACK:
                parent.remove(child)
    return root


def omml_equations(xml_bytes):
    """Every top-level m:oMath of a document part, in order (for Pandoc's docx)."""
    root = without_fallbacks(xml_bytes)
    out = []

    def walk(el, display):
        for ch in el:
            if ch.tag == M + "oMath":
                out.append(equation(ch, "display" if display else "inline"))
            else:
                walk(ch, display or ch.tag == M + "oMathPara")
    walk(root, False)
    return out


def docx_content(path):
    """The original's (char, bold) pairs, equations, pictures and drawings.

    Each picture is {"descr", "part", "extent", "crop", "in_figure"}; each
    drawing that is not a picture is {"id", "descr", "lone_text_box"}.
    """
    with zipfile.ZipFile(path) as z:
        styles = ET.fromstring(z.read("word/styles.xml"))
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
        document = z.read("word/document.xml")
    info, default_para = {}, None
    for s in styles.iter(W + "style"):
        sid = s.get(W + "styleId")
        based = s.find(W + "basedOn")
        name = s.find(W + "name")
        info[sid] = {
            "based": based.get(W + "val") if based is not None else None,
            "bold": on(s.find(f"{W}rPr/{W}b")),
            "name": name.get(W + "val") if name is not None else sid,
        }
        if s.get(W + "type") == "paragraph" and s.get(W + "default") in ("1", "true"):
            default_para = sid
    doc_default = on(styles.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr/{W}b"))

    def style_bold(sid):
        seen = set()
        while sid and sid in info and sid not in seen:
            seen.add(sid)
            if info[sid]["bold"] is not None:
                return info[sid]["bold"]
            sid = info[sid]["based"]
        return None

    root = without_fallbacks(document)
    # The sinks text, equations and pictures go to; an anchored drawing is
    # read into sinks of its own and laid after its paragraph's words.
    sink = {"out": [], "equations": [], "pictures": []}
    drawings = []
    fields = []  # open complex fields: {"instr", "shown"}

    def blocks(el):
        """Paragraphs in document order, at any depth (tables, text boxes)."""
        for ch in el:
            if ch.tag == W + "p":
                paragraph(ch)
            else:
                blocks(ch)

    def picture(pic, extent, in_figure, drawing_id=None):
        doc_pr = pic.find(f"{PIC}nvPicPr/{PIC}cNvPr")
        blip = pic.find(f".//{A}blip")
        src = pic.find(f".//{A}srcRect")
        crop = tuple(int(src.get(k, "0")) for k in "ltrb") if src is not None else (0, 0, 0, 0)
        target = rels.get(blip.get(R + "embed")) if blip is not None else None
        sink["pictures"].append({
            "id": drawing_id,
            "descr": doc_pr.get("descr", "") if doc_pr is not None else "",
            "part": ("word/" + target) if target else None,
            "extent": extent,
            "crop": crop if any(crop) else None,
            "in_figure": in_figure,
        })
        placeholder(sink["out"], PICTURE)

    def figure_content(el):
        """A drawing that is not a picture: its pictures and text boxes, in
        the order the XML holds them."""
        for ch in el:
            if ch.tag == PIC + "pic":
                picture(ch, None, True)
            elif ch.tag == W + "txbxContent":
                blocks(ch)
            else:
                figure_content(ch)

    def drawing(el):
        holder = el[0]
        doc_pr = holder.find(WP + "docPr")
        data = el.find(f".//{A}graphicData")
        if data is not None and data.get("uri") == PIC_URI:
            ext = holder.find(WP + "extent")
            picture(data.find(PIC + "pic"), (int(ext.get("cx")), int(ext.get("cy"))), False,
                    doc_pr.get("id") if doc_pr is not None else None)
            return
        shapes = data.findall(WPS + "wsp") if data is not None else []
        drawings.append({
            "id": doc_pr.get("id") if doc_pr is not None else None,
            "descr": doc_pr.get("descr", "") if doc_pr is not None else "",
            "lone_text_box": len(shapes) == 1 and shapes[0].find(f"{WPS}txbx") is not None,
        })
        figure_content(el)

    def paragraph(p):
        ps = p.find(f"{W}pPr/{W}pStyle")
        pstyle = ps.get(W + "val") if ps is not None else default_para
        heading = bool(
            HEADING_STYLE.match(pstyle or "")
            or HEADING_STYLE.match(info.get(pstyle, {}).get("name", "")))
        para_bold = style_bold(pstyle)
        anchored = []

        def run_bold(r):
            if heading:
                return None
            rs = r.find(f"{W}rPr/{W}rStyle")
            bold = on(r.find(f"{W}rPr/{W}b"))
            if bold is None and rs is not None:
                bold = style_bold(rs.get(W + "val"))
            if bold is None:
                bold = para_bold
            if bold is None:
                bold = bool(doc_default)
            return bold

        def symbol_text(text):
            """A Symbol-font run's characters as Word draws them; a slot may be
            stored as the byte or in the private-use page U+F0xx."""
            out = []
            for c in text:
                code = ord(c) - 0xF000 if 0xF000 <= ord(c) <= 0xF0FF else ord(c)
                if c.isspace():
                    out.append(c)
                elif code in SYMBOL_FONT:
                    out.append(SYMBOL_FONT[code])
                else:
                    raise SystemExit(
                        f"{path}: Symbol-font character {code} is not in SYMBOL_FONT;"
                        " read what Word displays (D-0123)")
            return "".join(out)

        def run(r):
            bold = run_bold(r)
            rf = r.find(f"{W}rPr/{W}rFonts")
            symbol = rf is not None and "symbol" in (
                (rf.get(W + "ascii") or "").lower(), (rf.get(W + "hAnsi") or "").lower())
            for el in r:
                if el.tag == W + "fldChar":
                    kind = el.get(W + "fldCharType")
                    if kind == "begin":
                        fields.append({"instr": "", "shown": None})
                    elif kind == "separate" and fields:
                        m = SYMBOL_FIELD.match(fields[-1]["instr"])
                        if m:
                            code = int(m.group(1), 0)
                            if code not in SYMBOL_FONT:
                                raise SystemExit(
                                    f"{path}: SYMBOL field character {code} is not in"
                                    " SYMBOL_FONT; read what Word displays (survey section 6)")
                            fields[-1]["shown"] = SYMBOL_FONT[code]
                            sink["out"].append((fields[-1]["shown"], bold))
                    elif kind == "end" and fields:
                        fields.pop()
                elif el.tag == W + "instrText" and fields:
                    fields[-1]["instr"] += el.text or ""
                elif el.tag == W + "t":
                    if not any(f["shown"] for f in fields):
                        text = el.text or ""
                        if symbol:
                            text = symbol_text(text)
                        sink["out"].extend((c, bold) for c in text)
                elif el.tag in (W + "tab", W + "br", W + "cr"):
                    sink["out"].append((" ", bold))
                elif el.tag == W + "drawing":
                    if el[0].tag == WP + "anchor":
                        anchored.append(el)
                    else:
                        drawing(el)
                else:
                    for d in el.iter(W + "drawing"):
                        (anchored.append(d) if d[0].tag == WP + "anchor" else drawing(d))
                    if el.find(f".//{W}drawing") is None:
                        blocks(el)  # text boxes in other wrappers

        def inline(el):
            for ch in el:
                if ch.tag == W + "r":
                    run(ch)
                elif ch.tag == M + "oMathPara":
                    for om in ch.findall(M + "oMath"):
                        sink["equations"].append(equation(om, "display"))
                        placeholder(sink["out"], EQUATION)
                elif ch.tag == M + "oMath":
                    sink["equations"].append(equation(ch, "inline"))
                    placeholder(sink["out"], EQUATION)
                elif ch.tag == W + "p":
                    paragraph(ch)
                elif ch.tag != W + "pPr":
                    inline(ch)  # hyperlinks, content controls, simple fields

        inline(p)
        sink["out"].append((" ", False))
        for d in anchored:
            drawing(d)
            sink["out"].append((" ", False))

    blocks(root)
    return sink["out"], sink["equations"], sink["pictures"], drawings


def xlsx_chars(path, sheet_name):
    z = zipfile.ZipFile(path)
    st = ET.fromstring(z.read("xl/styles.xml"))
    font_bold = [bool(on(f.find(X + "b"))) for f in st.find(X + "fonts")]
    xf_font = [int(x.get("fontId", 0)) for x in st.find(X + "cellXfs")]
    shared = list(ET.fromstring(z.read("xl/sharedStrings.xml")).iter(X + "si"))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    names = [s.get("name") for s in wb.iter(X + "sheet")]
    if sheet_name not in names:
        raise SystemExit(f"sheet {sheet_name!r} not in {names}")
    # Sheets are stored in workbook order as sheet1.xml, sheet2.xml, ...
    sheet = ET.fromstring(z.read(f"xl/worksheets/sheet{names.index(sheet_name) + 1}.xml"))
    out = []
    for c in sheet.iter(X + "c"):
        cell_bold = font_bold[xf_font[int(c.get("s", 0))]]
        v = c.find(X + "v")
        if c.get("t") == "s" and v is not None:
            si = shared[int(v.text)]
            runs = si.findall(X + "r")
            if runs:
                for run in runs:
                    b = on(run.find(f"{X}rPr/{X}b"))
                    b = cell_bold if b is None else b
                    out.extend((ch, b) for ch in "".join(t.text or "" for t in run.iter(X + "t")))
            else:
                out.extend((ch, cell_bold) for ch in "".join(t.text or "" for t in si.iter(X + "t")))
        elif c.get("t") == "inlineStr":
            out.extend((ch, cell_bold) for ch in "".join(t.text or "" for t in c.iter(X + "t")))
        elif v is not None:
            out.extend((ch, cell_bold) for ch in (v.text or ""))
        out.append((" ", False))
    return out


def ast_chars(node, out, bold=False, found=None):
    """Collect (char, bold) from a Pandoc JSON node; attributes are skipped.

    found, when given, collects {"math": [(kind, tex)], "images": [{...}],
    "figures": [{...}]} and holds "figure", which reads a drawn figure's
    words, equations and pictures from its SVG (figure_tokens).
    """
    if isinstance(node, list):
        for n in node:
            ast_chars(n, out, bold, found)
        return
    if not isinstance(node, dict):
        return
    t, c = node.get("t"), node.get("c")
    if t == "Str":
        out.extend((ch, bold) for ch in c)
    elif t in ("Space", "SoftBreak", "LineBreak"):
        out.append((" ", bold))
    elif t == "Math":
        if found is not None:
            kind = "display" if c[0]["t"] == "DisplayMath" else "inline"
            found["math"].append((kind, c[1]))
        placeholder(out, EQUATION)
    elif t == "Image":
        if found is None:
            placeholder(out, PICTURE)
            return
        (_, classes, attrs), alt_inlines, (target, _) = c
        alt = []
        ast_chars(alt_inlines, alt)
        alt = " ".join(w for w, _ in tokens(alt))
        attrs = dict(attrs)
        if "drawn" not in classes:
            found["images"].append({"alt": alt, "src": target, "attrs": attrs, "figure": False})
            placeholder(out, PICTURE)
            return
        ids = attrs.get("drawings", "").split()
        found["figures"].append({"alt": alt, "ids": ids, "src": target})
        for kind, value in found["figure"](ids):
            if kind == "text":
                out.extend((ch, None) for ch in value)
            elif kind == "math":
                found["math"].append(("figure", value))
                placeholder(out, EQUATION)
            else:
                found["images"].append({"alt": value, "figure": True})
                placeholder(out, PICTURE)
    elif t == "Code":
        out.extend((ch, bold) for ch in c[1])
    elif t == "Quoted":
        q = "“”" if c[0]["t"] == "DoubleQuote" else "‘’"
        out.append((q[0], bold)); ast_chars(c[1], out, bold, found); out.append((q[1], bold))
    elif t == "Strong":
        ast_chars(c, out, True if bold is not None else None, found)
    elif t in INLINE_CONTAINERS:
        # Formatting runs join their neighbours: **Individually**, is one word.
        ast_chars(c, out, bold, found)
    elif t == "Header":
        out.append((" ", None)); ast_chars(c[2], out, None, found); out.append((" ", None))
    elif t == "Figure":
        # The page shows the image, then its caption, as Word does.
        out.append((" ", False))
        ast_chars(c[2], out, bold, found)
        ast_chars(c[1], out, bold, found)
        out.append((" ", False))
    elif t == "CodeBlock":
        out.extend((ch, bold) for ch in " " + c[1] + " ")
    elif isinstance(c, (list, dict)):
        # Block-level node: its text is a separate run of words. Attributes
        # are lists of plain strings, which the walk ignores.
        out.append((" ", False))
        ast_chars(c, out, bold, found)
        out.append((" ", False))


def tex_equations(math, api_version):
    """Pandoc's Word writer's OMML for each (kind, tex), read back in order."""
    if not math:
        return []
    kinds = {"display": "DisplayMath", "inline": "InlineMath"}
    doc = {"pandoc-api-version": api_version, "meta": {}, "blocks": [
        {"t": "Para", "c": [{"t": "Math", "c": [{"t": kinds[k]}, tex]}]} for k, tex in math]}
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "equations.docx")
        subprocess.run([PANDOC, "-f", "json", "-t", "docx", "-o", out],
                       input=json.dumps(doc), check=True, capture_output=True,
                       encoding="utf-8")
        with zipfile.ZipFile(out) as z:
            back = omml_equations(z.read("word/document.xml"))
    for eq, (kind, tex) in zip(back, math):
        eq["kind"], eq["tex"] = kind, tex
    return back


def svg_equation(node):
    """A figure's equation, drawn by tools/figures.py as tspans that mirror
    its OMML, as the record compare_equations reads."""
    text = "".join(node.itertext())
    return {"kind": node.get("data-kind", "inline"), "text": text, "norm": math_norm(text),
            "shape": tuple(sum(1 for el in node.iter() if el.get("data-omml") == k) for k in OMML_KINDS),
            "tex": "(figure) " + text}


def figure_tokens(svg_text):
    """A drawn figure's labels and pictures in the original's reading order
    (data-i): ("text", str), ("math", record) and ("picture", alt)."""
    root = ET.fromstring(svg_text)
    items = sorted((el for el in root.iter() if el.get("data-i")),
                   key=lambda el: tuple(int(x) for x in el.get("data-i").split(".")))
    out = []

    def walk(node, top):
        if node.get("class") == "figure-math":
            out.append(("math", svg_equation(node)))
        else:
            if node.text:
                out.append(("text", node.text))
            for child in node:
                walk(child, False)
        if node.tail and not top:
            out.append(("text", node.tail))

    for el in items:
        if el.get("class") == "figure-picture":
            out.append(("picture", el.get("data-alt", "")))
            continue
        for line in el:
            out.append(("text", " "))
            walk(line, True)
        out.append(("text", " "))
    return out


def meta_value(m):
    t, c = m["t"], m.get("c")
    if t in ("MetaInlines", "MetaBlocks"):
        buf = []
        ast_chars(c, buf)
        return " ".join(w for w, _ in tokens(buf))
    if t == "MetaString":
        return c
    if t == "MetaList":
        return [meta_value(x) for x in c]
    if t == "MetaMap":
        return {k: meta_value(v) for k, v in c.items()}
    return c


def remove_passage(toks, passage):
    """Remove the first occurrence of passage (a word list) from toks."""
    n = len(passage)
    ws = [w for w, _ in toks]
    for i in range(len(ws) - n + 1):
        if ws[i:i + n] == passage:
            return toks[:i] + toks[i + n:], True
    return toks, False


STATE_NAME = {"B": "bold", "N": "not bold", "M": "partly bold"}


def shown(words):
    return " ".join(SHOWN.get(w, w) for w in words)


def compare_equations(original, converted):
    problems = []
    if len(original) != len(converted):
        problems.append(f"equations: original {len(original)}, converted {len(converted)}")
    for i, (o, c) in enumerate(zip(original, converted), 1):
        if o["kind"] != c["kind"]:
            problems.append(f"equation {i}: original {o['kind']}, converted {c['kind']}"
                            f" ({c['tex']!r})")
        if o["norm"] != c["norm"]:
            problems.append(f"equation {i}: original text {o['text']!r},"
                            f" converted {c['tex']!r} reads {c['text']!r}")
        elif o["shape"] != c["shape"]:
            diff = ", ".join(f"{k} {a}->{b}" for k, a, b in
                             zip(OMML_KINDS, o["shape"], c["shape"]) if a != b)
            problems.append(f"equation {i}: structure differs ({diff}) in {c['tex']!r}")
    return problems


def same_words(a, b):
    split = lambda s: [w for w, _ in tokens([(ch, False) for ch in s])]
    return split(a) == split(b)


def compare_pictures(original, converted, entries, md_dir, package, figures):
    """Alt text for every picture; for a picture of its own, its file, its
    front matter entry and Word's size and crop (D-0118)."""
    problems = []
    if len(original) != len(converted):
        problems.append(f"pictures: original {len(original)}, converted {len(converted)}")
    # A picture a figure lists among its drawings is drawn in that figure
    # (PH 212 Lab 3's screenshots under their arrows, D-0117 call 4).
    in_figures = {d for f in figures for d in f["ids"]}
    by_file = {e.get("file"): e for e in entries}
    used = set()
    for i, (o, c) in enumerate(zip(original, converted), 1):
        if not same_words(o["descr"], c["alt"]):
            problems.append(f"picture {i}: alt text {c['alt']!r}, Word's is {o['descr']!r}")
        o_figure = o["in_figure"] or o["id"] in in_figures
        if o_figure != c["figure"]:
            where = "inside a drawn figure" if o_figure else "a picture of its own"
            problems.append(f"picture {i}: Word's is {where}")
            continue
        if c["figure"]:
            continue
        entry = by_file.get(c["src"])
        if entry is None:
            problems.append(f"picture {i}: {c['src']!r} is not listed in front matter images")
            continue
        used.add(c["src"])
        path = os.path.join(md_dir, c["src"])
        data = open(path, "rb").read() if os.path.isfile(path) else None
        if data is None:
            problems.append(f"picture {i}: no file {c['src']!r}")
        elif hashlib.sha256(data).hexdigest() != entry.get("sha256"):
            problems.append(f"picture {i}: {c['src']!r} does not hash to its sha256")
        if entry.get("source_part") != o["part"]:
            problems.append(f"picture {i}: source_part {entry.get('source_part')!r}, Word's is {o['part']!r}")
        elif data is not None and data != package.read(o["part"]):
            problems.append(f"picture {i}: {c['src']!r} is not {o['part']} byte for byte")
        for axis, emu in zip(("width", "height"), o["extent"]):
            value = c["attrs"].get(axis, "")
            if not value.endswith("in"):
                problems.append(f"picture {i}: {axis} {value!r}, Word's is {emu / 914400:.4f}in")
            elif abs(float(value[:-2]) * 914400 - emu) > SIZE_TOLERANCE:
                problems.append(f"picture {i}: {axis} {value}, Word's is {emu / 914400:.4f}in")
        crop = c["attrs"].get("crop")
        want = " ".join(str(v) for v in o["crop"]) if o["crop"] else None
        if crop != want:
            problems.append(f"picture {i}: crop {crop!r}, Word's is {want!r}")
    for e in entries:
        if e.get("file") not in used:
            problems.append(f"front matter images lists {e.get('file')!r}, which no picture shows")
    return problems


def compare_figures(drawings, figures, descrs):
    """Every drawing that is not a picture is in one figure, or is a lone
    text box; a figure's alt text is Word's descr of its drawings."""
    problems = []
    listed = {}
    for k, f in enumerate(figures, 1):
        for d in f["ids"]:
            if d in listed:
                problems.append(f"drawing {d} is in figures {listed[d]} and {k}")
            listed[d] = k
        want = " ".join(descrs.get(k, []))
        if not same_words(want, f["alt"]):
            problems.append(f"figure {k}: alt text {f['alt']!r}, Word's is {want!r}")
    for d in drawings:
        if d["id"] not in listed and not d["lone_text_box"]:
            problems.append(f"drawing {d['id']} ({d['descr']!r}) is in no figure (S13)")
    return problems


def check(md_path, repo_root):
    doc = json.loads(subprocess.run(
        [PANDOC, "-f", FROM, "-t", "json", md_path],
        capture_output=True, check=True, encoding="utf-8").stdout)
    meta = {k: meta_value(v) for k, v in doc["meta"].items()}
    problems = []

    src = os.path.join(repo_root, meta["source_file"])
    digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if digest != meta.get("source_sha256"):
        problems.append(f"source_sha256 mismatch: file is {digest}")

    o_eqs, o_pics, o_drawings = [], [], []
    if src.lower().endswith(".docx"):
        chars, o_eqs, o_pics, o_drawings = docx_content(src)
        original = tokens(chars)
    elif src.lower().endswith(".xlsx"):
        original = tokens(xlsx_chars(src, meta["source_sheet"]))
    else:
        raise SystemExit(f"unsupported original type: {src}")
    descrs = {}

    def figure(ids):
        """Make the figure's SVG as the build does and read it back."""
        import figures
        try:
            text, alts = figures.svg(src, ids)
        except SystemExit as e:
            problems.append(f"figure {ids}: {e}")
            return []
        descrs[len(found["figures"])] = alts
        return figure_tokens(text)

    buf, found = [], {"math": [], "images": [], "figures": [], "figure": figure}
    ast_chars(doc["blocks"], buf, found=found)
    converted = tokens(buf)

    for key, side in (("ruled_omissions", "original"), ("ruled_additions", "converted")):
        for item in meta.get(key, []) or []:
            if not item.get("ledger"):
                problems.append(f"{key} entry lacks a ledger reference: {item.get('text')!r}")
            passage = [w for w, _ in tokens([(ch, False) for ch in item["text"]])]
            if side == "original":
                original, found_ = remove_passage(original, passage)
            else:
                converted, found_ = remove_passage(converted, passage)
            if not found_:
                problems.append(f"{key} passage not found in {side}: {item['text']!r}")

    a = [w for w, _ in original]
    b = [w for w, _ in converted]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    compared = 0
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            ctx = shown(a[max(0, a0 - 6):a0])
            problems.append(
                f"{op} after ...{ctx!r}: original {shown(a[a0:a1])!r}"
                f" -> converted {shown(b[b0:b1])!r}")
            continue
        run = None  # (start index, original state, converted state)
        for i, j in zip(range(a0, a1 + 1), range(b0, b1 + 1)):
            pair = None
            if i < a1:
                sa, sb = original[i][1], converted[j][1]
                if sa is not None and sb is not None:
                    compared += 1
                    if sa != sb:
                        pair = (sa, sb)
            if run and (pair is None or pair != run[1:]):
                words_ = " ".join(a[run[0]:i])
                problems.append(
                    f"bold differs on {words_!r}: original {STATE_NAME[run[1]]},"
                    f" converted {STATE_NAME[run[2]]}")
                run = None
            if pair and not run:
                run = (i, *pair)

    back = iter(tex_equations([m for m in found["math"] if m[0] != "figure"], doc["pandoc-api-version"]))
    c_eqs = [m[1] if m[0] == "figure" else next(back) for m in found["math"]]
    problems += compare_equations(o_eqs, c_eqs)
    if src.lower().endswith(".docx"):
        with zipfile.ZipFile(src) as package:
            problems += compare_pictures(o_pics, found["images"], meta.get("images") or [],
                                         os.path.dirname(os.path.abspath(md_path)), package,
                                         found["figures"])
        problems += compare_figures(o_drawings, found["figures"], descrs)
    words = sum(1 for w in a if w not in SHOWN)
    return {"words": words, "bold": compared, "equations": len(o_eqs),
            "pictures": len(o_pics), "figures": len(found["figures"])}, problems


def main(paths):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    failed = 0
    for p in paths:
        n, problems = check(p, repo_root)
        if problems:
            failed += 1
            print(f"FAIL {p}")
            for line in problems:
                print("  " + line)
        else:
            print(f"ok   {p} ({n['words']} words identical; bold identical on"
                  f" {n['bold']} words outside headings; {n['equations']} equations,"
                  f" {n['pictures']} pictures and {n['figures']} drawn figures identical)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
