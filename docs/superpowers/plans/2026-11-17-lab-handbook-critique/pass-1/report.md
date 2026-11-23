# Executing critique, pass 1: Lab Handbook plan

Plan read: 222301f (base 33d6cb2; 222301f is 33d6cb2 plus four docs files).
Run 2026-11-17 by a fresh subagent (Opus, high effort) in a throwaway worktree
of 33d6cb2. Environment: Windows 11 Enterprise 10.0.26200, Git Bash, Python
3.12.10 (`-X utf8`), Pandoc 3.10 (Quarto's bundled copy), Quarto 1.10.18.
The harness refused the subagent's write of this file; the parent session
saved its returned report here verbatim in substance, lightly reformatted.

## Tasks executed: 7 of 7

T1 to T7 applied in order, verbatim. No F commits were needed.

Each task went red with the predicted failure, then green; all the plan's
script asserts held.

- T1: 11 errors, `KeyError: 'text'`; then 63 tests passed.
- T2: 3 failures, "Word has 2 numbered paragraphs to place..." (the plan
  predicted two of the three); then 23 tests passed.
- T3: 1 failure, `[] != [... (ruled_additions)]`.
- T4: page and Word links unchanged, 2 failures.
- T5: `KeyError: 'ph21x-lab-handbook'`.
- T6: no `<h1>` reading Lab Handbook.
- T7: no `href` or `Target` pointing at the handbook.

The plan's full Verify, run verbatim after T4, T5, T6 and T7, passed every
time (em-dash scan, word check, number check, build with no Quarto warning,
tests). Test count 368, 370, 371, 373. Each task's own Verify reached its
expected value.

Negative probes at T5: without `labels:` the number check fails ("Word has 30
numbered paragraphs to place"); with the span's `to` one paragraph later the
word check fails.

Premises confirmed: Lab 7 child 131 holds the Appendix B heading once; tables
at children 11, 29, 36, 59; 30 labels o1 to o11.2. Lab 3 "Required Plot
Elements" at children 96 and 98; last labels o14.0.1, o14.0.2. The scripts'
asserted line counts are right. Built pages put heading ids on the `<h2>`.

Built output after T7:

- Handbook page: one `<h1>` "Lab Handbook", the 7 `h2` ids as D-0190 lists
  them, 7 contents links, both icons with Word's alt text; listed under "For
  every course".
- Handbook downloads: Word 16,305 bytes with 7 internal links to matching
  bookmarks; HTML 169,306 bytes; PDF 111,844 bytes, prints; Markdown the
  source byte for byte.
- Lab 3: page, HTML download, Word and PDF each hold both library addresses.
  The Markdown download keeps `ph21x-lab-handbook#...` (declared limit).
- `media.lua` runs at `pre-ast` (`tools/quarto_build.py:128`), so Quarto never
  sees the source form of the link and never warns.

## Findings

1. **Medium, needs-ruling, CONFIRMED.** The number check excuses a declared
   run of labels without checking that the run lies in the span. D-0189 (3)
   and spec 4.1 say "exactly" the labels inside the span; T2's `span_labels`
   reads only `first`/`last`. T2's fixture span `to: "Any words."` is one the
   word check would reject, yet the number check passes it. Gap: a question
   converted as plain text with its label excused would pass both checks.
   This build does not hit it.
2. **Low-medium, mechanical, CONFIRMED.** Spec 5's "omits more" and "edge in a
   table cell" fixture cases are missing from T1.
3. **Low, needs-ruling, CONFIRMED.** D-0191 amends CLAUDE.md, but no task
   edits it; `CLAUDE.md` still says "never copy content into a second file".
4. **Low, mechanical, CONFIRMED.** The HTML cap factor: plan says x1.15 "as the
   neighbouring entries are"; `tests/test_downloads.py` says x1.10. For
   169,015 bytes that is 200,000 against 190,000.
5. **Low, mechanical, CONFIRMED.** The new docstring `- span:` example sits
   after the `ruled_equations` example; it belongs after `ruled_omissions`.
6. **Low, CONFIRMED in the build.** Lab 3's PDF splits the lead-in from its
   list: the lead-in ends page 9, the two-link list stands alone on page 10.
   The trial checks Word and Google Docs, not the PDF.
7. **Low, mechanical, CONFIRMED.** The HTML and PDF downloads' links are
   untested (T7 tests the page and Word). Measured correct.
8. **Low, mechanical, CONFIRMED.** T3's `ADDITION` regex reads only one-line
   double-quoted `text:` values; any other form is skipped silently.
9. **Low, mechanical, CONFIRMED.** Slips: Lab 3 has four pictures, not three;
   media.lua's `Link` is at lines 129 to 135, not 128 to 133; the docstring
   block ends at 77, not 78; T7's Files row names line 555 but the step
   names `MarkdownAndWord` (line 179).
10. **Low.** T1's conversion-spec section has no fixed text.
11. **Note.** The address list is held twice (`test_lab_handbook.py` and
    `test_quarto_site.LabHandbook`); spec 4.3 says "a test holds the table".
12. **Note, PLAUSIBLE, owner's call.** `site/how-this-site-works.md:50` to `52`
    says a changed passage lists "the original's words"; a span lists only
    its edges. The "listed passages" sentence D-0189 ruled on stays true.

Ordering and scope: no findings. T1 to T4 touch disjoint files; T5 needs T1
and T2 (T4 only for the test module); T6 passes without T3; T7 needs T1, T4,
T6, not T2. Every commit touched exactly the files the Files tables name.

## Plan edits proposed

1. T2: a ruling on finding 1 (map the run to the span, or amend D-0189 (3)).
2. T2 fixture span: edges the fixture satisfies.
3. T1: add `test_span_omits_more_fails`, `test_edge_in_a_table_cell_stops`.
4. T1 docstring: span example after `ruled_omissions`.
5. T1: conversion-spec section text verbatim.
6. T5 cap: x1.10 (190,000), or rule a new factor.
7. One home for the seven addresses.
8. T7 Files row: `MarkdownAndWord` (`test_downloads.py:179`), drop "line 555".
9. T7: test HTML download and PDF `/URI` links; owner looks at the PDF break.
10. T3: report an entry it cannot parse instead of skipping it.
11. Fix the slips of finding 9.
12. Add, or rule out, a CLAUDE.md change for D-0191.

## Patch folder and tripwire

`0001-T1-as-written.patch` to `0007-T7-as-written.patch`; `probes/` holds the
scripts that copied the plan's code blocks, `body_probe.py` and `verify.sh`
(home paths removed). Tripwire printed nothing; all 7 subjects are
"T<n> as written".

## Cleanup and cost

Scratch worktree removed, branch `critique-scratch-handbook` deleted.
`lib-strip` unchanged apart from this folder. No server started; no
student-identifiable data met. Wall time about 2 h 15 min, most of it four
full Verify runs (22 to 27 min each). Usage: 305,787 tokens, 100 tool uses,
7,301 s.
