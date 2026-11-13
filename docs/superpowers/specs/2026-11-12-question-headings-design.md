# Question labels as headings: design

Status: draft for the owner's review, 2026-11-12. Written by Claude in a
side session started from the D-0167 (equations) session: step 1 (spec) of
the working sequence, then a hard critique (section 8) and the owner's
questions (section 9). Ledger: D-0176 (proposed). Ledger entries win over
this file. Plan and build wait for the ruling; the build ends in a draft PR
with green `verify`.

## 1. Problem

The NVDA 2026.3 test of the six PH 212 pages
(`docs/accessibility/2026-11-05-nvda-ph212.md`, section 5, item 6): every
"QUESTION n" label is plain text, so a screen-reader user cannot reach a
question with H (next heading) or D (next landmark), and the page's
elements list does not show them. A blind student told by a TA to "go to
Question 7" has to read or search the page linearly.

Counts, from `tests/question-ids.json` and a Pandoc parse of each source on
2026-11-12: 194 questions in 18 labs (PH 211 66, PH 212 78, PH 213 50), no
checkpoint on `main`. PH 212: Lab 1 16, Lab 2 9, Lab 3 24, Lab 4 11,
Lab 5 8, Capstone 10. The NVDA report counted 17 on Lab 1; the source and
the pinned ids both hold 16 and Lab 1 has not changed since pass 4 (#52).
The report is a record and stays as written; the build counts from the
source.

Scope: every lab in PH 211, 212 and 213, on the lab page and in the HTML
download, which both come from `tools/filters/questions.lua`. Word is an
open call (section 5). The direction is ruled: headings, preferred over
landmark regions (chat, before this spec, from best practice rather than one
person's preferences).

## 2. WCAG effects, up front

| Criterion | Level | Today | After |
|---|---|---|---|
| 1.3.1 Info and Relationships | A | The label works visually as a heading (own style, starts a block) and is a `<p>` in markup: structure shown only by presentation. | Met for the label: its role is in markup, at a level that fits the outline. One relationship stays imperfect: content after a box and before the next heading falls under the question in the outline (critique 8.1). |
| 2.4.6 Headings and Labels | AA | Not engaged: no heading, nothing to judge. | Engaged: every new heading must describe its topic or purpose. "Question 7" names it as the lab, the TA and the rubric do; call 2 decides whether that is enough. |
| 2.4.10 Section Headings | AAA | Questions, the unit a student works in, have no heading. | Met for questions. |
| 2.4.1 Bypass Blocks | A | Already met (D-0166's skip link, headings). | Strengthened: headings are a sufficient technique (H69), now down to the question. |

Landmarks (D) are not used: a region per question would add 8 to 24 region
landmarks to a page, and region landmarks are for page-level areas. That is
the ruled direction, not reopened here.

## 3. The heading level rule (call 1)

**Rule.** A question's (or checkpoint's) label is a heading one level below
the nearest heading before it in document order, outside any question box.
Every lab page opens with its H1, so the level is always 2 or more. A level
past 6 fails the render; the deepest section on `main` is H4, so labels run
H3 to H5.

Measured on `main` (parse of every source, 2026-11-12):

| Section level | Questions | Label |
|---|---|---|
| H2 | 112 | H3 |
| H3 | 66 | H4 |
| H4 | 16 | H5 |

H4 sections with questions: PH 211 Capstone, PH 211 Uncertainty, PH 212
Lab 3, PH 213 Data Analysis.

**Why this rule.** A label one level down never makes a skip, whatever the
section's depth, so `tests/test_headings.py`'s ratchet holds without a new
`KNOWN_SKIPS` entry. The three labs that skip today (PH 211 Capstone,
PH 211 Uncertainty, PH 213 Data Analysis) skip in their own headings. Their
labels follow the same rule and add no skip.

**Headings inside a box.** Two questions hold a heading of their own, both
in a `::: box` the question tells the student to read:
`ph212-data-analysis:uncertainty-sources` ("What is Uncertainty?") and
`ph212-extending-a-model:assumptions` ("Assumptions:"). Each is `###`
under an H2 section, so its question's label would be H3 and the box's
heading H3 too: a sibling of the question, not inside it. The rule adds:
a heading inside a question box is deeper than that question's label. Call
4 decides how the two sources meet it.

**Test.** `tests/test_headings.py` today reads the source's ATX headings.
It gains a second reading: the Pandoc AST after `questions.lua`
(`theme-name=modern`, the non-Word branch), where it asserts (a) no skip
across source and label headings together, with the same `KNOWN_SKIPS`
ratchet; (b) each label is its section's level plus one; (c) every heading
inside a question box is deeper than its label.

## 4. The accessible name (call 2)

**Lean: the label alone**, "Question 7" (or "Checkpoint 2"), the same words
the box shows today.

- It is what the lab, the TA and the rubric call the item, so "go to
  Question 7" maps to one heading.
- The box's first paragraph follows at once: one down-arrow after H reads
  the stem. A heading holding the stem's first words would be read twice in
  a row: once as the heading, then as the paragraph.
- The visible text and the accessible name stay identical, so a sighted
  helper and the student mean the same words.
- A stem often opens with a generic instruction ("Read the box below on
  sources of uncertainty.", "Record your data") or with math; first words
  would not make the elements list much more useful.

Alternative: the label plus the stem's first words, written into the
heading and hidden visually. Benefit: the elements list (NVDA+F7) shows
topics, so a student can find "the one about friction". Costs: the stem
spoken twice; hidden text a sighted reader cannot see (a mismatch between
the two); a cut point to choose in each of 194 stems, or a word count that
cuts some mid-phrase or mid-equation. On 2.4.6: the alternative is the
safer reading for an auditor, and the lean depends on the number being the
item's real name in this course.

Whatever the name, the heading carries **no id**. The question's `Div`
keeps its descriptor id (ledger 14) for links. A generated id such as
`question-1` would repeat after a week restart (S9). A build probe confirms
Quarto adds none.

## 5. Word (call 3, open)

Today the Word label is a paragraph in the "Question Label" style
(`tools/reference.docx`, from `tools/make_reference_docx.py`), first in the
one-cell table that is the question box (D-0082). Word knows nothing of it
as a heading.

**Lean: Word gets them too**, as outline levels. `make_reference_docx.py`
writes "Question Label 3", "Question Label 4" and "Question Label 5", each
today's "Question Label" look plus `<w:outlineLvl>` at that heading's level
(2, 3, 4, zero-based). The filter picks the style by the rule in section 3,
as it already sets `custom-style`. That is Pandoc's own route, since
custom-style reaches a Div's paragraphs (the label is one, D-0057's probe),
so no raw paragraph XML. The box looks as it does today.

- Why: DAS may give the student the Word file. Word is a common accessible
  format, and a screen reader in Word navigates by headings as on the web.
  If Word is left as it is, the gap the NVDA test found stays open in
  exactly that format.
- Cost of the lean: three styles where there was one; `test_downloads`'
  Word assertions name the three. What the outline level does is
  **unmeasured**: whether Word's Navigation pane lists a label inside a
  table cell, whether NVDA or JAWS in Word announces it as a heading, and
  whether Google Docs keeps it on import. Only the owner checks what Word
  and Google Docs show (runbook); those three checks are the build's
  acceptance for Word, and one that fails is reported, not argued.
- Alternative 1, base the styles on Word's built-in Heading 3 to 5: the
  surest route for every consumer (Google Docs maps headings by style), but
  it inherits the Heading styles' look, so each style overrides it back.
  This is the fallback if outline levels alone fail the owner's check.
- Alternative 2, Word unchanged: no work, no risk to the box; the gap stays
  in Word, and the Word download is the only output that differs from the
  page in structure.

## 6. How the box stays as it is

On the page and in the HTML download the label becomes
`<hN class="question-label">Question 7</hN>`, in place of
`<div class="question-label"><p>Question 7</p></div>`. The box (`.question`,
its rule, tint and padding) does not change.

- **CSS.** `themes/modern.css`'s `.question-label p, .checkpoint-label p`
  becomes `.question-label, .checkpoint-label` and sets, besides today's
  values, what a heading would otherwise bring: `font-weight: 400`,
  `line-height` and `color` as the body paragraph has them, and margins
  `0 0 .35rem`. It must outrank `h1, h2, h3, h4` (0,0,1) and Quarto's
  `:where(.quarto-light) h5` (0,0,0), which one class does. Lab pages use
  `template.html`, so the site pages' `body.site-page h3` (0,1,2) does not
  reach them; the HTML download embeds `site/site.css`, so that is checked
  there too.
- **Print.** `.question` is already `break-inside: avoid`, so a label
  cannot leave its box except in a box taller than a page
  (`TALLER_THAN_A_PAGE`). The print rule `h1, h2, h3, h4 { break-after:
  avoid }` would reach H3 and H4 labels but not H5. So `.question-label`
  is named in the print rule itself and every level behaves the same.
- **Acceptance (measured, never assumed).** On screen, the label's computed
  style (font size, weight, family, letter-spacing, transform, colour,
  line-height, margins) and its box's height are equal before and after,
  at desktop width and 375 px, on one lab per label level (H3, H4, H5),
  read in the in-app browser. In print, each lab's PDF is rasterized before
  and after (pdftoppm) and compared page by page. A difference is reported
  with its cause. A page break that moves because of the print rule is
  allowed if it strands nothing.
- **Word.** The three styles share today's run and paragraph properties; the
  Word test asserts they differ from "Question Label" only by
  `outlineLvl`.

## 7. Other outputs

- **HTML download.** Same filter, same headings, same CSS (embedded). It
  gets everything the page gets. `HTML_CAPS` is unaffected in direction (the
  new markup is shorter); `test_downloads`' print-split check matches the
  label by its old `<div><p>` form and moves to the heading form.
- **PDF.** Chrome prints the built page, and its PDF is tagged: a local
  build of PH 212 Lab 1 (2026-10-26, HeadlessChrome 156) reads `Tagged: yes`
  with `/H1`, `/H2` and `/H3` structure elements. So the labels should reach
  the PDF's structure tree as H3 to H5 with no change to the print step. The
  build checks this on its own PDFs, not the stale local one. The PDF has
  no bookmarks (`/Outlines` absent); adding Chrome's document outline would
  bookmark every heading and is a separate change (declined list).
- **Markdown download.** The source, byte for byte: it carries the
  `::: {.question #id}` fence and no label at all, since numbers come only
  at render. No effect, and none intended here: a reader of the `.md`
  meets no question number today either (declined list).
- **Number check.** `tools/check_numbers.py` reads the label as the plain
  text of the box's first block. A Header's plain text is the same "Question
  N", so the check runs unchanged; the build confirms it on all 18 labs.
- **Course download.** The zip bundles the per-lab files above; nothing of
  its own.

## 8. Hard critique

1. **The outline files trailing content under the question.** In 69 of the
   194 questions, other content (activity bullets, instructions, a
   paragraph) follows the box before the next heading or question. In a
   heading outline that content belongs to the question's heading. Reading
   in order is unharmed, and the next question's or section's heading
   restores the outline. The only markup that would close a question's
   section is a `<section>`, which is a landmark when named (ruled out) and
   does nothing for heading navigation when not. Accepted, recorded under
   1.3.1 in section 2.
2. **No single key for "next question".** Labels run H3 to H5, so NVDA's
   level key (3, 4 or 5) finds a lab's questions only within one section
   depth; H walks everything. A fixed level per lab (one more than its
   deepest section) would give one key, but it skips levels under shallower
   sections: it fails `test_headings.py` and the outline. Lean holds: H, or
   the elements list, which shows all levels.
3. **Heading count roughly doubles** on question-heavy pages (PH 212 Lab 3:
   28 headings to 52). This is the point of the change, and the level
   structure keeps sections findable with 2 and 3. Noted so it is not a
   surprise in the next NVDA run.
4. **"QUESTION 7" in capitals.** `text-transform: uppercase` reaches the
   accessibility tree in Chromium; the 2026-11-05 log records `QUESTION n`.
   eSpeak spoke it as a word. A screen reader that spells out all-caps words
   would spell it; none in the test did. Unchanged by this spec, noted.
5. **Word is the least verified output.** The tests read the XML; whether a
   reader treats an outline-level paragraph in a table cell as a heading is
   for the owner to see. Section 5 makes that his acceptance check, with a
   named fallback.
6. **Quarto might add ids or wrappers.** `section-divs: false` and
   `anchor-sections: false` are set (`_quarto.yml`), so none is expected;
   the build probes one page before writing the filter change, and a test
   asserts no duplicate id on any page.
7. **Collision with D-0167.** The `ph212-math` branch edits PH 212 sources.
   Call 4's lean touches one heading line in each of PH 212 Labs 1 and 2;
   different lines, one PR at a time, rebase before review.
8. **Does it belong in the filter?** Yes: labels are already generated
   there and nowhere else, so the heading is one changed node in one place.
   No new file, no new option, no new metadata.

## 9. The owner's calls

Four calls, each in the ledger entry with its lean. Claude's own calls
(veto open): checkpoints follow the same rule; the heading has no id; the
print rule names the label; the number check is not changed; the NVDA
report is not edited except a "Fixes since" line when the build lands.

1. Level rule: one below the nearest heading (lean) or a fixed level per lab.
2. Accessible name: the label alone (lean) or the label plus first words.
3. Word: outline-level styles (lean), Heading-based styles, or unchanged.
   Also, if known, which format DAS gives the student.
4. The two box headings in PH 212 Labs 1 and 2: `###` becomes `####` in
   the source (lean; format only, words unchanged; the box heading shows at
   1rem instead of 1.1rem), or the filter demotes headings inside a box at
   render (the source and the page disagree), or leave them (the outline is
   wrong in two places).

## 10. D-0168: format only

No source wording changes. The label's words ("Question N") are generated at
render and are not source text, and they do not change. If call 4 rules the
lean, two source lines change heading level only, `###` to `####`, words
identical. The word check reads words, not structure, and passes. Neither
file gets `ruled_omissions` or `ruled_additions`, and neither `status`
changes. Nothing else in a source changes.

## 11. Build outline (for the plan, after the ruling)

`tools/filters/questions.lua` (track the section level; the label as a
Header; the Word style by level), `themes/modern.css` (label rule, print
rule), `tools/make_reference_docx.py` and `tools/reference.docx` (call 3),
two PH 212 sources (call 4), `tests/test_headings.py` (rendered reading),
`tests/test_downloads.py` (label form; Word styles; no duplicate ids),
`docs/accessibility/2026-11-05-nvda-ph212.md` (one "Fixes since" clause).
Verification: the full `verify` sequence, the screen and print comparisons
in section 6, the PDF's structure tags, and an NVDA spot check of PH 212
Lab 1 (H3 labels) and Lab 3 (H5 labels) under the 2026-11-05 setup. The
owner checks Word and Google Docs.

## Declined

- Landmark regions per question (ruled direction; landmark noise).
- A fixed heading level per lab (skips levels; critique 8.2).
- Hidden first words in the heading (call 2's alternative, if not ruled).
- PDF bookmarks from Chrome's document outline: useful, but it changes every
  heading's role in the PDF, not only questions. Its own small change.
- Question labels in the Markdown download: the download is the source byte
  for byte (D-0052), and labels are render-time only.
- Editing the NVDA report's Lab 1 count: it is a record of that run.
