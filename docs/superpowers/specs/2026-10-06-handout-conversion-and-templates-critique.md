# Critique, step 1: handout conversion and report templates

Target: `2026-10-06-handout-conversion-and-templates-design.md` (this folder).
Step 1 of `/critique` (hard critique, before any question), run 2026-10-06 by
the session that wrote the spec, at the owner's request ("Run the hard
critique now, since you already hold the context"). Steps 2 and 3 (question
rounds, synthesis) are the next session's, with the owner. Findings are
proposals; none is ruled. Premises were checked against files the same day.
A second pass by a fresh agent follows the first (F1 to F16), with its
corrections to the first marked where they apply.

## Fixed in the spec before its first commit

Factual errors, corrected because a repo must not state them (charter floors
2 and 5). No design changed.

1. Section 4.6 called the AI statement "already approved by colleagues". No
   file in this repo or the owner's chat says so; the owner said colleagues
   may not support the slot. Now: the statement's own words, not Claude's.
2. Section 2 said the folder "agrees with" `site/courses.md`. True for PH211
   only: PH212 and PH213 list no labs there (`labs: []`). See finding 7.
3. Section 2 said the four sample files were read. Only their graded prompts
   were displayed from a text extraction; none was read in full for student
   data, which `CLAUDE.md` asks before planning around an original. PH213
   Lab 2 alone was vetted, on 2026-10-03 (`STATE.md`). Now said plainly.

## Findings, most severe first

1. **Equations will likely trip the build's warning gate.** Extracting the
   sample handouts with Quarto's Pandoc (3.10) to plain text printed
   "Could not convert TeX math" warnings for equations as Pandoc reads them
   from Word: PH213 Lab 2's `\overset{⃑}{F_{E}}` (a combining arrow), and
   PH212 Lab 2's `T = 2\pi\sqrt{\frac{L}{g}\ }\` ("unexpected eof", a trailing
   backslash). `tools/downloads.py` fails on any `[WARNING]`, and the Quarto
   build's gate fails on any Pandoc warning. The Word download converts TeX
   to Word equations through the same library, so it is at risk; the plain
   writer was the one observed, so this is unproven for Word. Bites: pass 3's
   first equation-bearing lab fails CI, and the only cure, rewriting the
   LaTeX, is a format change the word check (once it counts equations) must
   accept, by a rule nobody has written. Proposed: pass 2 probes every
   sample equation through the Word and HTML writers, and the conversion
   spec gains an equation rule (what normalization is allowed, and how the
   check compares an equation before and after). Section 6 names neither.

2. **Matching the original's numbers is ruled but nothing proves it.** Rule
   3.8 says template numbers equal the original's. The word check reads
   `w:t` only; Word's list numbers are not in `w:t`, so it cannot see them.
   The ordered-ids pin (4.8) freezes whatever order the conversion produced,
   not its agreement with the original. A wrong call on one S1 or S2 item
   shifts every later number, passes the word check, is then pinned, and
   silently puts the rubrics, the Gradescope outlines and in-text citations
   ("question 11", S6) out of step. Evidence that a check is feasible: the
   extraction showed Pandoc's reader keeping Word's numbering, including
   numbers that continue across parts (PH212 Lab 1: 9 and 10 after Part 4).
   Proposed: pass 2 adds a check that reads the original with Pandoc and
   compares its numbered-item sequence with the converted lab's question
   numbers. The two guards then have separate jobs: the original check
   during the conversion phase, the pin once ruled content changes begin.
   Unproven: whether Pandoc resolves a mid-question restart (PH212 Lab 1 #7's
   second "a.") the way Word displays it.

3. **The Word download breaks before the template exists.** D-0057: a
   question box drawn with `custom-style` misses list items, so a question
   holding a list (S4: PH212 Lab 1 #19, PH213 Lab 2 #2) draws in pieces. The
   spec defers the fix to pass 6, after all 18 conversions, so from pass 4
   (PH212) the production Word download shows broken boxes. Proposed: decide
   whether pass 2 fixes the box. A one-cell shaded table could draw the
   question box with the same mechanism as the answer box (3.6), one fix for
   both; whether Google Docs keeps cell shading is part of the owner's check.

4. **S1 and S2 have a template rule but no page rule.** `questions.lua`
   labels every `.question` "Question N" on the modern page, and ledger 29
   makes that block mean a graded question. Marking "Read the box below"
   (S1) or a stem (S2) as a question would print "Question 4: Read the box
   below on sources of uncertainty" on the modern page and box it in the Word
   download. Section 5 says only what the template does. Proposed: pass 1's
   rule states what each output shows for S1 and S2 (faithful page, modern
   page, Word download, template), with the faithful page keeping the
   original's "4)" exactly.

5. **The template's value waits on the launch, and the spec never says
   when students should have it.** Call 4.3 keeps "Draft: license pending,
   not for distribution." on every page; the license ask (D-0073) and the
   public flip (D-0062 to D-0066) are proposed, not ruled. The conversion of
   18 handouts comes first. If the owner wants templates in students' hands
   in a given term, that date drives the pass order and may need its own
   distribution ruling. Question: the target term, if any.

6. **No outcome measure.** The spec says how B is built, not how anyone will
   know it worked. The session named TA minutes per report as the measure;
   it is not in the spec, and without a baseline taken before first use
   there is nothing to compare. Lean-plus-earmark: a one-line estimate from
   a few TAs now, the same question a term after first use; or the owner
   declines a measure explicitly.

7. **The course pages now state something false.** `site/courses.md` says of
   PH212 and PH213: "none is in hand to list". Both curriculum summaries are
   in the owner's folder as of 2026-10-06. Ledger 43 quotes a course's lab
   list from its summary's Activities table. Proposed: after vetting the two
   summaries, quote both lists (a small PR, in pass 1 or before it), so
   course pages list the labs before they are converted, as PH211's does.
   Corrected by the second pass: the quoting rule is LEDGER 45, not 43 (43
   is the first site build); `site/courses.md` line 8 carries the same wrong
   citation, and the PR amends LEDGER 45's last sentence, so it needs a
   `DECISIONS.md` entry.

8. **A ruling recorded on an ambiguous yes.** Rule 3.5 (one question per
   page) rests on the owner's "Yes" to a question that bundled two things:
   whether every section submits a PDF to Gradescope, and the proposal to
   start each question on a page. Confirm before it goes in the ledger.

9. **The order of passes changes an earlier answer without a ruling.** On
   2026-10-03 the owner chose PH213 Lab 2 as the next conversion (`STATE.md`;
   item 4b). The spec moves it to pass 5. Separately, the conversion rules
   are tested hardest by the handout with the most structures (PH212 Lab 1
   shows S1 to S6 and S8), and a course-by-course order may meet it last.
   Proposed: each conversion pass orders its tasks hardest first by the
   survey, and the owner confirms or re-rules the course order.

10. **Pass 1's instructor landing has no job.** Section 6 has pass 1 land
    "notes and rubric facts" in the instructor repo, a phrase that can be
    read two ways, and the cross-reference is in passes 3 to 5 anyway.
    Delete it, keeping only a vetting record per instructor file (clean, or
    flagged at a location, never quoting) in the instructor repo's ledger.

11. **The pin looks like the drift the spec declines.** 4.1 declines a
    committed template as a second copy; 4.8's pinned id list is also a
    second copy of the source's order. It is a deliberate lock that fails
    loudly, like `tests/test_assets.py`'s logo hashes. The spec should say so,
    or a reader will take 4.1 and 4.8 as a contradiction.

12. **The usage estimate is partial.** The owner's budget was six passes in
    total; the spec's six exclude the critique session that settles it, so
    seven sessions at least. It counts dispatches for the conversion passes
    (14 each, before fix rounds) and pass 1 (3), but not passes 2 and 6.
    Estimate them or mark them unknown.

13. **The later rubric check needs a secret, or the public flip.** Section
    7's instructor-repo check reads this repo's source. While this repo is
    private, the instructor repo's CI needs a token or deploy key to read it,
    and `CLAUDE.md` forbids touching a secret without the owner's word. After
    the flip it needs none. Name the dependency: build it after the flip, or
    rule a key.

14. **Quoting the AI statement is quoting co-owned work.** The statement is
    not in this repo, its authors are not recorded, and its terms are as
    unsettled as the handouts'. The template would quote its sentence
    without credit (charter floor 9: authors are kept). Question: convert the
    statement as a library document the slot can name, or credit it in the
    AI file.

## Checked and found sound

- PH211 Lab 1's rubric scores four of five questions
  (`good-lab-partner`, `build-process`, `contributions`, `rebuild-changes`;
  not `sketches`), as section 7 says.
- D-0052's title carries "each carrying the draft banner", as call 4.3 says.
- The SDD workspace `.superpowers/sdd/` is ignored by its own `.gitignore`,
  so pass ledgers cannot be committed by accident. Disputed by the second
  pass (its finding 13): that `.gitignore` is untracked (`git ls-files
  .superpowers` is empty) and the root `.gitignore` has no rule, so this
  holds in the main checkout only, not in a fresh worktree.
- The instructor repo has its own word check (`tools/check_unchanged.py`)
  and CI (`.github/workflows/verify.yml`), as section 7 says. Disputed in
  part by the second pass (its finding 10): its CI installs Pandoc 3.11,
  which the library retired (D-0044, D-0061), and pass 2 would break its
  LEDGER 5 rule that the check is an identical copy.
- The counts in section 2's table match the folder's file list (86 files in
  all, listed by name 2026-10-06).

## Second pass (a fresh agent, 2026-10-06)

The owner asked for a second hard critique by a fresh subagent that had not
seen the conversation; it read the spec, formed its critique, then read the
first pass and dropped exact duplicates. Its 16 findings are condensed below
as F1 to F16, most severe first. The session that wrote the spec re-checked
these citations before recording them: the four-items plan's 4a scope and
Q12 to Q17 (lines 367 to 368, 506 to 529); LEDGER 22(e) and 45; the em-dash
scan's paths (`verify.yml` lines 38 to 41); `render.converted_labs` needing a
`document` key; `.superpowers/` untracked; the instructor repo's Pandoc 3.11
and LEDGER 5; and the handouts' file dates (11 of 19 dated 2026-07-20 to
2026-08-20, by `ls -l`). Not re-checked, the second pass's own reads: Lab 1's
`numbering.xml` ids and formats, the rubric workbooks' sheet names, the
`app.xml` Company field, file sizes.

- **F1, high. The number check must read Word's numbering from the XML,
  not through Pandoc.** Disputes the method of finding 2. The word check
  reads the original "independent of Pandoc" (`docs/conversion-spec.md`),
  and the four-items plan declined Pandoc as the source of truth for images
  for the same reason (line 537). Questions become Divs at conversion, so
  Pandoc's numbers are lost, and `questions.lua` hard-codes the faithful
  "N)" from Lab 1. Proposed: in pass 2, map each question, stem and
  no-answer block to its source paragraph (the word alignment exists) and
  compute Word's displayed label from `numPr` and `numbering.xml`, restarts
  included; compare with both presentations, letter formats included. Pass
  1 tabulates each handout's list formats. Owner ruling only if some
  original is not "N)".
- **F2, high. "Supersedes 4a and 4b" drops most of 4a and five open
  questions.** Pass 2 lists only the check, the pin and metadata. 4a also
  carried `--resource-path` and `--mathml` for the downloads, image
  extraction and alt-text compare, CSS for img, figure and math, and HTML
  caps per lab; Q12 (the labelled photo), Q13, Q14, Q15 and Q17 are missing
  from spec section 9. Section 5 has no row for text boxes over a photo,
  one-cell tables whose description repeats the box text, or math letters
  outside the font subset, all already in the four-items premises. A
  plain-text sample cannot see them. Proposed: pass 2 is all of 4a (or 2a
  and 2b); carry Q12 to Q15 and Q17 with their leans; survey columns read
  from the XML. Extends finding 1.
- **F3, medium-high. FERPA: delegated vetting puts unvetted text into three
  more transcripts, and the exclusions have holes.** "Never quoted in a
  report" protects the report, not the reader's context. The four
  course-wide files are assigned to no reader. `PH211/List of terms.docx` at
  the course root is not excluded, though LEDGER 22(e) groups it with the
  sample-contract candidates and records that the PDF names a TA and a
  term. Out-of-scope files (make-up data, raw CSVs) are not forbidden by
  gate 8.1. Proposed: a pre-scan script that prints counts and locations
  only (comment and revision authors, `people.xml`, email patterns, 9-digit
  numbers, document properties), then only flagged spots are read, by the
  main session or the owner; gate 8.1 becomes "nothing outside the in-scope
  list is opened". Owner rules whether vetting may be delegated.
- **F4, medium (conditional). The em-dash scan can collide with
  format-only conversion.** CI fails on U+2014 in `curriculum/` and `site/`,
  and the word check fails on any changed word, so an original holding an
  em dash has no legitimate route to green; the AI file in `site/` has the
  same exposure. Whether any original holds one is unverified. Proposed: the
  survey counts them; a rule before pass 3; implementers never write
  `ruled_omissions` or `ruled_additions` without a promoted entry.
- **F5, medium. The originals are live documents.** 11 of 19 handouts were
  saved between 2026-07-20 and 2026-08-20, and sections use the Word files
  now. Nothing freezes them or detects a later edit, and rule 3.8 does not
  say which version is "the original". Proposed: pass 1 records each hash;
  each task re-hashes and stops on a change; a rule on who edits a Word
  original after conversion and how the edit reaches the Markdown.
- **F6, medium. Spec 9.2 is too narrow.** Identity also sits in comment and
  revision authors, `people.xml`, `app.xml`, template paths, and photo EXIF,
  and in both repos: the instructor repo's committed rubric workbook carries
  `creator` and `lastModifiedBy` (presence checked by the second pass).
  Proposed: widen 9.2 to every identity-bearing part and both repos; EXIF
  stripped or ruled before any image is published.
- **F7, medium. The template does not fit every lab.** If paper wins the
  open decision, pass 6 has no user, and its gate does not say so. Capstones
  span two weeks with their own rubric sheets; some labs may hand in paper
  data sheets (file names only); the legend counts "data, plots, or
  drawings" as report items, which a questions-only template drops; and the
  handout itself says "If you submit through Gradescope". Proposed: pass 6's
  gate adds "typed ruled, or the owner rules B ships regardless"; the survey
  records per lab the deliverable, weeks and submissions; capstones get a
  rule. Extends findings 5 and 8.
- **F8, medium. The reason for holding A applies to B.** A Word file on a
  shared lab PC leaves names and answers in Downloads, the recent-files list
  and AutoRecover; and how sketches and photos reach a lab PC's Word file is
  untested, though Lab 1 question 2 asks for every member's sketch.
  Proposed: record the lab PCs' reset policy (a lab-ops fact) beside the
  decline, and name where the file is saved and how photos arrive.
- **F9, medium. A one-time owner check gates a file rebuilt on every push.**
  Gate 8.6 covers the first merge only; later changes to sources, filters,
  `reference.docx`, the Pandoc pin or the AI file ship unchecked, and pass 6
  names no test invariants. The probe's parameters (one-cell table, row
  height 1440 twips, border colour 8C8C8C) are recorded nowhere durable, and
  explicit page breaks may leave a near-blank page when an answer ends at a
  page foot (unprobed). Proposed: name what reopens the owner check; pin
  per template that question words equal the source's, page breaks equal
  answered items less one, one table per answered item, an at-least row
  height; record the owner's check in an entry, as D-0057 did.
- **F10, medium-low. Pass 2 breaks the instructor repo's copy rule** (its
  LEDGER 5), and that repo's CI still installs Pandoc 3.11. Proposed: pass 2
  updates the instructor copy and its Pandoc, or the owner rules it may lag.
- **F11, medium-low. The rubric lockstep exists for 1 lab of 19.** Only
  PH211 Lab 1's rubric is converted and keyed by id; the others name
  questions as "Qn:" text. F1's check is the interim guard. (Spec section 7
  corrected; see below.)
- **F12, medium-low. The cross-reference has no job yet, and several
  outputs have no named file.** In a format-only phase its findings change
  nothing, they land in the instructor repo with no file named, written
  from a library worktree (a path around gate 8.7). Pass 1's survey table,
  the outline maintainers' notice (4.8) and 9.2's second hash have no named
  home. Proposed: delete the cross-reference until content changes begin,
  or name its file and run it from an instructor checkout; name the rest.
  Contradicts finding 10, which keeps it.
- **F13, medium-low. Worktrees break the relative path and may lose the
  SDD ignore.** Proposed: pass prompts carry the absolute originals path;
  track a `.superpowers/` line in the root `.gitignore` before pass 1.
- **F14, low-medium. Three code paths.** (a) `questions.lua` counts a
  question before checking that it opens with a paragraph, then returns
  silently, so a block opening with a list keeps a number but gets no label;
  make it an error. (b) S8 breaks the D-0057 Word box as S4 does; add it to
  finding 3's fix. (c) PH212 and PH213 labs stay off course pages, tiles and
  the course download until each has a `document` key in `site/courses.md`;
  add the keys per conversion through an entry amending LEDGER 45.
- **F15, low-medium. Spec section 3 mixes rulings, restatements and
  Claude's calls.** 3.11 restates LEDGER 2 and embeds a recommendation; 3.7's
  mechanism is also call 4.6; 3.4's "never a phone" is a premise, not a
  ruling; no rule records who proposed it, which `DECISIONS.md` requires.
  Proposed: a proposed-by per rule; 3.4 to premises; 3.7's mechanism to
  section 4. Extends finding 8.
- **F16, low. Smaller errors and parts with no job.** Three spec errors,
  fixed (below). Gates 8.3 and 8.4 repeat the pass gates. The owner's review
  of 18 labs, each four downloads and two pages, is uncounted, and his time,
  not dispatches, is the binding cost. The AI statement is unvetted, yet 4.6
  plans around its sentence; the probe's paraphrase is the one 4.6 declines.

**Fixed in the spec from the second pass** (factual, no design changed):
section 5 said PH211 Lab 1 has none of the structures, but it has S7 (bold
that is not a question, LEDGER 25); section 7 said rubric rows are keyed to
question ids, true only for PH211 Lab 1's converted rubric; section 2 read
D-0071's Lab files group as covering figures and slide decks, but it names
only data files (CSV) and simulations (HTML).

## For the question rounds

Load-bearing first. Pass 2's shape: findings 1, 2, 3 with F1 (how the number
check reads Word), F2 (all of 4a, Q12 to Q15 and Q17) and F14. Pass 1's
gates: spec 9.1 and 9.2 with F3 (who may read unvetted files, a no-print
pre-scan) and F6, plus finding 4, F4 and F5. Order and purpose: findings 5,
8, 9 with F7 (does the template fit every lab, and does it wait on paper or
typed). Then the rest of spec section 9, findings 6, 7, 10 to 14 and F8 to
F13, F15, F16. Where the two passes disagree (finding 2's method against F1,
finding 10 against F12), the owner rules.
