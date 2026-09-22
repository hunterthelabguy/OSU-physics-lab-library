# State

Volatile handoff, capped at one screen. Updated 2026-09-21.

**Focus:** site branding refresh, the pilot for the decision ledger spec.
Spec approved 2026-09-21. Plan: `docs/superpowers/plans/2026-09-21-site-branding.md`.
Ledger: 20 ruled, 3 declined, 4 proposed (D-0013, D-0016, D-0018,
D-0019). No branding code yet.

**Next step:** execute the plan subagent-driven on branch
`branding-refresh` from main (owner ruling 2026-09-21, Sonnet where
reasonable). PRs 8 and 9 (sim law codes, vectors off) are on main; Task 7
edits the same sim file. Then the plan via
writing-plans, with `Ledger:` and `binds` header lines.

**Blockers (header and sim-bar tasks stop on these):**
- None. D-0027, D-0028 and the download are approved.

**Open questions:**
- Pilot comparison feature and verdict date (spec section 8): placeholders,
  awaiting owner.
- Page weight once logo and font are embedded in every page: measured at
  build, judged by the owner, no threshold ruled.

**Pilot measures:**
- Spec gaps caught before code: 6. Logo variant versus banner colors
  (D-0013, D-0020); PNG versus ruled SVG (D-0014); off-palette count three,
  not six (D-0008); sim policy blocks fonts (D-0021); orange draft banner
  stacked on orange brand banner (D-0022); copyright wording would assert
  ownership (D-0023).
- Owner corrections: 1. D-0021 flipped: sims may change their font.
- Proposed entries promoted without edits: 4 of 9 reviewed in round 1
  (D-0011, D-0012, D-0014, D-0015); 1 declined without a stated reason
  (D-0017); 4 left proposed (D-0013, D-0016, D-0018, D-0019). Round 2:
  4 of 6 promoted without edits (D-0020, D-0022, D-0023, D-0024); 1
  reversed (D-0021); 1 held for a question (D-0025). Round 3: D-0025 and
  D-0026 ruled; the owner narrowed D-0025 to a Latin and Greek subset.
- Spec gaps caught before code, continued: 8. Italics and weights 600,
  650 and 500 (D-0027); base64 data can trip the sim's banned-word check
  (D-0028). Round 4: D-0027 and D-0028 ruled without edits.

**Not built:** the ledger validator (spec section 6, D-0019). Only
`tests/test_brand.py` runs.

**Sandbox note:** `OSU-style-guide.md` moved into `../OSU-branding/`; the
comment in `site/site.css` still points at the old path (fix in the refresh).
