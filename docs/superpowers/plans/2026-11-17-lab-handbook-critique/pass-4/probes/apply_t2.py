"""Apply T2 as written. `tests` writes the new test module (plan block 16);
`impl` replaces media.lua's Link (block 17) and adds the comment (block 18)
after line 30.

Run from the scratch tree's root: python -X utf8 apply_t2.py BLOCKS tests|impl
"""
import sys
from pathlib import Path

B, step = Path(sys.argv[1]), sys.argv[2]


def block(n, ext):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


if step == "tests":
    Path("tests/test_lab_handbook.py").write_text(block(16, "python"), encoding="utf-8", newline="\n")
else:
    p = Path("tools/filters/media.lua")
    lines = p.read_text(encoding="utf-8").split("\n")
    assert lines[128] == "    Link = function(el)" and lines[134] == "    end,", lines[128:135]
    lines[128:135] = block(17, "lua").rstrip("\n").split("\n")
    assert lines[29].startswith("-- download alike"), lines[29]
    lines[30:30] = block(18, "lua").rstrip("\n").split("\n")
    p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("T2", step, "applied")
