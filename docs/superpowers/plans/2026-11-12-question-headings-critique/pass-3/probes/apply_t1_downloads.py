"""T1 test_downloads steps, verbatim from the plan."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
f = tree / "tests/test_downloads.py"
t = f.read_text(encoding="utf-8")
lines = t.split("\n")
old = r"""r'<div class="question-label">\s*<p>Question (\d+)</p>\s*</div>(.*?)</div>'"""
assert old in lines[876], lines[876]
new = re.search(r"pattern becomes\s+`(r'[^`]+')`", plan).group(1)
lines[876] = lines[876].replace(old, new)
t = "\n".join(lines)
anchor = "\n\nclass MediaDownloads("
assert t.count(anchor) == 1
t = t.replace(anchor, "\n" + B[7].rstrip("\n") + "\n" + anchor)
f.write_text(t, encoding="utf-8", newline="\n")
