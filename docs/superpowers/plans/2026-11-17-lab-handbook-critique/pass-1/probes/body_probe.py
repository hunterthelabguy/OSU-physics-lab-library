import sys, zipfile, os
sys.path.insert(0, os.path.join(sys.argv[1], "tools"))
import check_unchanged as cu
W = cu.W
def ptext(p):
    return " ".join("".join(t.text or "" for t in p.iter(W + "t")).split())
for path, wants in [("originals/PH211/Lab 7 - Capstone - Handout.docx", ["Appendix B – Reference Information", "This section contains key information from previous labs:"]),
                    ("originals/PH211/Lab 3 - Uncertainty - Handout.docx", ["Required Plot Elements", "Linearization", "Appendix – Reference Information", "This section contains key information from previous labs:"])]:
    full = os.path.join(sys.argv[1], path)
    with zipfile.ZipFile(full) as z:
        data = z.read("word/document.xml")
    body = cu.without_fallbacks(data).find(W + "body")
    kids = list(body)
    print(path, "children", len(kids))
    tbls = [i for i, c in enumerate(kids) if c.tag == W + "tbl"]
    print(" top-level tables", tbls)
    print(" nested tables anywhere", sum(1 for _ in body.iter(W + "tbl")))
    for w in wants:
        print(" ", repr(w), [i for i, c in enumerate(kids) if c.tag == W + "p" and ptext(c) == w])
    # Any text in tables/textbox matching
    last = len(kids)
    print(" last child tag", kids[-1].tag.split('}')[1])
