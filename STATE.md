# State

Volatile handoff, capped at one screen. Updated 2026-09-21.

**Focus:** site branding refresh, the pilot for the decision ledger spec.
Spec written: `docs/superpowers/specs/2026-09-21-site-branding-design.md`.
Ledger: 16 ruled, 3 declined (D-0003, D-0017, D-0021), 7 proposed. No
branding code.

**Next step:** owner rules D-0025 (asked what is special about Open Sans
first) and D-0026, and approves the spec (D-0013 is met in substance; its
status is the owner's). Then the plan via
writing-plans, with `Ledger:` and `binds` header lines.

**Blockers (header and sim-bar tasks stop on these):**
- D-0025 plus download approval for the Open Sans files (font tasks).
- D-0026 (sim font task).

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
  reversed (D-0021); 1 held for a question (D-0025).

**Not built:** the ledger validator (spec section 6, D-0019). Only
`tests/test_brand.py` runs.

**Sandbox note:** `OSU-style-guide.md` moved into `../OSU-branding/`; the
comment in `site/site.css` still points at the old path (fix in the refresh).
