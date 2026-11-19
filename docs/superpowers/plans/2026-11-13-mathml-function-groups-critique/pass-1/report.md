# Executing critique, pass 1 (2026-11-13)

Read: abc8671. Windows 11 10.0.26200; Python 3.12.10; Pandoc 3.10. Opus,
high effort; 166,948 tokens, 38 tool uses, 449 s. Tasks executed: 2 of 2,
as written; no F commits. Patches `0001` and `0002` here are `T<n> as
written`; the tripwire printed nothing.

Over CI's build (38 lab files, 86 HTML files in all): exactly four files
changed, one equation each (PH 212 Lab 6 and PH 213 Data Analysis, page and
HTML download); every other file was byte-identical; every `<math>` parsed
before and after; the built-page test failed on the untouched copies and
passed on the rewritten ones.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | high | `MATH_TAG` counted only `<mrow>`: a `)` closing inside `<msup>`/`<msub>` (`\sin(x)^{2}`) or a bracket across aligned rows gave malformed XML and no stop | every element's tags counted; a close below the start stops the build (D-0181 (1)); test added. Prototype on Pandoc output: `^{2}`, `_{i}` and aligned rows stop; nested and repeated functions group |
| 2 | medium | the T1 verify needs `build/quarto-site` (`setUpModule`) | stated: an empty folder does locally |
| 3 | medium | Pandoc writes `&#8289;`; the literal comes from Quarto and `--embed-resources`; the entity form would pass silently | rewrite and tests accept the literal, `&#8289;` and `&#x2061;`; an entity test added; the claim corrected |
| 4 | medium | `\sin|x|` stopped the build; the plan widened D-0181's `( )` to every prefix bracket; brackets paired by count, not character | narrowed to round brackets matched by character, as D-0181 (1) says; `[x]` and `|x|` left alone, tested |
| 5 | low | the built-page test reused the rewrite's regex; only Lab 6's page asserted grouped; the reader's added check had no code | grouped form asserted on all four files; entity accepted; the reader check given as code |
| 6 | low | Lab 6's `\frac{m g\sin\theta}{b_1}` (U+2061 before a letter) unstated | stated, left alone |

Mutants M3 (no `rows < 0` break) and M9 (any `<mo>` instead of U+2061)
survived; the unmatched test now has a `)` after the enclosing row, and the
left-alone test has a row of `<mi>` and `<mo>+</mo>`. Known limit recorded:
`\cos{\left( x \right) + E}` (two nested rows) is left alone; no page holds it.
