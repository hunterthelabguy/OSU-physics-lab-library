"""Every link target in every converted source, as Pandoc reads it, sorted
by kind: what the plan's DOC_TARGET (`^[A-Za-z0-9-]+#`) selects, what
media.lua's media-file pattern rewrites, and the rest.

Run from a tree's root with PANDOC set: python -X utf8 link_targets.py
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, "tools")
import render  # noqa: E402

PANDOC = os.environ["PANDOC"]
DOC_TARGET = re.compile(r"^[A-Za-z0-9-]+#")
MEDIA_FILE = re.compile(r"^([A-Za-z0-9-]+)-media/[^/]+$")
kinds = collections.Counter()
others = []


def walk(node, out):
    if isinstance(node, list):
        for n in node:
            walk(n, out)
    elif isinstance(node, dict):
        if node.get("t") == "Link":
            out.append(node["c"][2][0])
        walk(node.get("c"), out)


for doc_id, d in render.converted_documents().items():
    tree = json.loads(subprocess.run([PANDOC, d["path"], "-f", render.FROM, "-t", "json"],
                                     capture_output=True, check=True, encoding="utf-8").stdout)
    targets = []
    walk(tree["blocks"], targets)
    for t in targets:
        if DOC_TARGET.match(t):
            kinds["DOC_TARGET"] += 1
            others.append((doc_id, t))
        elif MEDIA_FILE.match(t):
            kinds["media file"] += 1
        elif re.match(r"^[a-z]+:", t):
            kinds["scheme " + t.split(":", 1)[0]] += 1
        elif t.startswith("#"):
            kinds["local #"] += 1
        else:
            kinds["other relative"] += 1
            others.append((doc_id, t))
print(dict(kinds))
for o in others:
    print("  ", o)
