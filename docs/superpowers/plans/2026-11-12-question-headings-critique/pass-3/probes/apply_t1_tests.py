"""T1 test steps, verbatim from the plan: Filter tests, test_headings.py."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
f = tree / "tests/test_check_numbers.py"
t = f.read_text(encoding="utf-8")
guard = '\n\nif __name__ == "__main__":'
assert t.count(guard) == 1
t = t.replace(guard, "\n" + B[0].rstrip("\n") + guard)
f.write_text(t, encoding="utf-8", newline="\n")
(tree / "tests/test_headings.py").write_text(B[1], encoding="utf-8", newline="\n")
