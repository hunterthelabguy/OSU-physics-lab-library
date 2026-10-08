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
4. pictures (four-items call 4.3): each picture (`w:drawing` holding a
   `pic:pic`) and each `Image` node takes one place in the word sequence; then,
   in order, Word's alt text (`wp:docPr descr`) against the image's alt text,
   word for word.

A SYMBOL field counts as the character Word displays, not its stored result
(survey section 6). A text box's words are read once, where it is anchored.
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
PIC_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
PANDOC = os.environ.get("PANDOC", "pandoc")
INLINE_CONTAINERS = {
    "Emph", "Underline", "Strikeout", "Superscript", "Subscript",
    "SmallCaps", "Span", "Link", "Cite",
}
HEADING_STYLE = re.compile(r"^(heading\s*\d|title|subtitle)$", re.I)

# One word each in the sequence; private-use characters, so no text has them.
EQUATION, PICTURE = "\ue000", "\ue001"
SHOWN = {EQUATION: "[equation]", PICTURE: "[picture]"}

# The Symbol font's slots that a SYMBOL field in the originals uses, and the
# character Word displays for each. 87 (0x57, "W") draws as capital omega:
# Word's PDF of PH 213 Lab 5 prints it as Ω (survey sections 3 and 6). A slot
# not listed here fails the check until someone reads what Word displays.
SYMBOL_FONT = {0x57: "\u03a9"}
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
    """The original's (char, bold) pairs, equations and pictures' alt text."""
    z = zipfile.ZipFile(path)
    styles = ET.fromstring(z.read("word/styles.xml"))
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

    root = without_fallbacks(z.read("word/document.xml"))
    out, equations, pictures = [], [], []
    fields = []  # open complex fields: {"instr", "shown"}

    def blocks(el):
        """Paragraphs in document order, at any depth (tables, text boxes)."""
        for ch in el:
            if ch.tag == W + "p":
                paragraph(ch)
            else:
                blocks(ch)

    def paragraph(p):
        ps = p.find(f"{W}pPr/{W}pStyle")
        pstyle = ps.get(W + "val") if ps is not None else default_para
        heading = bool(
            HEADING_STYLE.match(pstyle or "")
            or HEADING_STYLE.match(info.get(pstyle, {}).get("name", "")))
        para_bold = style_bold(pstyle)

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

        def run(r):
            bold = run_bold(r)
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
                            out.append((fields[-1]["shown"], bold))
                    elif kind == "end" and fields:
                        fields.pop()
                elif el.tag == W + "instrText" and fields:
                    fields[-1]["instr"] += el.text or ""
                elif el.tag == W + "t":
                    if not any(f["shown"] for f in fields):
                        out.extend((c, bold) for c in (el.text or ""))
                elif el.tag in (W + "tab", W + "br", W + "cr"):
                    out.append((" ", bold))
                elif el.tag == W + "drawing":
                    data = el.find(f".//{A}graphicData")
                    if data is not None and data.get("uri") == PIC_URI:
                        doc_pr = el.find(f".//{WP}docPr")
                        pictures.append(doc_pr.get("descr", "") if doc_pr is not None else "")
                        placeholder(out, PICTURE)
                    else:
                        blocks(el)  # shapes and groups: their text boxes
                else:
                    blocks(el)  # text boxes in other wrappers

        def inline(el):
            for ch in el:
                if ch.tag == W + "r":
                    run(ch)
                elif ch.tag == M + "oMathPara":
                    for om in ch.findall(M + "oMath"):
                        equations.append(equation(om, "display"))
                        placeholder(out, EQUATION)
                elif ch.tag == M + "oMath":
                    equations.append(equation(ch, "inline"))
                    placeholder(out, EQUATION)
                elif ch.tag == W + "p":
                    paragraph(ch)
                elif ch.tag != W + "pPr":
                    inline(ch)  # hyperlinks, content controls, simple fields

        inline(p)
        out.append((" ", False))

    blocks(root)
    return out, equations, pictures


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

    found, when given, collects {"math": [(kind, tex)], "images": [alt]}.
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
        if found is not None:
            alt = []
            ast_chars(c[1], alt)
            found["images"].append(" ".join(w for w, _ in tokens(alt)))
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
        back = omml_equations(zipfile.ZipFile(out).read("word/document.xml"))
    for eq, (kind, tex) in zip(back, math):
        eq["kind"], eq["tex"] = kind, tex
    return back


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


def compare_pictures(original, converted):
    problems = []
    if len(original) != len(converted):
        problems.append(f"pictures: original {len(original)}, converted {len(converted)}")
    for i, (o, c) in enumerate(zip(original, converted), 1):
        if [w for w, _ in tokens([(ch, False) for ch in o])] != c.split():
            problems.append(f"picture {i}: alt text {c!r}, Word's is {o!r}")
    return problems


def check(md_path, repo_root):
    doc = json.loads(subprocess.run(
        [PANDOC, "-f", "markdown-smart", "-t", "json", md_path],
        capture_output=True, check=True, encoding="utf-8").stdout)
    meta = {k: meta_value(v) for k, v in doc["meta"].items()}
    problems = []

    src = os.path.join(repo_root, meta["source_file"])
    digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if digest != meta.get("source_sha256"):
        problems.append(f"source_sha256 mismatch: file is {digest}")

    o_eqs, o_pics = [], []
    if src.lower().endswith(".docx"):
        chars, o_eqs, o_pics = docx_content(src)
        original = tokens(chars)
    elif src.lower().endswith(".xlsx"):
        original = tokens(xlsx_chars(src, meta["source_sheet"]))
    else:
        raise SystemExit(f"unsupported original type: {src}")
    buf, found = [], {"math": [], "images": []}
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

    problems += compare_equations(o_eqs, tex_equations(found["math"], doc["pandoc-api-version"]))
    problems += compare_pictures(o_pics, found["images"])
    words = sum(1 for w in a if w not in SHOWN)
    return {"words": words, "bold": compared, "equations": len(o_eqs),
            "pictures": len(o_pics)}, problems


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
                  f" {n['bold']} words outside headings; {n['equations']} equations"
                  f" and {n['pictures']} pictures identical)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
