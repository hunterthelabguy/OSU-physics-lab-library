# Student resources and the skills matrix (stub)

**Status: stub, 2026-11-23.** Records the inventory and the owner's first
rulings (D-0202 to D-0205, proposed) so nothing lives only in chat. Not yet
a design: it is shaped by spec-first (critique, questions, approval) before
any conversion starts.

## 1. Inputs

**Path:** `../Old Reference Material/` relative to this repo's root (the
owner's folder of originals), as in the 2026-10-06 conversion spec.

Cleared by the owner 2026-11-23 and read in full for student data (D-0205).
None holds student data. Staff names appear only in document properties,
which the strip tool removes (D-0086), and in the data script's author line,
removed by hand before any commit.

| File | What it is | Size of the job |
|---|---|---|
| `Student Resources/Excel Skills.docx` | "PH21X Excel Primer": importing data, formatting, cell references, formulas, scatter plots, adding error bars, trendlines and LINEST, several data sets; an appendix on numerical slopes and areas | 19 pictures, 2 equations, links to OSU's software page and a video |
| `Student Resources/Excel Skills examples.xlsx` | The primer's two example sheets (area under a curve; several data sets) | Synthetic numbers |
| `Student Resources/Sample Lab Report/PH21X Sample Lab Report.docx` | An annotated example report (a dropped ball), commentary in text boxes beside the response | 60 text boxes, 82 drawing objects, 18 equations, 1 table |
| `Student Resources/Sample Lab Report/PH 21X Sample Lab Data.xlsx` and its generator script | The report's data, made by adding random noise to free-fall times | Synthetic |
| `Student Resources/Lab Guidance for Students.docx` | Learning outcomes, what earns an outstanding response, a course rubric, data and uncertainty, an advanced appendix on propagation | 9 pictures, 54 equations, 20 text boxes, 4 tables |
| `Student Resources/Lab Conduct and Report Instructions.docx` | Submission on Gradescope, the next-day 11:59 pm deadline, conduct terms, grading | Course policy |
| `Lab Skills Matrix.xlsx` | Eight skill areas and about sixty sub-skills coded per lab and course, a weights sheet, and review comments | Goes to the instructor repo, never here (LEDGER 31, D-0204) |

Not opened and not cleared: the three Office lock files and `Archive/`.

## 2. Ruled so far (promoted 2026-11-23)

- D-0202: a handbook link opens its section in place on the web page; the
  downloads keep D-0190's links.
- D-0203: Excel Skills is the one home of the error-bar steps; Lab 3's
  error-bar appendix becomes a link to it.
- D-0204: the matrix's comments stay as role-credited review notes; its
  columns are re-keyed to lab ids first; every library PR states the matrix
  rows it touches.
- D-0205: the inventory above; order Excel Skills, Sample Lab Report, Lab
  Guidance, then Lab Conduct on the owner's word that its policy is current.

## 3. Open questions (for the spec-first round)

1. Does the "fold changes in" rule (D-0204 (3)) also cover these documents?
   Two already describe the curriculum and will go stale: the Sample Lab
   Report says many labs have an appendix of earlier boxed information, and
   Lab Conduct tells students to address "all bold face questions".
2. Section identifiers for Excel Skills, fixed like the handbook's (D-0190),
   at least for "Adding error bars".
3. The Sample Lab Report's commentary: a callout convention for text boxes
   beside a response (the conversion spec's known hard case), and how it
   reads in Word, in the PDF and to a screen reader.
4. Lab Guidance's overlap with the handbook: its uncertainty sections repeat
   the handbook's wording; resolved by D-0201 (4)'s absorption pass or by
   cutting from Lab Guidance.
5. The example workbooks and the data script: published as lab files
   (D-0071's group), or left out.
6. External links (OSU's software page, a video): kept as they are, or
   checked by the build.
7. Lab Conduct: is its policy current, and does it belong on a public site.
8. Credit and license per document: D-0073 and D-0076 still hold authors'
   names and the license; D-0159's byline rule applies only where an
   original prints its author on its face. None of these four prints a
   byline; their authors are known only from document properties.

## 3a. Question round 1 (drafted 2026-11-24, not yet asked)

Four load-bearing questions from section 3, each with a lean, its reason
and the cost of the alternative. The other four are carried with a default
at the end, for the owner's veto. Facts below are from `grep` on main at
2665e40 and from Pandoc's reading of `Excel Skills.docx` (cleared, D-0205).

**Record note.** Four converted handouts name Excel Skills, not three:
PH 211 Labs 2 and 3, PH 212 Lab 1 (`ph212-data-analysis-handout.md` line
232, there since 2026-10-09) and PH 213 Lab 1. D-0205's rationale ("Three
... Claude first counted four, wrongly") and D-0203's "five documents" (six
with PH 212 Lab 1) are each off by one. The ledger is corrected by a new
entry, never by editing those two.

**Q1 (section 3, item 2). Which Excel Skills sections get fixed
identifiers?** Lean: only the three a converted handout already names, at
their own heading levels: `plotting-and-fitting-data` (a `#` chapter; PH 211
Lab 2, PH 212 Lab 1, PH 213 Lab 1), `adding-error-bars` (PH 211 Lab 3,
D-0203) and `plotting-multiple-data-sets` (PH 211 Lab 2). The other ten
titled sections keep Pandoc's derived ids until a link needs one; that link
adds its fixed id in its own PR. Reason: D-0190 (3)'s test already fails a
link to an unknown identifier, so the gate holds without a list of ids no
one links. Cost of the alternative (all thirteen now): a test-held list
with ten entries and no consumer; cheap, but each is a promise kept for
nobody. Riders: (a) three of the four handouts point at the whole
"Plotting and fitting data" chapter, which D-0202 would open in place as one
long box holding three subsections; when those links are ruled, the lean is
that each names the narrowest section it means. (b) D-0202's filter takes
any converted document's section, not only the handbook's (D-0203 (2)
already assumes it). WCAG: none from identifiers; the disclosure's are
D-0202's.

**Q2 (section 3, item 3). How does the Sample Lab Report's commentary
read?** Lean: each comment text box becomes a `::: comment` div placed
right after the paragraph it is anchored to (the word check already reads an
anchored drawing after its paragraph's words), with a visible lead label
"Comment:" written by the filter, not typed in the source (as question
numbers are). Web: an inset box with no landmark role. Word and PDF: a
one-cell box, as questions are (D-0082). Before the spec rules it, a probe
of the original classifies the 60 text boxes (comment, or part of the
report itself) and the 82 drawing objects (connectors to a passage, or
other), and confirms each text box's double appearance in the file is
counted once. Reason: one reading order in every output; a reader meets
each comment right after what it comments on (1.3.2), the label carries the
difference rather than colour or position alone (1.3.1, 1.4.1), and there
is no side column to collapse at 320 px (1.4.10); 60 `<aside>` landmarks
would flood landmark navigation (a usability cost, not a criterion).
Cost of the alternative (margin notes on wide screens): a second layout for
one document, inline on phones anyway, and Word's floating boxes do not
survive Pandoc. Any arrows from a comment to its passage are lost in both
forms and become a declared omission.

**Q3 (section 3, item 1). Does D-0204 (3)'s fold-in rule cover these
documents?** Lean: not by a second PR line. Instead, one CLAUDE.md
sentence: a ruled change that makes a statement in a published course-wide
document false fixes it in the same PR or names it in the PR body as a
follow-up. And this spec lists each document's known stale passages as
ruled-change rows, drafted after its conversion lands: Lab Conduct's
"address all bold face questions" (LEDGER 33's retired cue) and the Sample
Lab Report's line that many labs carry an appendix of earlier boxed
information, which the appendix cuts (D-0192, D-0201 (2)) are making less
true. Reason: the trigger is the ruled change, which already has a ruling
and a reviewed diff, so the rule has a moment to fire; an untriggered rule
decays (D-0204's own argument). Cost of the alternative: a second line on
every PR, almost always "none", for four documents; with no rule at all,
stale text is found by a student or not at all, as LEDGER 33's legend was.
WCAG: none.

**Q4 (section 3, item 8). Credit and license.** Lean: as every handout. No
credit line and no name in front matter, since none of the four prints a
byline (D-0159 does not reach them); the strip removes document properties
(D-0086) and the data script's author line goes by hand (D-0205 (1)). The
authors become an item for D-0073's conversation, recorded by role in the
instructor repo, not here. Reason: document properties may name whoever
created or last saved the file, not the writer, and copying them puts a
staff name into a soon-public repo on metadata the document does not print.
Cost of the alternative: a wrong credit is harder to retract from permanent
git history than a missing one is to add. WCAG: none.

**Carried with a default (veto if wrong).**
- Item 4, Lab Guidance's overlap: waits for D-0201 (4)'s absorption pass,
  as D-0205 (4) orders; nothing is cut at conversion (D-0168).
- Item 5, the workbooks and the script: left out at conversion. The
  primer's text never names its examples workbook (no match for "examples"
  or "xlsx"), so publishing it needs a ruled sentence that links it, with
  D-0165's `files:` as the mechanism (PH 212's capstone uses it); the script
  generates data and carries a staff author line.
- Item 6, external links: the three kept as they are (two OSU IT pages, one
  video); no build-time link check, since a network check in CI fails on
  someone else's outage.
- Item 7, Lab Conduct: already before the owner (D-0205 (4)); not asked
  twice.

## 4. Non-goals

- The skills matrix's data file itself (instructor repo, its own spec).
- Any wording change folded into a conversion (D-0168).
- The `Archive/` folder and the lock files.
