"""D-0195 (1): the pin still fails on a reordered ruled-change file. Swaps the
first two question blocks of Lab 6 (ruled-change since D-0169) in a copy and
reads its ids as tests/test_question_ids.py does. Run from the tree root."""
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
sys.path.insert(0, "tools")
import check_unchanged  # noqa: E402
import test_question_ids as t  # noqa: E402

src = Path("curriculum/ph211/ph211-describing-an-experiment-handout.md")
print("rebaselined:", check_unchanged.rebaselined(src))
text = src.read_text(encoding="utf-8")
starts = [m.start() for m in re.finditer(r"^::: \{\.question #", text, re.M)]
a, b = starts[0], starts[1]
a_end = text.index(":::\n", text.index("\n", a)) + 4
b_end = text.index(":::\n", text.index("\n", b)) + 4
swapped = text[:a] + text[b:b_end] + text[a_end:b] + text[a:a_end] + text[b_end:]
with tempfile.TemporaryDirectory() as d:
    md = Path(d) / "lab.md"
    md.write_text(swapped, encoding="utf-8", newline="\n")
    lab, ids = t.read(md)
print("same ids, other order:", sorted(ids) == sorted(t.PIN[lab]), "pin fails:", ids != t.PIN[lab])
print("the pin's selection includes it:", src in list(t.converted_labs()) or
      any(p.name == src.name for p in t.converted_labs()))
