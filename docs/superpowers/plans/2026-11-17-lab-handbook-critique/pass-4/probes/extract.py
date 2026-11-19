"""Dump the plan's fenced code blocks, numbered, to blocks/NN.<lang>.

Usage: python -X utf8 extract.py PLAN OUTDIR
"""
import os
import sys

plan, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
lines = open(plan, encoding="utf-8").read().split("\n")
n, i = 0, 0
while i < len(lines):
    s = lines[i].lstrip()
    if s.startswith("```") and len(s) > 3:
        lang = s[3:].strip()
        indent = len(lines[i]) - len(s)
        start = i + 1
        j = start
        while lines[j].strip() != "```":
            j += 1
        body = [ln[indent:] if ln[:indent].strip() == "" else ln for ln in lines[start:j]]
        n += 1
        name = os.path.join(out, "{:02d}.{}".format(n, lang))
        with open(name, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(body) + "\n")
        print(n, lang, "plan lines", start + 1, "to", j)
        i = j + 1
    else:
        i += 1
