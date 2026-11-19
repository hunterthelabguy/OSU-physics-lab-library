"""T4, step 1: Lab 3's three link tests, as written."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

B = extract.blocks()
p = Path("tests/test_quarto_site.py")
text = p.read_text(encoding="utf-8")
i = text.index("class LabHandbook(unittest.TestCase):")
j = text.index("\nclass ", i)
text = text[:j].rstrip("\n") + "\n\n" + B[19][1] + "\n" + text[j:]
p.write_text(text, encoding="utf-8", newline="\n")

p = Path("tests/test_downloads.py")
text = p.read_text(encoding="utf-8")
i = text.index("class MarkdownAndWord(unittest.TestCase):")
j = text.index("\n# Each lab's HTML download, measured", i)   # the class ends before HTML_CAPS
k = text.rfind("\nclass ", i + 1, j)
assert k == -1, "another class inside"
text = text[:j].rstrip("\n") + "\n\n" + B[20][1] + "\n" + text[j:]
p.write_text(text, encoding="utf-8", newline="\n")
print("written")
