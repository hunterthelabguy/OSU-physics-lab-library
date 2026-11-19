"""Where Lab 3's appendix lands in its built PDF, page by page (the plan's
T4 PR-body claim, D-0198 (6): heading and lead-in end page 9, the two
links alone on page 10), and whether both /URI links are in it.

Run from the scratch tree's root after a build, PDFTOTEXT set:
python -X utf8 lab3_pdf_pages.py
"""
import os
import subprocess
import sys

sys.path.insert(0, "tools")
import render  # noqa: E402

pdf = os.path.join("build", "quarto-site", "labs", "ph211-uncertainty-handout",
                   "ph211-uncertainty-handout.pdf")
text = subprocess.run([os.environ["PDFTOTEXT"], "-layout", pdf, "-"], capture_output=True,
                      check=True, encoding="utf-8").stdout
pages = text.split("\f")
print("pages:", len([p for p in pages if p.strip()]))
for needle in ("Appendix – Reference Information", "Read the Lab Handbook",
               "Required Plot Elements", "Linearization", "Appendix – Error Bars"):
    where = [i + 1 for i, p in enumerate(pages) if needle in p]
    print("{!r}: pages {}".format(needle, where))
last = [p for p in pages if p.strip()][-1]
print("last page's lines:", [ln.strip() for ln in last.split("\n") if ln.strip()])
data = open(pdf, "rb").read()
for a in ("plot-elements", "linearization"):
    url = render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#" + a
    print(a, "URI in PDF:", url.encode("ascii") in data)
