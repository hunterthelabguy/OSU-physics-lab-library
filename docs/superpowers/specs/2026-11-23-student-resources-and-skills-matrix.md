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

## 2. Ruled so far (proposed entries, 2026-11-23)

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

## 4. Non-goals

- The skills matrix's data file itself (instructor repo, its own spec).
- Any wording change folded into a conversion (D-0168).
- The `Archive/` folder and the lock files.
