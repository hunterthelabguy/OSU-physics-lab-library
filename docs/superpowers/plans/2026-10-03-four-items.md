# Four items of 2026-10-03: course links, width, dialog words, PH 213 Lab 2

Plan only. Nothing built. Written 2026-10-03 at `474cc4d` (its `main` run
green) from the owner's four items in `STATE.md` ("Next, plan only"). Each
item is its own PR; item 4 is two (4a, 4b) for the reason under its call 4.1.
Questions for the owner are batched at the end, numbered Q1 to Q17, each with
Claude's lean; nothing that needs a ruling is built before it is ruled, and no
visible word ships that the owner has not seen.

Binds: D-0010, D-0029, D-0040, D-0053, D-0059, D-0067 (proposed), D-0068
(proposed), LEDGER 14, 18, 24, 28, 39, 43, 56, 57, 58; `docs/conversion-spec.md`.
Not built past: everything under "Awaiting owner" in `STATE.md`. Items 1 to 3
touch the course index, which D-0067 and D-0068 (both still proposed) also
govern, so their rulings come first (Q1).

## Premises, checked 2026-10-03

Measured on a fresh `python tools/quarto_build.py` of `474cc4d`, served from
`build/` and loaded in same-origin iframes in the browser pane (the scrollbar
takes 15 px, so a 1440 px window is 1425 px of client width).

1. **Course index today.** Three courses from `site/courses.md`: PH 211 with
   eight labs (one converted), PH 212 and PH 213 with no labs and one note
   each. The PH 212 heading is 2203 px from the top of a 2787 px page at 768
   px and wider, and 2907 px down a 3634 px page at 375 px; PH 211's is at
   432 px (621 px at 375). A PH 212 or PH 213 reader scrolls past about 1770
   px of PH 211 at desktop widths, 2290 px on a phone.
2. **Heading ids are Pandoc's automatic ones:** `ph-211-general-physics-with-calculus`,
   `ph-212`, `ph-213`. They change when a course's name is filled in, so a
   link to one would break silently.
3. **Widths at 1440 px.** Site pages' `main` is 1184 px from x = 121 (the
   72rem shell plus 16 px padding each side); prose, the lab rows, the h1 and
   the Download all button all start at x = 363; prose and rows are 700 px,
   68 zero-widths of 18 px Open Sans. Each side of the prose leaves a 226 px
   track inside the shell, the same at 1280 and 1920 (the shell caps `main`);
   at 1024 the tracks are 139 px, at 768 they are 27 px. The lab page's
   `main` is 771 px at 1440 and up (LEDGER 57's type growth), 693 px below.
   At 375 px nothing scrolls sideways on any of the five pages measured.
4. **Row text.** Lab titles and descriptions are 18 px. The eight descriptions
   are 53 to 175 characters; the longest would be 1502 px on one line. A row
   has 40 px of padding and border, so a 700 px row sets about 64
   zero-widths a line; a row spanning the 1152 px shell would set about 108,
   past WCAG 2.2 SC 1.4.8's 80 and LEDGER 56's 68. LEDGER 56 let lists use
   the shell because "a card holds a title and one short line"; D-0068's rows
   hold quoted descriptions up to 175 characters, so that premise no longer
   holds for them.
5. **Controls are sized by their content:** Download all 130 by 44 px; the lab
   page's download row 405 px. Widening a button adds no information, so
   "widen the controls" has nothing to act on except where a control sits.
6. **Download all failure today.** `site/download-all.js` catches a failed
   fetch, logs it to the console and re-enables the button: the reader sees
   nothing happen. From a copy opened from disk the button is shown and every
   fetch is refused, which is the same silence.
7. **The PH 213 file, vetted.** `../Old Reference Material/21X Lab
   Curriculum/PH213/Lab 2 - Hypothesis Testing - Handout.docx`: 3,070,663
   bytes, SHA-256 `36f41045875ea1bb0c1699a1ed50c7b18ae2d8e6397a0da37d05546aa069ab68`.
   Read in full (body, both headers, footnotes, endnotes, custom XML): no
   student-identifiable data. It names Gradescope as where reports go and
   asks for "everyone's name" on a report; those are instructions, not data.
   `docProps/core.xml` names two people as `creator` and `lastModifiedBy`
   (the open metadata question, Q16). No comments, no tracked changes.
   Two copy errors in the original, kept as written under the no-content-change
   rule: "Part 4" is used twice (Analyze; Submit), and "measured from zeroFor
   the rest" has no break.
8. **Its equations.** 71 `m:oMath` elements: 1 inside the `mc:Fallback` copy
   of a drawing, 70 in the primary content, 3 of those display equations
   (`m:oMathPara`), 1 inside a text box. Pandoc 3.10 (Quarto's) reads 69
   `Math` nodes, 3 display and 66 inline: every primary equation except the
   text box's. The model equations are fractions (equation 1 is
   `\Psi\ \left\lbrack \frac{E_{D}d_{D}}{E_{A}d_{A}} \right\rbrack\ \ \ \ (1)`,
   its number inside the math); force and field vectors use
   `\overset{⃑}{...}` (U+20D1). Some symbols are not equations but
   mathematical italic letters typed as text (`𝛥𝑉𝐴`, U+1D6E5 and up), which
   the Latin and Greek subset of Open Sans (D-0025) does not hold.
9. **The word check cannot see equations.** `tools/check_unchanged.py` reads
   the original's `w:t` only, so all 70 equations are absent from its
   original-side words, while its converted side reads each `Math` node's
   LaTeX as characters. A first run on this file would fail on every
   equation, and a careless "fix" (dropping `Math` from the converted side)
   would let a lost equation pass. The conversion spec already says so:
   "Equations and image counts are to be added when the first document that
   has them is converted."
10. **Its images.** Two primary drawings, both floating (`wp:anchor`), both
    with alt text in Word: `image1.png` (140,606 bytes, the CRT schematic,
    labels and caption drawn into the PNG) and the power supply photograph
    (944,032 bytes, 2637 by 1482 px JPEG, stored twice in the package as
    `image2.jpeg` and `image3.jpeg`, byte-identical, once for the drawing and
    once for its VML fallback; the fallback group is 1.35 MB of
    `document.xml`). The photograph has **no labels in it**: "Accelerating
    voltage control", "Deflecting voltage control ΔVD", "Accelerating voltage
    display", "Do not use" and the caption "Figure 1: Power supply" are five
    text boxes, with three further shapes (by count, presumably the pointers),
    grouped over the photo in Word. Pandoc drops all five text boxes and their
    one equation, and anchors the photo inside question 6. "Do not use" marks
    one knob, so these positions carry a safety instruction.
11. **Its boxes.** "Using the CRT" and "Sources of uncertainty" are one-cell
    tables, the `::: box` convention. Each table's Word alt description
    (`w:tblDescription`) holds the box's whole text, and Pandoc writes it as a
    table caption, so the box's words would appear twice. "The maximum value
    for VA is 400 V!" is a table too, with the same caption duplication.
12. **The downloads would mishandle both.** `tools/downloads.py` pipes the
    source to Pandoc on stdin, so a relative image path resolves against the
    working directory, not the source's folder; and its HTML download passes
    no math option, so Pandoc would write its plain-text math, not D-0040's
    MathML. Both are caught today only because the image path would warn and
    the warning fails the build; the math would pass silently.
13. **The CSS has no reference for new elements.** The quarto-only reverts
    cover the element types measured against the old build, which phase 4
    deleted; `docs/agent-reference.md` says what replaces it is not chosen.
    This lab brings `math`, `img`, `figure` and `figcaption` to a lab page.

## Item 1: a way to a course without scrolling past PH 211 (PR 1)

### Call 1.1: links or a select

- **Lean: an in-page list of course links, no script.** A `<nav>` after the
  intro paragraph and before the PH 211 heading, holding one link per course
  in `courses.md` order, each the course code as its text ("PH 211", "PH 212",
  "PH 213") and pointing at that course's heading. Three choices are visible
  at once, work from a copy on disk (LEDGER 39), need no script, and are
  plain links to a screen reader. On a phone they sit on one line as three
  44 px tap targets (3 by about 80 px fits 328 px; to be measured).
- **Alternative: a `<select>`.** It hides three choices behind a tap, and a
  select cannot move the page without script (a form submit cannot target a
  fragment), so it needs a script, a label and a no-script fallback. It
  earns its place at about eight or more courses, not three.
- **Words added.** Visible: none new; the link texts are the course codes the
  page already shows as headings. Spoken only: the nav's accessible name;
  Claude proposes `aria-label="Courses"` (Q2). The select would add a visible
  label (Claude would propose "Go to a course") and its option texts.

### Call 1.2: stable anchors

- **Lean:** `course_index_markdown()` writes each heading with an explicit id
  from the course code, lowercased with spaces removed (`## PH 211: General
  Physics with Calculus {#ph211}`), the same slug D-0067's zip name uses. The
  ids then survive a course name being filled in. Cost of the alternative
  (Pandoc's automatic ids): the PH 213 link breaks the day its name is added
  (premise 2).

### Not in this PR

A "back to the top" link after each course (new words; the browser's own
scroll does it); collapsing PH 211 by default (hides the one course with
labs); a sticky list (that is item 2's call 2.2).

### Tests and checks

`tests/test_quarto_chrome.py`, new `CourseLinks`: one link per course in
`courses.md` order, each `href` equal to an `id` of an h2 on the page, the
texts equal to the course codes read from `courses.md` (never retyped), no
`<script>` added for it, the nav before the first h2. Measured at 375 and
1440 px: nav height, tap target sizes, no sideways scroll. `test_bodies_unchanged`
untouched (the course index is not a lab page).

Ledger: one proposed entry, amending nothing.

## Item 2: wider use of the screen on site pages (PR 2)

### Critique of the unruled lean

"Widen the rows and controls, keep prose near 68ch" has two problems the
measurements show. Rows hold prose: at the shell's width their descriptions
set about 108 zero-widths a line (premise 4), so widening them as they are
breaks the measure the lean means to keep. And controls are content-sized
(premise 5), so widening them is a no-op. What can use the width is (a) the
row's inside, laid out in two columns so the description keeps the measure,
(b) the two 226 px tracks beside the prose, and (c) type size, as LEDGER 57
already does for documents.

### Call 2.1: rows across the shell, two columns inside (lean)

From a breakpoint up, `.lab-list` spans `main`'s full tracks (D-0029's first
form), and each row becomes a grid: the title and the state line in the left
column, the description in the right column capped at `--chrome-measure`.
Computed, not yet measured: at 1440 px a 1152 px row has 1112 px inside its
padding; a 700 px description column plus a 24 px gap leaves 388 px for the
title column. Titles run to 41 characters ("Lab Skills practical (not
implemented)"), about 2 lines at 388 px. Breakpoint: where the title column
would fall under 16rem (288 px), i.e. a 1052 px row, about a 1120 px window
(70rem); below it, today's one column. The Download all button follows the
rows' left edge. Rows get shorter (the description wraps in fewer, measure-length
lines beside the title instead of under it), so more labs fit a screen. This
amends D-0068, which is still proposed; if D-0068 is ruled first, this is a
new entry amending it.

### Call 2.2: the course links in the left track (lean, needs item 1)

From the same breakpoint, item 1's nav moves into the left track as a
vertical list that stays in view (`position: sticky`), so a reader jumps from
anywhere on the page. 226 px holds "PH 211" at 18 px many times over. It
cannot coexist with call 2.1 as written, since full-width rows fill that
track: either rows span the prose and the right track only (rows 700 + 226 +
24 = about 950 px, title column about 186 px, under the 16rem floor, so the
two-column row would need a higher breakpoint), or the nav stays above the
rows. Claude's lean is call 2.1 with the nav above the rows (item 1 as built);
the sticky side nav is the alternative if the owner values the jump from
mid-page over wider rows (Q5).

### Call 2.3: type growth above 1440 px on site pages

LEDGER 57 grows document type to 1.1875rem above 1440 px; site pages stay at
18 px. Doing the same on site pages makes the column 739 px at 1920, as on lab
pages (premise 3), more pixels and the same characters. Small payoff on pages
that are mostly short; Claude's lean is not now (Q6).

### Call 2.4: the landing cards

The landing page's four link cards are two across inside the 700 px column.
Spanning them across the shell (four across at 1440, two below 70rem) uses the
width without long lines, since each card is a title and one sentence; the
hero band already spans. Lean: include, as the same kind of change as call
2.1 (Q7).

### Not proposed

Widening `--chrome-measure` itself: the evidence review's number, an owner
decision (LEDGER 57, `docs/agent-reference.md` "Widths"). Lab pages: not site
pages, and D-0010 holds their `<main>`.

### Before any CSS

Mockup boards for 2.1, 2.2 and 2.4 at 375, 1024, 1440 and 1920 px, kept under
`docs/design/2026-10-0x-wide-site-pages/` with a README, the owner picks;
then build, then measure the built pages (not the mockups) at the same four
widths with the measuring script, and put the numbers in the entry. Known
traps: `body.site-page .lab-list` specificity, grid children stretch
(`justify-self: start` for the button), quarto-only `content-box`.

### Tests

`LabRows` edited and disclosed: one column below the breakpoint, the
two-column inner grid above it, the description column capped by
`--chrome-measure` (asserted from the CSS text, as today); the 375 px
no-sideways-scroll measurement recorded in the entry.

## Item 3: a close button and a failure message in the Download all dialog (PR 3)

### Call 3.1: close

A "Close" button in the dialog, inside `<form method="dialog">`, which closes
a dialog natively, with no script. Placed beside "Download selected", in the
quiet outline of the Download all opener, so the orange stays the one action.
Escape and a tap outside still close it. Proposed word: **"Close"** (Q8; the
alternatives are "Cancel", which suggests something is under way to cancel,
and a "×" with "Close" as its accessible name, which is the same word to a
screen reader and a smaller target to everyone else).

### Call 3.2: a failure message

A message element written into the dialog at build time by
`render.download_all()` (so the words live in Python, pinned by the tests,
never in the script), hidden until a download fails; the script shows it on
any failure, hides it when the dialog opens or a new download starts, and
announces it (`role="alert"`). A zip is all or nothing today, so the message
can say nothing was saved. Proposed wording, for the owner to pick or rewrite
(Q9):

- A: "The download did not finish, so nothing was saved. Check your
  connection and try again." (lean: says what happened and what to do)
- B: "Something went wrong and nothing was downloaded. Try again."
- C: "Download failed. Try again."

### Call 3.3: from a copy on disk

Today the button shows on a copy opened from disk and every fetch fails
(premise 6). Lean: the script leaves the button hidden when the page is
opened from `file:`, as it already does for a browser without `<dialog>`, so
no message is needed for that case and no words are added; each lab's own
four buttons still work from disk. Alternative: show it and let the failure
message speak, which would then need wording that names the website (Q10).

### Call 3.4: a busy state

A PH 211 zip of four formats is small; with PH 213 Lab 2's 944 KB photograph
in its Word, HTML and PDF files, a phone may wait seconds. Today the disabled
button is the only sign. A visible "Preparing…" in the button is a new word.
Lean: not now; measure the wait on a phone after item 4, then ask (Q11).

### Tests

`Control.test_words` extended with the approved words, read from
`render.py`; the close form and its `method="dialog"`; the message hidden as
built with `role="alert"`. The node test gains a case where one fetch fails:
`buildZip` rejects and nothing is saved. The script's show-and-hide of the
message is DOM code outside `BEGIN CORE`, untested by node (no DOM library);
checked by hand on the preview with a renamed file (a 404) and recorded in the
entry. The phone check of a real zip (`STATE.md`, awaiting) still stands.

Ledger: a proposed entry amending D-0067 ("No close word is shown" and the
declined visible close button).

## Item 4: PH 213 Lab 2 through the pipeline (PRs 4a and 4b)

Superseded 2026-10-07 (D-0082, ruled): 4a becomes passes 2a (checks) and
2b (downloads) of `docs/superpowers/specs/2026-10-06-handout-conversion-and-templates-design.md`
(its section 11.2), and 4b becomes a task of its pass 3. The calls below
still hold as that work's design where not amended; Q12 to Q15 and Q17 are
answered as leaned (D-0092), Q16 by D-0086.

### Call 4.1: two PRs, the check before the content

- **4a, tooling only:** the word check learns equations and images, the
  downloads learn images and MathML, the CSS reverts for the new elements.
  Proved on fixtures and on PH 211 (989 words and bold on 943 unchanged).
- **4b, content:** the original committed, the Markdown, the images, the
  course index entry (as ruled), the HTML cap remeasured.
  Cost of one PR: a check written in the same diff as the content it passes,
  so a reviewer cannot tell a check that works from one shaped to pass.

### Call 4.2: how the check counts and compares equations (4a)

Both sides put one placeholder token in the word sequence where an equation
sits, so the existing sequence compare proves count and position; each
equation's content is then compared separately, in order.

- **Original side** (independent of Pandoc, as now): with `mc:Fallback`
  removed, each `m:oMath` in document order, text boxes included, yields the
  placeholder and a record: display or inline (`m:oMathPara` parent), its
  `m:t` text, and a structure signature (counts of `m:f`, `m:sSub`, `m:sSup`,
  `m:sSubSup`, `m:rad`, `m:acc`, `m:d`, `m:nary`).
- **Converted side:** each `Math` node yields the placeholder, its kind
  (`DisplayMath` or `InlineMath`) and its LaTeX. The LaTeX is turned back
  into OMML by Pandoc's own writer (one docx of all the equations, read with
  the same OMML reader), giving the same `m:t` text and signature.
- **Compare:** counts equal (70 for this file), kinds equal in order, and per
  equation the normalized `m:t` text equal (Unicode NFKC, whitespace removed,
  U+2206 to U+0394, the invisible operators U+2061 to U+2064 removed) and the
  signatures equal. Equations are exempt from the bold compare (heading
  rule's `None`), since `\mathbf` is styling inside math.
- **Honest limits:** the converted side's comparison goes through Pandoc's
  LaTeX-to-OMML writer, so it checks that the LaTeX carries the same symbols
  and structure as the Word equation, not how a browser draws it; the owner's
  eye on the page, the PDF and the Word file is the check of that, as for the
  Word question box (D-0057).
- **Probe first, in 4a's first task:** run the round trip on this file's
  Pandoc output and list every equation whose normalized text or signature
  differs. If the round trip cannot be made equal by normalization alone,
  stop and bring the list to the owner (Q13) rather than loosen the compare
  until it passes.
- **Tests:** a fixture docx made by Pandoc from known LaTeX (inline, display,
  fraction, sub and superscript, accent), with cases that must fail: an
  equation dropped, two swapped, a subscript changed, a display equation made
  inline, an equation inside a text box missing from the Markdown. PH 211 has
  none, so its results are unchanged (a test asserts its equation count is 0).

### Call 4.3: how images are extracted, stored, published and checked (4a, 4b)

- **Extracted** from the docx package by Python reading the relationships,
  not by Pandoc's `--extract-media`: each primary drawing's `a:blip`
  `r:embed` to its `word/media/` part, bytes copied unchanged. The VML
  fallback's duplicate JPEG is not extracted.
- **Stored** beside the source as `curriculum/ph213/<id>-media/<name>`, with
  descriptor names, not positions (LEDGER 14): `crt-schematic.png`,
  `power-supply-panel.jpeg`. Front matter gains `images:`, one entry per
  image: `file`, `source_part` (`word/media/image1.png`), `sha256`.
- **Published** at `labs/<id>/<id>-media/<name>`, each listed under
  `resources` in `_quarto.yml` (Quarto publishes what a page references,
  listed or not; the list is written by the build from front matter, never
  typed). The `.md` download's relative paths then resolve on the served site,
  and D-0067's Markdown checkbox carries the media files too, under the same
  relative path, so a zipped `.md` opens with its images. The lab pages live
  at `labs/<id>/modern/` and `/faithful/`, one level down, so their image
  paths need a prefix; how Quarto resolves a path inside an `{{< include >}}`
  is to be probed, and the fix is a filter or the generated page, never a
  second copy of the source (LEDGER 28).
- **Checked:** primary drawings with an image (2) equal `Image` nodes (2),
  in order; each image's bytes hash to its recorded `sha256` and equal its
  `source_part` in the original; each image's alt text in the Markdown equals
  Word's `wp:docPr` `descr`, word for word. Alt text is taken out of the word
  sequence on both sides and compared here instead, since the original side
  does not read `descr` as words today and the converted side does.
- **Downloads:** Word and HTML get `--resource-path` set to the source's
  folder; the HTML download gets `--mathml` (D-0040). The HTML download
  embeds the 944 KB JPEG as base64, about 1.26 MB, so `HTML_CAP_BYTES` is
  remeasured per lab, as `tests/test_downloads.py` says to when a lab is
  added. Page weight: the modern lab page goes from about 262 KB to about
  1.35 MB with both images; Q15 asks whether a smaller derived copy may be
  published.
- **CSS reverts:** with no old build to compare against, the reference for
  `img`, `figure`, `figcaption` and `math` is the HTML download, which
  renders the same Markdown with the same theme CSS and no Bootstrap. Measure
  computed styles in both, add a revert where Bootstrap differs, pin each in
  `QuartoOnlyCss`, and record the reference in `docs/agent-reference.md`.

### Call 4.4: the labelled photograph (4b; Q12)

Premise 10: the labels exist only as positioned text boxes, one of them "Do
not use". Options:

- **A, labels kept at their positions (lean).** The figure is the photograph
  with the five labels and three pointers laid over it at the positions Word
  stores (the group's offsets and extents in EMU, scaled to percentages), as
  an inline SVG or positioned HTML generated by the build from the original,
  never hand-placed. The words stay text, so the check counts them and a
  screen reader reads them; the safety label stays on its knob. Cost: a new
  build piece and a new convention in the conversion spec; the faithful page
  gets the same figure.
- **B, labels as a list under the photograph.** Words kept, positions lost:
  "Do not use" no longer says which knob. Cheap, and wrong for a safety label.
- **C, labels drawn into a derived image.** Positions kept, words leave the
  text (ruled omissions, a ledger reference each), and alt text must carry
  them. Loses the check and searchability.

Pandoc drops all five today, so any option needs the converter step to write
them; the check (which reads text boxes) will fail until it does.

### Call 4.5: the rest of the conversion (4b)

Follows the PH 211 conversion and the handout conventions: `::: box` for the
three one-cell tables with their duplicated alt-description captions dropped
(a structure change, not a word change; the check confirms no word is lost or
doubled); questions as `::: question` with descriptor ids scoped to the
document; no smart quotes; title and course line as written ("Lab 2 –
Hypothesis Testing", "PH 213 – General Physics with Calculus", en dashes as
in the original). Identity per the spec: `id: ph213-hypothesis-testing-handout`
(Q14), `course: PH213`, `sequence: 2`, `source_file:
"originals/PH213/Lab 2 - Hypothesis Testing - Handout.docx"`. The original is
committed byte for byte (LEDGER 18) only after Q16 is answered, since its
metadata names two people and git history is permanent. Structure reviewed by
parse-tree block counts against the original (premise counts: 12 headings, 3
tables, 6 bullet and 14 ordered lists as Pandoc reads them, to be reconciled
with what the conventions make of them). Display checks by the owner: the
modern page, the faithful page, the PDF and the Word file, for the fractions,
the vector arrows and the mathematical italic letters (premise 8: they fall
back to a system font).

### Call 4.6: the course index entry (owner's, Q3 and Q4)

Amended 2026-10-07 (D-0088, ruled): pass 1 quotes the PH 212 and PH 213
lab lists from their summaries, now in the owner's folder, which answers Q3;
Q4 (the course name's source) stays open.

`site/courses.md` lists no PH 213 labs, and its rule is that nothing is added
for a lab its source summary does not list (LEDGER 43); the PH 211 entries are
quoted from the PH 211 Curriculum Summary. No PH 213 summary is in hand to
this session. Until the owner rules, the lab is converted and published at its
own address but not listed, and D-0067's Download all for PH 213 stays absent
(it lists converted labs that the index lists). Claude does not invent a
title, number or description.

### Tests and verification (4a and 4b)

The repo's verify sequence (the exports in `CLAUDE.md`, `check_unchanged.py`
on both converted files, the em-dash grep, `quarto_build.py` with 0 warning
lines, the unit tests with node on PATH), PH 211 still 989 words identical
and bold on 943, the new file's word, bold, equation and image counts in the
PR body. Measured at 375 and 1440 px: no sideways scroll on the new pages,
image and equation boxes inside the column.

## Order

PR 1, then PR 3 (both small, independent), then 4a, then 4b after its
rulings, then PR 2 after its mockups are picked (it is the one that changes
the most layout, and it should be measured with PH 213's rows present if Q3
lists them). Every push to `main` deploys production: read each `main` run
once it reports, and do not push while another is in flight.

## Questions for the owner

Rulings that gate the others:

- **Q1.** Promote D-0067 and D-0068 before items 1 to 3 amend them? Lean:
  yes; otherwise each amendment rewrites a proposed entry in place.

Item 1:

- **Q2.** Course links (no script), not a select, with the course codes as
  their only visible words and "Courses" as the nav's spoken name? Lean: yes.

Item 4, the course index (yours, not Claude's):

- **Q3.** Where does PH 213 Lab 2's course-index entry come from? Is there a
  PH 213 curriculum summary to quote, as PH 211's is? If not, may the
  handout's own title line be the source for its title and number, with no
  description, and the note under PH 213 rewritten (new words, yours to
  approve)? Or does the lab stay unlisted until a summary is in hand?
- **Q4.** PH 213's name: `courses.md` takes PH 211's from "the Lab 1
  handout's own course line". This handout's line reads "PH 213 – General
  Physics with Calculus". Use it the same way? Lean: yes, it is the same rule.

Item 2:

- **Q5.** Rows across the shell with the description kept at the measure
  beside the title (call 2.1, lean), or the course links in a sticky side
  column with rows as today (call 2.2)? Both after mockups.
  Owner, chat 2026-10-03 after this plan landed, not a ruling: "Table of
  contents on the left hand side? Select -> auto-scroll, etc." That is call
  2.2 (a sticky list in the left track) and touches call 1.1 (a select that
  scrolls on choice, which needs script). Next session: mock the left-hand
  contents as links and as a select side by side at 375, 1024 and 1440 px,
  and say whether call 2.2 then displaces call 2.1 as the lean.
  Done 2026-10-05: boards and measurements in
  `docs/design/2026-10-05-left-contents/`. Lean now: call 2.2 as links (board
  C) displaces call 2.1; the select (board D) stays declined.
  Superseded 2026-10-06: the owner reviewed board C and chose one page per
  course, a dense lab table and a 96rem shell, so neither call 2.1 nor 2.2
  is built. D-0069 to D-0071 (proposed), boards in
  `docs/design/2026-10-06-course-pages/`. Item 1's nav and item 3's dialog
  words change with them: read those entries before building either.
- **Q6.** Grow site-page type above 1440 px as document pages do (call 2.3)?
  Lean: not now.
- **Q7.** Landing cards across the shell (call 2.4)? Lean: yes, in PR 2.

Item 3, words for your approval:

- **Q8.** The close button's word: "Close"? Lean: yes.
- **Q9.** The failure message: A, B, C, or your own. Lean: A.
- **Q10.** Hide Download all on a copy opened from disk (no words) rather
  than show it and let it fail? Lean: hide.
- **Q11.** A visible busy state ("Preparing…") now, or after measuring a
  phone with PH 213's files? Lean: after.

Item 4, conversion:

- **Q12.** The labelled photograph: A (labels kept at their positions,
  generated from Word's own coordinates), B (a list under the photo) or C
  (drawn into the image)? Lean: A, because "Do not use" must stay on its knob.
- **Q13.** If the equation round trip shows differences normalization cannot
  remove, may Claude bring the list to you before deciding, rather than
  declare them? Lean: yes, it stops there.
- **Q14.** The id `ph213-hypothesis-testing-handout`? PH 211 Lab 4 is also
  titled "Hypothesis Testing"; the course code keeps them apart, and a PH 211
  conversion would be `ph211-hypothesis-testing-handout`. Lean: yes.
- **Q15.** Publish the photograph as is (944 KB, 2637 px wide), or also a
  smaller derived copy for the page (provenance recorded: made from the
  original by a named tool, its hash in front matter), the original kept in
  the Word file and the Markdown download? Lean: publish as is in 4b, measure
  the page on a phone, then decide.
- **Q16.** The original's `creator` and `lastModifiedBy` name two people.
  Strip them before committing (the original would then not be byte for byte
  the file in Old Reference Material, so `source_sha256` would name the
  stripped file and the entry would record both hashes), or commit as is?
  This is the open STATE question for PH 211 and PH 212 too, and D-0062's
  history scan. 4b waits on it.
- **Q17.** Commit the 3 MB original (1.35 MB of it a fallback copy of one
  drawing, and the photo stored twice) to a repo that will be public, with
  permanent history? Lean: yes, LEDGER 18 asks for the original byte for
  byte, and the size is a one-time cost; noted so the size is a choice.

## Declined, with reasons

- A `<select>` for three courses: hides choices, needs script, adds words.
- Rows widened as they are: about 108 characters a line (premise 4).
- Wider buttons: content-sized controls gain nothing (premise 5).
- Widening the measure: an owner decision on the evidence review's number.
- Pandoc's `--extract-media` as the image source of truth: it would make the
  check depend on the tool it checks.
- Equations compared as LaTeX strings typed by hand, or dropped from the
  converted side's words: the first is unmaintainable, the second lets a lost
  equation pass.
- One PR for item 4: a check and the content it passes in one diff.
- Inventing a PH 213 course-index entry: LEDGER 43, and the owner's question.
