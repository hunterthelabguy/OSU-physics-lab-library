from pathlib import Path

p = Path("curriculum/ph211/ph211-uncertainty-handout.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert len(lines) == 285 and lines[284] == "", "Lab 3 changed since 33d6cb2"
assert lines[241] == "## Appendix – Reference Information"
assert lines[243] == "This section contains key information from previous labs:"
assert lines[245] == '::: {.numbered anchors="o14.0.1 o14.0.2"}'
assert lines[246:249] == ["1.  Required Plot Elements", "2.  Linearization", ":::"]
assert lines[250] == "#### **Required Plot Elements**"
lines[243] = "Read the Lab Handbook. It holds the key information from previous labs:"
lines[246] = "1.  [Required Plot Elements](ph21x-lab-handbook#plot-elements)"
lines[247] = "2.  [Linearization](ph21x-lab-handbook#linearization)"
lines = lines[:249] + [""]             # drop line 250 on: both sections, to the end
assert lines[10] == "status: converted"
lines[10] = "status: ruled-change"
end = lines.index("---", 1)            # front matter's closing line
lines[end:end] = [
    "ruled_omissions:",
    "  - span:",
    '      from: "Required Plot Elements"',
    '      from_occurrence: "2"',
    '    ledger: "D-0192"',
    '  - text: "This section contains key information from previous labs:"',
    '    ledger: "D-0192"',
    "ruled_additions:",
    '  - text: "Read the Lab Handbook. It holds the key information from previous labs:"',
    '    ledger: "D-0192"',
]
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
