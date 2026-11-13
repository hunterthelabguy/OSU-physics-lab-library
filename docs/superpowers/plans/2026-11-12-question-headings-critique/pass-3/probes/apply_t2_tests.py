"""T2 test steps, verbatim from the plan's prose and blocks."""
import re, sys
from pathlib import Path
plan, tree = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
B = [b for _, b in re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)]
f = tree / "tests/test_downloads.py"
t = f.read_text(encoding="utf-8")

def once(old, new):
    global t
    assert t.count(old) == 1, old
    t = t.replace(old, new)

# LABEL_STYLE and is_label directly after class OwnText.
once("\n\nclass Links(", "\n\n" + B[9].rstrip("\n") + "\n\n\nclass Links(")
# MarkdownAndWord edits named in the prose.
once('labelled = [b for b in self.boxes(doc_id) if "QuestionLabel" in b[1]]',
     "labelled = [b for b in self.boxes(doc_id) if is_label(b[1][0])]")
once('self.assertEqual(styles[0], "QuestionLabel")', "self.assertTrue(is_label(styles[0]))")
once("""                self.assertNotIn('w:val="QuestionLabel"', re.sub(
                    r"<w:tbl>.*?</w:tbl>", "", self.part(doc_id, "word/document.xml"), flags=re.S))""",
     r"""                self.assertNotRegex(re.sub(
                    r"<w:tbl>.*?</w:tbl>", "", self.part(doc_id, "word/document.xml"), flags=re.S),
                    r'w:val="QuestionLabel\d?"')""")
once('''                    if "QuestionLabel" not in styles:
                        continue''', '''                    if not is_label(styles[0]): continue''')
# The three probe bodies.
once(r'body = ("::: {.question #probe:parts}', r'body = ("## Part\n\n::: {.question #probe:parts}')
once(r'body = "::: {.checkpoint #c}\nExchange', r'body = "## Part\n\n::: {.checkpoint #c}\nExchange')
once(r'input="::: {.question #a}\nText.\n:::\n"', r'input="## Part\n\n::: {.question #a}\nText.\n:::\n"')
# New tests at the end of MarkdownAndWord.
once("\n\n# Each lab's HTML download, measured", "\n" + B[10].rstrip("\n") + "\n\n\n# Each lab's HTML download, measured")
f.write_text(t, encoding="utf-8", newline="\n")

f = tree / "tests/test_check_numbers.py"
t = f.read_text(encoding="utf-8")
once('\n\n\nif __name__ == "__main__":', "\n\n" + B[13].rstrip("\n") + '\n\n\nif __name__ == "__main__":')
f.write_text(t, encoding="utf-8", newline="\n")
