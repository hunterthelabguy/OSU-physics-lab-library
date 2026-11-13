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

    def test_anchor_outside_the_question_lists_with_nothing_to_meet_fails(self):
        problems = self.run_fixture(q("a"), [["o1", "1)"], ["x1", "1."]])
        self.assertTrue(problems)
        self.assertTrue(any("x1" in p for p in problems), problems)

    def test_second_list_parts_compare_by_label(self):
        # D-0122 (1): PH 211 Lab 3's x1 to x3, a question's parts drawn from
        # a second list.
        labels = [["o1", "1)"], ["x1", "a."], ["x2", "b."], ["o2", "2)"]]
        self.assertEqual(self.run_fixture(q("a", "a.  one\nb.  two") + q("b"), labels), [])
        wrong = [["o1", "1)"], ["x1", "a."], ["x2", "c."], ["o2", "2)"]]
        problems = self.run_fixture(q("a", "a.  one\nb.  two") + q("b"), wrong)
        self.assertTrue(any("x2" in p and "label differs" in p for p in problems), problems)

    def test_report_item_list_compares_by_label(self):
        # D-0122 (2): PH 211 Lab 6's x1 to x4, bold report items (S11).
        labels = [["o1", "1)"], ["x1", "1."], ["x2", "2."], ["o2", "2)"]]
        body = q("a") + "::: report-item\n1.  **First.**\n2.  **Second.**\n:::\n\n" + q("b")
        self.assertEqual(self.run_fixture(body, labels), [])
        # Unmarked, the list is not read and Word's x1, x2 meet question 2.
        unmarked = q("a") + "1.  **First.**\n2.  **Second.**\n\n" + q("b")
        self.assertTrue(self.run_fixture(unmarked, labels))
        # A report item's list where Word's question list numbers fails.
        wrong = [["o1", "1)"], ["o1.1", "a."], ["o2", "2)"]]
        problems = self.run_fixture(q("a") + "::: report-item\na.  x\n:::\n\n" + q("b"), wrong)
        self.assertTrue(any("report item" in p for p in problems), problems)

    def test_numbered_list_names_its_anchors(self):
        # D-0122 (3): PH 211 Lab 3's appendix contents, o14.0.1 and o14.0.2.
        labels = [["o1", "1)"], ["o1.0.1", "1."], ["o1.0.2", "2."]]
        good = q("a") + '::: {.numbered anchors="o1.0.1 o1.0.2"}\n1.  One\n2.  Two\n:::\n'
        self.assertEqual(self.run_fixture(good, labels), [])
        for body, said in (
                (q("a") + '::: {.numbered anchors="o1.0.1 o1.0.2"}\nA.  One\nB.  Two\n:::\n', "label differs"),
                (q("a") + '::: {.numbered anchors="o1.0.1 o1.0.2"}\n1.  One\n:::\n', "list ends first"),
                (q("a") + '::: {.numbered anchors="o1.0.1"}\n1.  One\n2.  Two\n:::\n', "no anchor named"),
                (q("a") + '::: {.numbered anchors="o1.0.1 o1.0.9"}\n1.  One\n2.  Two\n:::\n', "do not have"),
                (q("a") + "1.  One\n2.  Two\n", "to place")):
            with self.subTest(said=said):
                problems = self.run_fixture(body, labels)
                self.assertTrue(any(said in p for p in problems), problems)

    def test_real_ph211_lab3_and_lab6_skeletons(self):
        # Word's real labels against skeletons marked up as D-0122 says.
        lab3 = (q("q1") + q("q2") + q("q3") + q("q4") + q("q5") + q("q6") + q("q7") + q("q8")
                + q("q9", "a.  x") + q("q10", "a.  x\nb.  y") + q("q11", "a.  x\nb.  y") + q("q12")
                + q("q13", "a.  x\nb.  y\nc.  z") + q("q14")
                + '::: {.numbered anchors="o14.0.1 o14.0.2"}\n1.  Plots\n2.  Linearization\n:::\n')
        lab6 = (q("q1", "a.  x\nb.  y") + q("q2") + q("q3") + q("q4")
                + "::: report-item\n1.  **a**\n2.  **b**\n3.  **c**\n4.  **d**\n:::\n\n"
                + q("q5") + q("q6", "a.  x\nb.  y\nc.  z") + q("q7", "a.  x\nb.  y"))
        for key, body in (("PH211/Handouts/Lab 3", lab3), ("PH211/Handouts/Lab 6", lab6)):
            with self.subTest(lab=key), tempfile.TemporaryDirectory() as d:
                md = Path(d) / "lab.md"
                md.write_text(body, encoding="utf-8", newline="\n")
                items = check_numbers.rendered_items(str(md))
                self.assertEqual(check_numbers.compare(record(key)["labels"], items), [])

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

    def test_a_redacted_record_carries_its_originals_labels(self):
        # D-0133: redaction changes document.xml, so a redacted original gets
        # its own record, keyed to its parts, naming the record Word read.
        by_sha = {r["sha256"]: r for r in RECORDS["originals"].values()}
        for key, r in RECORDS["originals"].items():
            if "redacted_from" in r:
                with self.subTest(key=key):
                    self.assertIn(r["redacted_from"], by_sha)
                    self.assertEqual(r["labels"], by_sha[r["redacted_from"]]["labels"])
                    self.assertNotEqual(r["parts_sha256"],
                                        by_sha[r["redacted_from"]]["parts_sha256"])


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

    def test_label_is_a_heading_one_below_its_section(self):
        # D-0176: the label is a heading one level below the last heading
        # before it; a body with none sits under the page's H1.
        body = "\n".join([q("z"), "## Week 1\n", q("a"), "### Part A\n", q("b"),
                          "#### Deep\n", q("c"), "## Week 2\n", q("d", cls="checkpoint")])
        out = self.render(body, "-t", "html").stdout
        for tag in ('<h2 class="question-label">Question 1</h2>',
                    '<h3 class="question-label">Question 2</h3>',
                    '<h4 class="question-label">Question 3</h4>',
                    '<h5 class="question-label">Question 4</h5>',
                    '<h3 class="checkpoint-label">Checkpoint 1</h3>'):
            self.assertIn(tag, out)
        self.assertNotIn("<p>Question", out)
        # A Div opening with a heading is written as a <section> carrying
        # the heading's class (Pandoc 3.10); the box stays a div (spec 8.1).
        self.assertIn('<div id="a" class="question">', out)
        self.assertNotIn("<section", out)

    def test_heading_in_a_box_is_not_a_section(self):
        # D-0176: a heading inside a question's box leaves the section as
        # it was, so the next question's label keeps the same level.
        body = "\n".join(["## Week 1\n", q("a", "::: box\n#### Box title\n\nWords.\n:::"), q("b")])
        out = self.render(body, "-t", "html").stdout
        self.assertIn('<h3 class="question-label">Question 1</h3>', out)
        self.assertIn('<h3 class="question-label">Question 2</h3>', out)

    def test_label_past_h6_fails(self):
        out = self.render("###### Six\n\n" + q("a"), "-t", "html")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("h7", out.stderr)

    def test_word_label_outside_h3_to_h5_fails(self):
        # D-0176 ("Keep three"): Word has Question Label 3 to 5; an h2
        # label (no section above it) or an h6 one has no style, so the
        # render stops.
        for body in (q("a"), "##### Five\n\n" + q("a")):
            with self.subTest(body=body):
                out = self.render(body, "-t", "docx", "-o", os.devnull)
                self.assertNotEqual(out.returncode, 0)
                self.assertIn("Question Label 3 to 5", out.stderr)


if __name__ == "__main__":
    unittest.main()
