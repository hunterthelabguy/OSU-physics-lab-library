KEEP = "Kept words before.\n\n"
CUT = ("# Cut Heading\n\nCut words with $x = 1$ inside.\n\n![Cut dot](dot.png)\n\n"
       + table([10, 45, 45]) + "\n1. First cut item\n2. Second cut item\n\n")
TAIL = "# Next Heading\n\nKept words after.\n"
REPEATED = "Repeated\n\nFirst words.\n\nRepeated\n\nSecond words.\n"


def span_front(*spans, ledger=True):
    """Front matter declaring span omissions; each span a dict of strings."""
    out = "ruled_omissions:\n"
    for s in spans:
        out += "  - span:\n" + "".join('      {}: "{}"\n'.format(k, v) for k, v in s.items())
        if ledger:
            out += '    ledger: "D-0189"\n'
    return out


class Spans(unittest.TestCase):
    """D-0189: a declared span of the original is left out of every comparison."""

    setUp, tearDown = WordCheck.setUp, WordCheck.tearDown
    original, check, assertFails = WordCheck.original, WordCheck.check, WordCheck.assertFails

    def test_span_left_out_passes(self):
        front = span_front({"from": "Cut Heading", "to": "Next Heading"})
        n, problems = self.check(KEEP + CUT + TAIL, KEEP + TAIL, front=front)
        self.assertEqual(problems, [])
        self.assertEqual((n["equations"], n["pictures"]), (0, 0))

    def test_span_kept_fails(self):
        # The Markdown still holds the declared span's words.
        _, problems = self.check(KEEP + "Cut words.\n\n" + TAIL, KEEP + "Cut words.\n\n" + TAIL,
                                 front=span_front({"from": "Cut words.", "to": "Next Heading"}))
        self.assertTrue(any("insert" in p for p in problems), problems)

    def test_span_partly_kept_fails(self):
        front = span_front({"from": "Cut Heading", "to": "Next Heading"})
        _, problems = self.check(KEEP + CUT + TAIL,
                                 KEEP + "Cut words with $x = 1$ inside.\n\n" + TAIL, front=front)
        self.assertTrue(problems)

    def test_from_the_start_passes(self):
        _, problems = self.check(KEEP + CUT + TAIL, TAIL,
                                 front=span_front({"to": "Next Heading"}))
        self.assertEqual(problems, [])

    def test_to_the_end_passes(self):
        _, problems = self.check(KEEP + TAIL, KEEP,
                                 front=span_front({"from": "Next Heading"}))
        self.assertEqual(problems, [])

    def test_unmatched_edge_stops(self):
        with self.assertRaises(SystemExit) as stop:
            self.check(KEEP + TAIL, KEEP, front=span_front({"from": "No Such Paragraph"}))
        self.assertIn("matches no paragraph", str(stop.exception))

    def test_ambiguous_edge_stops(self):
        with self.assertRaises(SystemExit) as stop:
            self.check(REPEATED, "Repeated\n\nFirst words.\n", front=span_front({"from": "Repeated"}))
        self.assertIn("matches 2 paragraphs", str(stop.exception))

    def test_occurrence_names_the_edge(self):
        _, problems = self.check(REPEATED, "Repeated\n\nFirst words.\n",
                                 front=span_front({"from": "Repeated", "from_occurrence": "2"}))
        self.assertEqual(problems, [])

    def test_overlapping_spans_stop(self):
        with self.assertRaises(SystemExit) as stop:
            self.check(KEEP + CUT + TAIL, KEEP,
                       front=span_front({"from": "Cut Heading"}, {"from": "Next Heading"}))
        self.assertIn("overlap", str(stop.exception))

    def test_reversed_span_stops(self):
        with self.assertRaises(SystemExit) as stop:
            self.check(KEEP + CUT + TAIL, KEEP + TAIL,
                       front=span_front({"from": "Next Heading", "to": "Cut Heading"}))
        self.assertIn("no paragraph before", str(stop.exception))

    def test_a_span_needs_a_ledger(self):
        _, problems = self.check(KEEP + CUT + TAIL, KEEP + TAIL,
                                 front=span_front({"from": "Cut Heading", "to": "Next Heading"},
                                                  ledger=False))
        self.assertTrue(any("lacks a ledger reference" in p for p in problems), problems)
