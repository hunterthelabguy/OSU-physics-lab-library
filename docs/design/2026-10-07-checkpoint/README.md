# Checkpoint colour board (2026-10-07)

`board.html` draws three palette colours for the checkpoint block (D-0109,
D-0110) beside today's question box, in the modern page's light and dark
themes, with WCAG contrast computed from the hex values. It is an Artifact
page source (no doctype; the Artifact tool wraps it) and opens in a browser
as it is. Published for the owner at
https://claude.ai/artifact/P99gGBPsZWzEPYmhKB2aJF (private).

- A: Pine Stand rule on the question's tint.
- B: High Tide rule on the question's tint.
- C (lean): Candela fill and a Luminance rule; in dark, the dark tint and a
  Luminance rule.

Decision: none yet. PR 2 of pass 2a (D-0112) builds the owner's pick in the
page and the Word download, and pins it in `tests/test_brand.py`.

A mockup, never the source of truth for what the site does.
