# How this site works

This site holds the lab handouts for OSU's introductory physics courses,
to read on screen or download. It is a set of plain files, the same for
every reader: no accounts, and nothing loaded from other sites.

## The basics, in plain terms

- **A static site.** Every page is a finished file, made ahead of time and
  handed to your browser as is. There is no program running behind the
  page, no database, and nothing to log in to. A static site is cheap to
  host, fast, and hard to break into, and a copy of its files works
  anywhere.
- **A build.** "Building" the site means running the tools below once to
  turn the handouts into those files. A change to a handout means a new
  build, never an edit to a page.
- **A repository.** The handouts, the tools' settings and the site's
  history live in one Git repository: a folder that records every change,
  who made it and when, so any earlier version can be recovered.

## One file per handout

Each handout is one Markdown file: plain text with light marks for
headings, lists and bold, readable in any text editor. That file is the
only copy anyone edits. Every version you can open here is built from it:
the web page for each lab and the four downloads, Word, PDF, HTML and the
Markdown file itself. Nothing is copied by hand, so the versions cannot disagree.

## How a page is built

Two free, open-source tools do the building. Pandoc converts Markdown into
web pages and Word files. Quarto runs Pandoc across the whole site and lays
out its pages. A web browser prints each lab's PDF from its web page. The OSU header, footer and colors come from the site's own
templates; the handouts themselves carry no branding.

## How we know what changed

The site began by converting format only: no wording, curriculum, objective
or convention was changed. For every converted handout, a program reads the
words of the original Word file and the words of the Markdown file and
compares them in order, along with which words are bold, every equation,
and the description of every picture. A second program compares each
question's number with the number Word shows. They must match
exactly; PH 211's Lab 1, the first converted, matches on all 989 words.

Handouts now change as well, one ruled change at a time, and only in the
Markdown file. Each changed passage is listed in the handout's own file:
the original's words, the words that replace them, and the ledger entry
that approved the change. The same check still runs on every handout and
passes only if the words match the original apart from the listed
passages. A difference that has not been recorded and ruled stops the
change from being published. The original Word files are kept, their words unchanged, so anyone who
prefers them loses nothing; the copies stored with the site have their
author and company fields removed.

## How a change is published

Every change takes the same path to this site. The site is rebuilt from
scratch, the word check runs on every converted handout, and more than two
hundred automated tests check the pages, the downloads and the site's own
rules. Only if every one passes is the result published, and the published
files are then compared byte for byte with the files that were tested.
Each decision behind the site is written down, dated, in a decision ledger
kept with it.

## Where the site lives

The files are served by Cloudflare Pages, a service that hosts static
sites. Cloudflare keeps copies of the files on servers around the world
and sends each reader the nearest one. The site's own pages set no
cookies, run no analytics, and load nothing from other sites, so the site
itself learns nothing about who reads it. Like any web host, Cloudflare
handles each request and keeps its own records under its own privacy
policy: [Cloudflare's privacy policy](https://www.cloudflare.com/privacypolicy/).

## Search engines and AI crawlers

While the license is open, the site asks not to be found. Every page tells
search engines not to index it or follow its links, and the site's
robots.txt asks every crawler, search engines and AI crawlers alike, to
read nothing. These are requests: well-behaved crawlers honor them, and
nothing forces the rest to. When the license is settled, these rules will
be decided again.

## Who did the work

The heavy lifting is done by the two open-source tools described above:
Pandoc converts the files and Quarto builds the site. Around them is
software written for this site (the word check, the downloads and the
publishing steps), which Hunter Reaves built with Claude, an AI model from
Anthropic, as he did the conversion of the original Word documents to
Markdown. Every ruling is his, recorded in the ledger,
and he answers for the work. The project holds itself to the
standard it sets for students in these labs: disclose the use of AI, keep
the reasoning human, and the human answers for the work.

Common concerns, answered briefly:

| Concern | Answer |
|---|---|
| Accuracy | The word check, per document; every change listed and ruled. |
| Authorship and credit | Original authors are kept and credited. |
| A double standard for faculty | The project follows the students' AI policy. |
| Deskilling | Every judgment is a human ruling in the ledger. |
| Data privacy | No student data enters any repo, by rule. |
| Jobs and labor | Time saved goes to teaching and TA preparation. |

## If the people change

The site is built so that it does not depend on any one person. Everything
needed to rebuild it, the handouts, the original Word files, the build
settings, the tests and the decision ledger, is in one repository. That
repository is private for now and is planned to become public once its
whole history has been checked for anything that must not be published.
Its instructions are being written so that a successor can rebuild the
site and move it to another host; until someone starting from nothing has
followed them, that is all this page claims for them.
The accounts the site depends on (the host, and later a domain) are to be
listed in the repository by role, with how each is handed over.
