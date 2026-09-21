# State

Volatile handoff, capped at one screen. Updated 2026-09-21.

**Focus:** site branding refresh, the pilot for the decision ledger spec.
Ledger bootstrapped: D-0001 to D-0019 in `DECISIONS.md` (8 ruled, 1
declined, 10 proposed). No branding code yet.

**Next step:** owner batch-reviews D-0011 to D-0019, one line each. Then the
Superpowers spec (`docs/superpowers/specs/`), citing entry IDs.

**Blockers:**
- D-0013: the supplied logo is the light-background version and cannot sit
  on the orange banner (D-0004) or the black sim strip (D-0005). Reversed
  variants needed, or a new ruling.
- Open Sans files (D-0006): fetching them is a download needing the owner's
  approval of source and size.

**Open questions:**
- Footer policy-link URLs and copyright wording (D-0009): placeholders.
- Pilot comparison feature and verdict date (spec section 8): placeholders,
  awaiting owner.

**Pilot measures:**
- Spec gaps caught before code: 3. (1) Logo variant conflicts with the
  banner and strip colors (D-0013). (2) Supplied PNG versus ruled SVG
  (D-0014). (3) Off-palette count was three in round 2, is six (D-0008).
  Also noted: the style guide's 18 px bold large-text size is below WCAG's
  18.66 px; moot, since orange passes AA at normal size on white and black.
- Owner corrections: 0.
- Proposed entries promoted without edits: pending first batch review.

**Not built:** the ledger validator (spec section 6). Nothing checks the
ledger's format; only `tests/test_brand.py` runs. See D-0019.
