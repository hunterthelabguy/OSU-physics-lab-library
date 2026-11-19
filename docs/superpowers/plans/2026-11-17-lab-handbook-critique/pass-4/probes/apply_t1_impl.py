"""Apply T1's implementation steps (plan blocks 07, 08, 09/10, 11 and the
prose edits of plan lines 239 to 272), as written in revision 2.3.

Run from the scratch tree's root: python -X utf8 apply_t1_impl.py BLOCKS
Where the plan says "rewrap", a paragraph is refilled to the widest line it
had before the edit (revision 2.3's rule), with "PH 211" and "D-0198" kept
whole (no break on hyphens; a space in "PH 211" is protected).
"""
import sys
import textwrap
from pathlib import Path

B = Path(sys.argv[1])
NBSP = " "


def block(n, ext="python"):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


def norm(s):
    return " ".join(s.split())


def wrap(words, width, first="", rest=""):
    words = words.replace("PH 211", "PH" + NBSP + "211")
    out = textwrap.wrap(words, width=width, initial_indent=first, subsequent_indent=rest,
                        break_long_words=False, break_on_hyphens=False)
    return [ln.replace(NBSP, " ") for ln in out]


def paragraph(lines, contains, prefix=""):
    """(start, end) of the blank-line delimited paragraph whose lines start
    with `prefix` and whose text, whitespace normalised, contains `contains`."""
    paras, cur = [], []
    for i, ln in enumerate(lines):
        inside = ln.startswith(prefix) and ln[len(prefix):].strip() and ln.strip() != '"""'
        if inside:
            cur.append(i)
        elif cur:
            paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    hits = [p for p in paras if contains in norm(" ".join(lines[i][len(prefix):] for i in p))]
    assert len(hits) == 1, (contains, len(hits))
    return hits[0][0], hits[0][-1] + 1


def replace_in_paragraph(text, old, new, prefix="", anchor=None):
    """Replace `old` (whitespace normalised) in its paragraph and refill the
    paragraph to its own widest line before the edit."""
    lines = text.split("\n")
    a, b = paragraph(lines, anchor or old, prefix)
    width = max(len(ln) for ln in lines[a:b])
    words = norm(" ".join(ln[len(prefix):] for ln in lines[a:b]))
    assert words.count(old) == 1, (old, words)
    words = words.replace(old, new)
    lines[a:b] = wrap(words, width, prefix, prefix)
    return "\n".join(lines), width


# --- tools/check_unchanged.py
p = Path("tools/check_unchanged.py")
t = p.read_text(encoding="utf-8")
fr = 'FROM = "markdown-smart-implicit_figures"\n'
t = once(t, fr, fr + block(7).rstrip("\n") + "\n\n\n", "FROM")
t = once(t, "    for p in paths:\n        n, problems = check(p, repo_root)\n",
         block(8).rstrip("\n") + "\n        n, problems = check(p, repo_root)\n", "cu main")
old = "Differences are allowed only when declared in front matter and ruled in a\nledger:"
new_par = ("A file whose `status` is `ruled-change` is skipped with a printed reason: from a "
           "handout's first ruled change its own Markdown is the baseline (D-0195). The "
           "declarations below are for conversions only.")
# A new paragraph, no width named: the width of the paragraph it precedes.
t = once(t, old, "\n".join(wrap(new_par, 74)) + "\n\n" + old, "cu doc")
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/check_numbers.py
p = Path("tools/check_numbers.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import zipfile\n",
         "import zipfile\nfrom check_unchanged import SKIP, rebaselined  # noqa: E402  (D-0195)\n", "cn import")
t = once(t, "    for p in paths:\n        items, problems = check(p)\n",
         "    for p in paths:\n        if rebaselined(p):\n            print(SKIP.format(p))\n            continue\n"
         "        items, problems = check(p)\n", "cn main")
t, w = replace_in_paragraph(
    t, "Exit code 0 when every file passes.",
    "A file whose `status` is `ruled-change` is skipped with a printed reason (D-0195). "
    "Exit code 0 when every file passes.")
print("check_numbers docstring width", w)
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/check_em_dash.py
p = Path("tools/check_em_dash.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import sys\n", "import sys\nfrom check_unchanged import rebaselined  # D-0195\n", "ed import")
t = once(t, block(9).rstrip("\n") + "\n", block(10).rstrip("\n") + "\n", "ed scan")
t, w = replace_in_paragraph(
    t,
    "is skipped: it keeps every em dash its original holds, and the word check proves its "
    "words are the original's (D-0103).",
    "is skipped unless its status is `ruled-change`: it keeps every em dash its original holds, "
    "and the word check proves its words are the original's (D-0103). A `ruled-change` file "
    "is the site's own wording and is scanned (D-0195).")
print("check_em_dash docstring width", w)
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/media.py
p = Path("tools/media.py")
t = p.read_text(encoding="utf-8")
old_loop = ('    for e in media["images"]:\n        src = os.path.join(source_dir, e["file"])\n'
            '        name = os.path.basename(e["file"])\n        shutil.copyfile(src, os.path.join(dest, name))\n'
            '        published.append(name)\n')
comment = ("A picture's bytes are pinned the same way (D-0198 (4)): the word check that compares "
           "pictures skips a ruled-change file.")
# The comment above the files loop is 78 wide; the new one matches it.
cmt = "\n".join(wrap(comment, 78, "    # ", "    # "))
t = once(t, old_loop, cmt + "\n" + block(11).rstrip("\n") + "\n", "media loop")
p.write_text(t, encoding="utf-8", newline="\n")

# --- .github/workflows/verify.yml (comments, rewrapped to their block's width)
p = Path(".github/workflows/verify.yml")
t = p.read_text(encoding="utf-8")
t, w1 = replace_in_paragraph(t, "a converted file keeps its original's (D-0103).",
                             "a converted file keeps its original's (D-0103); a ruled-change file is "
                             "scanned (D-0195).", prefix="        # ")
t, w2 = replace_in_paragraph(t, "The word check, then Word's labels (D-0102, D-0112).",
                             "The word check, then Word's labels (D-0102, D-0112); both skip a "
                             "ruled-change file (D-0195).", prefix="          # ")
print("verify.yml widths", w1, w2)
p.write_text(t, encoding="utf-8", newline="\n")
print("T1 impl applied")
