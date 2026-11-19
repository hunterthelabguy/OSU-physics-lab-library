"""T1, step "Amend the words", as written. Run from the tree root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

B = extract.blocks()


def norm(s):
    return " ".join(s.split())


# CLAUDE.md: the "Conversion first" bullet, found by normalised text.
p = Path("CLAUDE.md")
lines = p.read_text(encoding="utf-8").split("\n")
starts = [i for i, l in enumerate(lines) if l.startswith("- Conversion first, then ruled changes (D-0168).")]
assert len(starts) == 1
s = starts[0]
e = next(i for i in range(s, len(lines)) if "Never loosen the check for a change." in lines[i])
assert norm(" ".join(lines[s:e + 1])).endswith("Never loosen the check for a change.")
lines[s:e + 1] = B[9][1].rstrip("\n").split("\n")
text = "\n".join(lines)
# The Build bullet: the exception after "never copy content into a second file".
OLD = "never copy content into a second file"
flat = norm(text)
assert flat.count(OLD) == 1
i = text.index("never copy content into a second\n  file") if OLD not in text else text.index(OLD)
j = i + len(text[i:].split("file", 1)[0]) + len("file")
text = text[:j] + " (one exception, until PH 211's appendix copies are cut: the Lab Handbook's sections, D-0191)" + text[j:]
p.write_text(text, encoding="utf-8", newline="\n")

# docs/conversion-spec.md: the template's line 21 comment; the new paragraph.
p = Path("docs/conversion-spec.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[20].startswith("status: converted") and "# converted | checked | ruled-change" in lines[20]
lines[20] = lines[20].split("#", 1)[0] + "# converted | checked | ruled-change (the Word checks skip ruled-change, D-0195)"
text = "\n".join(lines)
sec = text.index("## Content-unchanged check")
end = text.index("(ledger 20).\n", sec) + len("(ledger 20).\n")
text = text[:end] + "\n" + B[10][1] + text[end:]
p.write_text(text, encoding="utf-8", newline="\n")
print("words written")
