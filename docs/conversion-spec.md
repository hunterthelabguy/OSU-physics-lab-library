# Conversion spec: original Word documents to Markdown

Status: draft, 2026-09-19. Rulings in [../LEDGER.md](../LEDGER.md) win.

## Identity: descriptors, never sequence numbers

Lab order changes and labs get replaced, so no identifier encodes a position
(ledger 14). An `id` is the course code plus a descriptor unique enough that
it will never be reused, even after the item is retired. File names follow
the `id`. Position lives in a separate field that can change freely.

```yaml
id: ph211-team-building-handout   # permanent, never reused
course: PH211
sequence: 1                       # current position in the term; editable
audience: student                 # student | instructor | public
visibility: public                # public | private
layer: curriculum                 # curriculum | osu-local
source_file: "originals/PH211/Lab 1 - Team Building - Handout.docx"
source_sha256: "<hash of the original file>"
status: converted                 # converted | checked | ruled-change
ruled_omissions: []               # see Content-unchanged check
ruled_additions: []
```

Retired ids are listed in the ledger so they are never reissued.

## Handout conventions

The handout legend gives three conventions a reader sees: bold numbered
questions, round-bullet actions, arrow hints. Blocks are classified by the
glyph the reader sees, not by the Word style name, because the originals use
several styles for the same glyph (ledger 19).

- `::: action` wraps a list of round-bullet items.
- `::: hint` wraps a list of arrow items.
- `::: box` wraps boxed content (the legend is a one-cell table in Word).
- `::: {.question #<id>}` holds one report question. The id is a descriptor
  scoped to the document, for example `ph211-team-building:build-process`.
  The question text is stored plain; bold and the number a student sees
  ("Question 3") are applied at display time from document order.
- `::: legend-question` is the legend's sample of question styling; it is
  not a question.

## Rubrics (instructor repo)

One file per lab, one `::: {.rubric-item question="<question id>"}` per
scored question: the objective in bold, then an ordered list starting at 0
giving the description for each score. The question text is not copied; it
lives in the handout and is found by id. The spreadsheet's header row and
question-text cells are declared as ruled omissions.

## Originals

Each original file is committed under `originals/`, byte for byte, and its
SHA-256 is recorded in the converted file's front matter (ledger 18).

## Content-unchanged check

`tools/check_unchanged.py FILE.md ...` verifies the original's hash, reads
the original's words straight from the Office XML (independent of Pandoc),
reads the Markdown's words from Pandoc's parse tree, and compares the two
word sequences. It fails on any difference that is not declared in front
matter as `ruled_omissions` or `ruled_additions`, each with a ledger
reference; a declared passage that does not occur also fails. CI runs it on
every file with a `source_file` (ledger 20).

What it does not check: structure (headings, list nesting, which block a
line sits in), emphasis, and images. Structure is reviewed by counting blocks
in the parse tree against the original. Equations and image counts are to be
added when the first document that has them is converted.

## Known hard cases

- Word equations (Lab Guidance for Students): Pandoc converts them to LaTeX;
  a plain text extraction drops them silently.
- Text-box annotations (Sample Lab Report): they appear twice in the raw
  file and are the teaching point of the document; they need a callout
  convention.
- Images and alt text: at least 25 images across Excel Skills and Lab
  Guidance for Students.

## Tools

Pandoc 3.11 (installed 2026-09-19). Website builder not yet chosen; the site
is static and deploys on Vercel (ledger 3: no server needed now).

## Flow

Word (once) -> Markdown (source of truth) -> web and Word. Feedback on any
version is applied to the Markdown by a person, and the other versions are
rebuilt from it. After the first conversion there is no reverse path from
Word back to Markdown.
