# State

Volatile handoff, capped at one screen. Updated 2026-10-01.

**Focus (2026-10-01):** Phase 3 (one Pandoc) done, PR #15; phase 2 (chrome
rewrite) before it, PR #14. D-0036 to D-0046 are all ruled. `PANDOC` is the
Pandoc bundled with Quarto (3.10 under Quarto 1.10.18, not 3.11) for the word
check, the Quarto build, the chrome lift and the tests; the old build and its
tree test keep the standalone 3.11 until phase 4, because production builds
with it (D-0046). Green `verify` with 92 tests (89 before phase 3). The chrome
contract, `tests/test_site_chrome.py` (9 tests), passes against both builds
and is a step of `verify` (D-0042). No tool or page changed in phase 3, so the
Quarto measurements below stand: they match the old build except the two
landing footnote rows (D-0038). Locally, export `QUARTO`, `PANDOC` and
`PANDOC_OLD_BUILD` (CLAUDE.md, Build, Quarto, "Which Pandoc"). Next is phase
5, the new host, which needs the Cloudflare deploy token the owner creates;
phase 4 follows the cutover. Production still serves the old build; the owner
looked at the live landing page and banner on 2026-10-01: unchanged from
before. Plans: `docs/superpowers/plans/2026-09-30-quarto-phase-3.md` and
`-phase-2.md`. Phase 2 review follow-ups are done
(2026-10-01): page-shell and load-order tests, and a `dd` revert; `strong` and
`b` already matched.

**Previous focus:** site design review of 2026-09-22 (owner-led, from the live site).
PR #11 and PR #12 are merged and live: spacing and type tokens, a print
stylesheet, the new landing lead, the centered reading column, the landing
hero band, link cards, the one-line draft banner, and the site-name color
fix. Mockup boards from the review are in `docs/design/2026-09-22-review/`.
The design review is done; nothing from it is left unbuilt except the two
items below that need a ruling first.

**Awaiting owner:**
- Phase 5 (new host): the eight calls were approved as leaned on 2026-10-01;
  D-0047 to D-0049 are still proposed (promote?). The owner is partway through
  `docs/quarto-phase-5-owner-checklist.md` (at Step E, the two repo secrets;
  Claude never handles them). Open: the interim project name and a custom
  domain via OSU IT (the owner will ask for the IT note once the site is
  live); whether the project name comes from a repository variable (a D-0048
  amendment); account ownership (call 2) is the owner's fact. Nothing built:
  Tasks 1 and 2 (tests, then the deploy job) wait on the owner's word.
- Print preview Lab 1 on paper. The print rules shipped in PR #11 and have
  never been checked in a real print dialog.
- Two design items were deliberately not built, pending a ruling:
  moving the nav into the orange bar (D-0004 mirrors the Physics site), and a
  new hero headline (the mockup's wording was never approved).
- Carried from 2026-09-21: the D-0012 heads-up to University Marketing, and
  the pilot comparison feature and verdict date (spec section 8).

**Measurements (Quarto build, 2026-09-30):** `build/quarto-site/`, built fresh,
served from `build/` over HTTP and measured in the browser pane by
`tools/measure_chrome.js`, which loads each page of both builds in same-origin
iframes at fixed sizes. Page weights come from a script kept in the session
scratchpad, not committed: the page file, every linked stylesheet and script
that exists in the build, and the four WOFF2 fonts, in bytes.
- Old build versus Quarto, computed style and box of 25 chrome and content
  selectors on the six pages at 1440 and 375 px: two rows differ. `.site-foot`
  is missing in Quarto on index.html at 1440 px and at 375 px; that is D-0038
  (the landing footnote is not carried). Nothing else differs.
- Sim bar at 1280x720: bar 34 px, page 720 px, fits: true.
- Phone width 375 px, scrollWidth: 360 on /, /courses/, /how-this-was-made/,
  /sims/, and both ph211 team-building handout pages (modern and faithful).
  The measurement runs in a 375 px iframe whose own vertical scrollbar takes
  15 px (clientWidth 360, innerWidth 375, checked on the landing and faithful
  pages of both builds), so 360 means nothing scrolls sideways.
- Draft banner at 1440 px: 39 px closed, 107 px open, the same on all six pages.
- Landing prose column at 1440 px (`main > p`): left 363 px, right 378 px.
- Contrast, computed from the rendered page with the WCAG formula, the same on
  all six pages: draft banner 11.86:1, site name 4.56:1. Landing hero only:
  title 11.8:1, lead 8.19:1, button 4.56:1.
- Page weights in bytes: `build/site/` page; Quarto page; Quarto first visit (the
  page, every linked file and all four fonts; an upper bound, since a browser
  fetches only the font faces a page uses):
  - landing: 388501; 256206; 1159320
  - course index: 388518; 256359; 1159473
  - how-this-was-made: 387355; 255356; 1158470
  - sims index: 385619; 253568; 1156682
  - modern handout: 396679; 261916; 1169060
  - faithful handout: 395419; 261790; 1167066

**Measurements (2026-09-22):**
- Landing prose column at 1440 px: left 362 px, right 378 px (the 16 px
  difference is the scrollbar). Before centering: 136 px and 643 px.
- Draft banner at 1440 px: 39 px closed, 107 px open. Was 110 px.
- Phone width 375 px: scrollWidth 375 on the landing page with the hero.
- Contrast, computed with the WCAG formula: white on Star Canvas 11.8:1,
  Moondust on Star Canvas 8.19:1, white on Beaver Orange 4.56:1.

**Measurements (2026-09-21, branding refresh):**
- Sim bar at 1280x720: bar 34 px, page 720 px, fits: true.
- Phone width (375 px, scrollWidth <= 375): true on /, /courses/,
  /how-this-was-made/, /sims/, /labs/ph211-team-building-handout/modern/.
- Page weights (largest five, post-font embedding):
  - modern handout: 381 KB
  - faithful handout: 380 KB
  - course index: 373 KB
  - landing: 373 KB
  - how-this-was-made: 372 KB
  - published sim (fonts as data: URIs, no site CSS): 341 KB

**Pilot measures (spec section 6):**
- Spec gaps caught before code: 8. Logo variant versus banner colors
  (D-0013, D-0020); PNG versus ruled SVG (D-0014); off-palette count three,
  not six (D-0008); sim policy blocks fonts (D-0021); orange draft banner
  stacked on orange brand banner (D-0022); copyright wording would assert
  ownership (D-0023); italics and weights 600, 650 and 500 (D-0027);
  base64 data can trip the sim's banned-word check (D-0028).
- Owner corrections: 1. D-0021 flipped: sims may change their font.
- Proposed entries promoted without edits: 4 of 9 reviewed in round 1
  (D-0011, D-0012, D-0014, D-0015); 1 declined without a stated reason
  (D-0017); 4 left proposed (D-0013, D-0016, D-0018, D-0019). Round 2:
  4 of 6 promoted without edits (D-0020, D-0022, D-0023, D-0024); 1
  reversed (D-0021); 1 held for a question (D-0025). Round 3: D-0025 and
  D-0026 ruled; the owner narrowed D-0025 to a Latin and Greek subset.
  Round 4: D-0027 and D-0028 ruled without edits.

**Not built:** the ledger validator (spec section 6, D-0019). Only
`tests/test_brand.py` runs.

**Commits on branding-refresh (7fb7b82..54663d3):**
- `982f860` Palette-only chrome colors (T1)
- `08f9a0c` Luminance draft banner (T2)
- `69f9897` Commit the three official logo files (T3)
- `7af0e13` Header and footer on every site and document page (T4)
- `95b4d87` Slim black sim bar (T5)
- `63714c8` Sim bar logo under border-box fix (T5 fix)
- `20b4462` Self-host Open Sans, subset to Latin and Greek (T6)
- `54663d3` Embed Open Sans in the Electric Force sim (T7)
