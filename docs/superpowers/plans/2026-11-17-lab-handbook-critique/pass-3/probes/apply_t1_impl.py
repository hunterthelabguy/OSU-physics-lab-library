"""Apply T1's implementation steps (plan blocks 07, 08, 09/10, 11 and the
prose edits of plan lines 237 to 270), as written.

Run from the scratch tree's root: python -X utf8 apply_t1_impl.py BLOCKS
Where the plan says "rewrap", a paragraph is refilled to the widest line it
had before (its block's width).
"""
import re
import sys
import textwrap
from pathlib import Path

B = Path(sys.argv[1])


def block(n, ext="python"):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


def norm(s):
    return " ".join(s.split())


def refill_paragraph(text, contains, prefix="", width=None):
    """Refill the paragraph (blank-line delimited, each line starting with
    `prefix`) that contains `contains` once whitespace is normalised. A
    docstring's closing quotes stay on their own line."""
    lines = text.split("\n")
    paras, cur = [], []
    for i, ln in enumerate(lines):
        inside = ln.startswith(prefix) and ln[len(prefix):].strip() if prefix else ln.strip()
        if ln.strip() == '"""':
            inside = False
        if not inside:
            if cur:
                paras.append(cur)
            cur = []
        else:
            cur.append(i)
    if cur:
        paras.append(cur)
    hits = [p for p in paras if contains in norm(" ".join(lines[i][len(prefix):] for i in p))]
    assert len(hits) == 1, (contains, len(hits))
    p = hits[0]
    words = norm(" ".join(lines[i][len(prefix):] for i in p))
    w = width or max(len(lines[i]) for i in p)
    new = textwrap.wrap(words, width=w - len(prefix), break_long_words=False, break_on_hyphens=False)
    lines[p[0]:p[-1] + 1] = [prefix + ln for ln in new]
    return "\n".join(lines)


def width_of(path, first, last):
    ls = Path(path).read_text(encoding="utf-8").split("\n")
    return max(len(x) for x in ls[first - 1:last])


W_CN = width_of("tools/check_numbers.py", 29, 32)
W_EM = width_of(".github/workflows/verify.yml", 34, 36)
W_CU = width_of(".github/workflows/verify.yml", 50, 52)

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
t = once(t, old, "\n".join(textwrap.wrap(new_par, 75)) + "\n\n" + old, "cu doc")
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/check_numbers.py
p = Path("tools/check_numbers.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import zipfile\n",
         "import zipfile\nfrom check_unchanged import SKIP, rebaselined  # noqa: E402  (D-0195)\n", "cn import")
t = once(t, "    for p in paths:\n        items, problems = check(p)\n",
         "    for p in paths:\n        if rebaselined(p):\n            print(SKIP.format(p))\n            continue\n"
         "        items, problems = check(p)\n", "cn main")
t = once(t, "outside them is typed from the page and not compared. Exit code 0\nwhen every file passes.",
         "outside them is typed from the page and not compared. A file whose `status` is "
         "`ruled-change` is skipped with a printed reason (D-0195). Exit code 0\nwhen every file passes.",
         "cn doc")
t = refill_paragraph(t, "A file whose `status` is `ruled-change` is skipped with a printed reason (D-0195).", width=W_CN)
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/check_em_dash.py
p = Path("tools/check_em_dash.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import sys\n", "import sys\nfrom check_unchanged import rebaselined  # D-0195\n", "ed import")
t = once(t, block(9).rstrip("\n") + "\n", block(10).rstrip("\n") + "\n", "ed scan")
old = ("is skipped: it keeps every em dash its original holds, and the word check proves its "
       "words are the original's (D-0103).")
new = ("is skipped while its status is `converted`: it keeps every em dash its original holds, "
       "and the word check proves its words are the original's (D-0103). A `ruled-change` file "
       "is the site's own wording and is scanned (D-0195).")
lines = t.split("\n")
# The docstring paragraph is lines 5 to 10 (1-based); replace within it, whitespace normalised.
start = next(i for i, ln in enumerate(lines) if ln.startswith("Scans only the published sources"))
end = next(i for i in range(start, len(lines)) if lines[i].strip() in ("", '"""'))
para = norm(" ".join(lines[start:end]))
assert para.count(old) == 1, para
para = para.replace(old, new)
w = max(len(ln) for ln in lines[start:end])
lines[start:end] = textwrap.wrap(para, w, break_long_words=False, break_on_hyphens=False)
t = "\n".join(lines)
p.write_text(t, encoding="utf-8", newline="\n")

# --- tools/media.py
p = Path("tools/media.py")
t = p.read_text(encoding="utf-8")
old_loop = ('    for e in media["images"]:\n        src = os.path.join(source_dir, e["file"])\n'
            '        name = os.path.basename(e["file"])\n        shutil.copyfile(src, os.path.join(dest, name))\n'
            '        published.append(name)\n')
comment = ("A picture's bytes are pinned the same way (D-0198 (4)): the word check that compares "
           "pictures skips a ruled-change file.")
cmt = "\n".join("    # " + ln for ln in textwrap.wrap(comment, 74))
t = once(t, old_loop, cmt + "\n" + block(11).rstrip("\n") + "\n", "media loop")
p.write_text(t, encoding="utf-8", newline="\n")

# --- .github/workflows/verify.yml (comments, rewrapped to their block's width)
p = Path(".github/workflows/verify.yml")
t = p.read_text(encoding="utf-8")
t = once(t, "# a converted file keeps its original's (D-0103). The list is in the",
         "# a converted file keeps its original's (D-0103); a ruled-change file is scanned (D-0195). The list is in the",
         "vy em")
t = refill_paragraph(t, "a ruled-change file is scanned (D-0195).", prefix="        # ", width=W_EM)
t = once(t, "# check, then Word's labels (D-0102, D-0112).",
         "# check, then Word's labels (D-0102, D-0112); both skip a ruled-change file (D-0195).", "vy cu")
t = refill_paragraph(t, "both skip a ruled-change file (D-0195).", prefix="          # ", width=W_CU)
p.write_text(t, encoding="utf-8", newline="\n")
print("T1 impl applied")
