from pathlib import Path

FRONT = """---
id: ph21x-lab-handbook
title: "Appendix B – Reference Information"
course: PH21X
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 7 - Capstone - Handout.docx"
source_sha256: "b8f38b5a04e1a01304f7ec7b71e7e54c2e13e46af80f5fe91f58cf76c8722ea6"
status: converted
ruled_omissions:
  - span:
      to: "Appendix B – Reference Information"
      labels:
        first: "o1"
        last: "o11.2"
    ledger: "D-0188"
images:
  - file: "ph21x-lab-handbook-media/graphical-analysis-view-icon.png"
    source_part: "word/media/image1.png"
    sha256: "7a85a2239d2a80de52693e4df786a1a22c14eff78027951153a8b42bdf2c941a"
  - file: "ph21x-lab-handbook-media/graphical-analysis-graph-tools-icon.png"
    source_part: "word/media/image2.png"
    sha256: "36df8e6bdf281576cc60c1e819bfc8b499fad38ed8027eaee5ca5e8dc9a32b4f"
---

"""
SWAPS = {
    "## Appendix B – Reference Information": "# Appendix B – Reference Information",
    "#### Required Plot Elements": "## Required Plot Elements {#plot-elements}",
    "#### Linearization": "## Linearization {#linearization}",
    "#### What is Uncertainty?": "## What is Uncertainty? {#what-is-uncertainty}",
    "#### Sources of Uncertainty:": "## Sources of Uncertainty: {#sources-of-uncertainty}",
    "**[Predictions, Hypotheses, and Models]{.underline}**":
        "## Predictions, Hypotheses, and Models {#predictions-hypotheses-models}",
    "#### Tips for Using Graphical Analysis:":
        "## Tips for Using Graphical Analysis: {#graphical-analysis-tips}",
    "#### Variables and Parameters": "## Variables and Parameters {#variables-and-parameters}",
}
lines = Path("curriculum/ph211/ph211-capstone-handout.md").read_text(encoding="utf-8").split("\n")
body = lines[283:378]                      # lines 284 to 378 at 33d6cb2: Appendix B
assert body[0] == "## Appendix B – Reference Information", body[0]
assert len(lines) == 379 and lines[378] == "", "capstone handout changed since 33d6cb2"
for old, new in SWAPS.items():
    assert body.count(old) == 1, old
    body[body.index(old)] = new
text = "\n".join(body).replace("ph211-capstone-handout-media/", "ph21x-lab-handbook-media/")
assert text.count("ph21x-lab-handbook-media/") == 2
Path("curriculum/ph21x/ph21x-lab-handbook.md").write_text(FRONT + text + "\n", encoding="utf-8",
                                                          newline="\n")
