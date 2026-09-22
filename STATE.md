# State

Volatile handoff, capped at one screen. Updated 2026-09-21.

**Focus:** site branding refresh complete. Branch `branding-refresh` ready
for PR review. Plan: `docs/superpowers/plans/2026-09-21-site-branding.md`.

**Awaiting owner:**
- Open the PR (Step 6 of Task 8, or proceed directly below).
- Verify CI is green on the PR before merging.
- D-0012 heads-up to University Marketing: screenshots of the landing page
  and the sim are taken (2026-09-21 session); send them yourself.
- Pilot comparison feature and verdict date (spec section 8): placeholders
  still await your ruling.

**Measurements (2026-09-21):**
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
