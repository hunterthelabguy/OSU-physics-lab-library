"""The number check and the filter's labels (D-0078, D-0102, D-0109, D-0110, D-0112).

Fixture originals are made by Pandoc at test time; their Word labels are
written here, keyed to the fixture's own parts. Two cases use the real records
of docs/word-labels.json, whose originals are not in this repo: only the
labels are compared, against a skeleton lab marked up as the spec says.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_numbers  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
PH211 = ROOT / "curriculum" / "ph211" / "ph211-team-building-handout.md"
FILTER = ROOT / "tools" / "filters" / "questions.lua"
RECORDS = json.loads((ROOT / "docs" / "word-labels.json").read_text(encoding="utf-8"))


def record(key_part):
    return next(r for k, r in RECORDS["originals"].items() if key_part in k)


def q(ident, *parts, cls="question"):
    body = "::: {." + cls + " #" + ident + "}\nText of " + ident + ".\n"
    if parts:
        body += "\n" + "\n".join(parts) + "\n"
    return body + ":::\n"


class Fixture:
    """A temp folder holding an original docx, a lab and a labels record."""

    def __init__(self, body, labels):
        self.dir = tempfile.TemporaryDirectory()
        root = Path(self.dir.name)
        src = root / "src.md"
        src.write_text("Any words.\n", encoding="utf-8")
        subprocess.run([PANDOC, str(src), "-o", str(root / "original.docx")], check=True)
        self.md = root / "lab.md"
        self.md.write_text('---\nsource_file: "original.docx"\n---\n\n' + body,
                           encoding="utf-8", newline="\n")
        self.root = root
        self.labels = {"originals": {"fixture": {
            "parts_sha256": check_numbers.parts_sha256(root / "original.docx"),
            "labels": labels}}}

    def check(self):
        return check_numbers.check(str(self.md), str(self.root), self.labels)[1]

    def close(self):
        self.dir.cleanup()


class NumberCheck(unittest.TestCase):

    def run_fixture(self, body, labels):
        f = Fixture(body, labels)
        try:
            return f.check()
        finally:
            f.close()

    def test_ph211_matches_words_labels(self):
        _, problems = check_numbers.check(str(PH211))
        self.assertEqual(problems, [])

    def test_matching_numbers_pass(self):
        labels = [["o1", "1)"], ["o2", "2)"], ["o3", "3)"]]
        self.assertEqual(self.run_fixture(q("a") + q("b") + q("c"), labels), [])

    def test_a_number_differing_from_words_fails(self):
        # D-0102's test: Word says 1), 3).
        problems = self.run_fixture(q("a") + q("b"), [["o1", "1)"], ["o2", "3)"]])
        self.assertTrue(any("question number differs" in p for p in problems), problems)

    def test_item_needing_no_answer_marked_a_question_fails(self):
        # D-0078's test: Word's "0)" made a question shifts every later number.
        labels = [["o1", "0)"], ["o2", "1)"], ["o3", "2)"]]
        problems = self.run_fixture(q("a") + q("b") + q("c"), labels)
        self.assertTrue(any("question number differs" in p for p in problems), problems)

    def test_checkpoint_where_word_numbers_it_passes(self):
        labels = [["o1", "0)"], ["o2", "1)"], ["o3", "2)"]]
        body = q("a", cls="checkpoint") + q("b") + q("c")
        self.assertEqual(self.run_fixture(body, labels), [])

    def test_restart_marked_passes_and_unmarked_fails(self):
        labels = [["o1", "1)"], ["o2", "2)"], ["o3", "1)"], ["o4", "2)"]]
        marked = q("a") + q("b") + q("c", cls="question .restart") + q("d")
        self.assertEqual(self.run_fixture(marked, labels), [])
        unmarked = q("a") + q("b") + q("c") + q("d")
        self.assertTrue(self.run_fixture(unmarked, labels))

    def test_parts_compare_their_letters(self):
        labels = [["o1", "1)"], ["o1.1", "a."], ["o1.2", "b."], ["o2", "2)"]]
        good = q("a", "a.  first\nb.  second") + q("b")
        self.assertEqual(self.run_fixture(good, labels), [])
        # A part made its own question (S10, Pandoc's misread) fails.
        bad = q("a", "a.  first") + q("b") + q("c")
        self.assertTrue(self.run_fixture(bad, labels))
        # Letters restarting at a. where Word continues fail.
        split = q("a", "a.  first\n\nText between.\n\na.  second") + q("b")
        problems = self.run_fixture(split, labels)
        self.assertTrue(any("part label differs" in p for p in problems), problems)

    def test_anchor_outside_the_question_lists_fails(self):
        problems = self.run_fixture(q("a"), [["o1", "1)"], ["x1", "1."]])
        self.assertTrue(any("x1" in p for p in problems), problems)

    def test_no_record_for_the_original_fails(self):
        f = Fixture(q("a"), [["o1", "1)"]])
        try:
            f.labels["originals"]["fixture"]["parts_sha256"]["word/document.xml"] = "0" * 64
            problems = f.check()
        finally:
            f.close()
        self.assertTrue(any("no record" in p for p in problems), problems)


class RealRecords(unittest.TestCase):
    """Skeleton labs marked up as the spec says, against Word's real labels."""

    def labels_of(self, body):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "lab.md"
            md.write_text(body, encoding="utf-8", newline="\n")
            return check_numbers.rendered_items(str(md))

    def test_ph213_lab6_checkpoints_and_week_restart(self):
        # D-0109, D-0110: "0)" and Week 3's "1)" are checkpoints.
        body = (q("contacts", cls="checkpoint") + q("q1")
                + q("q2", "a.  one\nb.  two\nc.  three")
                + q("w2q1", cls="question .restart") + q("w2q2") + q("w2q3")
                + q("w2q4") + q("w2q5") + q("slides", cls="checkpoint"))
        items = self.labels_of(body)
        self.assertEqual(check_numbers.compare(record("PH213/Handouts/Lab 6")["labels"], items), [])
        shown = [i[2] for i in items if i[1] != "part"]
        self.assertEqual(shown[:3], ["Checkpoint 1", "Question 1", "Question 2"])
        self.assertEqual(shown[-1], "Checkpoint 2")

    def test_ph212_lab6_restart_and_three_levels(self):
        five = "a.  1\nb.  2\nc.  3\nd.  4\ne.  5"
        body = (q("q1", five) + q("q2", "a.  1\nb.  2\nc.  3") + q("q3", five) + q("q4")
                + q("w2q1", "a.  1\nb.  2", cls="question .restart") + q("w2q2")
                + q("w2q3", "a.  1\nb.  2\nc.  3") + q("w2q4", "a.  1\nb.  2")
                + q("w2q5", "a.  1\nb.  2\n\n    i.  x\n    ii. y") + q("w2q6"))
        items = self.labels_of(body)
        self.assertEqual(check_numbers.compare(record("PH212/Handouts/Lab 6")["labels"], items), [])


class Filter(unittest.TestCase):

    def render(self, body, *args):
        return subprocess.run([PANDOC, "-f", "markdown-smart", "--lua-filter", str(FILTER), *args],
                              input=body, capture_output=True, encoding="utf-8")

    def test_modern_unbolds_the_whole_block(self):
        body = ("::: {.question #a}\n**Stem.**\n\n**Second paragraph.**\n\n"
                "a.  **A part.**\n\n::: action\n- **An action.**\n:::\n:::\n\n**Outside.**\n")
        out = self.render(body, "-t", "html").stdout
        self.assertEqual(out.count("<strong>"), 1, out)
        self.assertIn("<strong>Outside.</strong>", out)

    def test_faithful_keeps_bold_and_prefix(self):
        out = self.render("::: {.question #a}\n**Stem.**\n:::\n", "-t", "html",
                          "-M", "theme-name=faithful").stdout
        self.assertIn("<strong>1) </strong><strong>Stem.</strong>", out)

    def test_checkpoint_before_two_questions(self):
        # D-0109's and D-0110's test.
        body = q("c", cls="checkpoint") + q("a") + q("b")
        out = self.render(body, "-t", "html").stdout
        order = [out.index(s) for s in ("Checkpoint 1", "Question 1", "Question 2")]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("Question 3", out)
        self.assertIn('class="checkpoint-label"', out)

    def test_question_not_opening_with_a_paragraph_fails(self):
        # D-0082 (F14(a)): today it would be counted and left unlabelled.
        for body in ("::: {.question #a}\n- a list first\n:::\n",
                     "::: {.checkpoint #c}\n- a list first\n:::\n",
                     "::: {.question #a}\n:::\n"):
            with self.subTest(body=body):
                r = self.render(body, "-t", "html")
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("must open with a paragraph", r.stderr)


if __name__ == "__main__":
    unittest.main()
