# State

Volatile handoff, capped at one screen. Updated 2026-10-02.

**Focus (2026-10-01):** Phase 5 cutover done. Production is the Quarto build
on Cloudflare Pages, `https://osu-physics-labs.pages.dev/` (project
`osu-physics-labs` in the owner's own account; name from the repository
variable `CLOUDFLARE_PAGES_PROJECT`). PR #17 (deploy job, `tools/check_deployed.py`,
404 page) and PR #18 (hand-run `create-pages-project.yml`) merged; 134 tests.
The first production run passed `check_deployed.py` against the deployment
URL and the `pages.dev` alias: every file byte for byte, unknown paths 404
with `404.html`, so Pages does not rewrite the HTML. Cloudflare refuses
Python's default user agent (error 1010); the check names itself. The owner
checked production on a phone and printed Lab 1 in both presentations
(2026-10-01): fine. The old Vercel URL redirects there (308, path kept).
Downloads merged 2026-10-01, PR #19 squashed as `bbfa9b6` (D-0052 to
D-0056): four files per lab from modern, the department line in each, the
header logo published once; 148 tests; `verify` and the preview `deploy`
green on the PR's head. Demo 2026-10-06. Then two design passes, ruled as
leaned 2026-10-01 ("Rule your way on all of them and build it"), merged as
PR #20, squashed `6ee86ee` (D-0057 to D-0059, ruled 2026-10-02; 158 tests): the
Word file's draft notice is a page header, its footer size is on a Footer
style, its page is Letter at 0.75 in, its body takes the modern page's
spacing, and questions are the page's tinted, orange-ruled box; the owner
checked both builds in Word ("Looks right in Word, merge it"). The PDF's
keep rules already worked (probe: no split in 40 offsets, 50 with the
rules off), so no CSS was added and a print test pins them. The download
links are four buttons (mockups and measurements in
`docs/design/2026-10-01-download-control/`). Next: phase 4, spec written
2026-10-02 for ruling (its plan text deletes the templates that D-0036 and D-0054 now
depend on; it retires `build/site`, Pandoc 3.11, the tree test and the
old-build comparisons, not the templates).
Plans: `docs/superpowers/plans/2026-10-01-quarto-phase-5.md`.

**Previous focus:** phases 2 and 3 of the Quarto migration (PR #14, #15,
#16); site design review of 2026-09-22 (PR #11, #12, boards in
`docs/design/2026-09-22-review/`).

**Build pass, ruled 2026-10-02, in this order (one PR each, squash):**
1. D-0060: `check_deployed.py --wait`, alias step only. Until it merges, a
   red alias step on a docs-only commit is the known lag (two of eight
   `main` runs since the downloads), not a production fault: confirm the
   deployment-URL step passed.
2. D-0061, phase 4, per `docs/superpowers/specs/2026-10-02-quarto-phase-4-design.md`:
   D-0038 pins first, then the deletions. Vercel still builds `main` and
   posts a commit status until the owner turns builds off or deletes the
   project; a red Vercel status after phase 4 blocks nothing.
3. D-0067 (proposed; its calls ruled as leaned): Download all per course,
   five zips; its words are approved pending the owner's look at the preview.

**Awaiting owner:**
- Promote D-0067 (calls ruled; entry text proposed). D-0062 to D-0066
  (public flip, logo, domain, cold test) are another session's, proposed.
- Vercel: delete the project, the owner's leaning (2026-10-02); it ends the
  redirect, the Git builds and the commit statuses. When he says it is done,
  record it (an entry amending D-0049, the spec's call 1, the agent
  reference's Vercel paragraph, lab-ops' `lab-handbook/lab-library-site.md`).
- A second handout to convert: PH212 Lab 1 (17 equations, 4 tables, no
  images) leaned; Lab Guidance for Students has 9 images and 54 equations
  but is not a lab. The content check must count equations first
  (`docs/conversion-spec.md`).
- Originals' Word metadata names authors (`creator`, `lastModifiedBy`,
  set in the committed PH211 original and the PH212 file): strip before
  committing, and does PH211's history need it (see D-0062)?
- Not built, for a later ruling: a Word box for the legend and the hint
  arrow (D-0057: `custom-style` misses list items; the arrow would be a
  character in the text). The legend's "arrow" and "Boxed" stay unmet in
  Word until then.
- Downloads: check production on a phone (the four download buttons,
  each file, the PDF footer); the owner does not treat the 2026-10-06 demo
  as a deadline; PR #19 and PR #20 merged
  without a phone check of the preview.
- Open, the owner's, not to be designed until he raises it: how students
  complete handouts. Either a browser-only fillable worksheet with an
  export (nothing leaves the browser, so no student data is stored; the
  cost is work lost if the browser's storage is cleared), or paper
  handouts completed individually during lab, one per group graded at
  random each week, replacing the group lab report. His drivers: peer
  accountability, answers free of AI text, the 1 h 50 min lab, and any
  outside work moved to simulation-based prelabs. He has not decided.
- Phase 5 is done, Task 4 included (2026-10-01): migration plan marked,
  CLAUDE.md Deploy rewritten, successor page
  `OSU-lab-ops/lab-handbook/lab-library-site.md` (lab-ops ledger 29).
  Open from lab-ops' hosting plan (driver 3, AI training): Cloudflare's
  AI-training crawler setting has not been checked for `osu-physics-labs`;
  it is a dashboard setting, the owner's to look at.
- D-0051 (actions to current majors) is built after downloads or before, as
  the owner says; it waits on nothing.
- Two design items were deliberately not built, pending a ruling:
  moving the nav into the orange bar (D-0004 mirrors the Physics site), and a
  new hero headline (the mockup's wording was never approved).
- Carried: the D-0012 heads-up to University Marketing; the draft note to
  OSU IT by role (library address, custom domain), offered, never sent; the
  pilot comparison feature and verdict date (spec section 8).

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
