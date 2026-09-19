"""Content-unchanged check: original Word or Excel file vs converted Markdown.

Usage: python tools/check_unchanged.py FILE.md [FILE.md ...]

For each Markdown file, reads `source_file` and `source_sha256` from its front
matter, verifies the original's hash, extracts the original's words directly
from the Office XML (independent of Pandoc), extracts the Markdown's words
from Pandoc's syntax tree, and compares the two word sequences. Formatting,
list markers, and block structure are not compared; words are.

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
    "Emph", "Strong", "Underline", "Strikeout", "Superscript", "Subscript",
    "SmallCaps", "Span", "Link", "Image", "Cite",
}


def words(text):
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return text.split()


def docx_text(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    # Text boxes carry a fallback copy of themselves; read only the primary.
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == MC_FALLBACK:
                parent.remove(child)
    out = []
    for p in root.iter(W + "p"):
        for el in p.iter():
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag in (W + "tab", W + "br", W + "cr"):
                out.append(" ")
        out.append(" ")
    return "".join(out)


def xlsx_text(path, sheet_name):
    z = zipfile.ZipFile(path)
    shared = [
        "".join(t.text or "" for t in si.iter(X + "t"))
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(X + "si")
    ]
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    names = [s.get("name") for s in wb.iter(X + "sheet")]
    if sheet_name not in names:
        raise SystemExit(f"sheet {sheet_name!r} not in {names}")
    # Sheets are stored in workbook order as sheet1.xml, sheet2.xml, ...
    sheet = ET.fromstring(z.read(f"xl/worksheets/sheet{names.index(sheet_name) + 1}.xml"))
    out = []
    for c in sheet.iter(X + "c"):
        v = c.find(X + "v")
        if c.get("t") == "s" and v is not None:
            out.append(shared[int(v.text)])
        elif c.get("t") == "inlineStr":
            out.append("".join(t.text or "" for t in c.iter(X + "t")))
        elif v is not None:
            out.append(v.text or "")
    return " ".join(out)


def ast_text(node, out):
    """Collect visible text from a Pandoc JSON node; attributes are skipped."""
    if isinstance(node, list):
        for n in node:
            ast_text(n, out)
        return
    if not isinstance(node, dict):
        return
    t, c = node.get("t"), node.get("c")
    if t == "Str":
        out.append(c)
    elif t in ("Space", "SoftBreak", "LineBreak"):
        out.append(" ")
    elif t in ("Code", "Math"):
        out.append(c[1])
    elif t == "Quoted":
        q = "“”" if c[0]["t"] == "DoubleQuote" else "‘’"
        out.append(q[0]); ast_text(c[1], out); out.append(q[1])
    elif t in INLINE_CONTAINERS:
        # Formatting runs join their neighbours: **Individually**, is one word.
        ast_text(c, out)
    elif t == "CodeBlock":
        out.append(" " + c[1] + " ")
    elif isinstance(c, (list, dict)):
        # Block-level node: its text is a separate run of words. Attributes
        # are lists of plain strings, which the walk ignores.
        out.append(" ")
        ast_text(c, out)
        out.append(" ")


def meta_value(m):
    t, c = m["t"], m.get("c")
    if t in ("MetaInlines", "MetaBlocks"):
        buf = []
        ast_text(c, buf)
        return " ".join(words("".join(buf)))
    if t == "MetaString":
        return c
    if t == "MetaList":
        return [meta_value(x) for x in c]
    if t == "MetaMap":
        return {k: meta_value(v) for k, v in c.items()}
    return c


def remove_passage(tokens, passage):
    """Remove the first occurrence of passage (a token list) from tokens."""
    n = len(passage)
    for i in range(len(tokens) - n + 1):
        if tokens[i:i + n] == passage:
            return tokens[:i] + tokens[i + n:], True
    return tokens, False


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
        original = words(docx_text(src))
    elif src.lower().endswith(".xlsx"):
        original = words(xlsx_text(src, meta["source_sheet"]))
    else:
        raise SystemExit(f"unsupported original type: {src}")
    buf = []
    ast_text(doc["blocks"], buf)
    converted = words("".join(buf))

    for key, side in (("ruled_omissions", "original"), ("ruled_additions", "converted")):
        for item in meta.get(key, []) or []:
            if not item.get("ledger"):
                problems.append(f"{key} entry lacks a ledger reference: {item.get('text')!r}")
            if side == "original":
                original, found = remove_passage(original, words(item["text"]))
            else:
                converted, found = remove_passage(converted, words(item["text"]))
            if not found:
                problems.append(f"{key} passage not found in {side}: {item['text']!r}")

    sm = difflib.SequenceMatcher(a=original, b=converted, autojunk=False)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            ctx = " ".join(original[max(0, a0 - 6):a0])
            problems.append(
                f"{op} after ...{ctx!r}: original {' '.join(original[a0:a1])!r}"
                f" -> converted {' '.join(converted[b0:b1])!r}")
    return len(original), problems


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
            print(f"ok   {p} ({n} words identical)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
