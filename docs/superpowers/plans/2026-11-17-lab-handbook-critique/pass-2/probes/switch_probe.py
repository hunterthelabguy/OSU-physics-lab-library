"""The status line alone turns both Word checks off. A copy of PH 211 Lab 1
with one word changed fails the word check; the same copy with
`status: ruled-change` passes both, and nothing else names the file.
Run from the tree root after T1."""
import contextlib
import io
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tools")
import check_numbers  # noqa: E402
import check_unchanged  # noqa: E402

src = Path("curriculum/ph211/ph211-team-building-handout.md").read_text(encoding="utf-8")
assert "status: converted" in src
body = src.index("\n---\n", 4) + 5           # after the front matter
at = src.index(" the ", body)
changed = src[:at] + " a " + src[at + 5:]   # one word changed in the body
assert changed != src
with tempfile.TemporaryDirectory() as d:
    for status in ("converted", "ruled-change"):
        md = Path(d) / "lab.md"
        md.write_text(changed.replace("status: converted", "status: " + status, 1),
                      encoding="utf-8", newline="\n")
        for tool in (check_unchanged, check_numbers):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = tool.main([str(md)])
            print(status, tool.__name__, "exit", code, out.getvalue().split("\n")[0][:60].replace(d, "<tmp>"))
