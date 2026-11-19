"""Apply T4's tests (blocks 25, 26) and pin, as written.

Run from the scratch tree's root: python -X utf8 apply_t4.py BLOCKS tests|pin
"""
import sys
from pathlib import Path

B, step = Path(sys.argv[1]), sys.argv[2]


def block(n):
    return (B / "{:02d}.python".format(n)).read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


if step == "tests":
    # In LabHandbook, after its last method (the class ends before NoThirdParty).
    p = Path("tests/test_quarto_site.py")
    t = p.read_text(encoding="utf-8")
    t = once(t, "\n\n\nclass NoThirdParty(", "\n\n" + block(25).rstrip("\n") + "\n\n\nclass NoThirdParty(", "qs")
    p.write_text(t, encoding="utf-8", newline="\n")
    # In MarkdownAndWord (line 179), after its docx() helper.
    p = Path("tests/test_downloads.py")
    t = p.read_text(encoding="utf-8")
    t = once(t, '        return QSITE / "labs" / doc_id / (doc_id + ".docx")\n\n',
             '        return QSITE / "labs" / doc_id / (doc_id + ".docx")\n\n' + block(26).rstrip("\n") + "\n\n",
             "dl")
    p.write_text(t, encoding="utf-8", newline="\n")
else:
    p = Path("tests/test_check_unchanged.py")
    t = p.read_text(encoding="utf-8")
    t = once(t, '        "curriculum/ph211/ph211-describing-an-experiment-handout.md": "D-0169",\n',
             '        "curriculum/ph211/ph211-describing-an-experiment-handout.md": "D-0169",\n'
             '        "curriculum/ph211/ph211-uncertainty-handout.md": "D-0192",\n', "pin")
    p.write_text(t, encoding="utf-8", newline="\n")
print("T4", step, "applied")
