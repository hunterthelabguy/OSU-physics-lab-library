"""Number check: a converted lab's numbers against Word's own labels.

Usage: python tools/check_numbers.py FILE.md [FILE.md ...]

Word's displayed labels for every anchored paragraph of the originals'
question lists were read once through Word's automation and recorded in
docs/word-labels.json (D-0102). For each Markdown file this finds the record
whose `parts_sha256` equals the SHA-256 of its original's document, numbering
and styles parts, which D-0086's strip leaves unchanged (D-0112, call 1); no
match fails. It then renders the file through tools/filters/questions.lua and
reads, in document order, the labels students see:

- a question block's "Question N", against Word's "N)" at that anchor;
- a checkpoint block (D-0110), where Word shows a number that is not a
  question's: a checkpoint is required there and no number is compared
  (D-0112, call 3);
- each part, an item of an ordered list directly inside the block or nested
  in such an item, its marker ("a.", "i.") from the list's own numbering,
  against Word's label at the part's anchor and level.

- an `xN` anchor (a numbered paragraph in a second list, D-0122): matched in
  document order with the rest; it records no level, so its label alone is
  compared, with a part's marker or with an item of the ordered list inside
  a `::: report-item` (S11), which the check reads in place;
- a `::: {.numbered anchors="..."}` list: a list Word numbers from its
  question list outside any question (PH 211 Lab 3's appendix contents);
  its markers, in order, against Word's labels at the anchors it names.

An anchor no rule places fails. Exit code 0 when every file passes.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

PANDOC = os.environ.get("PANDOC", "pandoc")
# How every step reads a source (render.FROM; tested to agree).
FROM = "markdown-smart-implicit_figures"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILTER = os.path.join(ROOT, "tools", "filters", "questions.lua")
LABELS = os.path.join(ROOT, "docs", "word-labels.json")
PARTS = ("word/document.xml", "word/numbering.xml", "word/styles.xml")
TOP = re.compile(r"^(\d+)\)$")


def parts_sha256(path):
    z = zipfile.ZipFile(path)
    return {p: hashlib.sha256(z.read(p)).hexdigest() for p in PARTS}


def roman(n):
    out = ""
    for value, digits in ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
                          (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
                          (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")):
        while n >= value:
            out, n = out + digits, n - value
    return out


def letters(n):
    out = ""
    while n:
        n, r = divmod(n - 1, 26)
        out = chr(ord("a") + r) + out
    return out


def marker(n, style, delim):
    """The marker an ordered list shows for item n, as Word writes its labels."""
    text = {
        "LowerAlpha": letters(n), "UpperAlpha": letters(n).upper(),
        "LowerRoman": roman(n), "UpperRoman": roman(n).upper(),
    }.get(style, str(n))
    if delim == "OneParen":
        return text + ")"
    if delim == "TwoParens":
        return "(" + text + ")"
    return text + "."


def plain(node):
    if isinstance(node, list):
        return "".join(plain(n) for n in node)
    if isinstance(node, dict):
        if node.get("t") == "Str":
            return node["c"]
        if node.get("t") == "Space":
            return " "
        return plain(node.get("c"))
    return ""


def rendered_items(md_path):
    """[(level, kind, label, id)] in document order, as the filter labels them.
    A report item's list items are kind "report" (level None); a `.numbered`
    list's are kind "numbered", their id the anchor named for them, or None
    past the last one named."""
    doc = json.loads(subprocess.run(
        [PANDOC, md_path, "-f", FROM, "-t", "json",
         "--lua-filter", FILTER, "-M", "theme-name=modern"],
        capture_output=True, check=True, encoding="utf-8").stdout)
    items = []

    def parts(blocks, level):
        for b in blocks:
            if b["t"] == "OrderedList":
                (start, style, delim), entries = b["c"]
                for k, entry in enumerate(entries):
                    items.append((level, "part",
                                  marker(start + k, style["t"], delim["t"]), None))
                    parts(entry, level + 1)

    def listed(blocks, kind, anchors):
        for b in blocks:
            if b["t"] == "OrderedList":
                (start, style, delim), entries = b["c"]
                for k, entry in enumerate(entries):
                    anchor = anchors.pop(0) if anchors else None
                    items.append((None, kind, marker(start + k, style["t"], delim["t"]), anchor))
                    listed(entry, kind, anchors)
            elif b["t"] == "Div":
                listed(b["c"][1], kind, anchors)

    def walk(blocks):
        for b in blocks:
            if b["t"] != "Div":
                continue
            (ident, classes, attrs), content = b["c"]
            if "report-item" in classes:
                listed(content, "report", [])
                continue
            if "numbered" in classes:
                anchors = dict(attrs).get("anchors", "").split()
                listed(content, "numbered", anchors)
                for anchor in anchors:
                    items.append((None, "numbered", None, anchor))
                continue
            kind = next((k for k in ("question", "checkpoint") if k in classes), None)
            if kind is None:
                walk(content)
                continue
            items.append((0, kind, plain(content[0]), ident))
            parts(content[1:], 1)

    walk(doc["blocks"])
    return items


def compare(word, items):
    """Problems between Word's [(anchor, label)] and the rendered items."""
    problems = []
    labels = dict(word)
    named = set()
    for _, kind, shown, anchor in items:
        if kind != "numbered":
            continue
        if anchor is None:
            problems.append(f"a .numbered list item {shown!r} has no anchor named for it")
        elif anchor not in labels:
            problems.append(f".numbered names {anchor}, which Word's labels do not have")
        elif shown is None:
            problems.append(f".numbered names {anchor} ({labels[anchor]!r}), but its list ends first")
        elif shown != labels[anchor]:
            problems.append(f"{anchor} (Word {labels[anchor]!r}, converted {shown!r}): .numbered label differs")
        named.add(anchor)
    items = [i for i in items if i[1] != "numbered"]
    for anchor, label in word:
        if anchor[0] not in "ox":
            problems.append(f"anchor {anchor} ({label!r}): no rule places it (D-0112, D-0122)")
    word = [(a, l) for a, l in word if a[0] in "ox" and a not in named]
    if len(word) != len(items):
        problems.append(f"Word has {len(word)} numbered paragraphs to place, the"
                        f" converted lab {len(items)}; Word's from"
                        f" {word[len(items)][0]} on are unmatched"
                        if len(word) > len(items) else
                        f"Word has {len(word)} numbered paragraphs to place, the"
                        f" converted lab {len(items)}")
    for (anchor, label), (level, kind, shown, ident) in zip(word, items):
        where = f"{anchor} (Word {label!r}, converted {shown!r}"
        where += f", #{ident})" if ident else ")"
        if anchor.startswith("x"):
            # A second list's paragraph records no level (D-0122).
            if kind not in ("part", "report"):
                problems.append(f"{where}: Word's {anchor} is a second list's item,"
                                f" converted as a {kind}")
            elif shown != label:
                problems.append(f"{where}: label differs")
            continue
        if kind == "report":
            problems.append(f"{where}: a report item's list where Word's question list numbers")
            continue
        if anchor.count(".") != level:
            problems.append(f"{where}: Word's level {anchor.count('.')},"
                            f" converted level {level}")
            continue
        if kind == "part":
            if shown != label:
                problems.append(f"{where}: part label differs")
        elif kind == "question":
            m = TOP.match(label)
            if not m:
                problems.append(f"{where}: Word's label is not \"N)\"")
            elif shown != f"Question {int(m.group(1))}":
                problems.append(f"{where}: question number differs")
        elif not re.match(r"^Checkpoint \d+$", shown):
            problems.append(f"{where}: checkpoint label")
    return problems


def check(md_path, repo_root=ROOT, labels=None):
    if labels is None:
        with open(LABELS, encoding="utf-8") as fh:
            labels = json.load(fh)
    doc = json.loads(subprocess.run(
        [PANDOC, md_path, "-f", FROM, "-t", "json"],
        capture_output=True, check=True, encoding="utf-8").stdout)
    meta = doc["meta"]["source_file"]
    source = meta["c"] if meta["t"] == "MetaString" else plain(meta["c"])
    hashes = parts_sha256(os.path.join(repo_root, source))
    record = next((r for r in labels["originals"].values()
                   if r.get("parts_sha256") == hashes), None)
    if record is None:
        return None, [f"no record in docs/word-labels.json has this original's"
                      f" parts ({', '.join(PARTS)}); read Word's labels again (D-0102)"]
    items = rendered_items(md_path)
    return items, compare(record["labels"], items)


def main(paths):
    failed = 0
    for p in paths:
        items, problems = check(p)
        if problems:
            failed += 1
            print(f"FAIL {p}")
            for line in problems:
                print("  " + line)
        else:
            count = {k: sum(1 for i in items if i[1] == k)
                     for k in ("question", "checkpoint", "part")}
            print(f"ok   {p} (Word's labels on {count['question']} questions,"
                  f" {count['checkpoint']} checkpoints and {count['part']} parts)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
