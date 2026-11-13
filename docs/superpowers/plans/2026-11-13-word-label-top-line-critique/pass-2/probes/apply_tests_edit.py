import re, sys
p = 'tests/test_downloads.py'
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
print("newline", repr(nl))
s = s.replace('\r\n', '\n')

new_labelled = r'''    # D-0180: a label paragraph, then directly its box's table.
    LABEL_BEFORE_BOX = re.compile(
        r'(<w:p><w:pPr><w:pStyle w:val="(QuestionLabel[3-5])" ?/>(?:(?!</w:p>).)*</w:p>)\s*(<w:tbl>.*?</w:tbl>)',
        re.S)

    def labelled(self, doc_id):
        """Each label paragraph and the table right after it: (its XML, its
        style, its text, the table's XML, the table's paragraphs' texts)."""
        out = []
        for para, style, tbl in self.LABEL_BEFORE_BOX.findall(self.part(doc_id, "word/document.xml")):
            text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", para))
            texts = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
                     for p in re.findall(r"<w:p\b.*?</w:p>", tbl, re.S)]
            out.append((para, style, text, tbl, texts))
        return out
'''
i = s.index('    def boxes(self, doc_id):')
j = s.index('    def test_word_questions_are_one_cell_tables')
s = s[:i] + new_labelled + '\n' + s[j:]

i = s.index('    def test_word_questions_are_one_cell_tables')
j = s.index('    def test_word_box_is_the_modern_block')
t1 = r'''    def test_word_questions_are_one_cell_tables(self):
        # D-0082 (amends D-0057): each question is one table of one cell
        # holding its words, so a list or a bullet between parts sits inside
        # the box. D-0180 (amends D-0082): its Question Label paragraph
        # ("Question N") sits directly before the table, outside every
        # table, since Word's Navigation pane leaves out a heading in a
        # table cell; in document order.
        for doc_id, source in converted():
            text = source.read_text(encoding="utf-8")
            numbers = question_numbers(text)
            count = len(numbers)
            doc = self.part(doc_id, "word/document.xml")
            with self.subTest(doc=doc_id, questions=count):
                labelled = self.labelled(doc_id)
                self.assertEqual(len(re.findall(r'<w:pStyle w:val="QuestionLabel\d"', doc)), len(labelled),
                                 "every label sits directly before its box")
                # A checkpoint is its own box, labelled on its own count
                # (D-0112, D-0115); the questions keep Word's numbers.
                boxes = [b for b in labelled if b[2].startswith("Question ")]
                checkpoints = [b for b in labelled if b[2].startswith("Checkpoint ")]
                self.assertEqual(len(boxes) + len(checkpoints), len(labelled))
                self.assertEqual([b[2] for b in checkpoints],
                                 ["Checkpoint {}".format(k) for k in range(1, checkpoint_count(text) + 1)])
                for _, _, _, tbl, texts in checkpoints:
                    self.assertEqual(len(re.findall(r"<w:tc>", tbl)), 1)
                    self.assertTrue(any(texts), "the checkpoint's words are in the box")
                self.assertEqual(len(boxes), count)
                self.assertTrue(count or doc_id in COURSE_WIDE)
                for n, (_, _, label, tbl, texts) in zip(numbers, boxes):
                    self.assertEqual(len(re.findall(r"<w:tc>", tbl)), 1)
                    self.assertEqual(label, "Question {}".format(n))
                    self.assertTrue(any(texts), "the question's words are in the box")
                self.assertNotRegex("".join(re.findall(r"<w:tbl>.*?</w:tbl>", doc, re.S)),
                                    r'w:val="QuestionLabel\d?"')

'''
s = s[:i] + t1 + s[j:]

old_start = s.index('                for tbl, styles, texts in self.boxes(doc_id):')
old_end = s.index('                label = self.style(doc_id, "QuestionLabel")')
loop = r'''                # D-0180: the label is the box's top line, in the box's
                # colours, and label to label is as before: the box's top
                # padding plus the label's space after equals the label's
                # top border and its space plus the cell's top margin.
                padding = round(float(re.search(r"\.question, \.checkpoint \{[^}]*padding: ([\d.]+)rem",
                                                _MODERN).group(1)) / 1.0625 * 12 * 20)
                after = int(re.search(r'<w:spacing\b[^>]*\bw:after="(\d+)"',
                                      self.style(doc_id, "QuestionLabel")).group(1))
                labelled = self.labelled(doc_id)
                # Without this the loop passes on a file whose labels are
                # missing (executing critique 1, finding 2).
                self.assertTrue(labelled or doc_id in COURSE_WIDE, "no label sits before a box")
                for para, _, text, tbl, _ in labelled:
                    # A checkpoint's box takes its own palette (D-0115).
                    edge, behind = (rule, fill) if text.startswith("Checkpoint ") else (accent, tint)
                    self.assertRegex(tbl, r'<w:left w:val="single" w:sz="24" w:space="0" w:color="{}"/>'.format(edge))
                    self.assertRegex(tbl, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(behind))
                    self.assertIn("<w:cantSplit/>", tbl)
                    self.assertIn('<w:tblW w:w="{}" w:type="dxa"/>'.format(page - left - right), tbl)
                    self.assertRegex(para, r'<w:left w:val="single" w:sz="24"(?=[^>]*\bw:color="{}")'.format(edge))
                    self.assertRegex(para, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(behind))
                    for side in ("top", "right"):
                        self.assertRegex(para, r'<w:{} w:val="single"(?=[^>]*\bw:color="{}")'.format(side, behind))
                    top = re.search(r'<w:top w:val="single" w:sz="(\d+)" w:space="(\d+)"', para)
                    cell = int(re.search(r'<w:tblCellMar><w:top w:w="(\d+)"', tbl).group(1))
                    self.assertEqual(int(top.group(1)) * 20 // 8 + int(top.group(2)) * 20 + cell, padding + after)
'''
s = s[:old_start] + loop + s[old_end:]

s = s.replace('word = [int(b[1][0][-1]) for b in self.boxes(doc_id) if is_label(b[1][0])]',
              'word = [int(style[-1]) for _, style, _, _, _ in self.labelled(doc_id)]')

i = s.index('        checkpoint, question = re.findall(r"<w:tbl>.*?</w:tbl>", doc, re.S)')
j = s.index('    def test_word_box_without_its_colours_fails')
cp = r'''        (cp_label, _, cp_box), (q_label, _, q_box) = self.LABEL_BEFORE_BOX.findall(doc)
        fill, rule = (MODERN_ROOT[k].lstrip("#").upper() for k in ("--checkpoint-fill", "--checkpoint-rule"))
        self.assertIn("Checkpoint 1", cp_label)
        for part in (cp_box, cp_label):
            self.assertRegex(part, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(fill))
            self.assertRegex(part, r'<w:left\b(?=[^>]*\bw:color="{}")'.format(rule))
        self.assertIn("Question 1", q_label)
        self.assertIn("Why?", q_box)
        for part in (q_box, q_label):
            self.assertRegex(part, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(MODERN_ROOT["--tint"].lstrip("#").upper()))

'''
s = s[:i] + cp + s[j:]
old_c = '''        # D-0110, D-0115: "Checkpoint 1" in a one-cell table with the light
        # page's Candela fill and Luminance rule, then "Question 1" in the
        # question's own colours.'''
assert old_c in s
s = s.replace(old_c, '''        # D-0110, D-0115, D-0180: "Checkpoint 1" before a one-cell table
        # with the light page's Candela fill and Luminance rule, then
        # "Question 1" in the question's own colours.''')
old_l = '''LABEL_STYLE = re.compile(r"QuestionLabel[3-5]")


def is_label(style):
    return bool(style and LABEL_STYLE.fullmatch(style))


'''
assert old_l in s
s = s.replace(old_l, '')
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
