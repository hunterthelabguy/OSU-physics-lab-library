# Faithful retirement: public wording, drafted for the owner's line edits

Status: draft, 2026-10-07. D-0108 retires the faithful page and asks for the
public words that describe two presentations to be redrafted for the owner's
line edits before PR 3 merges. Nothing here is built. Edit any line in
place, or answer by passage number.

Passages 1 to 4 are D-0108's. Passages 5 to 7 are found on the way and are
yours to take or leave in the same PR:

- 5 is made inexact by PR 1: the committed original is now stripped of its
  author fields (D-0086, D-0114), so "kept, unchanged" overstates it.
- 6 is STATE's open item: the landing page still says downloads are not
  built.
- 7 says what the word check now reads, true once PR 1 merges.

## 1. VISION.md, "Outputs", last paragraph

Now:

> During the pilot each document also renders two ways from that one source
> (ledger 28): one faithful to the original page settings, one following the
> evidence review. The point is to show the difference and agree on it, not to
> keep both forever.

Proposed:

> During the pilot each document also rendered two ways from that one source
> (ledger 28): one faithful to the original page settings, one following the
> evidence review. Colleagues agreed on the second, and since 2026-10-07 it is
> the one presentation (D-0108).

## 2. site/landing.md, "Why one lab is shown two ways" (whole section)

Now: the heading, the two linked bullets ("As it was written", "Rebuilt for
reading") and "Either page switches to the other at the top. ... The point
is to look at both and agree on one, not to keep both."

Proposed:

> ## How a lab page reads
>
> Each document is one Markdown file, and every page and download is built
> from that one copy we edit. A lab page keeps the original's words and
> drops the Word page settings: the typography follows the reading research
> and the accessibility guidelines, and graded questions get their own
> labeled block instead of leaning on bold. A second page that reproduced
> the Word layout was shown beside it until colleagues agreed on this one.

## 3. site/how-this-site-works.md, "One file per handout"

Now:

> Every version you can open here is built from it:
> the two web pages for each lab, "Rebuilt for reading" and "As it was
> written", and the four downloads, Word, PDF, HTML and the Markdown file
> itself.

Proposed:

> Every version you can open here is built from it:
> the web page for each lab and the four downloads, Word, PDF, HTML and the
> Markdown file itself.

## 4. site/how-this-site-works.md, "How a page is built"

Now:

> A web browser prints each lab's PDF from its "Rebuilt for
> reading" page.

Proposed:

> A web browser prints each lab's PDF from its web page.

## 5. The originals "kept, unchanged" (two places)

`site/landing.md`, "What has not changed", now:

> The original Word files are kept and are still available, so anyone who
> would rather teach from them loses nothing.

Proposed:

> The original Word files are kept and are still available, so anyone who
> would rather teach from them loses nothing. The copy kept with this site
> has its author and company fields removed; its words are untouched.

`site/how-this-site-works.md`, "How we know nothing changed", now:

> The original Word files are kept, unchanged, so anyone
> who prefers them loses nothing.

Proposed:

> The original Word files are kept, their words unchanged, so anyone who
> prefers them loses nothing; the copies stored with the site have their
> author and company fields removed.

## 6. Downloads described as not built (site/landing.md)

Now, under the hero:

> Coming later: download any handout for offline use as Markdown, Word, PDF,
> or HTML.

Proposed:

> Each converted handout downloads from its page as Markdown, Word, PDF or
> HTML.

Now, under "What is deliberately missing":

> - Downloads (Markdown, Word, PDF, HTML) are planned and not built yet.

Proposed: the bullet removed.

## 7. What the word check reads (site/how-this-site-works.md)

Now:

> For every converted handout, a program reads the
> words of the original Word file and the words of the Markdown file and
> compares them in order, along with which words are bold.

Proposed:

> For every converted handout, a program reads the
> words of the original Word file and the words of the Markdown file and
> compares them in order, along with which words are bold, every equation,
> and the description of every picture. A second program compares each
> question's number with the number Word shows.

## What PR 3 does besides the words (D-0108)

- No faithful page is built; `themes/faithful.css`, the faithful branch of
  `tools/filters/questions.lua`, the switch link and their tests and CSS go.
- `/labs/ph211-team-building-handout/faithful/` redirects to
  `/labs/ph211-team-building-handout/modern/`, as the old "How this was made"
  address does.
- The downloads are unchanged (they already come from the modern page); a
  test says so.
