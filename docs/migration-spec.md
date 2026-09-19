# Migration spec: legacy Word to Markdown

Status: draft, 2026-09-19. Rulings in [../LEDGER.md](../LEDGER.md) win.

## Source format

One Markdown file per document with YAML front matter:

```yaml
id: ph211-lab01-handout      # stable, never reused
course: PH211
lab: 1
audience: student            # student | instructor | public
visibility: public           # public | private
layer: curriculum            # curriculum | osu-local
source_file: "PH211/Lab 1 - Team Building - Handout.docx"
source_sha256: "<hash of the original file>"
status: migrated             # migrated | verified | ruled-change
```

Handout conventions become fenced blocks, matching the Word custom styles so
Word output keeps its look through a Pandoc reference document:

- `::: action` for round-bullet action items (Word style `Actionitem`)
- `::: hint` for arrow items (Word style `Hint`)
- `::: box` for boxed key concepts and report expectations
- Report questions carry stable IDs such as `211-L1-Q3`; rubrics in the
  instructor repo reference those IDs rather than copying question text.

## Content-unchanged check

For each migrated document: extract normalized text from the original Word
file and from the Markdown, compare word by word. The comparison must be empty
except for differences recorded in the ledger. Equations compare as LaTeX
after Pandoc conversion. Images compare by count, and alt text is carried
over.

## Known hard cases

- Word equations (Lab Guidance for Students): Pandoc converts them to LaTeX;
  a plain text extraction drops them silently.
- Text-box annotations (Sample Lab Report): they appear twice in the raw
  file and are the pedagogical point of the document; they need a callout
  convention.
- Images and alt text: at least 25 images across Excel Skills and Lab
  Guidance for Students.

## Tooling

Pandoc 3.11 (installed 2026-09-19). Site generator not yet chosen; the site
is static and deploys on Vercel (ledger 3: no server needed now).

## Pipeline

Word (once) -> Markdown (source of truth) -> web and Word. Feedback on any
output is applied to the Markdown by a person. No automated Word-to-Markdown
re-import after the first migration.
