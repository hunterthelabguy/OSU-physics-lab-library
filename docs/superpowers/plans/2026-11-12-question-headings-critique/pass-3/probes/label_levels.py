"""Count label levels and box headings over all sources via tests/test_headings.headings."""
import collections, sys
from pathlib import Path
sys.path.insert(0, "tests")
import test_headings as th
c = collections.Counter(); boxes = []
for p in sorted(Path("curriculum").glob("*/*.md")):
    for level, kind, box in th.headings(p):
        if kind == "label": c[level] += 1
        if kind == "box": boxes.append((p.stem, level, box))
print(dict(sorted(c.items())), sum(c.values()), boxes)
