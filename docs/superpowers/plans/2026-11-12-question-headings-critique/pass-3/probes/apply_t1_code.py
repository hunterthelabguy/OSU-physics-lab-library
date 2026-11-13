"""T1 code steps, verbatim from the plan: questions.lua and modern.css."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
f = tree / "tools/filters/questions.lua"
t = f.read_text(encoding="utf-8")
anchor = "local colours = {}\n"
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + B[2])
start = t.index("  {\n    Div = function(el)")
end = t.index("  },\n}", start) + len("  },\n")
t = t[:start] + B[3] + t[end:]
assert t.count(B[4]) == 1
t = t.replace(B[4], B[5])
f.write_text(t, encoding="utf-8", newline="\n")
c = tree / "themes/modern.css"
t = c.read_text(encoding="utf-8")
m = re.search(r"\.question-label p, \.checkpoint-label p \{.*?\n\}\n", t, re.S)
t = t[:m.start()] + B[6] + t[m.end():]
c.write_text(t, encoding="utf-8", newline="\n")
