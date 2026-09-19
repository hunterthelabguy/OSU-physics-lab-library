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
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
PANDOC = os.environ.get("PANDOC", "pandoc")
INLINE_CONTAINERS = {
    "Emph", "Underline", "Strikeout", "Superscript", "Subscript",
    "SmallCaps", "Span", "Link", "Image", "Cite",
}
HEADING_STYLE = re.compile(r"^(heading\s*\d|title|subtitle)$", re.I)

# Text is carried as a list of (character, bold) pairs. bold is True, False,
# or None (exempt: headings).


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
        if c.isspace():
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


def docx_chars(path):
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

    root = ET.fromstring(z.read("word/document.xml"))
    # Text boxes carry a fallback copy of themselves; read only the primary.
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == MC_FALLBACK:
                parent.remove(child)
    out = []
    for p in root.iter(W + "p"):
        ps = p.find(f"{W}pPr/{W}pStyle")
        pstyle = ps.get(W + "val") if ps is not None else default_para
        heading = bool(
            HEADING_STYLE.match(pstyle or "")
            or HEADING_STYLE.match(info.get(pstyle, {}).get("name", "")))
        para_bold = style_bold(pstyle)
        for r in p.iter(W + "r"):
            if heading:
                bold = None
            else:
                rs = r.find(f"{W}rPr/{W}rStyle")
                bold = on(r.find(f"{W}rPr/{W}b"))
                if bold is None and rs is not None:
                    bold = style_bold(rs.get(W + "val"))
                if bold is None:
                    bold = para_bold
                if bold is None:
                    bold = bool(doc_default)
            for el in r:
                if el.tag == W + "t":
                    out.extend((c, bold) for c in (el.text or ""))
                elif el.tag in (W + "tab", W + "br", W + "cr"):
                    out.append((" ", bold))
        out.append((" ", False))
    return out


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


def ast_chars(node, out, bold=False):
    """Collect (char, bold) from a Pandoc JSON node; attributes are skipped."""
    if isinstance(node, list):
        for n in node:
            ast_chars(n, out, bold)
        return
    if not isinstance(node, dict):
        return
    t, c = node.get("t"), node.get("c")
    if t == "Str":
        out.extend((ch, bold) for ch in c)
    elif t in ("Space", "SoftBreak", "LineBreak"):
        out.append((" ", bold))
    elif t in ("Code", "Math"):
        out.extend((ch, bold) for ch in c[1])
    elif t == "Quoted":
        q = "“”" if c[0]["t"] == "DoubleQuote" else "‘’"
        out.append((q[0], bold)); ast_chars(c[1], out, bold); out.append((q[1], bold))
    elif t == "Strong":
        ast_chars(c, out, True if bold is not None else None)
    elif t in INLINE_CONTAINERS:
        # Formatting runs join their neighbours: **Individually**, is one word.
        ast_chars(c, out, bold)
    elif t == "Header":
        out.append((" ", None)); ast_chars(c[2], out, None); out.append((" ", None))
    elif t == "CodeBlock":
        out.extend((ch, bold) for ch in " " + c[1] + " ")
    elif isinstance(c, (list, dict)):
        # Block-level node: its text is a separate run of words. Attributes
        # are lists of plain strings, which the walk ignores.
        out.append((" ", False))
        ast_chars(c, out, bold)
        out.append((" ", False))


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

    if src.lower().endswith(".docx"):
        original = tokens(docx_chars(src))
    elif src.lower().endswith(".xlsx"):
        original = tokens(xlsx_chars(src, meta["source_sheet"]))
    else:
        raise SystemExit(f"unsupported original type: {src}")
    buf = []
    ast_chars(doc["blocks"], buf)
    converted = tokens(buf)

    for key, side in (("ruled_omissions", "original"), ("ruled_additions", "converted")):
        for item in meta.get(key, []) or []:
            if not item.get("ledger"):
                problems.append(f"{key} entry lacks a ledger reference: {item.get('text')!r}")
            passage = [w for w, _ in tokens([(ch, False) for ch in item["text"]])]
            if side == "original":
                original, found = remove_passage(original, passage)
            else:
                converted, found = remove_passage(converted, passage)
            if not found:
                problems.append(f"{key} passage not found in {side}: {item['text']!r}")

    a = [w for w, _ in original]
    b = [w for w, _ in converted]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    compared = 0
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            ctx = " ".join(a[max(0, a0 - 6):a0])
            problems.append(
                f"{op} after ...{ctx!r}: original {' '.join(a[a0:a1])!r}"
                f" -> converted {' '.join(b[b0:b1])!r}")
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
    return len(a), compared, problems


def main(paths):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    failed = 0
    for p in paths:
        n, compared, problems = check(p, repo_root)
        if problems:
            failed += 1
            print(f"FAIL {p}")
            for line in problems:
                print("  " + line)
        else:
            print(f"ok   {p} ({n} words identical; bold identical on {compared}"
                  f" words outside headings)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
