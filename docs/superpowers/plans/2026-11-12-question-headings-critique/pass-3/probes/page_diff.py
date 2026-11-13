"""Every built HTML file, before vs after, with the label's markup normalised: what else changed?"""
import re, sys, difflib
from pathlib import Path
base, new = Path(sys.argv[1]), Path(sys.argv[2])
OLD = re.compile(r'<div class="(question|checkpoint)-label">\s*<p>((?:Question|Checkpoint) \d+)</p>\s*</div>')
NEW = re.compile(r'<h[2-6] class="(question|checkpoint)-label">((?:Question|Checkpoint) \d+)</h[2-6]>')
CSS = re.compile(r"/\* The label is a heading.*?\n\.question-label, \.checkpoint-label \{.*?\}|\.question-label p, \.checkpoint-label p \{.*?\}", re.S)
changed = 0
for p in sorted(new.rglob("*.html")):
    q = base / p.relative_to(new)
    if not q.exists(): print("new file", p.relative_to(new)); continue
    a = CSS.sub("CSS", OLD.sub(r"LABEL \1 \2", q.read_text(encoding="utf-8")))
    b = CSS.sub("CSS", NEW.sub(r"LABEL \1 \2", p.read_text(encoding="utf-8")))
    if a != b:
        changed += 1
        d = [l for l in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        print("==", p.relative_to(new), len(d)); print("\n".join(x[:200] for x in d[:12]))
print("files changed beyond the label:", changed)
for p in sorted(base.rglob("*.html")):
    if not (new / p.relative_to(base)).exists(): print("gone", p.relative_to(base))
