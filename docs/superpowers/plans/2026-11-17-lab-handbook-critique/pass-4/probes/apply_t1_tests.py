"""Apply T1's test blocks (plan blocks 02 to 06) exactly where the plan says.

Run from the scratch tree's root: python -X utf8 apply_t1_tests.py BLOCKS
"""
import sys
from pathlib import Path

B = Path(sys.argv[1])


def block(n):
    return (B / "{:02d}.python".format(n)).read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


GUARD = '\n\nif __name__ == "__main__":'

# tests/test_check_unchanged.py: imports, then the class at the end before the guard.
p = Path("tests/test_check_unchanged.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import hashlib\nimport os\n", "import contextlib\nimport hashlib\nimport io\nimport os\n", "cu imports")
t = once(t, GUARD, "\n\n" + block(2).rstrip("\n") + "\n" + GUARD, "cu guard")
p.write_text(t, encoding="utf-8", newline="\n")

# tests/test_downloads.py: after test_a_changed_file_stops_the_build.
p = Path("tests/test_downloads.py")
t = p.read_text(encoding="utf-8")
anchor = ("        with tempfile.TemporaryDirectory() as out, self.assertRaises(SystemExit):\n"
          "            media.build(doc, out, downloads.CHROME)\n\n    def test_word_links_the_file_at_the_library")
t = once(t, anchor, anchor.replace("\n\n    def test_word_links",
                                   "\n\n" + block(3).rstrip("\n") + "\n\n    def test_word_links"), "dl anchor")
p.write_text(t, encoding="utf-8", newline="\n")

# tests/test_check_numbers.py: imports, class at the end before the guard.
p = Path("tests/test_check_numbers.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import json\nimport os\n", "import contextlib\nimport io\nimport json\nimport os\n", "cn imports")
t = once(t, GUARD, "\n\n" + block(4).rstrip("\n") + "\n" + GUARD, "cn guard")
p.write_text(t, encoding="utf-8", newline="\n")

# tests/test_question_ids.py: import; EmDashScan's new test; Pin's new test.
p = Path("tests/test_question_ids.py")
t = p.read_text(encoding="utf-8")
t = once(t, "import check_em_dash  # noqa: E402\n",
         "import check_em_dash  # noqa: E402\nimport check_unchanged  # noqa: E402\n", "qi import")
t = once(t, "        self.assertEqual(check_em_dash.scan(), [])\n" + GUARD,
         "        self.assertEqual(check_em_dash.scan(), [])\n\n" + block(5).rstrip("\n") + "\n" + GUARD,
         "qi emdash")
t = once(t, "        self.assertNotEqual(ids, PIN[lab])\n\n\nclass EmDashScan",
         "        self.assertNotEqual(ids, PIN[lab])\n\n" + block(6).rstrip("\n")
         + "\n\n\nclass EmDashScan", "qi pin")
p.write_text(t, encoding="utf-8", newline="\n")
print("T1 tests applied")
