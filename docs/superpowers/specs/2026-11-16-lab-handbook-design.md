# The Lab Handbook and the first appendix cut: design

Status: revision 2, approved by the owner 2026-11-17 ("Approve and
promote"), with its two drafted lines (sections 4.2 and 4.5). Written by
Claude; step 1 (spec) of the working sequence, classified architectural by
spec-first. Revision 1 (commit 379f6fc) was critiqued the same day by a
fresh reviewer (`2026-11-16-lab-handbook-critique.md`), which found it not
buildable as written; the owner ruled the critique's six questions on
2026-11-17. This revision folds both in (section 3 maps each finding).
Entries D-0188 to D-0192, ruled, carry the rulings. Ledger entries win
over this file.

Inputs, in the private instructor repo: the handout-load review and the
PH 211 cut list (`reviews/2026-11-16-handout-load/`), and the owner's
rulings in its ledger entries 51 and 54 to 56.

## 1. Purpose

Seven reference sections are taught once in PH 211, each in a box in the
lab that introduces it, and copied into an "Appendix – Reference
Information" at the end of every later lab: 30 passages across Labs 3 to
7, 3,762 words, 19% of PH 211's handout text (cut list, sections 1 and 2).
PH 212 and PH 213 carry the same sections.

This build:

1. Publishes them once, as the **Lab Handbook**, a page for every PH 21X
   course, with its own downloads.
2. Gives each handbook section an address that survives rewording, and a
   way for a handout to link to it.
3. Adds one check feature, a declared span omission, that lets a
   converted document leave out a whole stretch of its original
   (equations and pictures included) under a ruling.
4. Makes the first cut as a trial: PH 211 Lab 3's appendix (rows C1 to C3)
   becomes a list of links to the handbook.

It does not show that students read more of a shorter handout, and it
measures nothing about reading.

## 2. Rulings

| Question | The owner | Where |
|---|---|---|
| Does the cut-only step wait for the restructure? | "The cut-only step can go ahead of the restructure." (2026-11-16) | Instructor ledger 51 |
| Where the reference text lives | "1. New reference page." (2026-11-16) | 54 |
| A list of links in place of each cut appendix | "2. Yes, good." | 54 |
| Downloads for the page | "3. Fine. Let's give the page its own download then." | 54 |
| PH 211 Lab 7's rows ruled now, applied in the capstone pass | "4. Agreed." | 54 |
| PH 211 Lab 3 first, as the trial | "5. Agreed." | 54 |
| Name and tone | "I lean towards calling it a Lab Handbook or Lab Manual and making it general and more emphatic. 'Read the fantastic handbook' is the golden rule." (2026-11-16) | 55 |
| A notes line about printed copies | "4. No." | 55 |
| Which name | "Lab Handbook" (2026-11-16) | 56 |
| The critique's six questions, each with a lean (section 3 below) | "Take the six leans" (2026-11-17) | D-0188 to D-0192 |

The six leans taken on 2026-11-17, as they were put:

1. List the handbook "for every course" now, with PH 211's text; PH 212
   and PH 213 differences become rows before their cuts.
2. One ruled span-omission feature in the word check, and a number-check
   rule to match.
3. Stable section addresses go ahead of the capstone pass; the table of
   contents rail becomes its own spec (amends D-0141).
4. The handbook lands in two steps, conversion first, wording second
   (D-0168 (1)).
5. "Never copy content into a second file" is amended for the handbook
   until the appendix copies are cut.
6. No bold on the new lines; emphasis is in the words.

Still open: the wording of the handbook's opening line (section 4.2) and
of the instructor-notes line that Lab 3's cut changes (section 4.5).

## 3. What the critique changed

| Finding | Revision 1 | Revision 2 |
|---|---|---|
| F1: the Lab 3 cut cannot pass the word check (five equations in the span) | Words-only `ruled_omissions` | Span omission, 4.1 |
| F2: a nested `sources:` list breaks or hides the page from eight readers | `sources:` list | Flat `source_file`, 4.2 |
| F3: a range must cut five streams; the number check needs a rule | Range from a heading | Span omission drops all streams, and the labels in it, 4.1 |
| F4: wording folded into a conversion | One step | Two steps, 4.2 |
| F5: a second copy of content, unsaid | Silent | Ruled amendment with an end condition, 4.6 |
| F6: the opening line's claim is false | "used in every PH 21X lab" | A claim checked by grep, 4.2 |
| F7: D-0141 amendment unconfirmed | Assumed | Ruled (lean 3), D-0190 |
| F8: Markdown download, course zip, preview links, validation | "every output" | Limits declared; landing order; a unit test, 4.4 |
| F9: no HTML cap, no question-id pin | Missing | 4.2 |
| F10: the span's edges undefined | Unstated | Defined, 4.1 |
| F11: heading promotion justified by a rule that does not exist | "same as titles" | A format call with its real reasons, 4.2 |
| F12: bold on the new lines | Bold | Plain (lean 6) |
| F13: statuses of D-0160, D-0165, D-0168; D-0168's date | "ruled", 2026-11-07 | Proposed, 2026-11-06 |
| F14: no pass criterion for the trial | None | 4.5 |
| F15: the public verification sentence | Loosened by a range | Literally true: a span is a listed passage |
| F16: the handbook pins Lab 7's original | Unbound | Bound, 4.2 |
| F17: the em-dash scan skips ruled additions | Unsaid | Scanned, 4.7 |

Also dropped: the four "assumed, not ruled" leans of revision 1. A1 is
ruled (lean 1); A2, the handbook as home for three documents not in the
repo, had no consumer and is gone; A3 (reference text kept word for word)
holds by D-0168, since any rewording is a ruled change of its own; A4 is
ruled by lean 6 and section 4.5.

## 4. Design

### 4.1 Span omission (D-0189)

A converted file may declare, under `ruled_omissions`, a span of its
original that it leaves out:

```yaml
ruled_omissions:
  - span:
      from: "Required Plot Elements"   # omitted: the document's start
      from_occurrence: 2               # only when the text matches more than once
      to: "Some Heading"               # omitted: the document's end
    ledger: "D-0192"
```

- **Edges.** `from` and `to` are the whole text of one paragraph of the
  original, whitespace normalised, any style. The `from` paragraph is
  inside the span; the `to` paragraph is not. If the text matches more
  than one paragraph, `from_occurrence` or `to_occurrence` (1-based, in
  document order) says which; without it, or with no match, the check
  stops and prints every matching paragraph's position. PH 211 Lab 3
  needs this: "Required Plot Elements" is both a list item and the
  section heading.
- **Everything inside goes.** The original's characters (so words and
  bold), equations, pictures, drawn figures, tables, text-box text and
  footnotes inside the span are left out of every comparison. The
  converted file is read as always; it simply does not hold the span.
- **The number check** excuses exactly the Word labels whose paragraphs
  lie inside a declared span, and no others. How `docs/word-labels.json`'s
  anchors map to paragraphs is read by the plan before it chooses the
  mechanism; the requirement is the sentence above.
- **Stops.** Overlapping spans; a span whose edges are out of order; an
  edge inside a table cell or text box (not supported); a span that holds
  no characters.
- **What it amends.** D-0168 (3) says both checks keep running "unchanged".
  This is a change to the check, ruled (lean 2) and recorded like D-0167.
  "How this site works" says the check "passes only if the words match the
  original apart from the listed passages"; a span is a listed passage, so
  the sentence stays true.

### 4.2 The handbook (D-0188)

`curriculum/ph21x/ph21x-lab-handbook.md`, a converted document of PH 211
Lab 7's original:

```yaml
id: ph21x-lab-handbook
title: "Appendix B – Reference Information"   # step A; "Lab Handbook" in step B
course: PH21X
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 7 - Capstone - Handout.docx"
source_sha256: "b8f38b5a04e1a01304f7ec7b71e7e54c2e13e46af80f5fe91f58cf76c8722ea6"
status: converted                               # step A; ruled-change in step B
ruled_omissions:
  - span:
      to: "Appendix B – Reference Information"
    ledger: "D-0188"
images:                                         # Lab 7's two icons, as Lab 7 lists them
```

`source_file` stays at the top level, so every reader of it works as it
does for any converted document: the build, `media.py`, the number check,
CI's file selection, the em-dash scan's skip, and the page, download and
pin tests (F2).

**Step A, the conversion** (format only, `status: converted`). The body is
Lab 7's Appendix B as converted (capstone handout lines 284 to 378), which
already passes the check inside Lab 7. Format calls, none checked by the
word check, each recorded in D-0188:

- Heading levels. "Appendix B – Reference Information" becomes the page's
  `#`, and the seven sections `##`. Every page carries one `<h1>` from its
  `#`, and `tests/test_headings.py` fails a skipped level.
- "Predictions, Hypotheses, and Models", a bold underlined paragraph in
  the original, becomes a `##` heading like the other six. Reasons: the
  heading test above, and a styled pseudo-heading becoming a real one
  lets a screen-reader user reach it by heading (WCAG 1.3.1, 2.4.6). The
  conversion spec maps heading styles only, so this is a call for the
  owner, not a rule being followed.
- Each of the seven headings carries its fixed identifier (4.3).

**Step B, the ruled change** (`status: ruled-change`), each passage
declared with D-0188:

- The `#` heading and `title` become "Lab Handbook".
- The lead-in "This section contains key information from previous labs:"
  becomes the opening line, plain text. New public wording for the owner
  to approve. Draft: "Every lab after the first uses the ideas on this
  page. Read it before you start a lab, and come back whenever a lab asks
  for a plot, a fit or an uncertainty." The claim is checked: of the 18
  converted PH 21X handouts, 17 contain "lineariz" or "uncertaint"; the
  one that contains neither is PH 211 Lab 1, Team Building (grep,
  2026-11-17; PH 213 Lab 6 is not yet in the library).
- The seven list items become links to their sections on the same page.
  Words unchanged.

Steps A and B merge one at a time, back to back. Between them production
shows the page under Lab 7's appendix heading for one deploy.

**Listing and downloads.** `course: PH21X` lists it on the course index
under "For every course" and gives it a page and the four downloads, as
D-0160 did for the problem-solving strategy. As D-0160 did, it gets an
`HTML_CAPS` entry measured from its built HTML download, and an empty
question-id pin. It is in no course zip: a course download lists the
course's labs from `site/courses.md`. Declared, not fixed.

**Lab 7's original is pinned.** The handbook's check reads
`originals/PH211/Lab 7 - Capstone - Handout.docx` by hash. The capstone
pass (D-0141) adds a new original beside it, or re-points the handbook in
the same PR; it never replaces that file in place. Cutting Lab 7's own
Markdown appendix does not affect the handbook.

### 4.3 Stable section addresses (D-0190)

| Section | Address |
|---|---|
| Required Plot Elements | `#plot-elements` |
| Linearization | `#linearization` |
| What is Uncertainty? | `#what-is-uncertainty` |
| Sources of Uncertainty | `#sources-of-uncertainty` |
| Predictions, Hypotheses, and Models | `#predictions-hypotheses-models` |
| Tips for Using Graphical Analysis | `#graphical-analysis-tips` |
| Variables and Parameters | `#variables-and-parameters` |

Written as explicit identifiers on the headings, never derived from their
words. A test holds the table: the built page has exactly these seven on
its `##` headings. Renaming one is a deliberate edit to the test.

This builds the "stable deep links" of D-0141 item 3 for the handbook
only, ahead of the capstone pass (lean 3). The table of contents rail
leaves that pass for its own spec. What is already ruled for the rail
(instructor ledger 55): it lists a page's parts, shows a part's questions
only while that part is in view, and at phone width is an "On this page"
list at the top, closed by default. It waits on `question-headings`
(D-0176), which decides what a page's headings are.

### 4.4 Links from a handout to the handbook (D-0190)

A handout writes `[Linearization](ph21x-lab-handbook#linearization)`. A
filter rewrites it to `render.LIBRARY_URL` +
`labs/ph21x-lab-handbook/modern/#linearization` on the page and in the
Word, HTML and PDF downloads, as D-0165 (proposed) does for a lab's own
file. Which filter carries it is the plan's call after reading
`tools/filters/media.lua`.

- **The Markdown download** is the source byte for byte, so it keeps
  `ph21x-lab-handbook#linearization`, which resolves to nothing outside
  the site. Declared limit; the Markdown download is for reuse, and the
  link text still names the section.
- **Paper.** A printed handout shows the link text only. The lead-in names
  the Lab Handbook, which is the paper reader's route.
- **Validation** is a unit test, not build plumbing: it scans every
  curriculum source for links of the form `<id>#<address>` and fails on an
  id that is not a converted document or an address that is not one of
  that document's explicit identifiers.
- **Landing order.** Every output links to production, a PR preview
  included. The handbook (steps A and B) is on production before any
  handout links to it.

### 4.5 The Lab 3 cut (D-0192)

`curriculum/ph211/ph211-uncertainty-handout.md`, rows C1 to C3:

- "## Appendix – Reference Information" stays.
- The lead-in "This section contains key information from previous labs:"
  becomes "Read the Lab Handbook. It holds the key information from
  previous labs:", plain text (lean 6). Drafted by Claude, from the
  owner's "Read the fantastic handbook"; approved by the owner when he
  approves this spec, or reworded.
- The numbered list stays, `.numbered` wrapper and anchors unchanged, its
  two items now links to `#plot-elements` and `#linearization`.
- One span omission from the second "Required Plot Elements" paragraph
  (the heading, after the list item) to the end of the document: both
  sections, 315 words of Markdown source as the cut list counts them
  (310 without the equations' source) and five equations.
- `status: ruled-change`; each passage declared with D-0192.
- "## Appendix – Error Bars", above it, is untouched; the body's pointer
  to "the appendix of this lab handout" points there and stays true.

The matching line in the Lab 3 instructor notes changes in the instructor
repo, by its own PR and ruling there. Nothing from the notes enters this
repo.

**The trial passes when:** verify is green; the owner has checked Lab 3's
Word download in Word and Google Docs; and after deploy both links open
the right handbook section on production. Then Labs 4 to 6 go together;
Lab 7's rows wait for the capstone pass.

### 4.6 The copies rule (D-0191)

CLAUDE.md: "One Markdown source feeds one presentation [...] never copy
content into a second file." Until the appendix copies are cut, the
handbook's sections also exist in PH 211 Labs 4 to 7. Every copy is
checked against a Word original, so none can drift without a declared,
ruled change. The amendment, for the handbook only: until the last copy is
cut, a ruled change to a handbook section is applied to every remaining
copy in the same PR. It ends when Lab 7's appendix is cut in the capstone
pass. PH 212 and PH 213 copies differ already (PH 212's Linearization by
two tokens, its Sources of Uncertainty in list form and items); each
difference is a row for the owner before that course's cuts.

### 4.7 Ruled additions get the em-dash scan

`tools/check_em_dash.py` skips a converted file whole, so it would never
read the handbook's or Lab 3's new public lines. It also scans each
converted file's `ruled_additions` text. Today no file's additions hold an
em dash (three files read, 2026-11-17), so nothing current changes.

### 4.8 Accessibility

Link text names the section it opens (WCAG 2.4.4). Sections are real
headings at the right levels (1.3.1, 2.4.6), the Predictions heading
included. The two icons keep Word's alt text (1.1.1). Links open in the
same tab (3.2.5). No script, motion or colour-only meaning is added.

## 5. Build order

Each a PR with green verify, merged one at a time, main's run read after
each.

1. **Checks.** Span omission in the word check and the number check; the
   link test (4.4); the em-dash scan of additions. Fixture tests: a
   fixture original with an equation, a picture, a two-column table and a
   numbered list inside a span and words outside; pass when the Markdown
   omits exactly the span, fail when it omits less or more; stop on an
   unmatched edge, an ambiguous edge without an occurrence, overlapping
   spans, an edge in a table cell.
2. **Handbook, step A.** Conversion, ids, HTML cap, empty pin, the
   addresses test.
3. **Handbook, step B.** Merged right after 2.
4. **Lab 3 cut.** After 3 is live on production.
5. In the instructor repo, beside 4: the Lab 3 notes line.

## 6. Checks that pin it

- The word check on the handbook (one span) and on Lab 3 (one span plus
  the lead-in), with the span tests of step 1.
- The number check on both, with labels in spans excused and no others.
- The seven addresses (4.3); the link test (4.4).
- The handbook in `converted_documents()` and under "For every course";
  its four downloads built; its HTML cap; its empty pin.
- Lab 3's built page and Word download each hold two links whose targets
  are the handbook's `#plot-elements` and `#linearization` at the
  library's address.
- No quantity here is from memory: 315 and five equations come from Lab
  3's handout at commit 33d6cb2 (to be re-read by the plan at the commit
  it builds on); 3,762 from the cut list's `repeats.py` at c70151f.

## 7. Considered and declined

- **A `sources:` list** for several originals (critique F2; its consumer
  was A2, with no date and no check).
- **A range key** (`from_heading`) on the document instead of a span
  omission: two features where one serves the handbook and all 30 cuts
  (critique, options 3 and 4).
- **A new Word original** cut down to Appendix B by hand: no check change
  for the handbook, but a derived original resting on one hand edit, and
  nothing for the cuts (option 6).
- **A hand-written `site/` page**: no check, no downloads (option 7).
- **The full appendix kept in Lab 7, other labs linking to it**: put to
  the owner, not chosen.
- **Collapsing the appendix** (stretches, D-0143): ruled for sandbox labs
  only, and still 30 copies to keep in step.
- **Rewriting the link in the Markdown download**, and **the handbook in
  each course zip**: new code for a reuse format and a zip; declared
  limits instead.
- **A build-time failure on a bad link**: needs metadata plumbing a unit
  test does not.
- **Bold on the new lines** (lean 6), and a **notes line about printed
  copies** ("4. No.").
- **"PH 211 lab reference" and "Lab Manual"** as names.

## 8. Not in this build

- The table of contents rail (its own spec; 4.3).
- PH 211 Labs 4 to 6 (rows C4 to C22), after the trial; Lab 7 (C23 to
  C30) in the capstone pass. Rows C14, C20 and C28 start at the
  Predictions paragraph, which the span's paragraph edges handle.
- PH 212 and PH 213 cuts, and their differences from PH 211's text.
- Any measurement of whether students read or use the handbook.

## 9. Entries

Ruled in `DECISIONS.md` with this revision: D-0188 (the handbook),
D-0189 (span omission), D-0190 (addresses and links; D-0141 amended),
D-0191 (the copies rule), D-0192 (the PH 211 appendix cuts and the Lab 3
trial).

## 10. Open items for later rulings

Added 2026-11-19 from a side discussion of PH 212 Labs 5 and 6's
uncertainty hint (D-0183). None is ruled, and none is part of this build.
Each would be a ruled wording addition under D-0168, after the handbook
lands. The drafts are Claude's and not approved.

1. **An "Error propagation" section: two steps.** The owner, 2026-11-19:
   "How is error propagation different from adding uncertainties in
   quadrature? Seems like that should be mentioned here. Or at least
   somewhere in the handbook." Quadrature is one step inside propagation,
   not an alternative to it. Draft:

   > **Error propagation**
   >
   > When you calculate a result from measured values, the result's
   > uncertainty comes from theirs. Error propagation works it out in two
   > steps.
   >
   > 1. **Find each measurement's contribution:** how much the result
   >    changes when that measurement changes by its uncertainty. For a
   >    result built from powers, w = x^α y^β / z^γ, each contribution is
   >    the exponent times the relative uncertainty: α Δx/x.
   > 2. **Combine the contributions.** Independent errors add in
   >    quadrature; errors that share a cause add directly (see *Combining
   >    uncertainties*).

2. **A "Combining uncertainties" section: independent errors, and not the
   independent variable.** The owner, 2026-11-19: "I can see students
   getting confused about independent measurements and independent
   variables. [...] For independent measurements, can we explain what
   exactly it means for a measurement to be independent of another
   measurement?" Lean: say "independent errors", never "independent
   measurements". Draft:

   > **Combining uncertainties**
   >
   > Two errors are *independent* when knowing one tells you nothing about
   > the other. If one measurement happens to read high, an independent one
   > is just as likely to read high as low. This is not the same as an
   > experiment's *independent variable*, the quantity you choose or
   > control, plotted on the horizontal axis. "Independent" here describes
   > errors, not the role a quantity plays in your experiment.
   >
   > Errors are usually independent when they come from separate readings,
   > taken with different tools, with nothing shared that could push both
   > the same way. Measuring a string's length with a meter stick and a
   > pendulum's period with a stopwatch gives independent errors.
   >
   > Errors are *not* independent when they share a cause:
   > - the same reading used twice, as in x² = x × x;
   > - one quantity calculated from another;
   > - two measurements made with the same miscalibrated instrument, which
   >   pushes both off in the same direction.
   >
   > Independent errors partly cancel: one may read high while the other
   > reads low. That is why they are added in quadrature, squared, added,
   > then square-rooted. Errors that are not independent cannot cancel, so
   > they add directly. For x² this gives 2 Δx/x rather than √2 Δx/x.

   Open in it: whether the miscalibrated-instrument bullet stays, or links
   to *Sources of Uncertainty* if that section covers systematic error.

3. **Any power, not only whole numbers.** "Repeated multiplication" explains
   only whole-number exponents; the rule α Δx/x holds for any power (for
   example ½ for a square root, as in PH 212 Lab 1's T ∝ √L), since
   ∂w/∂x = αw/x. Lean: one sentence in item 1, not in the handout hint.

4. **A link from the hint to the handbook.** The ruled hint (D-0183,
   2026-11-19) ships without one. Once item 1 or 2 is live, decide whether
   the hint ends "See *Error propagation* in the Lab Handbook." Lean: point
   to *Error propagation*, since step 1 is the answer for x².

5. **Where these sit against the copies rule (D-0191).** The appendices'
   "What is Uncertainty?" and related sections are the handbook's source
   text; decide whether items 1 and 2 extend those sections or stand as
   new ones.
