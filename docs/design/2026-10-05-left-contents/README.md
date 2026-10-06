# Left-hand contents on the course index, 2026-10-05

Mockups for Q5 of `docs/superpowers/plans/2026-10-03-four-items.md`: the
owner's idea of 2026-10-03, "Table of contents on the left hand side? Select
-> auto-scroll, etc.", drawn as links and as a select. These are mockups, not
the site: nothing here is built, tested, or served, and where a board and the
built site disagree, the site is right. No ruling has been made on any board.

Each board is the built course index from `build/quarto-site/` (built
2026-10-03 at `734878f`'s content) with Bootstrap left out, linking the
repo's `site/site.css`, as the 2026-10-01 boards did. Links go nowhere except
the course links. The h2 ids are the stable ones call 1.2 proposes (`ph211`,
`ph212`, `ph213`), not Pandoc's automatic ones. The Download all button is
shown, since its script is not loaded. To view a board, serve the repo root
over HTTP (`python -m http.server <port> --directory <absolute path to the
repo>`) and open `docs/design/2026-10-05-left-contents/<board>`.

| File | Board | Became |
|---|---|---|
| `current.html` | The course index as built | the baseline |
| `c-links.html` | C: the three course codes as links, no script; from 64rem a sticky column in the left track, below it a row above PH 211 | not built; reviewed 2026-10-06 and replaced by D-0069 to D-0071 (`../2026-10-06-course-pages/`) |
| `d-select.html` | D: a select named "Courses" that scrolls to the course chosen, then resets; placed as C | not built; declined, D-0069's alternatives |

Both new boards add visible words: C adds only the three course codes (the
words Q2 proposes), D adds those and "Courses" as its first option, since a
select must show something before a choice, and choosing the option already
showing fires no change. D needs script; C needs none.

## Measurements

Measured 2026-10-05 in the browser pane by script, each board in a
same-origin iframe of the stated width (its vertical scrollbar takes 15 px,
so the document is 15 px narrower). Boxes are x, y, width, height in CSS
pixels.

Method check: `current.html` at 1440 measures as the built page did on
2026-10-03 (`main` 1184 px from x=121, the reading column 700 px from x=363,
the page 2787 px tall), so the boards stand in for the built page.

| Width | Board | control box | its targets | PH 211 heading top | PH 213 heading top | page height | sideways scroll |
|---|---|---|---|---|---|---|---|
| 375 | current | none | none | 621 | 3068 | 3634 | none |
| 375 | C | 16, 597, 328, 52 (one row) | three, 60 by 44 | 689 | 3136 | 3702 | none |
| 375 | D | 16, 597, 328, 44 | one, 106 by 44 | 681 | 3128 | 3694 | none |
| 768 | current | none | none | 432 | 2340 | 2787 | none |
| 768 | C | 27, 408, 700, 52 (one row) | three, 60 by 44 | 500 | 2408 | 2855 | none |
| 768 | D | 27, 408, 700, 44 | one, 106 by 44 | 492 | 2400 | 2847 | none |
| 1024 | current | none | none | 432 | 2340 | 2787 | none |
| 1024 | C | 16, 408, 139, 156 (left track) | three, 60 by 44, stacked | 432 | 2340 | 2787 | none |
| 1024 | D | 16, 408, 139, 44 (left track) | one, 106 by 44 | 432 | 2340 | 2787 | none |
| 1440 | current | none | none | 432 | 2340 | 2787 | none |
| 1440 | C | 137, 408, 226, 156 (left track) | three, 60 by 44, stacked | 432 | 2340 | 2787 | none |
| 1440 | D | 137, 408, 226, 44 (left track) | one, 106 by 44 | 432 | 2340 | 2787 | none |

In the left track the control costs no height and moves nothing in the
reading column. Below 64rem it costs 52 px (C) or 44 px (D) above PH 211.
At 768 the left track is 27 px, too narrow for a 60 px code, so the
breakpoint is 64rem (1024 px), where the track is 139 px.

Behaviour checked at 1440: scrolled to PH 213, C's column stays 16 px from
the top (box 16 to 172); D's select scrolls PH 212 into view and resets to
"Courses". On both, the page ends before PH 212 or PH 213 can reach the top
(PH 213 stops at 453 px down the window, PH 212 at 316), as the built page's
own anchors would today.

## What the boards say about calls 2.1 and 2.2

Call 2.1 widens the rows across the shell; call 2.2 puts the course links in
the left track. They compete for the same track, so the owner picks one.
Claude's lean after measuring is that 2.2, as links (C), displaces 2.1. It
does the job item 1 exists for with no script and no words beyond the course
codes. It costs no height at 1024 and up, and it keeps every row at the
reading measure, where 2.1 would set about 108 characters a line or split
each row in two. It leaves the right track empty, which 2.1 would not; that
asymmetry is the cost, and it is visible on C at 1440. D is declined for the
reasons the plan already gives for a select (it hides choices, needs script,
adds a word); the idea's "auto-scroll" is what C's links already do.
