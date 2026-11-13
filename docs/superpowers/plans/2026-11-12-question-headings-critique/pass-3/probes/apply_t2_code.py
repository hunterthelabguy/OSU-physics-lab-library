"""T2 code steps, verbatim: make_reference_docx STYLES and docstring, filter Word branch."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
def once(t, old, new):
    assert t.count(old) == 1, old
    return t.replace(old, new)
f = tree / "tools/make_reference_docx.py"
t = f.read_text(encoding="utf-8")
end = "    '</w:style>')\n"
t = once(t, end, "    '</w:style>'\n" + B[11].rstrip("\n") + ")\n")
t = once(t, "  --quiet colour, kept with what follows. The box",
         "  --quiet colour, kept with what follows, and Question Label 3 to 5, the same\n"
         "  with the outline level of an h3 to h5 (D-0176), which the filter picks by\n"
         "  the label's level. The box")
f.write_text(t, encoding="utf-8", newline="\n")
f = tree / "tools/filters/questions.lua"
t = f.read_text(encoding="utf-8")
t = once(t, '      if FORMAT == "docx" then\n', '      if FORMAT == "docx" then\n' + B[12])
t = once(t, '{ ["custom-style"] = "Question Label" }', '{ ["custom-style"] = "Question Label " .. level }')
f.write_text(t, encoding="utf-8", newline="\n")
