# Executing critique, pass 3 of 3 (2026-11-13)

Read: 6906707, which is origin/main 6f6a6fd plus the plan and its critiques.
Environment: Windows 11 Enterprise 10.0.26200; Python 3.12.10; Pandoc 3.10
(Quarto's). Opus, xhigh effort; 234,167 tokens, 90 tool uses, 1,035 s.

Tasks executed: 6 of 6, as written, in a throwaway tree. There were no F
commits. Patches `0001` to `0006` here are `T<n> as written`, and the
tripwire printed nothing.

## What it confirmed

The rebase onto #69 to #75 broke none of these:
- the code anchors;
- the spec and CLAUDE.md anchors;
- every replacement count and every lab's word count;
- the test counts, 42 before T1 and 54 after;
- T4 to T6's undeclared problem lists and their front-matter placement.

T1 ran as planned:
- Red: 12 tests selected; 10 fail, 1 errors (the PdfText test,
  `AttributeError`), 1 passes.
- Green: all 12 pass.
- After T1, all 19 converted files check `ok`.

Every verify step reached its stated value:

| Lab | Word and number check | MathML reader |
|---|---|---|
| Lab 1 | 2602 words, 17 equations | 1 flagged (the expected one), `['total']` |
| Lab 2 | 2589 / 10 | 0 flagged, `['total', 'total']` |
| Lab 5 | 2623 / 15 | 0 flagged |
| Lab 3 | 4607 / 29 | 0 flagged, `['slope', 'slope']` |
| Lab 6 | 4427 / 21 | 0 flagged |

A token diff of the MathML before and after shows nothing changed outside
D-0167 (1) to (3).

## Mutation results

Of 13 mutants, 11 are killed. Two survive:
- **M6** (no normalization on the declaration). Now killed by declaring
  with spaces in `test_a_declared_sign_passes`.
- **M13** (declarations honoured only for Word originals). It survives, but
  it can only make a declared change on a PDF original fail loudly, never
  pass silently.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | medium-low, needs ruling | The plan's status rule was false to the record. Lab 2 (D-0133, D-0161), Lab 6 (D-0164) and PH 21X (D-0160) declare differences and stay `converted`; nothing reads `status`; D-0168 is still proposed. Labs 1 and 2's bold change is unlisted against how-this-site-works:50-54. | Held for the owner. T4 to T6 leave `status` alone until ruled. |
| 2 | low | T2's header still said it depends on T1 | "none" |
| 3 | low | Nothing makes T6 the last lab to land, so its STATE line could land too early | STATE line moves to whichever content PR merges last |
| 4 | low | Mutant M6 survives | `test_a_declared_sign_passes` declares with spaces |
| 5 | info | Draft PR #76 touches Labs 1 and 2 (heading levels only); its hunks apply cleanly over T2 and T3 | named in the order section |
| 6 | cosmetic | Timing is about 30 s, not 2 minutes; the "Conversion phase" label; a line anchor | fixed |

This was the third pass and it still found something, so by the
writing-plans skill the plan goes to the owner before any build.
