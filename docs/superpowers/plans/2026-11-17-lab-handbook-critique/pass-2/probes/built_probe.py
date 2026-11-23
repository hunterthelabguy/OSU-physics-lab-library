"""What the build holds after T4: the handbook page, its four downloads, the
course index, Lab 3's page and Word, HTML and PDF downloads. Run from the
tree root after a build."""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, "tools")
import render  # noqa: E402

Q = Path("build/quarto-site")
H = "ph21x-lab-handbook"
L3 = "ph211-uncertainty-handout"
WANT = ["plot-elements", "linearization", "what-is-uncertainty", "sources-of-uncertainty",
        "predictions-hypotheses-models", "graphical-analysis-tips", "variables-and-parameters"]

page = (Q / "labs" / H / "modern" / "index.html").read_text(encoding="utf-8")
print("handbook h1:", re.findall(r"<h1[^>]*>(.*?)</h1>", page, re.S))
print("handbook h2 ids:", re.findall(r'<h2[^>]*\bid="([^"]+)"', page))
print("handbook ids anywhere (section or h2):", [i for i in re.findall(r'\bid="([^"]+)"', page) if i in WANT])
print("contents links:", [a for a in WANT if 'href="#' + a + '"' in page])
print("icons with alt:", re.findall(r'<img[^>]*alt="([^"]*)"[^>]*graphical-analysis', page)
      or re.findall(r'<img[^>]*graphical-analysis[^>]*alt="([^"]*)"', page))
for ext in ("md", "docx", "html", "pdf"):
    f = Q / "labs" / H / (H + "." + ext)
    print("download", ext, f.is_file(), f.stat().st_size if f.is_file() else None)
src = Path("curriculum/ph21x/" + H + ".md").read_bytes()
print("md download is the source:", (Q / "labs" / H / (H + ".md")).read_bytes() == src)
with zipfile.ZipFile(Q / "labs" / H / (H + ".docx")) as z:
    doc = z.read("word/document.xml").decode("utf-8")
print("docx internal links:", re.findall(r'w:hyperlink w:anchor="([^"]+)"', doc))
print("docx bookmarks:", [b for b in re.findall(r'w:bookmarkStart[^>]*w:name="([^"]+)"', doc) if b in WANT])
hd = (Q / "labs" / H / (H + ".html")).read_text(encoding="utf-8")
print("html download contents links:", [a for a in WANT if 'href="#' + a + '"' in hd])
print("html download ids:", [i for i in re.findall(r'\bid="([^"]+)"', hd) if i in WANT])
pdf = (Q / "labs" / H / (H + ".pdf")).read_bytes()
print("pdf internal dests:", len(re.findall(rb"/Dest", pdf)), "pdf /URI:", len(re.findall(rb"/URI", pdf)))

idx = " ".join((Q / "courses" / "index.html").read_text(encoding="utf-8").split())
print("course index lists the handbook:", 'href="../labs/' + H + '/modern/">Lab Handbook</a>' in idx)
m = re.search(r"For every course</h2>(.*?)</ul>", idx)
print("for every course list:", re.findall(r">([^<]+)</a>", m.group(1)) if m else None)

URL = render.LIBRARY_URL + "labs/" + H + "/modern/#"
lp = (Q / "labs" / L3 / "modern" / "index.html").read_text(encoding="utf-8")
print("lab3 page:", [a for a in ("plot-elements", "linearization") if 'href="' + URL + a + '"' in lp])
with zipfile.ZipFile(Q / "labs" / L3 / (L3 + ".docx")) as z:
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
print("lab3 word:", [a for a in ("plot-elements", "linearization") if 'Target="' + URL + a + '"' in rels])
lh = (Q / "labs" / L3 / (L3 + ".html")).read_text(encoding="utf-8")
print("lab3 html:", [a for a in ("plot-elements", "linearization") if 'href="' + URL + a + '"' in lh])
lpdf = (Q / "labs" / L3 / (L3 + ".pdf")).read_bytes()
print("lab3 pdf /URI:", [a for a in ("plot-elements", "linearization") if (URL + a).encode() in lpdf])
lmd = (Q / "labs" / L3 / (L3 + ".md")).read_text(encoding="utf-8")
print("lab3 md keeps source form:", "](ph21x-lab-handbook#plot-elements)" in lmd)
print("lab3 page sizes: html", (Q / "labs" / L3 / (L3 + ".html")).stat().st_size)
