# Executing critique, pass 3 (2026-11-12)

Read: 01a5ca5. Base: 6599a5f (origin/main). Windows 11 Enterprise
10.0.26200; Python 3.12.10; Pandoc 3.10 (Quarto's); Quarto 1.10.18;
poppler 25.07.0; git 2.55.0. Tasks executed: 3 of 3, in order, exactly as
written, at 6599a5f in a throwaway tree at a short path, the plan's code
blocks applied by scripts that pull them verbatim from the plan
(`probes/apply_*.py`); no F commits. The tree, its branch and the baseline
worktree are removed. Opus, high effort; 287,132 tokens, 137 tool uses,
3,922 s. The patches in this folder are `T<n> as written`, each body
carrying its red-step messages; the tripwire printed nothing.

Every red step went red with the message the plan states. Before T1's
commit, 341 tests in 1,147 s, all OK; at T2's boundary, `Filter` (7) and
`tests.test_downloads` (54) OK after a build. At T3's head: em-dash check,
word and number checks on all 19 converted files, and the build passed;
345 tests in 650 s, all OK.

Against a build of 6599a5f made as the plan says (its PH 211 Lab 1
`<main>` digest equals the pinned 1f388b20…, its PH 212 Data Analysis page
3 `<section>`s): each lab page differs only in its labels, each HTML
download also in the embedded label CSS; the probe holds; `<section`
counts equal on all 19 pages; the print-split pattern matches all 194
labels and captures what the old one did but T3's box headings. PDFs:
equal page counts; 206 pages at 50 dpi byte-identical after T1 and T2,
H5-label pages included; after T3 two pages differ (PH 212 Data Analysis
p. 4, Extending a Model p. 5), the box heading reflowing within its page.
`pdfinfo -struct`: +194 headings, H3 to H5, per lab per level as labelled;
the two box headings H3 to H4. HTML downloads 29 to 276 bytes smaller in
18 labs, PH 21X +36; least headroom under `HTML_CAPS` 22,108 bytes (PH 211
Lab 1). Word: 112 × QuestionLabel3, 66 × 4, 16 × 5; `document.xml`
otherwise identical but finding 6's paths; each new style `basedOn`
QuestionLabel adding only its `outlineLvl`; regenerating
`tools/reference.docx` changes only `word/styles.xml`. T3's sources: word
counts 2602 and 2589, as at the base. The rendered heading walk equals the
sources' ATX headings, level for level, in all 19 (`probes/atx_vs_rendered.py`).
Not measured: on-screen computed style, the accessibility tree, Word's
Navigation pane, NVDA.

Held up: the revision 51be7c7..01a5ca5 broke nothing; the spliced
`test_headings.py` is whole, `__main__` guard last; T2's prose applies as
written; the Word failure test is red in T1's state at h2 and h6 and green
after T2; the baseline rebuilds from the plan alone; D-0176's amendment at
a24d7ad is additive.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | low | comments left stale: `questions.lua:21-22` names the one Question Label style; `make_reference_docx.py` comments `# .question-label p:`, a selector T1 deletes, and its docstring names Question Label as the filter's style | T2 rewrites all three, text given in the plan |
| 2 | low | the source-text heading reading is replaced, recorded as a departure from spec section 3 but not in D-0176, whose ruled decision says `test_headings.py` "reads the rendered headings too" | put to the owner: a sentence in D-0176's rationale, or keep both readings |
| 3 | low | Files table lists the `Filter` tests under T1 only; T2 adds one | "T1, T2" |
| 4 | low | the baseline is pinned to 6599a5f; after a rebase onto a later `main` the "only the labels changed" diff would show unrelated changes; the baseline worktree is never removed | the baseline is the branch's merge-base with `main`; After step 3 removes the worktree |
| 5 | none | nothing asserts screen equality (carried from pass 2, finding 3) | by design: After step 2, measured and reported |
| 6 | outside | three Word downloads (PH 212 Designing Experiments, PH 213 Hypothesis Testing, PH 213 Model Building) write the build machine's absolute path into a picture's `descr`; on the base build too | not this PR; proposed as its own task |

The pass found something, and it is the third: per the executing-critique
rule the plan goes to the owner with every report, not to `/build`.
Findings 1, 3 and 4 are folded as revision 3, unchecked by a fourth pass.
