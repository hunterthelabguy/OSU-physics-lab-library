# Download control, 2026-10-01

Mockups for the design pass on the lab page's download row, which the owner
found too small to find on a site whose purpose is the download. These are
mockups, not the site: nothing here is built, tested, or served, and where a
board and the built site disagree, the site is right.

Each board is the built modern Lab 1 page's chrome and the opening of its
`<main>`, taken from `build/quarto-site/` on 2026-10-01, with only the
download row swapped. The boards link the repo's own `site/site.css` and
`themes/modern.css` in Quarto's order; Bootstrap is left out. The mockup
rules sit in each board's `<style>` block, scoped to `.quarto-light` as the
quarto-only block would scope them. Links go nowhere. To view a board, serve
the repo root over HTTP (`python -m http.server <port> --directory <absolute
path to the repo>`) and open `docs/design/2026-10-01-download-control/<board>`;
from disk the stylesheets may not load.

| File | Board | Became |
|---|---|---|
| `current.html` | The row as built: "Download: Word · HTML · PDF · Markdown" as nav text | the baseline |
| `a-buttons.html` | A: the four formats as buttons, the landing hero's primary button (D-0031) at nav scale | pending the owner's ruling |
| `b-menu.html` | B: one "Download" button that opens a list, closed | pending the owner's ruling |
| `b-menu-open.html` | B, open | pending the owner's ruling |

Board B's button says "Download" alone, and board A drops the middots; both
are changes to the wording D-0053 approved and need the owner's word.

## Measurements

Measured 2026-10-01 in the browser pane by script, light scheme unless
noted. Boxes are x, y, width, height in CSS pixels.

Method check: `current.html` at 375 px measures the same as the built page
(`site-nav` 118 px tall, the title's top at 418 px, the Word link at
92, 305, 37, 19), so the boards stand in for the built chrome.

At 375 by 812 px:

| | `site-nav` height | title top | download targets | sideways scroll |
|---|---|---|---|---|
| current | 118 | 418 | four links, 19 px tall, 27 to 72 px wide | none (375) |
| A | 170 | 470 | four buttons, 44 px tall, 59 to 115 px wide, one row of 343 px under the label | none (375) |
| B, closed | 102 | 403 | one button, 123 by 44 | none (375) |
| B, open | 102 | 403 | a list of four rows, each 176 by 44, in a 178 by 186 box at 16, 352 that covers the title | none (375) |

At 1440 by 900 px: the current `site-nav` is 59 px tall; A and B are both
73 px, with A's four buttons 55 to 110 px wide and B's open list 178 by 186
below its button.

Contrast, computed with the WCAG formula from the rendered colors: white on
Beaver Orange 4.56:1 (the buttons' text, 16 px bold); the orange against the
page 4.56:1 in the light scheme and 3.91:1 in the dark one (`#14181b`); B's
list items 11.8:1 light and 14.47:1 dark.
