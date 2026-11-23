"""Apply T3 as written, step by step.

Run from the scratch tree's root: python -X utf8 apply_t3.py BLOCKS STEP
STEP: tests (blocks 19, 20) | pin (REBASELINED, question-ids.json) |
      cap BYTES (HTML_CAPS) | site (test_quarto_site import and block 24)
"""
import math
import sys
from pathlib import Path

B, step = Path(sys.argv[1]), sys.argv[2]


def block(n, ext="python"):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


def edit(path, *pairs):
    p = Path(path)
    t = p.read_text(encoding="utf-8")
    for old, new, what in pairs:
        t = once(t, old, new, what)
    p.write_text(t, encoding="utf-8", newline="\n")


if step == "tests":
    end_addresses = '"predictions-hypotheses-models", "graphical-analysis-tips", "variables-and-parameters"]\n'
    t = Path("tests/test_lab_handbook.py").read_text(encoding="utf-8")
    t = once(t, end_addresses, end_addresses + block(19).rstrip("\n") + "\n\n\n", "after ADDRESSES")
    t = t.rstrip("\n") + "\n\n\n" + block(20).rstrip("\n") + "\n"
    Path("tests/test_lab_handbook.py").write_text(t, encoding="utf-8", newline="\n")
elif step == "pin":
    edit("tests/test_check_unchanged.py",
         ('        "curriculum/ph211/ph211-describing-an-experiment-handout.md": "D-0169",\n',
          '        "curriculum/ph211/ph211-describing-an-experiment-handout.md": "D-0169",\n'
          '        "curriculum/ph21x/ph21x-lab-handbook.md": "D-0197",\n', "REBASELINED"))
    edit("tests/question-ids.json",
         ('  "ph21x-problem-solving-strategy": []\n', block(23, "json"), "pin json"))
elif step == "cap":
    measured = int(sys.argv[3])
    cap = math.ceil(measured * 1.10 / 10000) * 10000
    edit("tests/test_downloads.py",
         ('    "ph21x-problem-solving-strategy": 190_000,',
          '    "ph21x-lab-handbook": {:_},  # {:,} bytes, D-0188\n'
          '    "ph21x-problem-solving-strategy": 190_000,'.format(cap, measured), "HTML_CAPS"))
    print("cap", cap)
elif step == "site":
    edit("tests/test_quarto_site.py",
         ("import render                             # noqa: E402\n",
          "import render                             # noqa: E402\n"
          "import test_lab_handbook                 # noqa: E402  (ADDRESSES)\n", "import"),
         ("\n\n\nclass NoThirdParty(", "\n\n\n" + block(24).rstrip("\n") + "\n\n\nclass NoThirdParty(", "class"))
print("T3", step, "applied")
