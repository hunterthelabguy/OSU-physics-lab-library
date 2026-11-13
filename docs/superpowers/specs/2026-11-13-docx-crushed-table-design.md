# A table just before a question box joins it in Word: design

Status: ruled 2026-11-13 ("Leans as written" on the four calls in section 4). Written by Claude in a
side session started from the question-headings (D-0176) session, whose
Word probe found the symptom. Ledger: D-0179 (proposed). Ledger entries win
over this file. Plan and build wait for the ruling; the build ends in a
draft PR with green `verify`. Format only: no source, original or wording
changes, so no D-0168 passage.

## 1. Problem and cause

Reported: PH 211 Lab 3's Word download, opened in Word, draws the
stopwatch table (source `curriculum/ph211/ph211-uncertainty-handout.md`,
the grid table whose first column starts "The stopwatch display reads:")
with its first column one character wide: the header runs down a page a
letter at a time, the three stopwatch pictures sit in that column (one
on each of pages 5 to 7, per `pdfimages`) and do not show, and the table
fills pages 5 to 8. The file is 13 pages in Word.

Cause: the stopwatch table is followed in the source directly by Question
7's box. `tools/filters/questions.lua` writes a box as a raw one-cell
table (D-0082) and writes its spacer paragraph only **after** the box. So
in `word/document.xml` the stopwatch table's `</w:tbl>` is followed at once
by the box's `<w:tbl>`, with no paragraph between, and Word joins two
tables that touch into one. Pandoc's own Word writer already guards this
for its own tables: two Pandoc tables in a row get an empty `<w:p />`
between them (probe, Pandoc 3.10, 2026-11-13). The box is raw OpenXML, so
Pandoc never sees it as a table. The filter's comment says the gap after
the box "keeps two boxes in a row from joining into one table"; the case
of a table before a box was missed.

Why the joined table draws its first column that narrow is Word's own
layout and not known here (the joined table carries the stopwatch table's
percentage width and fixed layout over a grid that now holds a 10080-twip
one-cell row); that Word joins them, and that separating them fixes it, is
measured (1.1).

### 1.1 Evidence: bisect through Word

Desktop Word through PowerShell 5.1 COM, each file a copy in the
session scratchpad, opened read-only, `ExportAsFixedFormat(pdf, 17)`, never
saved, Word's own process stopped by its id; pages read with poppler's
`pdftotext` and `pdftoppm`. Input: PH 211 Lab 3's built `.docx` from a full
build of `main` at 6599a5f (the code `main` still runs at 6f6a6fd, a
ledger-only commit). Body children numbered from 0; child 65 is the
stopwatch table, child 66 Question 7's box.

| Variant of `word/document.xml` | Word pages | Word `Tables.Count` | `w:tbl` in the XML | Stopwatch table |
|---|---|---|---|---|
| as built | 13 | 14 | 15 | first column one character wide, pages 5 to 8 |
| split and rejoined, no change (control) | 13 | 14 | 15 | same |
| `<w:p/>` between children 65 and 66 | 10 | 15 | 15 | normal: two columns, three pictures |
| the box's own gap paragraph between them | 10 | 15 | 15 | normal |
| Question 7's box removed | 10 | 14 | 14 | normal |
| the stopwatch table removed | 9 | 14 | 14 | (gone) |

One paragraph between the two tables flips the render; Word's table count
going from 14 to 15 shows the join directly. The question-headings
session's top-line probe also rendered this table normally (10 pages): it
moved each label paragraph out of its box to just above it, which put a
paragraph between these two tables.

### 1.2 Survey: all 18 labs

The same build, all 19 Word downloads (18 labs and the PH 21X
problem-solving strategy), each rendered by Word as above.

- XML: one place in all 19 where a `</w:tbl>` is followed directly by a
  `<w:tbl>` (at any depth): PH 211 Lab 3, children 65 and 66.
- Word: `Tables.Count` equals the XML's `w:tbl` count in 18 downloads;
  PH 211 Lab 3 has one fewer (14 against 15). No download holds a nested
  table.
- Text of Word's PDFs: the longest run of one-character lines is 23 in PH
  211 Lab 3 (the crushed header) and at most 1 in every other download.

So only PH 211 Lab 3 is affected today. Any lab whose source puts a table
directly before a question or checkpoint would be.

### 1.3 What is not affected

- The lab page, the HTML download and the PDF download: HTML has no table
  joining, and the box there is a `div`.
- The word check and the number check: they read sources and originals,
  never a built download.
- The other 18 Word downloads: no table touches a box, so the fix writes
  nothing new in them.

## 2. Fix

In `questions.lua`, for Word only, a box that comes right after a table
gets the box's own gap paragraph before it as well: the same empty
paragraph, exactly 1.5rem high (339 twips), that already follows every
box. A pass after the one that writes the boxes walks each list of blocks
and inserts the gap between a Pandoc `Table` and a box's opening raw
block. The gap's text moves out of `word_box` to one constant both places
use.

Result in Word for PH 211 Lab 3: 15 tables, 10 pages, the stopwatch table
drawn whole, and 1.5rem between the table and Question 7's box, the
modern page's `margin: 1.5rem 0` on `.question`, as between two boxes.

## 3. Test

In `tests/test_downloads.py`, `MarkdownAndWord`:

1. **Probe through the filter** (as `test_word_checkpoint_is_its_own_box`
   does): a small Markdown table followed by a question, through Pandoc
   with `questions.lua` and the reference document. Two `w:tbl` elements,
   and between them exactly the gap paragraph. Independent of any lab's
   content.
2. **Every built Word download**: no `</w:tbl>` followed (whitespace
   aside) by `<w:tbl>`, anywhere in `word/document.xml`. This is the rule
   Word needs, so it also catches a shape the filter does not know (for
   example a table that ends a Div just before a box).

Both red on `main` (item 2 on PH 211 Lab 3 alone), green after. Word's
render is outside CI; the build reports it by hand (section 5).

## 4. Calls for the owner

1. **Height of the separator.** Lean: the box's own gap, 1.5rem exact, so
   a table and a box sit apart as two boxes do and as the modern page
   shows them. Cost of the alternative, Pandoc's bare `<w:p/>`: a
   paragraph in Word's Normal style whose height follows the body's line
   and spacing rules, so the space differs from every other box's for no
   reason. A near-zero (1 twip) paragraph would leave the table's bottom
   rule touching the box.
2. **Where the guard lives.** Lean: `questions.lua`, which writes the raw
   table and already writes the gap after it. Cost of the alternative, a
   post-pass in `tools/downloads.py` that puts a paragraph between any two
   touching tables in the finished `document.xml`: it would cover any raw
   table, not just boxes, but it is a second layer editing XML by pattern
   after Pandoc, for a case only the box creates today.
3. **What the filter checks.** Lean: a `Table` block directly before a
   box, nothing more. Cost of the alternative, also looking inside a Div
   that ends in a table: a few more lines for a shape no lab has; test 2
   fails if one ever appears.
4. **Test reach.** Lean: both tests in section 3. Cost of the
   alternative, only test 2: it would pass again the day PH 211 Lab 3's
   table moves, leaving the filter's rule unexercised.

## 5. Verification the build reports

- `verify` green in CI: the word check, number check, em-dash check,
  builds and tests.
- Local build compared with the `main` 6599a5f build: every Word
  download's `word/document.xml` identical except PH 211 Lab 3's, which
  differs by the one gap paragraph.
- PH 211 Lab 3's new Word download rendered by Word as in 1.1: 15 tables,
  10 pages, the table's page inspected. The owner's own check in Word and
  Google Docs stays his (Google Docs not measured here).

## 6. Critique

6.1 **Is the join really Word's rule and not this table's?** The control
row in 1.1 rules out the bisect tooling; the `Tables.Count` drop from 15
to 14 is Word reporting the join itself; Pandoc's writer carries a guard
for the same rule. Removing the box also fixes the table, so nothing in
the stopwatch table alone is at fault.

6.2 **Does the extra gap move anything else?** Only in PH 211 Lab 3, and
only by 1.5rem under the table; the page count drops because the table
stops being crushed. The other 18 downloads gain nothing (1.2), which
section 5's comparison confirms.

6.3 **Wrong layer?** The rule (Word joins touching tables) is about Word
output, and `questions.lua` is where a raw Word table is born, so the
guard sits with the thing that needs it. Pandoc guards its own tables the
same way, in its writer.

6.4 **A separator in the wrong place.** A gap between a table and a box
inside the same cell or Div is still between them in Word's body, so it is
always right where the filter puts it. The only place a gap could be
wrong is before a box that is not right after a table, and the filter
never puts one there.

6.5 **Not done here (declined, noted).** Why Word draws the joined table
this narrow; a Word render check in CI (no Word on the runner); Google
Docs import (not measured).
