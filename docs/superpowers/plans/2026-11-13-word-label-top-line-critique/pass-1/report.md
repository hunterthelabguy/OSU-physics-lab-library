# Executing critique, pass 1 (2026-11-13)

Read: 0f2e222. Base: 9075998 (branch `word-label-top` on
`question-headings`). Windows 11 Enterprise 10.0.26200; Python 3.12.10;
Pandoc 3.10 (Quarto's); Quarto 1.10.18; Word 16.0.20430.20180. Task
executed: 1 of 1, verbatim at 9075998 in a throwaway tree at a short path,
beside a base build in a second one; both trees and branches removed. Opus,
high effort; 237,476 tokens, 100 tool uses, 2,105 s. The patch in this
folder is `T1 as written` (its body the red message); no F commits; the
tripwire printed nothing. `probes/` holds the critique's own scripts.

At the T1 head: em-dash check, word and number checks on the 19 converted
files and the build passed; `MarkdownAndWord` and `Filter` 23 tests OK;
the full suite 345 tests OK (base also 345 OK). Against the base build:
every page and HTML download byte-identical; the PDFs differ only in their
dates and ids; each `document.xml` differs only in the label paragraphs,
the cell top margins (203 to 92), whitespace, the build path, and finding
3's stems. Labels 112 / 66 / 16, each directly before its table, texts and
order as base.

Word, measured: the pane lists none of PH 212 Lab 1's questions as base;
with every entry expanded, Questions 1 to 16 (PH 212 Lab 1) and 1 to 14
(PH 211 Lab 3). Edges at 300 dpi, label row against stem row: rule
16.56 to 19.44 pt and tint right 522.00 pt in both builds (0.00 pt). The
strand survey over 18 labs: base 0, T1 2, exactly the spec's; pages as
base but PH 211 Lab 3 (13 to 10) and PH 212 Lab 1 (10 to 11).

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | medium | the red step raises "build/quarto-site is missing" in a fresh worktree; `setUpModule` needs a build | T1 builds the unchanged filter first; the build-reading reds named |
| 2 | medium | `test_word_box_is_the_modern_block` passes with no labels (its loop is empty once `boxes` goes) | the test asserts a label sits before a box |
| 3 | needs ruling | 78 of 194 stems change from Body Text to First Paragraph (Pandoc's style after a heading; the raw label does not reset it); drawn the same | declared in spec section 4; put to the owner |
| 4 | medium | the committed pane probe expands only Part 1, so Questions 8, 9 and 12 of PH 212 Lab 1 stay folded | `nav_pane.ps1` presses Right on every entry; the after-step expects 1 to 16 and 1 to 14 |
| 5 | needs ruling | the label's rule starts 0.48 pt below its tint (the tint top border covers the corner); rows 90 and 250 cannot see it | `edges_scan.py` added to the after-step; put to the owner |
| 6 | low | the committed probe hard-codes indents 248 / 248, so it cannot make the measured 238 / 10 / 258 | indents are arguments, the design's values in its comment |
| 7 | low | the plan's grep lacks `-r` | fixed |
| 8 | low | a Word the owner opens at the same moment trips the probes' one-new-process check | the after-step says to rerun |
| 9 | low | no CI pin of the indents and border spaces | not taken: the spec's tests hold colours and the spacing sum, Word's render the edges |
| 10 | low | two comment lines past the file's width | the plan names the widths |
