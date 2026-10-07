# Handout conversion and report templates: design

Status: draft for `/critique`, 2026-10-06. Written by Claude from the owner's
rulings in chat the same day. Step 1 of the critique (hard critique) is in
`2026-10-06-handout-conversion-and-templates-critique.md` beside this file;
its findings (two passes) are not yet applied here. Nothing here is binding until it is entered in
`DECISIONS.md`; ledger entries win over this file. Supersedes items 4a and 4b
of `docs/superpowers/plans/2026-10-03-four-items.md` once ruled (both are
folded into passes 2 and 5 below).

**Amended 2026-10-07: critique steps 2 and 3 done with the owner.** The
rulings are in section 11 and in `DECISIONS.md` as D-0074 to D-0092
(proposed) and D-0093 to D-0098 (declined; full entries in `DECLINED.md`).
Sections 1 to 10 are kept as written, with short "Amended" notes where a
ruling changed them; where they differ from section 11, section 11 and the
ledger win.

## 1. Goal

1. Convert every remaining PH 21X lab handout from Word to Markdown, format
   only, under `docs/conversion-spec.md` (no content changes; the word check
   proves it).
2. Then build one Word report template per converted lab from the same
   Markdown source: the questions only, one per page, an answer box after
   each, for students to fill in and submit to Gradescope as a PDF.

Not in scope: the paper-versus-typed decision (`STATE.md`, open, the
owner's); the in-page worksheet (section 10); converting instructor notes or
rubrics (section 7 says where they live and what is checked later); content
changes of any kind.

## 2. Inputs

**Path:** `../Old Reference Material/21X Lab Curriculum/` relative to this
repo's root (the owner's folder of originals, curated 2026-10-06; given here
relative so no local user path enters a repo that will be public).

**Inventory by file name only, 2026-10-06.** No file in the folder was opened
for this inventory. Handouts are under `<course>/Handouts/`; instructor notes
and support files under each course's instructor folder.

| Course | Handouts | Converted | To convert | Instructor notes | Rubric workbooks | Summary |
|---|---|---|---|---|---|---|
| PH211 | Labs 1 to 7 | Lab 1 | 6 | 7, plus a second Lab 6 file (see 9.3) | `PH 211 Rubrics.xlsx` | yes |
| PH212 | Labs 1 to 6 | none | 6 | 6 | `PH 212 Rubrics.xlsx` | yes |
| PH213 | Labs 1 to 6 | none | 6 | 6 | `PH 213 Rubrics.xlsx`, Lab 6 Capstone rubric | yes |

Total to convert: 18 handouts. Course-wide files at the folder's root:
`Curriculum objectives.docx`, `Lab Guidance for Instructors.docx`,
`Statement on AI and labs.docx`, `21X Labs README_PII-stripped.txt`.

`site/courses.md` lists PH211 Labs 1 to 7 plus "Lab Skills practical (not
implemented)", which has no handout; the folder agrees with it for PH211.
For PH212 and PH213 it lists no labs and says none is in hand, which stopped
being true when their summaries reached the folder (critique, finding 7).

**Sample (2026-10-06):** the handouts for PH211 Lab 1, PH212 Labs 1 and 2,
PH213 Lab 2, and `Statement on AI and labs.docx` were extracted to text with
Quarto's Pandoc; only their graded prompts and the statement were displayed,
for the structures in section 5. None was read in full for student data
except PH213 Lab 2, vetted 2026-10-03 (`STATE.md`). The survey (pass 1)
reads every file in full before any conversion.

**Excluded until the owner rules (9.1).** Their names suggest student-made
or class-collected material, and the survey needs none of them:
- PH211: `GoodLabPartnert.txt`; `Descriptive.pdf` (root); the Lab 1 "Sample
  contracts" folder; the two Lab 6 "Makeup lab example description" files.
- PH212: Lab 1 "class data" and Lab 5 "class results" workbooks.
- PH213: Lab 1 "Sample results" workbook; the Lab 6 "Example presentations"
  folder.
- A Word lock file in the PH211 instructor folder (`~$b 1 - Team Building -
  Instructor notes.docx`); such files usually hold the name of whoever had
  the document open.

Data files, `.gambl` files, figures and slide decks are out of scope here.
D-0071's unbuilt "Lab files" group names only data files (CSV) and
simulations (HTML); how the rest attach to a lab is not designed.

**In scope for the survey:** the 19 handouts, the instructor notes (less the
excluded files), the rubric workbooks, the three curriculum summaries, and the
four course-wide files. Everything else is out of scope or excluded.

## 3. Rulings carried from chat (2026-10-06)

To be appended to `DECISIONS.md` as proposed entries once the critique
settles; the owner promotes.

Amended 2026-10-07: entered as D-0074 (3.1 to 3.4), D-0075 (3.5, 3.6),
D-0076 (3.7, 3.9), D-0077 (3.8), D-0080 (3.10) and D-0081 (3.11, resolved
for the private repo). Proposed by the owner: 3.1, 3.2, 3.3, 3.7, 3.8, 3.9,
3.10, and 3.11's git-ignore (declined, D-0093); by Claude: 3.5, 3.6. 3.4 is
a premise, not a rule. 3.5 confirmed alone (critique finding 8).

1. Students complete the report in a Word template generated per lab
   (approach B). The in-page worksheet (A) is held; Gradescope's Online
   Assignment (C) is declined (section 10).
2. Every section submits to Gradescope as a PDF, one report per group.
3. This is separate from the paper-versus-typed decision, which stays open.
4. The group's scribe writes the report on a lab PC or a laptop, never a
   phone; some groups open the Word file in Google Docs and co-edit there.
   The template must survive Word and Google Docs.
5. One question per page, so students tag pages to questions quickly.
6. The answer area is a one-cell bordered box. Untested: the owner's check in
   Word and Google Docs gates the template's merge.
7. The template adds two things the handout does not hold: a "Group
   members:" line on page 1, and an "AI use" slot at the end whose words live
   in their own file, so colleagues can edit it or delete it entirely.
8. The template's question numbers equal the handout's, which equal the
   original's. Gradescope outlines and the rubrics follow the original
   numbers. The rubrics are the owner's to edit in lockstep with handout
   changes; the outlines are not his task.
9. The lab page gets a separate button, "Download template (.docx)".
10. Templates wait until every handout is converted.
11. Instructor notes and rubrics are never tracked in this repo, which will
    be public. The owner proposed git-ignoring them here; section 7
    recommends the private instructor repo instead.

## 4. Design calls (Claude's, unless the owner rules otherwise)

1. **Generated, never committed.** `tools/downloads.py` writes
   `labs/<id>/<id>-report-template.docx` at every build from the same source
   through the same `tools/filters/questions.lua`, so numbers and words cannot
   drift. A committed template would be a second copy.
2. **A second filter, `tools/filters/report-template.lua`, after
   `questions.lua`.** One job each; `questions.lua` stays the only numberer.
3. **Draft notice and department line kept** from `tools/reference.docx`
   (D-0052 puts the banner on every download; dropping it would amend D-0052).
   So the template reaches students when the library does.
   Amended 2026-10-07 (D-0080): the template ships without the draft notice;
   every other download keeps it. Its header's content is pass 6's design.
4. **Word only.** A PDF template serves only the paper branch; held for it.
5. **Explicit page-break paragraphs**, not a "page break before" style, on
   the expectation that Google Docs keeps them on import (unverified; the
   owner's check settles it).
6. **The AI file** is Markdown, for example `site/report-template-ai-use.md`:
   its heading is the slot's label, its paragraph the prompt. Present: the
   template ends with the slot. Absent: no slot, no code change. A test
   covers both states. First words proposed: the statement's own sentence,
   "include a short note at the end of your report describing how it helped"
   (the statement's words, not Claude's), not a paraphrase.
7. **No response-kind attribute** in the source. In B every answer box is
   the same, so the attribute has no job; earmarked for the paper branch or
   the worksheet.
8. **Ordered question ids pinned per lab** by a test. Adding, removing or
   reordering a question fails the build until the pin is updated in the
   same PR with a ledger entry naming the numbers that moved: the owner's cue
   to edit the rubrics, and the outline maintainers' notice. Built in pass 2,
   so it holds from the first new conversion.
   Amended 2026-10-07 (D-0077, critique finding 11): the pin is a deliberate
   lock that fails loudly, like the logo hashes in `tests/test_assets.py`, not
   the second copy 4.1 declines. Agreement with the original is D-0078's job.

## 5. The interface: how a graded item is marked up

The conversion marks up graded items; the template filter reads that markup.
So the rules come first (pass 1), before any conversion. PH211 Lab 1 has
none of the cases below except S7 (its bold that is not a question, LEDGER
25); the sample (section 2) shows all of them. Item numbers are
from a plain-text extraction and are re-derived by the survey.

| | Structure | Seen in the sample | Proposed handling (ruled in pass 1) |
|---|---|---|---|
| S1 | Numbered item needing no answer | PH212 L1 #4, L2 #2 ("Read the box below") | Counted for numbering, marked no-answer; left out of the template, its number a visible gap |
| S2 | Stem whose answers are the next items | PH212 L1 #14, L2 #9 and #13 | Counted, marked stem; in the template its text heads its first child's page, no box |
| S3 | Lettered sub-parts, nested, lettering restarting | PH212 L1 #7 (a, b, i, ii, a second "a."), PH213 L2 #2 (a to c) | Inside the question block as written; one box per question unless 9.4 rules per part |
| S4 | Lists inside a question | PH212 L1 #19, PH213 L2 #2 | Inside the block; the Word box misses list items (D-0057), so the template pass must draw the question box another way |
| S5 | Equations in question text, inline and display | PH212 L1 #7, #13, #15; L2 #10; PH213 L2 #1, #10 | Pass 2 first: the word check must count them; Google Docs import of Word equations is part of the owner's check |
| S6 | A question citing another by number | PH212 L1 #7 ("question 4"), #17 ("question 11") | Numbers are content: the pin in 4.8 must hold them |
| S7 | Bold that is not a graded question | PH213 L2 ("You don't need to answer these questions in your report"; a voltage warning) | Never a question block |
| S8 | Actions or hints between a question's sub-parts | PH212 L1 #7 (two bullets between b and the second "a.") | Inside the block, as written; the TA sees the item whole |

The survey may add structures; each gets a row and a rule before conversion.

## 6. Passes

Six passes after this spec, each a session that ends with `/handoff`.
Subagent passes run under `subagent-driven-development` in a worktree.

Amended 2026-10-07 (D-0082): eight passes, in section 11.2's table, which
supersedes the table below. The cross-reference moved to pass 7 (D-0083);
the reviews are split as D-0090 says.

| Pass | Work | Lands | Gate before it starts |
|---|---|---|---|
| 1 | Vet and survey: read every in-scope file for student data; tabulate each handout's structures (section 5); amend `docs/conversion-spec.md` with one markup rule per structure | This repo: the conversion spec and a public survey table of handout structures. Instructor repo: notes and rubric facts | Spec ruled; exclusions ruled (9.1) |
| 2 | Word check counts equations and image alt text (`tools/check_unchanged.py`, item 4a); the ordered-ids pin (4.8); metadata handling for originals as ruled in 9.2 | PR, green `verify` | Pass 1's markup rules; 9.2 ruled |
| 3 | Convert PH211 Labs 2 to 7 (6), then cross-reference each with its instructor notes | PR here; findings in the instructor repo | Pass 2 merged |
| 4 | Convert PH212 Labs 1 to 6 (6), same | same | Pass 3 merged |
| 5 | Convert PH213 Labs 1 to 6 (6), same; PH213 Lab 2's metadata question (four-items Q16) is settled by 9.2 | same | Pass 4 merged |
| 6 | The template: filter, AI file, button on a board first, course download group, tests over every converted lab | PR; merge gated on the owner's Word and Google Docs check | Pass 5 merged |

**Why one template pass, not three.** The template is a build output with no
per-lab work: one filter over every converted source. Once it exists, every
lab has its template; a lab converted later gets one for free. Per-course
template passes would build the same filter three times or leave two passes
with nothing to do. Built last (rule 3.10), it meets every structure at once,
with the real converted labs as its test fixtures, so no made-up labs are
needed.

**Why not alongside each conversion.** There is no template work per lab to
do alongside; the only coupling is the markup, which pass 1 rules for both.

**In each conversion pass** (3 to 5), one task per handout:
- Implementer (Sonnet): Pandoc conversion, house markup per the amended
  conversion spec, front matter, original committed under `originals/` per
  9.2, the word check green.
- Task reviewer (Sonnet), scoped to what no machine checks: which items are
  questions, stems or no-answer items; block counts against the original.
- Cross-reference (Sonnet), once per course: each converted handout against
  its instructor notes. Findings name misalignments only, land in the
  instructor repo, and change nothing: conversion is format only.
- Final whole-pass review (Opus), once per pass, as the skill requires.

Floor per conversion pass: 6 implementers, 6 reviewers, 1 cross-reference, 1
final review, 14 dispatches before fix rounds. Pass 1 dispatches one Sonnet
reader per course (3) with a fixed output format; flags of possible student
data are judged in the main session, never quoted in a report.

## 7. Instructor notes and rubrics

Amended 2026-10-07: the home below is ruled (D-0081); the cross-reference
is pass 7 (D-0083); a CI check across the repos waits for the public flip
(D-0089).

**Home: `OSU-physics-lab-library-instructor`, private, tracked.** It already
holds PH211 Lab 1's instructor notes and rubric, converted, with its own word
check and CI. Its conversion rules for rubrics are already in
`docs/conversion-spec.md` ("Rubrics (instructor repo)"): one
`::: {.rubric-item question="<question id>"}` per scored question, the
question text found by id, never copied. A converted rubric is therefore
keyed to handout question ids, which is the lockstep mechanism; today that
is PH211 Lab 1's alone, and the unconverted rubrics name questions by number
in their cells ("Q1:").

The owner proposed keeping them git-ignored in this repo. Recommended
against, owner to rule in the critique: the private repo already tracks
them; an ignored file has no history, which lockstep needs ("what did the
rubric say when the handout said X"), and is not durable (charter floor 12);
a check that reads ignored files cannot run in CI, so it would pass
everywhere but one machine (floor 2); and one `git add -f` would put answer
keys into a public repo's permanent history.

**During passes 3 to 5:** the cross-reference reads the originals from the
folder in section 2 (or the instructor repo's `originals/`, if the owner
rules them copied there; 9.5). Its findings are the instructor repo's.

**Later, when content changes begin (not in these six passes):**
- Instructor repo check, rubrics: every `rubric-item` names a question id
  that exists in this repo's source. Not "every question has a rubric item":
  PH211 Lab 1's rubric scores four of its five questions.
- Instructor repo check, notes: structural only, once notes are converted:
  every question id or number the notes cite exists and matches. Whether the
  notes' prose agrees with a changed handout is a review, not a check.
- Direction: the private repo reads this one; this one never reads it.

## 8. Gates

1. No file on the exclusion list is opened until the owner rules (9.1).
2. No original is committed until 9.2 is ruled (ledger 18 commits originals
   byte for byte; their Word metadata names people, `STATE.md`).
3. No handout with an equation or an image is converted before pass 2 merges.
4. No conversion before pass 1's markup rules are in the conversion spec.
5. Conversion changes no content. Misalignments are recorded, never fixed.
6. The template merges only after the owner's Word and Google Docs check.
7. Nothing from the instructor notes or rubrics is written into this repo.

Amended 2026-10-07: gate 1 becomes "nothing outside the in-scope list is
opened", and `List of terms.docx` joins the exclusions (D-0084). Gate 2 is
D-0086's strip. Gates 3 and 4 repeat the pass gates (critique F16) and stay
as the record. Gate 6 is widened by D-0079.

## 9. Open questions for the critique

Answered 2026-10-07: 9.1 none opened, `List of terms.docx` added (D-0084);
9.2 every identity-bearing part stripped, both repos (D-0086); 9.3 pass 7
(D-0083); 9.4 one box per question unless the outlines split sub-parts,
asked in pass 6 (D-0075); 9.5 pass 7 (D-0083); 9.6 every course (D-0076);
9.7 the structure table here, nothing from notes or rubrics (D-0085); 9.8
fixed in pass 7 (D-0083).

1. **Exclusions.** May any excluded file be opened, and should any move out
   of the folder? Lean: none opened; the survey does not need them.
2. **Originals' metadata.** Commit originals byte for byte with names in
   their metadata (ledger 18 as it stands), or strip `creator` and
   `lastModifiedBy` first and record the stripped file's hash (amends ledger
   18)? Lean: strip, since the repo will be public and "roles, not names".
   PH211 Lab 1's committed original and its history stay a D-0062 question.
3. **Two PH211 Lab 6 instructor notes**, one with a person's email address in
   its file name. Which is canonical? Lean: the survey diffs them and reports;
   the owner picks; nothing is renamed or deleted without his word.
4. **Sub-parts in Gradescope.** Do the outlines grade lettered sub-parts as
   separate questions (7.a, 7.b)? If so, one box per sub-part; if not, one per
   question. Lean: one per question unless the outlines split them.
5. **Instructor originals.** Copy the notes and rubric workbooks into the
   instructor repo's `originals/` now (tracked, private), or read them in
   place until notes are converted? Lean: copy now; tracked beats a folder
   with no history.
6. **The AI slot's reach.** Does the AI statement apply to every PH 21X
   course? If not, the slot needs a per-course switch.
7. **Where the survey's results live.** Lean: the handout-structure table in
   this repo (public-safe), anything drawn from notes or rubrics in the
   instructor repo.
8. **Stale path.** The instructor repo's `CLAUDE.md` names
   `../Unsorted Legacy Resources/`, which does not exist (checked 2026-10-03
   for this repo). Fixed in pass 1.

## 10. Considered and declined

- **In-page worksheet (A), held.** Answer fields on the lab page, saved in
  the browser, exported by printing. One browser is one author, and groups
  co-edit; drafts left on a shared lab PC show the next section the last
  group's answers and names; phone photos exceed browser storage. Earmarked
  if typed reports win the paper decision.
- **Gradescope Online Assignment (C).** Built by hand per assignment in
  Gradescope: a second copy of every question. Group support unverified.
- **CSV or XLSX attachments.** No reader: a TA grading in Gradescope opens no
  spreadsheets, and an attachment cannot sit in a PDF.
- **HTML, JSON, or in-browser Word export.** Gradescope takes PDF; a Word
  export from the browser needs a library.
- **Templates in three per-course passes, or alongside each conversion.**
  Section 6.
- **A response-kind attribute in the source.** No job in B (4.7).
- **A committed template.** Drift (4.1).
- **A "page break before" style.** Google Docs import (4.5, unverified).
- **Template in PDF, HTML or Markdown.** Serves only the paper branch (4.4).
- **A plain empty paragraph as the answer area.** Invisible, so students
  guess where to type; the owner chose the box (3.6).

Amended 2026-10-07: the in-page worksheet's shared-PC reason is weaker than
stated above, since each student signs in to a lab PC with their own account
(the owner, D-0074); A stays held because one browser is one author and
groups co-edit. Declines added by the critique rounds are listed in 11.5.

## 11. Rulings of the critique rounds (2026-10-07)

### 11.1 How they were made

Step 1 is the two-pass critique beside this file. Steps 2 and 3 ran with the
owner on 2026-10-07 in eight question rounds, in the critique's order: pass
2's shape, pass 1's gates, order and purpose, then the rest. Each question
carried a lean, its reason and the cost of the alternative. For the two
disagreements between the critique passes (finding 2 against F1, finding 10
against F12), no lean was given. Every ruling is a `DECISIONS.md` entry,
proposed until the owner promotes it; the owner's words are quoted in each
entry's rationale.

### 11.2 Passes (D-0082; supersedes section 6's table)

| Pass | Work | Gate before it starts |
|---|---|---|
| 1 | Vet and survey (D-0084, D-0085): Sonnet readers may read the cleared files; per handout, structures, numbering counts (D-0078), em dashes, hash, deliverable; one markup rule per structure for every output in `docs/conversion-spec.md`; PH 212 and PH 213 course lists quoted (D-0088); `.superpowers/` in the root `.gitignore` | These entries promoted |
| 2a | Checks, one PR: equations and alt text in the word check; the number check (D-0078); the ids pin (D-0077); every equation probed through the Word and HTML writers, and an equation rule; `questions.lua` fails on a question not opening with a paragraph; the Word question box as a one-cell shaded table, rechecked by the owner in Word and Google Docs; the metadata strip (D-0086) | Pass 1's markup rules and counts |
| 2b | Downloads, one PR: `--resource-path`, `--mathml`, images extracted and published, CSS reverts, HTML caps per lab (four-items 4a); merged before pass 3 | Pass 1's survey (which labs carry images and equations) |
| 3 | The two hardest handouts by the survey (likely PH 213 Lab 2 and PH 212 Lab 1), then PH 211 Labs 2 to 7, hardest first (D-0092 for PH 213 Lab 2) | 2b merged |
| 4 | The rest of PH 212 | 3 merged |
| 5 | The rest of PH 213 | 4 merged |
| 6 | The template (D-0074 to D-0080): filter, AI file, button, tests; templates only for labs whose deliverable is a question report until the owner rules the rest | 5 merged; owner's Word and Google Docs check before merge |
| 7 | Cross-reference from an instructor checkout (D-0083): rubric "Qn:" text and notes' cited numbers against each handout; instructor originals copied and stripped; the two Lab 6 notes; stale path; that repo's check and Pandoc brought level | 6 merged |

Eight passes against a budget of six; recounted after the survey (D-0082).
Reviews per lab: Claude screenshots pages and PDFs; the owner checks Word
for the hardest two and one lab per later pass (D-0090).

### 11.3 Rulings by topic

- **What and why.** A Word template per converted lab, one PDF per group to
  Gradescope; it ships whether paper or typed wins, since paper worksheets
  would start from it (D-0074).
- **Layout.** One question per page; a one-cell bordered box per question
  unless outlines split sub-parts (D-0075). "Group members:" line; AI slot
  from its own file, every course, citing the statement by title, authors
  named per D-0073; "Download template (.docx)" (D-0076).
- **Numbers.** Equal to the original's; ids pinned as a deliberate lock
  (D-0077); checked through Pandoc where a pass-1 count shows simple
  numbering, the XML reader built only for a handout that needs it (D-0078).
- **Template checks.** The owner's Word and Google Docs check gates the merge
  and named changes reopen it; four invariants pinned; probe parameters
  recorded (D-0079).
- **Timing.** After all 18 conversions; Winter 2027 target, slipping if
  conversion does; no draft notice on the template, amending D-0052 for it
  alone (D-0080).
- **Instructor material.** Tracked in the private instructor repo (D-0081);
  read only in pass 7 (D-0083); cross-repo CI checks wait for the public flip
  (D-0089).
- **Vetting.** The owner's word clears the handouts, the PH 212 and PH 213
  summaries and the course-wide files; no pre-scan; nothing outside the
  in-scope list opened (D-0084).
- **Originals.** Every identity-bearing part stripped before commit, both
  repos, both hashes recorded, history not rewritten (D-0086); a Word
  original stays live until sections switch to the library's version
  (D-0087); each task re-hashes and stops on a change (D-0085).
- **Measure.** A TA estimate of minutes per report before Winter 2027, the
  same question a term after first use (D-0091).

### 11.4 Open

- Paper or typed: the owner's, still open; the template no longer waits on
  it (D-0074).
- When sections switch to the library's versions (D-0087): the owner's call.
- The survey's results: which handouts are the hardest two; numbering counts
  that send a handout to the owner (D-0078); any em dash (D-0085); which labs
  are not question reports (pass 6 rules); the recount of passes.
- Pass 6's design: the template's header in place of the draft notice; how
  sketches and photos reach the Word file (critique F8; PH 211 Lab 1
  question 2 asks for every member's sketch); the outline maintainers'
  answer on sub-parts; a near-blank page at a page foot, unprobed.
- The equation rule, from pass 2a's probe; Q13's stop applies.
- The TA estimate before Winter 2027 (D-0091): the owner's ask.
- Forgotten logouts on lab PCs: a lab-ops matter, outside this spec.

### 11.5 Considered and declined (full entries in `DECLINED.md`)

- D-0093: instructor notes and rubrics git-ignored here.
- D-0094: a no-print pre-scan before reading originals.
- D-0095: holding the template until paper or typed is decided.
- D-0096: no target term until the paper decision and the license settle.
- D-0097: the template built after pass 3, amending 3.10.
- D-0098: the cross-reference during the conversion passes (and F12's
  deletion of it).

Not declined but earmarked: the XML number reader (F1), built only where
D-0078's count calls for it.
