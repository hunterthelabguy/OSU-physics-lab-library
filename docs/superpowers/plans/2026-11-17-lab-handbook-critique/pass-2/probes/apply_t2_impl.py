"""T2, step 3: media.lua's Link and its comment, as written. Run from the tree root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

B = extract.blocks()
p = Path("tools/filters/media.lua")
lines = p.read_text(encoding="utf-8").split("\n")
# Link, lines 129 to 135.
assert lines[128] == "    Link = function(el)" and lines[134] == "    end,", (lines[128], lines[134])
lines[128:135] = B[12][1].rstrip("\n").split("\n")
# After the comment paragraph on a lab's own file (line 30), a new paragraph.
assert lines[29] == "-- download alike, so a saved Word, HTML or PDF file still reaches it.", lines[29]
assert lines[30] == "--"
lines[30:30] = ["--"] + B[13][1].rstrip("\n").split("\n")
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("written")
