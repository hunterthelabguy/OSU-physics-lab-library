"""T3: the HTML cap (argument: the cap) and the LabHandbook class, as written."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

cap, measured = sys.argv[1], sys.argv[2]
p = Path("tests/test_downloads.py")
text = p.read_text(encoding="utf-8")
OLD = '    "ph21x-problem-solving-strategy": 190_000,  # 164,146 bytes, D-0160\n'
assert text.count(OLD) == 1
text = text.replace(OLD, OLD + '    "ph21x-lab-handbook": {},  # {} bytes, D-0188\n'.format(cap, measured))
p.write_text(text, encoding="utf-8", newline="\n")

p = Path("tests/test_quarto_site.py")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[21].startswith("import render"), lines[21]
lines.insert(22, "import test_lab_handbook                 # noqa: E402  (ADDRESSES)")
text = "\n".join(lines)
i = text.index("    def test_course_index_links_course_wide_documents(self):")
j = text.index("\nclass ", i)            # the end of the class that holds it
text = text[:j] + "\n" + extract.blocks()[18][1] + "\n" + text[j:]
p.write_text(text, encoding="utf-8", newline="\n")
print("written")
