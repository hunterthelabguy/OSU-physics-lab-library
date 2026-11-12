# Executing critique, pass 1 (2026-11-12)

Read: 0e233cb. Base: 6599a5f (origin/main). Windows 11 Enterprise
10.0.26200; Python 3.12; Pandoc 3.10 (Quarto's); Quarto 1.10.18. Tasks
executed: 3 of 3 in a throwaway tree, in the order T1, F1, F2, T2, T3; the
tree and its branch are removed. Opus, default effort; 277,155 tokens, 141
tool uses, 7,160 s. The patches in this folder are `T<n> as written` and
`F<k>:` commits, each body carrying its red step; the tripwire printed
nothing.

Full verify at the tree's head: em-dash check, word and number checks on
the 19 converted files, and the build all passed. 344 tests, 2 errors, both
`ZipReadBack` failing on a 270-character media path from the scratch
tree's location (Windows MAX_PATH), not from the plan. No screen
measurement was made (headless print only).

Settled by running: Pandoc 3.10 accepts a list of blocks plus `false`
from a top-down Div function; Quarto honours `traverse = "topdown"`
(the page and the plain Pandoc render agree label for label, including
PH 212 Lab 1's Q4, whose box holds a `###`); Quarto writes the label as
`<h3 class="question-label">Question 1</h3>` with no id and no `anchored`
class; Pandoc reorders a style's attributes in the output docx but keeps
its children, so T2's assertions hold; regenerating the reference changes
only `word/styles.xml`. After F1: page counts equal in all 19 PDFs, every
page rasterized at 50 dpi pixel-identical to the baseline but the two
MAX_PATH pages, `<section>` counts per page unchanged, each tagged PDF
gaining exactly its labels as structure headings (`pdfinfo -struct`), HTML
downloads within 100 bytes of the baseline, T3 moving no page break.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | critical | a Div opening with a Header is written as `<section id=… class="question-label question">`, so the label's rule styles the whole box (every stem small capitals, PH 212 Lab 1 PDF 12 pages to 11; 105 `PrintKeeps` failures); the plan's tests and probe read only the `<hN>` | F1 adopted: the label Header sits in an attribute-less Div, written as no element; `test_headings` reads through it; a Filter assertion that the box stays a div and no `<section` appears; the probe reads the parent and the page's `<section` count |
| 2 | high | the pinned PH 211 Lab 1 `<main>` digest (`tests/fixtures/main-bodies.json`) goes stale; not in the plan | F2's step adopted: T1 recomputes it as the test does, after diffing that `<main>` against the baseline |
| 3 | medium | the plan made styles Question Label 2 to 6 where D-0176 rules 3, 4 and 5; 2 and 6 have no consumer on `main` | brought back to D-0176's three; the Word render fails, naming D-0176, on any other level, with a Filter test; put to the owner |
| 4 | medium | "probe before the full build" is the full build, and it read only the label tag | the probe follows the build and reads the box's tag and the `<section` count |
| 5 | medium | the new print rule `.question-label { break-after: avoid }` has no test that can fail (`PrintKeeps` reads `<h[1-4]`, the print says "QUESTION N", `RULES_OFF` does not undo it) | the rule is dropped: H3 and H4 labels already take `h1, h2, h3, h4 { break-after: avoid }`, the box keeps `break-inside: avoid`, and an H5 label prints as the old `<p>` did |
| 6 | low | the plan drops the source-text heading reading the spec keeps | recorded in T1 as a departure from spec section 3, measured as losing nothing on `main` |
| 7 | low | NVDA sentence is on line 8; a 130-character comment line; `LABEL_STYLE` placement worded two ways | fixed: line 8, the comment given in full, placement named once |
| 8 | low | a question nested in a question is not labelled under top-down traversal | none on `main`; stated in the plan's Files notes; `check_numbers` would fail on a missing label |
