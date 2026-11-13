# The Word label as the box's top line: design

Status: draft, 2026-11-13. Written by Claude in the question-headings
session, after the owner's Word check on PR 76. Ledger: D-0180 (proposed),
which amends D-0176's Word call and D-0082's box. Ledger entries win over
this file. Stacked on branch `question-headings` (PR 76); it lands as its
own PR after 76.

## 1. Problem

D-0176 gives every label in the Word download a "Question Label N" style
with an outline level, accepted only on the owner's check in Word's
Navigation pane. The owner, 2026-11-13: "Questions do not appear in the
navigation bar."

Measured the same day (shared note `word-navigation-pane-probe.md`; Word
driven read-only on copies, the pane read through UI Automation):

- Word gives each label its outline level (3, 4 or 5) under the right
  section; every label is the first paragraph of its box's one-cell table
  (D-0082).
- The pane leaves out a heading in a table cell, whatever its style. PH 212
  Lab 1: as built, no question listed (nor the in-box Heading 4 "What is
  Uncertainty?"); each label moved just above its table, same style, every
  question listed under its Part; labels left in the table with Word's
  built-in Heading 3 and 4, none listed. D-0176's fallback, Heading-based
  styles, therefore does not fix it.
- The pane opens with each level-3 heading folded; H4 and H5 entries under
  an H3 show when it is expanded (PH 211 Lab 3, Part 1: Question 1 and
  Questions 2 to 5). This is Word's own behaviour, boxed or not.

## 2. Rulings

1. The label leaves the table and is drawn as the box's top line (the
   owner, 2026-11-13: "As the box's top line"), against a plain label above
   the box.
2. The box's row stays unsplittable (D-0082), and the labels it strands are
   accepted: the owner, 2026-11-13, "I'd really rather avoid boxes splitting
   across pages if possible", then to landing this first with the two
   stranded labels accepted, "Yes, fix first".
3. Answer areas under the questions, raised the same day, are their own
   change after this one; they will move every page, and the strandings are
   counted again then (section 6).

## 3. Design (Word only)

`tools/filters/questions.lua`, Word branch: the label paragraph is written
directly before the box's table instead of as the cell's first paragraph.
The rest of the box is unchanged: same table, same rule, tint, width,
`cantSplit` row and gap after it.

The label paragraph keeps its style, `Question Label N` (D-0176), and gains
direct formatting that draws it as the box's top line. Every number below
was measured in Word's own render of PH 212 Lab 1 at 300 dpi (section 7)
or derives from the box's existing numbers:

| Property | Value | Why |
|---|---|---|
| left border | single, `sz` 24 (3 pt), the box's rule colour | the box's rule |
| left indent, first line | 238 twips, first line +10 | the rule lands on the box's (border space moves it in whole points; 9 pt left it 0.48 pt right, 10 pt 0.48 pt left), the text stays at 248 |
| left border space | 9 pt | with the indent above |
| shading | the box's tint | the box's fill |
| top border | single, `sz` 4 (0.5 pt), in the tint, space 9 pt | the box's top padding, shaded |
| right border | single, `sz` 4, in the tint, space 11 pt; right indent 258 twips | the tint ends at the box's right edge (space 12 pt overshot 1.68 pt, 11 pt 0.48 pt) |
| spacing before, after | 0, 0 | the table follows at once |
| keep with next | from the style (`Question Label`) | label and box move together |

The box's cell top margin drops from 203 twips (`twips(.9)`) to 92, so the
distance from one label to the next is unchanged: as built, 203 (cell top)
+ 79 (the label's space after) = 282 twips above the stem; now 10 (top
border) + 180 (its space) + 92 (cell top) = 282. Measured: Question 2 to
Question 3 labels 112.11 pt apart in both. The filter cannot read the
reference's styles, so it writes 92 with the sum in a comment, and a test
holds the sum against the reference's `Question Label` spacing after
(section 7, test 2).

A checkpoint takes its own colours (D-0115), as its box does.

## 4. What does not change

The lab page, the HTML download and the PDF (none uses the Word branch);
`tools/reference.docx` and its styles (`test_word_label_styles_add_only_an_outline_level`
still holds: the drawing is direct formatting, since the colours differ
between questions and checkpoints); the box's table, colours and
`cantSplit`; the headings inside a box (PH 212 Lab 1 "What is
Uncertainty?", Lab 2 "Assumptions:"), which stay in the table and out of
the pane, since moving them out would split the box; Word's folding of
level-3 headings.

One change inside the box, found by executing critique 1 and put to the
owner, who accepted it (D-0180): Pandoc gives the paragraph after a heading its "First Paragraph"
style, and a raw paragraph does not reset that, so in 78 of 194 boxes (those
directly under a section heading) the stem's style changes from Body Text
to First Paragraph. In `tools/reference.docx` First Paragraph is based on
Body Text with nothing of its own, so Word draws it the same (the stem rows
measured identical); it shows only in Word's style box. Pandoc already
gives it to every paragraph after a heading outside the boxes.

## 5. WCAG

1.3.1 and 2.4.10: met in Word as on the page, the labels now navigable
headings in the pane (screen readers in Word: the owner's check, not yet
measured). 1.4.3: colours unchanged. 2.4.6: unchanged (D-0176's name).

## 6. Pagination

All 18 labs rendered by Word as built and with this design (36 PDFs, probe
D2 with the cell margin and top spacing above): stranded labels, a page
ending on a label, as built 0, this design 2 of 194: PH 211 Designing an
Experiment p. 3 Question 1, PH 212 Lab 1 p. 4 Question 4. In both, label
and box together exceed a page and the box alone does not; the row cannot
split, so it moves and leaves the label (PH 212 Lab 1's page 4 holds only
"QUESTION 4"). Accepted (ruling 2). Page counts otherwise as built but
PH 212 Lab 1 (+1, the stranding) and PH 211 Lab 3 (13 to 10, see section 8).

## 7. Tests and checks

In CI, reading the Word XML (the tests can read nothing else):

1. `test_word_questions_are_one_cell_tables` becomes: each label paragraph
   is outside every table and directly followed by its box's `<w:tbl>`;
   the box holds the question's words; labels and boxes pair one to one in
   document order, numbers as today.
2. `test_word_box_is_the_modern_block` adds: the label paragraph's left
   border and shading are its box's rule and fill; its top and right
   borders are in the fill; the cell's top margin plus the label's top
   border and its space equals `twips(.9)` plus the reference's
   `Question Label` spacing after (282 twips), so a change to either side
   fails here. It also fails on its own when no label sits before a box
   (critique 1, finding 2).
3. `test_word_label_levels_match_the_page` reads labels from the new place.
4. The three probe tests (`holds_a_list_between_parts`,
   `checkpoint_is_its_own_box`, `without_its_colours_fails`) keep their
   meaning: the list test counts one table still; the checkpoint test finds
   each label before its own table.

On this machine, at the build, not in CI (Word is not in CI):

5. The pane reader (UI Automation, pressing Right on every entry, since
   Word folds level-3 headings) lists Questions 1 to 16 of PH 212 Lab 1
   and 1 to 14 of PH 211 Lab 3; as built, none.
6. The edges, from Word's PDF at 300 dpi: the label's rule within 0.1 pt
   of the box's on the left; the tint's right edge within 0.1 pt of the
   box's (critique 1: 0.00 pt both). A scan of every row through the seam
   reports where the rule starts against the tint's top: critique 1
   measured it 0.48 pt below, the label's top border (in the tint) drawn
   over the rule's top corner, where as built rule and tint start on the
   same row. Put to the owner (section 9, item 5).
7. The strand survey over all 18 labs: exactly the two in section 6.

The owner's acceptance, unchanged from D-0176: Word's Navigation pane, a
screen reader in Word, a Google Docs import.

## 8. Interplay

- D-0179 (branch `docx-crushed-table`, not ruled): a table directly before
  a box joins it in Word (PH 211 Lab 3's stopwatch table, 13 pages). With
  this design a label paragraph precedes every box, so no table touches a
  box: PH 211 Lab 3 renders at 10 pages here. D-0179's gap would then sit
  between a table and the label's top line; its test (b), no `</w:tbl>`
  directly followed by `<w:tbl>`, holds either way. Whichever lands second
  rebases.
- Answer areas (ruling 3) follow this change.

## 9. Hard critique

1. The edge numbers are measured on one Word build on one machine; another
   Word or Google Docs may draw paragraph borders a fraction differently.
   A sub-point step at the seam is the worst case; the owner's checks
   cover Word and Docs.
2. Direct formatting on 194 paragraphs instead of a style: a style cannot
   carry two palettes (question, checkpoint) without two more styles per
   level; direct formatting keeps the reference unchanged and the D-0176
   style test true. Cost: a student restyling a label in Word loses the
   look, which no one is asked to do.
3. The two strandings are a regression in Word's print against as built
   (0). Ruled acceptable; re-counted with answer areas.
4. The tests cannot see the pane or the seam; both are local checks (5 to
   7) reported in the PR, and the owner's.
5. The rule starts 0.48 pt below the tint (about 2 px at 300 dpi, under one
   screen pixel at 100% zoom): a notch at the top-left corner that the
   design as built does not have. Ruled: accepted (the owner,
   2026-11-13: "Accept both"). The alternative is a
   thinner top border (0.25 pt) with its space and the cell margin
   re-derived, which halves the notch and needs a new measurement.
6. The 78 stems' First Paragraph style (section 4). Ruled: accepted and
   recorded in D-0180 ("Accept both"); drawn the same. The alternative is to reset Pandoc's
   paragraph style after the raw label, which needs the filter to write
   the stem's style itself.

## Declined

A plain label above the box (ruling 1); Heading-based styles in the box
(probe C: not in the pane); a box without a table (reverses D-0082; Pandoc's
paragraph styles never reach list items); letting the box's row split
(ruling 2); a table of contents or bookmarks in place of headings; moving
the in-box headings out of the box.
