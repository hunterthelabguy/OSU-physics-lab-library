# Word pagination: tables kept whole, the originals' page breaks carried

**Revision 1, 2026-11-23.** Rulings D-0206 and D-0207 (proposed). Found in
the owner's Word check of PH 211 Lab 3 for the handbook trial (D-0192 (3)),
after PR #84 (D-0179) stopped Word from joining the stopwatch table to the
question box after it.

## 1. The problem

In Lab 3's Word download:

1. **"Part 1: Uncertainty in a Single Measurement" starts on page 1.** The
   original has a hard page break before it. The conversion drops every hard
   page break: 33 in 15 originals, none ruled.
2. **The stopwatch table is cut into two pieces.** Nothing in the original
   keeps it on one page either: it is a floating table with one row marked
   "can't split", which only stops a single row breaking. It stayed whole
   because the page break before Part 1 placed it high on a page. Our Word
   layout differs (margins, fonts, box gaps), so the table lands across a page
   boundary, and its header row, marked to repeat, prints again at the top of
   the second piece.

The PDF has neither problem with the table: `site/site.css`'s print rules keep
every table whole (`table { break-inside: avoid }`), and Lab 3's PDF holds all
three stopwatch rows on page 5. The PDF does drop the page breaks.

## 2. Scope

Two independent parts, two PRs, tables first, after PR #84 merges (D-0206,
D-0207).

**Part A, tables (bounded).** Word keeps every Pandoc table on one page where
it fits, as the PDF does.

**Part B, page breaks (architectural).** The originals' hard page breaks are
carried as source markup into the Word download and the PDF.

Non-goals: page breaks on the web page or in the HTML download (screens have
no pages); any page break the originals do not have; question boxes (they are
one-cell tables `questions.lua` writes with rows that already cannot split,
D-0082); the report template (not built; D-0079's gate reopens on a change to
`tools/reference.docx` and would cover it when it is).

## 3. Part A: tables kept whole in Word (D-0206)

**Measured 2026-11-23.** The 19 Word downloads hold 6 Pandoc tables, all in
the `Table` style: PH 211 Lab 7 (5 rows), PH 211 Lab 2 (24 rows, a data
table), PH 211 Lab 3 (4 rows, three pictures), PH 212 Lab 6 (3 rows, and the
6-row rubric on its own landscape page), PH 213 Lab 5 (4 rows).

**Mechanism.** `tools/make_reference_docx.py` adds two properties to Pandoc's
`Table` style, beside D-0130's grid:

- `<w:pPr><w:keepNext/></w:pPr>`: every paragraph in the table keeps with the
  next, so Word moves the table to the next page rather than break it;
- `<w:trPr><w:cantSplit/></w:trPr>`: no row breaks across a page.

The element order follows the schema (`pPr` before `tblPr`, `trPr` after it).
The function stops if the style already holds either property, as `grid`
stops on a second set of borders. `tools/reference.docx` is regenerated and
committed.

**Cost.** A table that does not fit the rest of a page moves whole to the next,
leaving white space, as the PDF already does. A table taller than a page still
breaks, where it must. Pandoc writes `w:lastRow="0"`, so the style cannot spare
the last row: the table also keeps with the paragraph after it. In these six
cases that is a box gap paragraph, a heading or body text.

**Untested premise, probed first.** That Word applies `keepNext` and
`cantSplit` from a table style. The probe renders Lab 3 through Word (COM,
read-only copies, only Claude's own instance stopped by its process id, as
D-0179's bisect did) and reads the stopwatch table's first and last row page
numbers. If Word ignores the style, the fallback, ruled with this part, writes
the same two properties into each Pandoc table's rows and cell paragraphs in
`tools/downloads.py` after Pandoc, beside `landscape_sections` and
`crop_pictures`.

**WCAG.** None: pagination only.

## 4. Part B: the originals' page breaks (D-0207)

**Survey, 2026-11-23** (`w:br w:type="page"` in each original's
`document.xml`, matched to the converted source by the text that follows):

| Before | Count |
|---|---|
| A heading (Part, Week, Appendix, introduction) | 30 |
| A table (PH 212 Lab 1) | 1 |
| A bold underlined line (PH 212 Lab 3, "Measuring linear motion") | 1 |
| A body paragraph (PH 213 Lab 5, "The GA default is not how...") | 1 |

Seven are in re-baselined handouts (PH 211 Labs 3 and 6, PH 212 Lab 1). The
Lab Handbook has none. Twelve precede an appendix. Only one goes with a cut:
Lab 3's break before "Appendix – Error Bars" (D-0203). D-0192 keeps each PH 211
appendix heading and its list of handbook links, so the breaks before PH 211
Labs 4 to 6's reference appendices stay, and each will start a page holding
only that short list, as Lab 3's two links stand alone on page 10 today
(D-0198 (6)). Claude first counted eleven, wrongly.

**Markup.** One form for every case: an empty fenced div immediately before
the block, with a blank line on each side:

```markdown
::: page-break
:::

### Part 1: Uncertainty in a Single Measurement
```

Probed 2026-11-23: Pandoc reads it as `Div ("", ["page-break"], []) []`, and
with three such divs in PH 211 Lab 4 both Word checks pass unchanged (3,020
words identical; Word's labels identical). The word check reads words, so the
marker adds none.

**Outputs.**

| Output | Effect |
|---|---|
| Word | `tools/filters/landscape.lua` (the filter for print layout taken from the originals) writes `<w:p><w:r><w:br w:type="page"/></w:r></w:p>`, the form the originals use: a paragraph holding only the break |
| PDF | `themes/modern.css`, `@media print`: `.page-break { break-before: page; }` |
| Web page | An empty div; nothing shows |
| HTML download | The same empty div; nothing shows on screen |
| Markdown download | The source, byte for byte: the two marker lines show |

**Conversion rule.** `docs/conversion-spec.md` gains "Page breaks": a hard page
break in an original becomes a `::: page-break` div before the block that
follows it; nothing else makes one. A converted file adding them stays
`converted` (format only, proven by both checks). In a `ruled-change` file the
markers are a ruled format change citing D-0207, reviewed in its diff (D-0195).

**Applying them.** A one-time script, kept outside the repo, inserts the 33
markers by the survey's following text, asserting each target is found exactly
once. It is not committed (as the handbook's creation script, D-0201 (1)).

**WCAG.** None: the marker is empty and has no role on screen.

## 5. Checks

Deterministic first (charter floor 13).

- **Part A.**
  - A test reads `tools/reference.docx`'s `Table` style for `keepNext` and
    `cantSplit`.
  - A test reads every built Word download: each Pandoc table's rows inherit
    them (no direct `w:keepNext w:val="0"` or row property undoing them).
  - The Word probe above, then all 19 downloads rendered through Word before
    and after: pages per download, and every Pandoc table's first and last
    row on one page unless it is taller than a page.
- **Part B.**
  - `tests/test_page_breaks.py`: for each `converted` source, its markers equal
    its original's page breaks, in order, by the text of the block that
    follows (a table counted as a table). `ruled-change` sources are skipped,
    as both Word checks skip them (D-0195).
  - Each built Word download holds one `w:type="page"` break per marker.
  - In Lab 3's PDF, "Part 1: Uncertainty in a Single Measurement" is the first
    text line of its page (pdftotext).
- **The owner** checks PH 211 Lab 3 and PH 212 Lab 3 (six breaks) in Word and
  in Google Docs, after each PR.

## 6. Considered and declined

- One PR for both parts (the table fix waits on a 15-file review).
- A class on the heading (`{.page-break}`) with a div for the three other cases
  (two forms for one job).
- Choosing breaks one by one (a judgement per break with no record to check it
  against; the originals' own breaks are the record).
- Breaks on the web page or in the HTML download.
- Keeping only small tables whole (a size rule with no measured need: six
  tables, the largest 24 rows).
- The per-table post-pass in `tools/downloads.py` as the first choice (a second
  layer editing XML after Pandoc, the kind D-0179 set aside); kept as the
  fallback if Word ignores the style.
- Doing nothing (a split table repeating its header reads as two tables, the
  owner's finding).
