# Course pages, 2026-10-06

Mockups for D-0069 to D-0071: one page per course, the course index as a
chooser, a dense lab table, and a course download control that covers more
than handouts. They follow the owner's review of board C in
`../2026-10-05-left-contents/` (chat, 2026-10-06), and they replace calls
2.1 and 2.2 of `docs/superpowers/plans/2026-10-03-four-items.md`. These are
mockups, not the site: nothing here is built, tested, or served, and where
a board and the built site disagree, the site is right.

The boards were drawn on a Claude Design canvas (private to the owner:
https://claude.ai/artifact/XbK6hpxvrqLvgoe8zbEDdu). The files here are that
canvas's source, copied 2026-10-06 at its version 8. They are `.dc.html`
Design Component files and need the canvas runtime (`support.js`), so they
do not open on their own in a browser. Read them as markup, or open the
canvas. `canvas.json` is the canvas's index: the frame of each board.

Unlike the 2026-10-01 and 2026-10-05 boards, these do not link
`site/site.css`. They restate its colors (Star Canvas, Beaver Orange,
Coastline, Rogue Wave, Luminance) and Open Sans by hand, so a value
here that differs from `site/site.css` is the board's mistake. Nothing was
measured: no box, height or line length below comes from a browser.
Numbers marked "computed" are arithmetic.

| File | Board | Shows |
|---|---|---|
| `Main.dc.html` | Course index, 1440 px frame | three course tiles, one per course, each linking to that course's page; the 96rem shell |
| `Course.dc.html` | PH 211 page at launch, 1440 px frame | course tabs under the site nav; one table, Lab, Title, Description; all eight labs as links |
| `Download.dc.html` | Future state, 1440 px frame | "Download PH 211 files" beside the h1, its dialog open: Handouts (four formats), Lab files (data, simulations) |
| `Phone.dc.html` | PH 211 page, 390 px | the table as stacked rows; the three tabs share the width |

## What the boards show that was ruled

The owner's answers, chat 2026-10-06, to the questions after board C:

1. One page per course: "1 yes".
2. The course index chooses the course, as tiles, not a popover that must
   be answered on load: "2 tiles".
3. Labs in a dense table, not cards: "3 dense table, otherwise we need
   rules that enforce cards to be the same size".
4. The site-page shell at 96rem: "4 96rem".
5. Labs not yet converted collapsed: "5 collapsed". Superseded the same day
   (item 7).
6. Download control hidden when there is one file: "6 hide".

Then, on the PH 211 board: the description column widened and relabeled
"Description"; the Status column deleted ("if they are converted and
checked, they'll be available, otherwise they won't be"); the "Converted"
heading deleted ("the site will have all lab materials converted by the time
it goes live"). Claude drew the collapse out by the same logic (item 7).
"Also available as it was written" leaves the course page for each lab's
page ("Move 'as written' to each lab's page"), where the switch
"Read it as it was written" already stands (`tools/render.py`, `switchlabel`).

On downloads, the owner: "the download all needs to be general enough
because it's not just labs that could be downloaded", naming a lab's
handout, a CSV attached to a lab, and an HTML simulation attached to a lab.

## Placeholders on the boards

- PH 212 and PH 213 course names (`[PH 212 course name]`; PH 213 waits on
  Q4 of the four-items plan).
- The data and simulation counts in the dialog (`[N files, placeholder]`):
  no lab has a CSV or a simulation attached today.
- The OSU logo (`[OSU logo]`); the site's published PNG was not uploaded.
- "Download PH 211 files" is shown only on the future-state board. With
  PH 211's one converted lab the built page would hide it (D-0071).

New words on the boards, Claude's, for the owner's approval: "Choose a
course to see its labs." (index), "One zip, a folder per lab. Only
converted labs are included." (dialog), "Download PH 211 files", "Lab
files", "Data files (CSV)", "Simulations (HTML)", "Description". "Close"
is Q8's lean.

## Built 2026-10-06 (D-0069, D-0070): for the owner before it merges

The first PR builds D-0069 and D-0070; measurements are in D-0070.
**Ruled 2026-10-06, chat, everything below as drafted:** "Collapse stands";
"Approve, merge PR 1" (the words and the builder's calls); "Promote D-0069,
D-0070". What it shipped for those rulings:

- **Before launch: Claude's lean, built.** The collapse stands until the
  last lab is converted: under the table, a `<details>` closed as built,
  "Not yet converted (7)" for PH 211, the seven labs inside in the same
  three columns without links. It needs no script and disappears by itself
  once every listed lab is converted. Reason: it is the owner's own "5
  collapsed"; it keeps what production shows today (all eight PH 211 labs)
  one tap away; and the other branch would hold the course pages, and the
  download work built on them, off `main` until the last lab is converted.
  The other branch stays open: if the owner rules it, the PR does not merge.
- **Words, visible and new:** "Choose a course to see its labs." (index);
  the tile counts "8 labs listed, 1 converted" and "No labs converted yet"
  (the board's), and "8 labs" once a course is fully converted (new, not
  shown today); the column names "Lab", "Title", "Description"; "Not yet
  converted (7)" (the site's "Not yet converted." with a count). At phone
  width each link reads "Lab 1: Team Building", as the course index's links
  read today.
- **Words, spoken only:** the tabs' `<nav>` is named "Courses" (Q2's lean).
- **Words that go:** "A lab reads as a link once its handout has been
  converted ... Everything else is listed so the gap is visible, not
  hidden."; "Converted and checked. Also available as it was written.";
  "Not yet converted." under each pending lab.
- **Builder's calls:** pages at `/courses/ph211/`, `/courses/ph212/`,
  `/courses/ph213/`; a course name not in hand is left out (the tile and
  the h1 show the code alone), never a placeholder; the h1 and the prose
  on these pages sit at the shell's left edge, as drawn, which amends
  D-0029's centering there; D-0067's Download all stays as it is, after the
  table, until the second PR moves it.
- **Seen by measuring, not ruled:** the header's content shifts 121 px at
  1440 px (192 px at 1920 px) between a site page (96rem) and a lab page
  (72rem); at 375 px the PH 211 h1 takes 4 lines (202 px).

## Open, for whoever builds this

- **Before launch.** The table assumes every lab is converted; today seven of
  PH 211's eight are not. Either the collapse ("Not yet converted (N)")
  stands until the last lab is converted, or the new course pages do not
  deploy until then. Ruled 2026-10-06: the collapse stands (above).
- **Rule 6's count.** "Fewer than two downloadable files": one handout in
  four formats is four files. Whether that counts as one or four is not
  ruled.
- **How a lab's data file or simulation is attached** to a lab (front
  matter, a manifest, a folder convention) is not designed. The sims
  catalog is the obvious source for simulations.
- **The description column's line length.** Computed, not measured: at
  1440 px the column is about 1,000 px, past the 68ch measure. The longest
  description (175 characters) wraps to about two lines. The owner chose
  this; measure it on the built page and record the number. Measured
  2026-10-06 (D-0070): 979 px at 1440 px, 1,122 px at 1920 px; the longest
  description is 173 characters and sets 2 lines, full lines of 111 and 127
  characters.
