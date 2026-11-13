"""Each Word download: label paragraph styles by level, label styles in styles.xml, other diffs vs baseline."""
import re, sys, zipfile, collections
from pathlib import Path
base, new = Path(sys.argv[1]), Path(sys.argv[2])
tot = collections.Counter()
for p in sorted(new.glob("labs/*/*.docx")):
    z = zipfile.ZipFile(p); doc = z.read("word/document.xml").decode(); sty = z.read("word/styles.xml").decode()
    c = collections.Counter(re.findall(r'<w:pStyle w:val="(QuestionLabel\d?)"', doc)); tot.update(c)
    zb = zipfile.ZipFile(base / p.relative_to(new))
    docb = zb.read("word/document.xml").decode()
    norm = re.sub(r'w:val="QuestionLabel\d"', 'w:val="QuestionLabel"', doc)
    other = [n for n in z.namelist() if n not in ("word/document.xml", "word/styles.xml", "docProps/core.xml") and z.read(n) != zb.read(n)]
    print(p.stem, dict(c), "doc equal but style names:", norm == docb, "other parts differ:", other)
print(dict(tot))
z = zipfile.ZipFile(next(new.glob("labs/ph212-data-analysis-handout/*.docx")))
for m in re.findall(r'<w:style\b[^>]*w:styleId="QuestionLabel\d?".*?</w:style>', z.read("word/styles.xml").decode(), re.S):
    print(m)
