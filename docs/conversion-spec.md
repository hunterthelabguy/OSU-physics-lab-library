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

Amended 2026-10-07: the faithful page is retired (D-0108), so the Faithful
column lapses; S1 at the top level is a checkpoint (D-0109, D-0110).

Amended 2026-10-08 (pass 2b; D-0117, D-0118): S12 and S13 as built, below
the table under "Pictures and drawn figures".

Amended 2026-10-08 (pass 3; D-0120, D-0122): headings, box alt text and the
number check's places for second lists, under "Pass 3 additions" below the
table.

| | Source | Faithful page | Modern page | Word download | Template |
|---|---|---|---|---|---|
| S1 top level | `::: {.checkpoint #id}` (D-0109, D-0110); counted apart from questions | (retired, D-0108) | "Checkpoint N" on its own count, in a question-like block of another palette colour (chosen on a board); questions keep Word's numbers | The same label and block | Left out |
| S1 part | A list item as written; no markup | As written | As written | As written | Inside its question's page |
| S2 | One question block: the stem's paragraph, then its parts (S3) | "N)", stem, parts | "Question N" (the stem is question N), one box around stem and parts | One box | Stem and parts on one page; one box after the last part, or one per part if the outlines split parts (D-0075) |
| S3 | An ordered list inside the block, nested and marked ("a.", "i.") as Word shows | Word's letters exactly | Word's letters; unbolded | Inside the box | As S2 |
| S4 | Inside the block as written: round bullets `::: action`, arrows `::: hint`, others plain | As written, bold kept | Inside the box; lean: every paragraph and item in the block unbolded, where `questions.lua` today unbolds only the first | Inside the box | On the question's page, above the answer box |
| S5 | Pandoc's TeX math from Word's equations, display kept display, corrected where the round trip differs (equation rule below); italic-text symbols stay text | Rendered math | Rendered math | Word equations | As Word; the equation rule itself comes from pass 2a's probe (D-0082) |
| S6 | Text as written, no link | As written | As written | As written | As written; the number check and the ids pin keep it true |
| S7 | A plain paragraph, `**bold**` as written, never in a question block | Bold | Bold (bold is emphasis on modern) | Bold | Absent |
| S8 | `::: action` or `::: hint` inside the block, where Word puts it | In place | In place, inside the box | Inside the box | On the question's page, in place |
| S9 | `::: {.question .restart #id}` on the first question of a run Word restarts; `questions.lua` resets its count there. Lists that continue need nothing | Word's numbers | Word's numbers | Word's numbers | Word's numbers (rule 3.8). Word's labels are read (D-0102); `.restart` needs no start value once PH 213 Lab 6's "0)" is a checkpoint (D-0112) |
| S10 | No new markup: the parts are nested as S3 by Word's level, though Pandoc's draft makes them questions | As S3 | As S3 | As S3 | As S2. Caught by a number check that reads Word's numbering, never Pandoc's |
| S11 | `::: report-item` around it; nothing numbers it | As written | As written, no box | As written | Lean: included with an answer box and no number; pass 6 rules. Marked at conversion so pass 6 can find it |
| S12 | `![alt](<id>-media/<name>){width="Win" height="Hin" crop="l t r b"}` at Word's position (after its paragraph's words when Word anchors it), alt Word's `descr` verbatim, empty where Word's is; size and crop Word's; the file in front matter `images:` (D-0118) | As placed | As placed, at Word's size and crop | As placed, at Word's size and crop | Included when inside a question's block |
| S13 | `![alt](<id>-media/<name>.svg){.drawn drawings="<docPr ids>"}` after its paragraph's words; the build makes the SVG from the original's drawings with tools/figures.py, its labels and equation SVG text at Word's positions, and a PNG from that SVG for Word (D-0101, D-0117). A lone text box is `::: box` (S14) | The SVG | The SVG, inline | The PNG | As S12, the PNG |
| S14 | One-cell tables `::: box`; other tables as Pandoc tables, blank cells blank; a box between parts stays inside its question block; rubric tables converted as handout content | As written | As written | As written | Lean: a table a question asks students to fill in is copied under that question; pass 6 rules |
| S15 | Not converted: page numbers and running headers (outside `document.xml`, so the word check loses nothing). The contents field becomes a list of links to the same headings, words unchanged. SEQ numbers stay text as stored. A content control's text stays plain text; empty controls vanish. The SYMBOL field gives what Word displays (section 6) | As listed | As listed | As listed | Absent |
| S16 | No markup; recorded in the table | | | | Pass 6 rules each lab's scope on this evidence (D-0085) |
| S17 | The owner's ruling before those conversions (section 7) | | | | |

## Pass 3 additions (D-0120, D-0122)

- **Headings.** The Word Title is the page's one `#`. Where the Word file
  uses no Heading 1, Heading 2 is `##` and Heading 3 `###`. Where it uses
  Heading 1 (Week and Appendix headings: PH 212 Lab 3, PH 211 Labs 3 and 7),
  Word's outline moves down one level whole: Heading 1 `##`, Heading 2
  `###`, Heading 3 `####`, so a Part stays under its Week (WCAG 1.3.1).
  Empty headings are dropped.
- **Box alt text.** Pandoc writes a one-cell table's Word alt text as a
  caption Word never shows; it repeats the box's words and is dropped.
- **Math-font text.** Characters an original types as text in its math font
  (Mathematical Alphanumeric Symbols, U+2206) stay as typed; the reader's
  math font sets them (`tests/test_fonts.py`).
- **Second lists (S11 and parts).** The number check matches an `xN`
  anchor in document order by its label: a question's parts drawn from a
  second list are written as its parts; a second list of report items is
  an ordered list inside `::: report-item`. A list Word numbers from its
  question list outside any question is wrapped in
  `::: {.numbered anchors="oN.0.1 ..."}`, which shows nothing.

## Pictures and drawn figures (S12, S13; pass 2b, D-0117, D-0118)

- **Reading.** Every step reads a source as `markdown-smart-implicit_figures`
  (`render.FROM`): a lone picture is a picture, not a figure with its alt
  text as a visible caption Word does not have. The lab page runs
  `tools/filters/media.lua` at Quarto's `pre-ast`, before Quarto's own
  figures, which ignore the reader setting and also drop the `alt`
  attribute (probed 2026-10-08).
- **Where.** Word anchors all 23 floating drawings in the 19 handouts at the
  start of a paragraph and shows them below its first lines, so the
  Markdown places each after that paragraph's words, and the word check
  reads it there. An inline picture stays where Word has it.
- **A picture (S12)** is the original's file, byte for byte, beside the
  source as `curriculum/<course>/<id>-media/<name>`, the name the
  converter's descriptor (ledger 14). Front matter `images:` names it
  (`file`, `source_part`, `sha256`). Its `width` and `height` are Word's
  extent in inches to four places, and `crop` is Word's `srcRect` (left,
  top, right, bottom, thousandths of a percent): Word crops 14 of the 49
  pictures and shows every screenshot smaller than its pixels.
  `python tools/media.py list ORIGINAL` prints each picture's part, size,
  crop and alt text in reading order; `extract ORIGINAL FOLDER NAME ...`
  copies them under the names given and prints the front matter and each
  image's Markdown.
- **A drawn figure (S13)** names the drawings it draws by their `wp:docPr`
  ids; PH 212 Lab 3's is two screenshots and the two arrows over them
  (D-0117, call 4). Its alt text is Word's `descr` of each drawing that is
  not a picture; a picture inside keeps its own. Its file is made at build,
  never committed; every drawing that is not a picture must be in one
  figure, unless it is a lone text box, which is `::: box`.
- **Outputs.** The page writes a figure's SVG inline (its labels reach a
  screen reader and find-in-page) and a picture as an `<img>` at Word's
  size, a cropped one in a span that shows Word's part. The Word download
  embeds the figure's PNG at the SVG's size, alt text the figure's and its
  pictures', and writes Word's crop back into each picture. The HTML
  download embeds both; its equations are MathML. The course download's
  Markdown carries each lab's media in the lab's folder.

## Equation rule (S5; pass 2a's probe, D-0113)

Probed 2026-10-07 on all 19 handouts (322 equations, 35 display) with
Quarto's Pandoc 3.10, by a scratchpad script, not committed:

- **Writers.** Pandoc's Word writer and its HTML writer with `--mathml`
  (the site's `html-math-method`) warn on none of the 322. Only the plain
  writer warns ("Could not convert TeX math", 66 warnings in 15 handouts),
  and no build step uses it. `tests/test_downloads.py` reads both the
  source and the Word download through it to compare words, so that test
  compares equations apart once a lab has them (pass 2b).
- **Round trip.** Pandoc's TeX, written back to OMML by its Word writer,
  equals Word's equation in 315 of 322 under the comparison below.
- **The source keeps Pandoc's TeX, corrected where the round trip
  differs.** The correction carries Word's own characters and structure,
  and the comparison is never loosened to pass it. The probe's six:
  - a typed "√" before R², which Pandoc reads as an empty `\sqrt{}`
    (PH 211 Lab 5): written as the character `√`;
  - a typed "°" (PH 212 Lab 1, twice; Lab 2, once), which Pandoc reads as
    a superscript `{^\circ}`: written as the character `°`;
  - bars that Word stores as a delimiter around E (PH 213 Lab 3, twice),
    which Pandoc writes as literal `|`: written `\left| E \right|`.
- **An equation inside a drawn figure** (S13) is not Math in the source:
  PH 213 Lab 2's one equation among the photograph's labels, which Pandoc
  drops, reaches the page with the figure's SVG (pass 2b). The word check
  takes figure equations from the figure, not from `Math`.

The comparison, four-items call 4.2 as amended here:

- **Count, kind, position:** every `m:oMath` outside a drawn figure (not
  nested in another, `mc:Fallback` removed) and every `Math` node take one
  place in the word sequence; display (inside `m:oMathPara`) against
  `DisplayMath`.
- **Text:** the equation's `m:t` in order, with the characters OMML keeps
  in attributes put in place: a delimiter's begin, separator and end
  (defaults "(", "|", ")"), an n-ary's operator (default "∫"), an
  accent's mark (default U+0302) and a group character's (default U+23DF).
  Normalized: Unicode NFKC; whitespace, U+200B and U+2061 to U+2064
  removed; U+2206 to U+0394; U+002D to U+2212.
- **Structure:** counts of `m:f`, `m:sSub`, `m:sSup`, `m:sSubSup`,
  `m:sPre`, `m:rad`, `m:acc`, `m:bar`, `m:d`, `m:nary`, `m:limLow`,
  `m:limUpp`, `m:groupChr`, `m:eqArr`, `m:m`, `m:box`, `m:borderBox`,
  `m:phant`. `m:func` is left out: it is how Word sets "sin" upright, and
  MathML does the same without it.
- **Bold:** none. `\mathbf` is styling inside math; equations are exempt
  from the bold compare, as headings are.

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
line sits in), italics and underline. Structure is reviewed by counting
blocks in the parse tree against the original. Equations (D-0113), pictures
and drawn figures (D-0117, D-0118) are checked as above.

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
