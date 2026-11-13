# The Word label as the box's top line: implementation plan

**Goal:** in the Word download, every question's and checkpoint's label
sits directly before its box's table, drawn as the box's top line, so
Word's Navigation pane lists it.
**Architecture:** `tools/filters/questions.lua`'s Word branch writes the
label as a raw OpenXML paragraph (style `QuestionLabelN`, direct borders,
shading and indents in the box's colours) before the raw table that
`word_box` opens, and the cell's top margin drops so the spacing is
unchanged. Tests read the Word XML; Word's own render is checked on this
machine after the task.
**Spec:** `docs/superpowers/specs/2026-11-13-word-label-top-line-design.md`;
ledger D-0180 (proposed; ruled in chat 2026-11-13, see the spec's section 2).
**Verify:** with `PANDOC`, `QUARTO`, `CHROME`, `PDFTOTEXT` exported as in
CLAUDE.md "Which Pandoc": `python tools/check_em_dash.py`; the converted
files' `python tools/check_unchanged.py $files` and
`python tools/check_numbers.py $files` (the loop in
`.github/workflows/verify.yml`); `python tools/quarto_build.py`;
`python -m unittest discover -s tests`.

## Global constraints

- Word only. The page, the HTML download, the PDF and `tools/reference.docx`
  do not change.
- The label paragraph: `<w:pStyle w:val="QuestionLabelN"/>` (N = 3 to 5,
  D-0176), then `<w:pBdr>` top single `sz` 4 space 9 in the fill, left
  single `sz` 24 space 9 in the rule, right single `sz` 4 space 11 in the
  fill; `<w:shd>` the fill; spacing before 0 after 0; indent left 238,
  right 258, first line 10. Values measured in Word's render (spec 3).
- The box's cell top margin is 92 twips (was `twips(.9)` = 203).
- A checkpoint uses `checkpoint-rule` / `checkpoint-fill`, a question
  `box-rule` / `box-fill`, for its label as for its box.
- The box's row keeps `<w:cantSplit/>`; nothing else in the box changes.
- No source changes (D-0168). Commit as hunterthelabguy with the noreply
  email, no trailer; subjects <=72 characters.

## Files

| File | Responsibility | Task |
|---|---|---|
| `tools/filters/questions.lua` | label paragraph before the box; cell top margin | T1 |
| `tests/test_downloads.py` (class `MarkdownAndWord`) | label before box, its drawing, the spacing sum, levels, the checkpoint probe | T1 |
| `DECISIONS.md` (D-0180 `test:`) | the tests as built | after T1 |
| `docs/superpowers/plans/2026-11-13-word-label-top-line-probes/` | the Word probes and render checks, committed as evidence (no personal paths) | already in |

`tools/check_numbers.py` is untouched: it renders to JSON, where the Word
branch never runs. `test_word_body_is_the_modern_words` holds as is: the
label's words still come before the stem's.

One task: the filter change and its tests are one cycle a reviewer
accepts or rejects whole.

Revision 1 (2026-11-13) folds executing critique 1 (read 0f2e222; report
and patches in `2026-11-13-word-label-top-line-critique/pass-1/`): the
build before the red step, the box test's own guard, the grep's `-r`,
comment widths, the pane probe expanding every entry, the row scan through
the seam, and the probe's indents as arguments. Two findings go to the
owner: 78 of 194 stems take Pandoc's First Paragraph style once a raw
label precedes them (drawn the same: it is based on Body Text with nothing
of its own), and the label's rule starts 0.48 pt below its tint. Optional
pins of the indents and border spaces in CI are not taken: the spec's
tests hold the colours and the spacing sum, and Word's render holds the
edges (spec section 7).

### T1: The Word label leaves the box and becomes its top line

**Depends on:** none (branch `word-label-top`, on `question-headings`)
**Files:** modify `tools/filters/questions.lua`; test `tests/test_downloads.py`
**Seams:** the built `.docx` via `MarkdownAndWord.part` and `.style`; the
filter through Pandoc in the probe tests
**Interfaces:** produces in `test_downloads.py` `MarkdownAndWord.labelled(doc_id)`
returning `[(label_xml, style_id, label_text, table_xml, table_paragraph_texts)]`
**Verify:** `python -m unittest tests.test_downloads.MarkdownAndWord.test_word_checkpoint_is_its_own_box -v`,
then build and `python -m unittest tests.test_downloads.MarkdownAndWord tests.test_check_numbers.Filter -v`

- [ ] Build the unchanged filter first (`python tools/quarto_build.py`):
  `tests/test_downloads.py`'s `setUpModule` raises "build/quarto-site is
  missing" for every test in the module, the probe tests included, and a
  fresh worktree has no build.
- [ ] Tests first. In `tests/test_downloads.py`, class `MarkdownAndWord`,
  after `boxes`, add:

```python
    # D-0180: a label paragraph, then directly its box's table.
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
```

  Replace `test_word_questions_are_one_cell_tables` with:

```python
    def test_word_questions_are_one_cell_tables(self):
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
```

  In `test_word_box_is_the_modern_block`, replace the loop
  `for tbl, styles, texts in self.boxes(doc_id): ... self.assertIn('<w:tblW ...', tbl)`
  with the loop below, and leave the `label = self.style(...)` lines after
  it as they are (the style itself still has no border or shading):

```python
                # D-0180: the label is the box's top line, in the box's
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
```

  `round(.9 / 1.0625 * 12 * 20)` is 203, the filter's `twips(.9)`; with
  the reference's 79 the sum is 282.

  In `test_word_label_levels_match_the_page`, replace the `word = ...`
  line with:

```python
                word = [int(style[-1]) for _, style, _, _, _ in self.labelled(doc_id)]
```

  Replace the body of `test_word_checkpoint_is_its_own_box` from
  `checkpoint, question = ...` to its end with:

```python
        (cp_label, _, cp_box), (q_label, _, q_box) = self.LABEL_BEFORE_BOX.findall(doc)
        fill, rule = (MODERN_ROOT[k].lstrip("#").upper() for k in ("--checkpoint-fill", "--checkpoint-rule"))
        self.assertIn("Checkpoint 1", cp_label)
        for part in (cp_box, cp_label):
            self.assertRegex(part, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(fill))
            self.assertRegex(part, r'<w:left\b(?=[^>]*\bw:color="{}")'.format(rule))
        self.assertIn("Question 1", q_label)
        self.assertIn("Why?", q_box)
        for part in (q_box, q_label):
            self.assertRegex(part, r'<w:shd\b(?=[^>]*\bw:fill="{}")'.format(MODERN_ROOT["--tint"].lstrip("#").upper()))
```

  and update its comment's first two lines to
  `# D-0110, D-0115, D-0180: "Checkpoint 1" before a one-cell table` /
  `# with the light page's Candela fill and Luminance rule, then`, the
  rest as it is, each line under 80 columns as in the file.

  Delete `boxes` (class `MarkdownAndWord`), `LABEL_STYLE` and `is_label`
  (module level): their three callers are the tests replaced above, and
  `grep -rn "is_label\|\.boxes(\|LABEL_STYLE" tests/` then prints nothing.

- [ ] Run `python -m unittest tests.test_downloads.MarkdownAndWord.test_word_checkpoint_is_its_own_box -v`;
  expected failure: `ValueError: not enough values to unpack (expected 2, got 0)`
  (no label paragraph sits before a table yet). Then
  `python -m unittest tests.test_downloads.MarkdownAndWord -v` on that
  build: `test_word_questions_are_one_cell_tables` fails "every label sits
  directly before its box", and `test_word_box_is_the_modern_block` fails
  on its own guard (below).

- [ ] Filter. In `tools/filters/questions.lua`, replace the comment above
  `word_box` and the function with:

```lua
-- .question { padding: .9rem 1.1rem .1rem; border-left: 4px; margin: 1.5rem 0 }:
-- the padding as cell margins, the rule as a 3 pt left border on the text
-- column's edge, and an empty paragraph after it for the bottom margin,
-- which also keeps two boxes in a row from joining into one table.
-- D-0180: the label sits directly before the table, since Word's Navigation
-- pane leaves out any heading in a table cell, drawn as the box's top line
-- by direct formatting (questions and checkpoints differ in colour): the
-- rule as its left border, the tint as its shading and as top and right
-- borders, so the shading reaches the box's edges. Spaces and indents land
-- the rule and the tint's edge on the box's, measured in Word's render at
-- 300 dpi (spec 2026-11-13, section 3).
-- The cell's top margin under the label: the box's top padding, twips(.9)
-- = 203, plus Question Label's space after, 79, as before, less the
-- label's top border (0.5 pt, 10) and its space (9 pt, 180).
local CELL_TOP = 92

local function word_label(text, level, rule, fill)
  return pandoc.RawBlock("openxml", '<w:p><w:pPr><w:pStyle w:val="QuestionLabel' .. level .. '"/>'
    .. '<w:pBdr><w:top w:val="single" w:sz="4" w:space="9" w:color="' .. fill .. '"/>'
    .. '<w:left w:val="single" w:sz="24" w:space="9" w:color="' .. rule .. '"/>'
    .. '<w:right w:val="single" w:sz="4" w:space="11" w:color="' .. fill .. '"/></w:pBdr>'
    .. '<w:shd w:val="clear" w:color="auto" w:fill="' .. fill .. '"/>'
    .. '<w:spacing w:before="0" w:after="0"/><w:ind w:left="238" w:right="258" w:firstLine="10"/></w:pPr>'
    .. '<w:r><w:t xml:space="preserve">' .. text .. '</w:t></w:r></w:p>')
end

local function word_box(text, level, blocks, rule, fill, kind)
  if not rule or not fill then
    error("the Word " .. kind .. " box needs its colours; tools/downloads.py passes them")
  end
  local side = twips(1.1)
  local open = '<w:tbl><w:tblPr><w:tblW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:tblInd w:w="' .. side .. '" w:type="dxa"/><w:tblBorders>'
    .. '<w:top w:val="nil"/><w:left w:val="single" w:sz="24" w:space="0" w:color="' .. rule .. '"/>'
    .. '<w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
    .. '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar>'
    .. '<w:top w:w="' .. CELL_TOP .. '" w:type="dxa"/><w:left w:w="' .. side .. '" w:type="dxa"/>'
    .. '<w:bottom w:w="' .. twips(.1) .. '" w:type="dxa"/><w:right w:w="' .. side .. '" w:type="dxa"/>'
    .. '</w:tblCellMar><w:tblLook w:val="0000"/></w:tblPr>'
    .. '<w:tblGrid><w:gridCol w:w="' .. TEXT_WIDTH .. '"/></w:tblGrid>'
    .. '<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:shd w:val="clear" w:color="auto" w:fill="' .. fill .. '"/></w:tcPr>'
  local gap = '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="' .. twips(1.5)
    .. '" w:lineRule="exact"/></w:pPr></w:p>'
  local out = { word_label(text, level, rule, fill), pandoc.RawBlock("openxml", open) }
  for _, b in ipairs(blocks) do table.insert(out, b) end
  table.insert(out, pandoc.RawBlock("openxml", "</w:tc></w:tr></w:tbl>"))
  table.insert(out, pandoc.RawBlock("openxml", gap))
  return out
end
```

  In the Word branch, drop the label `Div` and its `table.insert`, and pass
  the label to `word_box`:

```lua
      if FORMAT == "docx" then
        if level < 3 or level > 5 then
          error(kind .. " " .. name .. "'s label would be h" .. level
            .. "; tools/reference.docx has Question Label 3 to 5 only (D-0176)")
        end
        local prefix = kind == "question" and "box" or "checkpoint"
        return word_box(text, level, el.content, colours[prefix .. "-rule"], colours[prefix .. "-fill"], kind), false
      end
```

  In the header comment, replace "and the / -- label takes the Question
  Label N style of tools/reference.docx, N its / -- level, 3 to 5
  (D-0176)." with "and the / -- label, in the Question Label N style of
  tools/reference.docx (N its level, / -- 3 to 5; D-0176), sits directly
  before the box as its top line (D-0180).", rewrapped so no line passes
  the file's widest existing comment line (76 columns).

- [ ] Run the checkpoint probe test and `tests.test_check_numbers.Filter`;
  expected: pass (the colour and level errors fire before any XML is
  written, as before).
- [ ] Build (`python tools/quarto_build.py`), then
  `python -m unittest tests.test_downloads.MarkdownAndWord -v`; expected:
  pass, including `test_word_body_is_the_modern_words`.
- [ ] Full suite: `python -m unittest discover -s tests`; expected: all pass.
- [ ] Commit: "Word labels sit above their box as its top line (D-0180)".

## After the task (main session, not a task)

1. Simplify pass against the spec (fresh context, cap three), then the full
   Verify, green.
2. Word render checks on this machine (Word through COM, read-only copies
   in the scratchpad, never saved, stopping only the scripts' own Word
   process; the owner may have Word open), with the committed probes in
   `2026-11-13-word-label-top-line-probes/`:
   - `nav_pane.ps1` (expands every entry by pressing Right on it, so Word
     must be in front; it stops if another window is) on PH 212 Lab 1:
     Questions 1 to 16 listed; on PH 211 Lab 3: Questions 1 to 14. As
     built, PH 212 Lab 1 lists none. Word folds level-3 headings, so
     without the expansion Questions 8, 9 and 12 of PH 212 Lab 1 are
     hidden (critique 1, finding 4). If the owner opens Word while the
     probe starts, its one-new-process check stops it: rerun.
   - `word_pdf.ps1` on PH 212 Lab 1, then `edges.py` on page 3 at 300 dpi
     (`pdftoppm -r 300 -f 3 -l 3 -x 150 -y 620 -W 2400 -H 420`, rows 90
     and 250): the label's rule and the tint's right edge within 0.1 pt of
     the box's; then `edges_scan.py` on the same crop, every row through
     the seam, reporting where the rule starts against the tint's top
     (critique 1 measured the rule starting 0.48 pt below it; the owner's
     ruling on that notch is recorded in D-0180).
   - `strand_survey.ps1` and `strand_check.py` over all 18 labs, PR 76's
     build as `A.docx` and this build as `D2.docx`: exactly the two
     strandings of spec section 6.
3. D-0180's `test:` names the tests as built.
4. Draft PR on `main` after PR 76 lands (or on `question-headings` until
   then), body with the rulings, the Word checks and the owner's
   acceptance (Navigation pane, a screen reader in Word, a Google Docs
   import); green `verify`.
