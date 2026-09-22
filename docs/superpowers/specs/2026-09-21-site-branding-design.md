# Site branding refresh: design

Date: 2026-09-21. Status: written, awaiting owner review.
Ledger: D-0001 to D-0026 in `DECISIONS.md`. Declined: D-0003, D-0017, D-0021.

This spec cites entries by ID and does not restate their rationale. Where it
depends on a `proposed` entry, it says so, and the work that needs that entry
does not start until the owner rules it.

## 1. Goal

Make the library's site chrome read as an Oregon State University department
site and follow the brand guide closely enough that University Marketing could
sign off (D-0001), with the official logo (D-0002, D-0011). Documents
themselves are not restyled (D-0010).

## 2. What changes, page by page

| Page kind | Built by | Gets |
|---|---|---|
| Landing, course index, method, sims index | `render_page`, `tools/template-site.html` | Full header and footer (section 3) |
| Converted documents, both presentations | `render`, `tools/template.html` | Full header and footer; the document body, its theme, and the up-link and presentation switch row stay as they are (D-0010) |
| Published sims | `render_sim`, `SIM_CHROME` | Slim bar only (section 4, D-0005) |
| Redirect stubs (`labs/<id>/index.html`) | `redirect_page` | Unchanged; they show for an instant |

## 3. Full header and footer

Top to bottom:

1. **Draft banner** (LEDGER 37), wording unchanged, Luminance with black
   text (D-0022).
2. **Top strip**, Paddletail Black (D-0004). Content per D-0024: one link, "Department of Physics", to
   https://physics.oregonstate.edu, in white.
3. **Brand banner**, Beaver Orange (D-0004). Left: the logo file
   `OSU_horizontal_2C_W_over_B.png` (D-0020), as an `<img>` with
   `alt="Oregon State University"` (the typography page requires alt text
   that gives all the text in the image), linked to https://oregonstate.edu
   as the Physics site does. Right of it: the site name "Physics Lab
   Library" as live text in white. It is large enough for D-0008's
   large-text rule: 24 px regular or 18 px at weight 700 and up. White on
   orange is the same pair as orange on white, 4.56:1.
4. **Navigation bar**, Bucktooth White (D-0004): Library home, Course
   index, Sims, How this was made, the links the footer carries today. On
   document pages the existing row with the up-link and the presentation
   switch follows below it, unchanged.
5. **Footer**, Paddletail Black, white text (D-0004, D-0009): "Department of
   Physics"; the three policy links with the URLs the Physics footer uses
   (read 2026-09-21):
   - Accessibility Statement: https://oregonstate.edu/accessibility-statement
   - Privacy Disclaimer: https://oregonstate.edu/official-web-disclaimer
   - Non-Discrimination Statement: https://eoa.oregonstate.edu/about-us/policies-guidance-and-memos

   There is no address, email or phone (D-0009), and no copyright line
   until the license settles (D-0023). The page's existing footnote paragraph stays.

The logo's clear space is at least the width of the "O" in "Oregon State"
(logo guidelines page). It is set as padding around the image, sized
relative to the image's height, so it scales with the logo. The page names no
minimum size for the web; the print minimum (1.375 inches) is not applied.

## 4. Sim bar

It replaces today's orange `.lib-bar` in `SIM_CHROME`. It is a single
Paddletail Black strip (D-0005) holding:
- the logo `OSU_horizontal_2C_O_over_W.png` (D-0020) as a
  `data:` URI (the sim's policy allows `img-src data:`);
- the draft sentence (LEDGER 37) in the D-0022 colors;
- the Library home and Sims links.

Font: the owner ruled that sims may change their font (D-0021 declined).
How is D-0026 (proposed): the sim source itself gains `font-src data:` and
an embedded Open Sans, so the bar and the sim share it. The sim-font task
stops on D-0026 and D-0025. Height: the sim plus the bar fits 1280 by 720 with no page
scroll (LEDGER 51, D-0005). It is measured in the browser pane as LEDGER 51
was, and the measurement is recorded in `STATE.md`.

## 5. Color and type

- `site/site.css` uses palette values only (D-0008). The six off-palette
  values go: light `--chrome-rule` and `--chrome-tint`, and dark
  `--chrome-ink`, `--chrome-paper`, `--chrome-rule`, `--chrome-tint`.
  - The light rule becomes Coastline (#A7ACA2).
  - The tint is dropped: hover states and cards use a rule or an underline
    instead of a fill.
  - Dark paper is Paddletail Black and dark ink is Bucktooth White
    (D-0015). The dark rule becomes Crater (#8E9089).

  These replacement choices are part of this spec's approval.
- Headings may turn Beaver Orange only where they meet D-0008's large-text
  rule. `h1` (2rem, 32 px) qualifies. `h2` (1.35rem, 21.6 px, weight 650)
  does not, so it stays Star Canvas. `tests/test_brand.py` enforces this on
  every rule.
- Open Sans (D-0006) replaces the system stack in `site/site.css` and
  `themes/modern.css`, from `site/fonts/` via `@font-face`. The source and
  files depend on D-0025 (proposed) and the owner's download approval.
  `themes/faithful.css` keeps its original fonts (D-0010).

## 6. Assets and license

- `site/brand/`: the logo PNGs named in D-0020, byte for byte from
  `OSU-branding/` (D-0014), plus a `README.md` stating they are OSU
  registered trademarks, excluded from any license this repo adopts
  (D-0007).
- `site/fonts/`: Open Sans and its OFL text (D-0025).
- Every page embeds its resources, so each page carries the logo (about 176
  KB as a file, more as base64) and the font. The build reports the largest
  page size, and the owner judges whether that is acceptable. No threshold
  is ruled.

## 7. Tests

The existing `tests/test_brand.py` asserts the ruled quantities in D-0004 and
D-0008. It is extended, and a new `tests/test_site_chrome.py` reads
`build/site/`, so CI runs it after "Site builds". It fails, rather than
skips, when the build is missing (LEDGER 53). It asserts:

1. **Every `site.css` color is a palette value** (D-0008; the list is the
   style guide's primary and secondary colors).
2. **Every non-redirect page carries the logo, unaltered** (D-0002, D-0014).
   The logo image decodes to bytes whose SHA-256 matches the committed file,
   its alt text is "Oregon State University", and it links to
   https://oregonstate.edu.
3. **Every page carries the draft banner and `noindex`** (LEDGER 37).
4. **The footer is exactly as ruled** (D-0009): it has the three policy URLs
   and no `mailto:` or `tel:` link.
5. **Sims are untouched except for the bar** (LEDGER 51): each published sim
   equals its source with only the bar inserted after `<body>`.
6. **Document bodies are unchanged by branding** (D-0010): the content
   between `<main>` and `</main>` is identical before and after this
   refresh. It is compared against a copy captured from `main` at the start
   of the work.

The sim height (section 4) and phone-width layout (375 px, no sideways
scroll) are measured in the browser pane and recorded. They are not
automated, since CI has no browser.

## 8. Out of scope

- OSU icons on cards (D-0016, proposed).
- Infographic-style figures (D-0018, content phase).
- The ledger validator (D-0019, proposed).
- The grid pattern (D-0017, declined).
- Stratum 2 (D-0006).
- A license file (LEDGER 8).

## 9. Before implementation can start

Ruled 2026-09-21: D-0020, D-0022, D-0023, D-0024; D-0021 declined. Still
needed: D-0025 (Open Sans source; the owner asked what is special about
Open Sans before ruling), D-0026 (how sims take the font), and the owner's
approval of this spec. D-0013 is satisfied in substance by the logo library;
its status is the owner's.
