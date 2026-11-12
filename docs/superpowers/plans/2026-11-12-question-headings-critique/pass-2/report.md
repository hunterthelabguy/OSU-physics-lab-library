# Executing critique, pass 2 (2026-11-12)

Read: 51be7c7. Base: 6599a5f (origin/main). Windows 11 Enterprise
10.0.26200; Python 3.12.10; Pandoc 3.10 (Quarto's); Quarto 1.10.18;
poppler 25.07. Tasks executed: 3 of 3, verbatim at 6599a5f in a throwaway
tree at a short path, with one F commit; the tree and its branch are
removed. Sonnet, high effort; 229,177 tokens, 89 tool uses, 4,072 s. The
patches in this folder are `T<n> as written` and `F1:`; the tripwire
printed nothing.

At the tree's head after a full build: em-dash check, word and number
checks on all 19 converted files, and the build passed; 345 tests in
1,051 s, all OK (no `ZipReadBack` error at the short path). Against a
build of 0e233cb: equal page counts in all 19 PDFs; of 206 pages at
50 dpi, 204 byte-identical, the two others PH 212 Data Analysis p. 4 and
Extending a Model p. 5, T3's box heading reflowing within its page as call
4 predicts. Pages holding an H5 label, now with no `break-after` rule, are
pixel-identical. `<section` counts per page equal; `pdfinfo -struct` gains
+194 headings over the 19 PDFs, H3 to H5, one per label; the print-split
pattern matches all 194 labels. HTML downloads 40 to 280 bytes smaller in
18 labs, PH 21X +36; all under `HTML_CAPS`. Four HTML downloads printed
before and after: pixel-identical but T3's page. Not measured: screen
computed styles, Word's Navigation pane, NVDA.

Held up: the wrapper Div (no `<section`), the probe after the build, the
digest step, Word styles 3 to 5 matching D-0176's text, the declared
departure from the source-text heading reading.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | high | T2's "expected: pass" is false: `test_word_box_holds_a_list_between_parts`, `test_word_checkpoint_is_its_own_box` and `test_word_box_without_its_colours_fails` render heading-less bodies whose h2 label now stops the Word render; the hard failure at h2 and h6 needs a ruling | F1 adopted: each body opens with `## Part`; the failure was ruled before this report reached the plan (D-0176, "Keep three", a24d7ad) |
| 2 | medium | D-0176's decision still says the print rule names the label | already recorded in D-0176's rationale at a24d7ad, which this pass did not read |
| 3 | medium | nothing asserts the PDF structure tags or screen equality | left to the plan's After steps 2 and 3, measured and reported in the PR; this pass measured the tags (+194) |
| 4 | low | the replacement `test_headings.py` drops the `__main__` guard | kept |
| 5 | low | `PrintKeeps` cannot see a stranded label (h1 to h4 only, case) | not a regression; recorded in the plan since revision 1 |
| 6 | low | `test_no_duplicate_ids` has no red step | stated in T1 as a guard |
| 7 | low | the `assertNotRegex` change needs its arguments swapped | the call written out |
| 8 | low | the full suite takes about 18 minutes | not folded: T1 and the end each need the whole suite (the digest, `PrintKeeps`, the page against Pandoc) |
| - | revision | T1's probe and After step 2 named a scratchpad baseline, and revision 1 a scratchpad report | the baseline is a build of 6599a5f in a short-path worktree; the report path is this folder's |
| - | gap | the Word failure's h6 branch had no test | the Filter test runs h2 and h6 |
