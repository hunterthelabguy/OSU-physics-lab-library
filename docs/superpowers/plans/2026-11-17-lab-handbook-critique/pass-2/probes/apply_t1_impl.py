"""T1, step 3: the plan's implementation blocks, as written. Run from the tree root."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

B = extract.blocks()

# check_unchanged.py: SKIP and rebaselined() after the FROM line (112).
p = Path("tools/check_unchanged.py")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[111] == 'FROM = "markdown-smart-implicit_figures"', lines[111]
lines[112:112] = ["", ""] + B[4][1].rstrip("\n").split("\n") + ["", ""]
text = "\n".join(lines)
LOOP = "    for p in paths:\n        n, problems = check(p, repo_root)\n"
assert text.count(LOOP) == 1
text = text.replace(LOOP, B[5][1] + "        n, problems = check(p, repo_root)\n")
p.write_text(text, encoding="utf-8", newline="\n")

# check_numbers.py: the import and the same loop opening.
p = Path("tools/check_numbers.py")
text = p.read_text(encoding="utf-8")
assert text.count("\nimport zipfile\n") == 1
text = text.replace("\nimport zipfile\n",
                    "\nimport zipfile\nfrom check_unchanged import SKIP, rebaselined  # noqa: E402  (D-0195)\n")
LOOP = "    for p in paths:\n        items, problems = check(p)\n"
assert text.count(LOOP) == 1
text = text.replace(LOOP, B[5][1] + "        items, problems = check(p)\n")
p.write_text(text, encoding="utf-8", newline="\n")

# check_em_dash.py: the import, the scan's skip, the docstring.
p = Path("tools/check_em_dash.py")
text = p.read_text(encoding="utf-8")
assert text.count("\nimport sys\n") == 1
text = text.replace("\nimport sys\n", "\nimport sys\nfrom check_unchanged import rebaselined  # D-0195\n")
assert text.count(B[6][1]) == 1
text = text.replace(B[6][1], B[7][1])
OLD = ("is skipped: it keeps every em dash its original holds, and the word check proves its"
       " words are the original's (D-0103).")
NEW = ("is skipped while its status is `converted`: it keeps every em dash its original holds,"
       " and the word check proves its words are the original's (D-0103). A `ruled-change`"
       " file is the site's own wording and is scanned (D-0195).")
pat = re.compile(r"\s+".join(re.escape(w) for w in OLD.split()))
m = list(pat.finditer(text))
assert len(m) == 1, len(m)
# Rewrap the docstring paragraph that holds it at 76 columns.
para_start = text.rfind("\n\n", 0, m[0].start()) + 2
para_end = text.index('\n"""\n', m[0].end())  # the docstring's last paragraph
para = " ".join(text[para_start:para_end].replace(m[0].group(0), NEW).split())
out, line = [], ""
for w in para.split():
    if line and len(line) + 1 + len(w) > 76:
        out.append(line)
        line = w
    else:
        line = (line + " " + w) if line else w
out.append(line)
text = text[:para_start] + "\n".join(out) + text[para_end:]
p.write_text(text, encoding="utf-8", newline="\n")
print("implementation written")
