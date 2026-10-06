# How this site works: the "How this was made" page, re-framed

Draft for the owner's line edits. Nothing is built until the owner approves
the text. Written 2026-10-06 on the owner's request in chat: "edit the 'How
this was made' page to de-emphasize the use of AI tools. Not to hide it, but
rather to re-frame. I want it to explain the boring parts first. Markdown
SSOT, Pandoc, Quarto, etc. New page title 'How this site works'." His
choices the same day, each Claude's lean: the text gets its own file ("Its
own file"); a new address with the old one redirecting ("New URL plus
redirect"); his name and Claude stay named, the dictation tool goes ("Name,
Claude; drop Wispr"); and this draft comes first ("Draft first"). Ledger:
D-0072, proposed.

Every fact below is checked against the repo as of `f65b1d4`; numbers that
will go stale are marked.

## The page, drafted

The draft keeps the current page's substance: the four commitments, the
concerns table, the open standard for the later phase. It changes the order
(what the site is made of, how a page is built, how it is checked, how a
change is published, then who did the work) and adds plain explanations of
the tools. 551 words against today's 233 (counted 2026-10-06).

> # How this site works
>
> This site holds the lab handouts for OSU's introductory physics courses,
> to read on screen or download. It is a set of plain files, the same for
> every reader: no accounts, and nothing loaded from other sites.
>
> ## One file per handout
>
> Each handout is one Markdown file: plain text with light marks for
> headings, lists and bold, readable in any text editor. That file is the
> only copy anyone edits. Every version you can open here is built from it:
> the two web pages for each lab, "Rebuilt for reading" and "As it was
> written", and the four downloads, Word, PDF, HTML and the Markdown file
> itself. Nothing is copied by hand, so the versions cannot disagree.
>
> ## How a page is built
>
> Two free, open-source tools do the building. Pandoc converts Markdown into
> web pages and Word files. Quarto runs Pandoc across the whole site and lays
> out its pages. A web browser prints each lab's PDF from its "Rebuilt for
> reading" page. The OSU header, footer and colors come from the site's own
> templates; the handouts themselves carry no branding.
>
> ## How we know nothing changed
>
> This phase converts format only: no wording, curriculum, objective or
> convention is changed. For every converted handout, a program reads the
> words of the original Word file and the words of the Markdown file and
> compares them in order, along with which words are bold. They must match
> exactly; PH 211's Lab 1, the first converted, matches on all 989 words. A
> difference that has not been recorded and ruled stops the change from
> being published. The original Word files are kept, unchanged, so anyone
> who prefers them loses nothing.
>
> ## How a change is published
>
> Every change takes the same path to this site. The site is rebuilt from
> scratch, the word check runs on every converted handout, and more than two
> hundred automated tests check the pages, the downloads and the site's own
> rules. Only if every one passes is the result published, and the published
> files are then compared byte for byte with the files that were tested.
> Each decision behind the site is written down, dated, in a decision ledger
> kept with it.
>
> ## Who did the work
>
> Hunter Reaves directs Claude, an AI model from Anthropic, to convert the
> original Word documents to Markdown and to build the software that
> converts, checks and publishes them. Every ruling is his, recorded in the
> ledger, and he answers for the work. The project holds itself to the
> standard it sets for students in these labs: disclose the use of AI, keep
> the reasoning human, and the human answers for the work.
>
> Common concerns, answered briefly:
>
> | Concern | Answer |
> |---|---|
> | Accuracy | The content-unchanged check, per document. |
> | Authorship and credit | Original authors are kept and credited. |
> | A double standard for faculty | The project follows the students' AI policy. |
> | Deskilling | Every judgment is a human ruling in the ledger. |
> | Data privacy | No student data enters any repo, by rule. |
> | Jobs and labor | Time saved goes to teaching and TA preparation. |
>
> ## Not settled yet
>
> The license for this material is not settled, so the site is an unlisted
> draft, as the banner at the top of each page says. The standard for the
> later phase, when wording does change, is still open (ledger 11).

Sources for the facts: one Markdown source and its versions (VISION.md
principle 2, D-0052, D-0053, `tools/render.py` THEME_LABEL); Pandoc and
Quarto (D-0033, D-0044, `tools/downloads.py`); the PDF printed by Chrome
from the modern page (D-0052, `tools/downloads.py`); no branding inside
documents (D-0010); nothing loaded from other sites
(`tests/test_quarto_site.py::NoThirdParty`, self-hosted fonts D-0025); the
word and bold check and its 989 words (`tools/check_unchanged.py`, run
2026-10-06; stale once more labs convert, though still true of Lab 1); the
originals kept byte for byte (LEDGER 18, `originals/`); the publish path
(`.github/workflows/verify.yml`, `tools/check_deployed.py`, D-0048, D-0049);
207 tests at `f65b1d4` ("more than two hundred" holds while the count stays
above 200); the disclosure and the concerns table, today's page, word for
word except where marked below.

## Words that change, and where

- The disclosure: "drafts by voice with Wispr Flow and directs Claude" goes
  to "directs Claude"; "converts and checks them" to "converts, checks and
  publishes them"; "Same standard as students. The project follows the
  students' own AI policy in these labs" to "The project holds itself to the
  standard it sets for students in these labs". Today's "Every judgment is a
  human ruling" stays in the table; the body says "Every ruling is his".
- The nav, `tools/brandheader.html`: "How this was made" to "How this site
  works".
- The footer, `tools/brandfooter.html`: "License and credits: see How this
  was made." to "License and credits: see How this site works."
- The landing card, `site/landing.md`: "[How this was made] The method, what
  is checked, and what is not." to "[How this site works] How a page is
  built, how it is checked against the original, and who did the work."
- The page's footnote, `render.METHOD_FOOTNOTE`: "This page is built from
  VISION.md in the project's repository; ledger numbers refer to the dated
  decision ledger kept there." to "This page's source is
  site/how-this-site-works.md in the project's repository; ledger numbers
  refer to the dated decision ledger kept there."
- The redirect stub at `/how-this-was-made/`: `render.redirect_page()`
  always writes "Continue to the lab"; it gains a link text argument, and
  this stub says "Continue to How this site works".
- VISION.md: its "How this was made" section keeps the four commitments
  (no content changes; the claim is checked, not asserted; the originals
  remain; the same standard as students) and the open later-phase standard,
  and points to the page for the build and the disclosure. Principle 6's
  "(see below)" then points there too.

## What the build changes (after approval)

`site/how-this-site-works.md` included into the generated page as the
landing page is; `render.how_this_was_made()` deleted; `quarto_build.py`
writes `how-this-site-works/index.qmd` and the redirect; `_quarto.yml`'s
render list; `methodhref` in `render.site_vars()`; the tests that name the
page (`test_quarto_chrome.py`, `test_quarto_dress.py`, `test_quarto_site.py`)
and `tools/measure_chrome.js`; the CLAUDE.md lines that name it. The word
check, the downloads and the course pages are untouched. One PR, measured at
375 px for sideways scroll as every page is.

## Related, found while drafting, not in this change

The landing page still says downloads are not built ("Coming later:
download any handout ..." and "Downloads (Markdown, Word, PDF, HTML) are
planned and not built yet"); they shipped 2026-10-01 (D-0052). Its course
index card ("every lab its course summary lists, and where each one
stands") also predates the course pages. New public words, so the owner's
to approve; it could ride in the same PR.

## Declined

- Dropping the disclosure or moving it to a footnote: the owner said "Not to
  hide it", and the students' policy the page cites says disclose use.
- Version numbers for the tools (Quarto 1.10.18, Pandoc 3.10): they go
  stale, and a reader gains nothing from them; the ledger keeps them.
- A diagram of the build: more to keep true than the four sentences it
  would replace.
- Keeping the text in VISION.md: the owner chose its own file.
