"""T3 steps, verbatim: the box-heading test, then (with --sources) the two source lines and the NVDA clause."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
def edit(rel, old, new):
    f = tree / rel; t = f.read_text(encoding="utf-8")
    assert t.count(old) == 1, (rel, old); f.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
if "--sources" not in sys.argv:
    edit("tests/test_headings.py", '\n\n\nif __name__ == "__main__":', "\n\n" + B[14].rstrip("\n") + '\n\n\nif __name__ == "__main__":')
else:
    edit("curriculum/ph212/ph212-data-analysis-handout.md", "\n### What is Uncertainty?\n", "\n#### What is Uncertainty?\n")
    edit("curriculum/ph212/ph212-extending-a-model-handout.md", "\n### Assumptions:\n", "\n#### Assumptions:\n")
    edit("docs/accessibility/2026-11-05-nvda-ph212.md", "The math and the question labels are open.", "The question labels are headings (D-0176). The math is open.")
