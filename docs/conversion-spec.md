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
source_file: "PH211/Lab 1 - Team Building - Handout.docx"
source_sha256: "<hash of the original file>"
status: converted                 # converted | checked | ruled-change
```

Retired ids are listed in the ledger so they are never reissued.

## Handout conventions

Handout conventions become fenced blocks, matching the Word custom styles so
the Word version keeps its look through a Pandoc reference document:

- `::: action` for round-bullet action items (Word style `Actionitem`)
- `::: hint` for arrow items (Word style `Hint`)
- `::: box` for boxed key concepts and report expectations

Report questions carry descriptor ids scoped to their document, for example
`ph211-team-building:build-process`, never a question number. The number a
student sees (Question 3) is display only and may change. Rubrics in the
instructor repo reference the descriptor id rather than copying question
text.

## Content-unchanged check

For each converted document: extract normalized text from the original Word
file and from the Markdown, compare word by word. The comparison must be empty
except for differences recorded in the ledger. Equations compare as LaTeX
after Pandoc conversion. Images compare by count, and alt text is carried
over.

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
