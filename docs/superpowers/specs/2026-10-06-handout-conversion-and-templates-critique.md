# Critique, step 1: handout conversion and report templates

Target: `2026-10-06-handout-conversion-and-templates-design.md` (this folder).
Step 1 of `/critique` (hard critique, before any question), run 2026-10-06 by
the session that wrote the spec, at the owner's request ("Run the hard
critique now, since you already hold the context"). Steps 2 and 3 (question
rounds, synthesis) are the next session's, with the owner. Findings are
proposals; none is ruled. Premises were checked against files the same day.

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
  so pass ledgers cannot be committed by accident.
- The instructor repo has its own word check (`tools/check_unchanged.py`)
  and CI (`.github/workflows/verify.yml`), as section 7 says.
- The counts in section 2's table match the folder's file list (86 files in
  all, listed by name 2026-10-06).

## For the question rounds

Load-bearing first: findings 1, 2 and 3 shape pass 2; finding 4 and spec
9.1, 9.2 gate pass 1; findings 5, 8 and 9 set the order. Then the rest of
spec section 9, and findings 6, 7, 10 to 14.
