"""Does PrintKeeps' split pattern capture the same `rest` per label, before and after?"""
import re, sys
from pathlib import Path
base, new = Path(sys.argv[1]), Path(sys.argv[2])
OLD = r'<div class="question-label">\s*<p>Question (\d+)</p>\s*</div>(.*?)</div>'
NEW = r'<h[2-6] class="question-label">Question (\d+)</h[2-6]>(.*?)</div>'
tot = diff = empty = 0
for p in sorted(new.glob("labs/*/modern/index.html")):
    rel = p.relative_to(new)
    m = lambda t: re.search(r"<main id=\"content\">(.*?)</main>", t, re.S).group(1)
    a = re.findall(OLD, m((base / rel).read_text(encoding="utf-8")), re.S)
    b = re.findall(NEW, m(p.read_text(encoding="utf-8")), re.S)
    tot += len(b)
    empty += sum(1 for _, r in b if not r.strip())
    if [(n, r.strip()) for n, r in a] != [(n, r.strip()) for n, r in b]:
        diff += 1; print("differs", rel, len(a), len(b))
print("labels", tot, "empty rest", empty, "pages differing", diff)
