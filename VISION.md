# Vision: the OSU physics lab library

Status: draft, 2026-09-19. Rulings live in [LEDGER.md](LEDGER.md) and win
over this document.

## What it is

A deployed public website where students, faculty in the department, and the
general public can read the curriculum for the introductory physics labs
(the PH 21X sequence first) and use the software tools built to support the
labs, the curriculum, and lab operations.

## Principles

1. **Learning happens in students' minds, not in documents.** The documents
   are infrastructure for that learning. Effort goes to the decisions that
   shape learning (pedagogy, TA preparation, what changes and why), not to
   retyping.
2. **One copy we edit, per document.** Each document is one Markdown file.
   Web pages, Word files, and other versions are built from it and never
   edited directly. Feedback on any form is applied to the Markdown, and the
   other versions are rebuilt.
3. **Portable curriculum, local layer.** The curriculum is written so another
   institution can adopt it. OSU-specific operations live in a separate
   layer.
4. **Authors are kept.** Prior authors are credited; credit is extended,
   never replaced. Credits are pending the license conversation (ledger 8).
5. **Changes are ruled, not drifted.** Every change to wording is a dated
   ledger entry by a named role.
6. **Open about method.** How this material was made is published with it
   (see below, and the site's "How this site works" page).

## How this was made

The public page that explains how the site is built, how it is checked, and
who did the work is "How this site works", from
`site/how-this-site-works.md` (D-0072). Its commitments, in the current
phase:

- **No content changes.** Wording, curriculum, objectives, and conventions
  are exactly as the original authors wrote them. This is a change of format
  only.
- **The claim is checked, not asserted.** For each document, the text of the
  original Word file is compared with the text of the Markdown version. The
  comparison must be empty except for differences recorded and ruled in the
  ledger.
- **The originals remain.** Anyone who prefers not to use the converted
  material can teach from the original files and lose nothing.
- **Same standard as students.** The project follows the students' own AI
  policy in these labs: disclose use, keep the reasoning human, and the human
  answers for the work.

The standard for the later phase, when wording does change, is still open
(ledger 11).

## Outputs

Each resource is one Markdown file, and every other form is built from it:
a web page to read on screen, and downloads (Markdown, HTML, Word, PDF) for
anyone who wants a copy or a printed page. Students read on screen today, so
the site is the way in, but print is first class: paper may become the
graded artifact in the lab.

During the pilot each document also renders two ways from that one source
(ledger 28): one faithful to the original page settings, one following the
evidence review. The point is to show the difference and agree on it, not to
keep both forever.

## Out of scope for now

Instructor notes and rubrics (instructor repo, pending a faculty meeting);
gated access; content changes; a write-up of how this work was done (ledger 13).
