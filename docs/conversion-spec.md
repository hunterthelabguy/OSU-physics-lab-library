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
  The question text is stored bold, exactly as in the original; the number
  a student sees ("Question 3") is applied at display time from document
  order. Display never adds or removes bold (ledger 23).
- `::: legend-question` is the legend's sample of question styling; it is
  not a question.

## Markup rules per structure (D-0101)

Ruled 2026-10-07 from pass 1's survey (`docs/handout-survey.md`, which
lists where each structure occurs). S1 to S8 are the design spec's
section 5; S9 to S17 the survey's. Each row gives what the source holds
and what the four outputs show. "Box" is the question box, which pass 2a
redraws in Word as a one-cell shaded table (D-0082); "Template" is pass
6's report template (D-0075, D-0079).

| | Source | Faithful page | Modern page | Word download | Template |
|---|---|---|---|---|---|
| S1 top level | `::: {.question .no-answer #id}`; counted by `questions.lua` | "N)" and its bold, as Word shows | The number alone as its label, never "Question N"; text unbolded; no box | As modern: the number, no box | Left out, its number a visible gap (D-0075) |
| S1 part | A list item as written; no markup | As written | As written | As written | Inside its question's page |
| S2 | One question block: the stem's paragraph, then its parts (S3) | "N)", stem, parts | "Question N" (the stem is question N), one box around stem and parts | One box | Stem and parts on one page; one box after the last part, or one per part if the outlines split parts (D-0075) |
| S3 | An ordered list inside the block, nested and marked ("a.", "i.") as Word shows | Word's letters exactly | Word's letters; unbolded | Inside the box | As S2 |
| S4 | Inside the block as written: round bullets `::: action`, arrows `::: hint`, others plain | As written, bold kept | Inside the box; lean: every paragraph and item in the block unbolded, where `questions.lua` today unbolds only the first | Inside the box | On the question's page, above the answer box |
| S5 | Pandoc's TeX math from Word's equations, display kept display; italic-text symbols stay text | Rendered math | Rendered math | Word equations | As Word; the equation rule itself comes from pass 2a's probe (D-0082) |
| S6 | Text as written, no link | As written | As written | As written | As written; the number check and the ids pin keep it true |
| S7 | A plain paragraph, `**bold**` as written, never in a question block | Bold | Bold (bold is emphasis on modern) | Bold | Absent |
| S8 | `::: action` or `::: hint` inside the block, where Word puts it | In place | In place, inside the box | Inside the box | On the question's page, in place |
| S9 | `::: {.question .restart #id}` on the first question of a run Word restarts; `questions.lua` resets its count there. Lists that continue need nothing | Word's numbers | Word's numbers | Word's numbers | Word's numbers (rule 3.8). Waits on the owner's reading in section 3 |
| S10 | No new markup: the parts are nested as S3 by Word's level, though Pandoc's draft makes them questions | As S3 | As S3 | As S3 | As S2. Caught by a number check that reads Word's numbering, never Pandoc's |
| S11 | `::: report-item` around it; nothing numbers it | As written | As written, no box | As written | Lean: included with an answer box and no number; pass 6 rules. Marked at conversion so pass 6 can find it |
| S12 | `![alt](file)` at Word's position, alt Word's `descr` verbatim, empty where Word's is | As placed | As placed | As placed | Included when inside a question's block |
| S13 | An SVG the build makes from the original's shapes, groups and text boxes, its text kept as SVG text at Word's positions (so the word check can read it), with a PNG made from that SVG for Word. Pass 2b first measures LibreOffice's SVG of the three figures against Word; a small converter only if it is not faithful (D-0101) | The SVG | The SVG | The PNG | As S12, the PNG |
| S14 | One-cell tables `::: box`; other tables as Pandoc tables, blank cells blank; a box between parts stays inside its question block; rubric tables converted as handout content | As written | As written | As written | Lean: a table a question asks students to fill in is copied under that question; pass 6 rules |
| S15 | Not converted: page numbers and running headers (outside `document.xml`, so the word check loses nothing). The contents field becomes a list of links to the same headings, words unchanged. SEQ numbers stay text as stored. A content control's text stays plain text; empty controls vanish. The SYMBOL field gives what Word displays (section 6) | As listed | As listed | As listed | Absent |
| S16 | No markup; recorded in the table | | | | Pass 6 rules each lab's scope on this evidence (D-0085) |
| S17 | The owner's ruling before those conversions (section 7) | | | | |

## Rubrics (instructor repo)

One file per lab, one `::: {.rubric-item question="<question id>"}` per
scored question: the objective in bold, then an ordered list starting at 0
giving the description for each score. The question text is not copied; it
lives in the handout and is found by id. The spreadsheet's header row and
question-text cells are declared as ruled omissions.

## Originals

Each original file is committed under `originals/`, byte for byte, and its
SHA-256 is recorded in the converted file's front matter (ledger 18).

2026-10-07, D-0086 (amends ledger 18): every identity-bearing part is
stripped before commit (`core.xml` creator and lastModifiedBy, `app.xml`
Company and template, comment and revision authors, `people.xml`, photo
EXIF); `source_sha256` names the stripped file, and an entry records both
hashes. No `w:t` changes. A Word original stays live until sections switch
to the library's version (D-0087).

## Content-unchanged check

`tools/check_unchanged.py FILE.md ...` verifies the original's hash, reads
the original's words straight from the Office XML (independent of Pandoc),
reads the Markdown's words from Pandoc's parse tree, and compares the two
word sequences and the bold state of every word outside headings (ledger
24). Bold in the original is resolved through run, character style, and
paragraph style. It fails on any difference that is not declared in front
matter as `ruled_omissions` or `ruled_additions`, each with a ledger
reference; a declared passage that does not occur also fails. CI runs it on
every file with a `source_file` (ledger 20).

What it does not check: structure (headings, list nesting, which block a
line sits in), italics, underline, and images. Structure is reviewed by counting blocks
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

2026-10-01: the word check now reads with the Pandoc bundled with the pinned
Quarto (3.10 under Quarto 1.10.18; D-0044). The standalone 3.11 stays only for
the old build until phase 4 (D-0046). The 2026-09-19 line above records what
the first conversion was checked with.

2026-10-02: phase 4 retired the old build and the standalone Pandoc 3.11
with it (D-0061). Every tool and test reads with Quarto's bundled Pandoc.

## Flow

Word (once) -> Markdown (source of truth) -> web and Word. Feedback on any
version is applied to the Markdown by a person, and the other versions are
rebuilt from it. After the first conversion there is no reverse path from
Word back to Markdown.
