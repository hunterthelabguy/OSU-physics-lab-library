# Downloads Plan: Word, HTML and PDF per lab

Executable task plan: `docs/superpowers/plans/2026-10-01-downloads-tasks.md`.

Status: calls 1 to 7 ruled 2026-10-01 (see "Rulings" below; D-0053
proposed records them). Nothing built. Ruled already: D-0052 (proposed; the owner approved all six leans):
one set per lab, Word by Pandoc through Quarto, a self-contained HTML, a PDF
printed by headless Chrome with the approved print rules, the draft banner
in every file, tests for each. Demo on 2026-10-06; built properly, not
rushed (owner, 2026-10-01).

Ledger: D-0052 (proposed); binds D-0010, D-0016, D-0033, D-0036, D-0048,
LEDGER 28, 37, 51, 53

## Premises, checked 2026-10-01

1. **Chrome is on the runner.** GitHub's runner-images readmes list Google
   Chrome 153.0.8010.52 on Ubuntu 24.04 (image 20260920.314.1) and on Ubuntu
   26.04 (image 20260920.143.1), so the move of `ubuntu-latest` on
   2026-10-19 does not remove it. Locally, Chrome is at
   `C:\Program Files\Google\Chrome\Application\chrome.exe`.
2. **`pdftotext` is not on the runner** (neither readme lists poppler). CI
   installs `poppler-utils` with apt for the PDF tests. Locally, poppler
   25.07.0 was installed by winget on the owner's word (2026-10-01).
3. **Word works.** `quarto render <lab page> --to docx` on Quarto 1.10.18,
   after a full build: one 14,540-byte `.docx`, no warning; Pandoc reads it
   back as the full lab text, title once, "Question 1" to "Question 5" from
   `questions.lua`. No draft banner (the banner is chrome, not body).
4. **Self-contained HTML works, and is heavy.** A second small Quarto project
   (`embed-resources: true`, the modern theme, the same filter) rendered Lab
   1 to one 1,191,786-byte file with no external reference and no warning
   (spike 2's untraced warning did not recur). Spike 2 got 127 KB for a
   similar render; the difference is almost certainly Bootstrap and its icon
   font embedded whole. To be measured and cut, not guessed.
5. **Where links can go.** D-0010 and `test_bodies_unchanged` pin each lab
   page's `<main>`, so the links go in chrome. The lab page's `site-nav` bar
   already holds the presentation switch ("Read it as it was written"),
   written by `tools/template.html` and lifted into Quarto pages by
   `tools/quarto_chrome.py` (D-0036).
6. **Existing copy that becomes false.** The lab page footer, in
   `tools/template.html`, says "Downloads (Markdown, Word, PDF) are not wired
   up in this draft." It has to change in the same PR, and it names
   Markdown, which D-0052 does not.

## Rulings (owner in chat, 2026-10-01)

These win over the leans recorded under the calls below.

1. **Every file comes from modern:** HTML, PDF and Word. Not as leaned (PDF
   from faithful). The owner expects the faithful presentation to be
   retired, so no download is offered for it now. That retirement is an
   intent, not yet a ruling; nothing here changes the faithful pages. Word
   "from modern" means the modern question labels ("Question 1" blocks, as
   `questions.lua` writes them under `theme-name: modern`) with Pandoc's
   default Word styles; styling the Word file to look like modern (a
   reference document) was not asked for and is not built.
2. **Markdown too, as leaned:** the source file, byte for byte.
3. to 7. **As leaned.** The wording of call 3 is approved: "Download: Word ·
   HTML · PDF · Markdown" in the `site-nav` bar, and the footer sentence
   "Downloads carry the same draft notice as these pages." Ship them as
   approved copy, not placeholders.

## Numbered calls for the owner (as drafted; ruled above)

1. **Which presentation each file carries.** Lean: HTML from modern (it
   follows the reader's light or dark setting and the reading research,
   which is the library's point); PDF from faithful (a PDF is a printed
   page, and faithful is the printed original by design); Word from the
   Markdown with Pandoc's default styles (Word cannot carry either CSS
   presentation). Cost of the alternative, all from modern: one look
   everywhere, but the PDF handed to instructors would not look like the
   handout they know.
2. **Markdown too?** The footer has promised it. Lean: yes, the source file
   itself, byte for byte (LEDGER 28: one source; nothing to generate, and a
   test can compare bytes). Cost of the alternative, no Markdown: the footer
   sentence drops a format it promised.
3. **The words.** New page copy needs your approval. Proposed, marked as
   placeholders until approved: in the `site-nav` bar, "Download: Word ·
   HTML · PDF" (plus "Markdown" if call 2 says yes), each a link with a
   `download` attribute; the footer sentence becomes "Downloads carry the
   same draft notice as these pages." No other new copy.
4. **The banner inside each file.** Lean: the existing approved
   `BANNER_MAIN` and `BANNER_DETAIL` from `tools/render.py`, never new
   words: as the first two paragraphs of the Word file; as the page's own
   draft banner in the HTML; in the PDF, the printed banner and running
   header your print preview already showed.
5. **What chrome the HTML download carries.** Lean: the draft banner, the
   OSU logo (already embedded in every page) and the policy footer, but no
   nav and no presentation switch, because relative links break in a file
   opened from disk. Cost of the alternative, full chrome: dead links in a
   file that is meant to work offline.
6. **File names and place.** Lean: `labs/<id>/<id>.docx`, `.html`, `.pdf`
   (and `.md`) beside the two presentations, so a saved file is named after
   the lab, not `index`. They deploy and are byte-checked like every other
   file (D-0048, D-0049).
7. **The size of the HTML.** Lean: measure what is embedded first, then cut
   to what the page uses (likely Quarto's `minimal: true` for this one
   render, with the site and theme CSS), with a test that caps the size at
   the measured result plus a margin. Cost of not cutting: about 1.2 MB per
   lab download.

## Tasks, assuming the leans

Failing tests first, each watched failing for its named reason; a missing
tool (Chrome, `pdftotext`) fails, never skips (LEDGER 53).

**Task 1: red.** `tests/test_downloads.py` against `build/quarto-site/`:
for every converted lab, the files of call 6 exist and are non-empty; the
Word file read back by `$PANDOC` holds the banner text and the source's
words (the word check's comparison, not a new one); the HTML has no
external `src`/`href`, carries the banner, and is under the size cap; the
PDF starts with `%PDF`, and `pdftotext` finds the banner and the lab title;
the Markdown is byte-identical to the source; each lab page's `site-nav`
links every file and `<main>` is unchanged (the existing body hash). The
chrome contract gains nothing new to check.

**Task 2: green.** `tools/quarto_build.py` gains a downloads step after
`post()`: Word by `quarto render --to docx` per lab with the banner
paragraphs prepended to the generated page; HTML by a second small project
generated under `build/` (never committed) with `embed-resources`; PDF by
headless Chrome printing the built modern page from a local server, with
`CHROME` set like `QUARTO` (located, never guessed, and a missing browser
an error); Markdown copied. `tools/template.html` gains the links and the
new footer sentence. CI: install `poppler-utils`; Chrome is already there.

**Task 3: measure and review.** Sizes of each file; the HTML opened from
disk with the network off; the PDF compared by eye with the owner's print
preview; the deploy byte check green on the PR's preview, which the owner
opens on a phone before the demo.

## Declined

- PDF through Typst or LaTeX (D-0052).
- The original `.docx` (D-0052: unvetted metadata).
- A download page or listing: links on each lab page are enough for one
  lab; a listing is "later, enabled by the move".
- Generating downloads in the old build: production is the Quarto build.
