# A table just before a question box: plan (D-0179)

Spec: `docs/superpowers/specs/2026-11-13-docx-crushed-table-design.md`,
ruled 2026-11-13 ("Leans as written"). Branch `docx-crushed-table`.
Format only; no source, original or wording changes.

## Task 1: tests, red on main

In `tests/test_downloads.py`, class `MarkdownAndWord`, after
`test_word_checkpoint_is_its_own_box`:

1. `test_word_box_after_a_table_keeps_its_own_table`: the Markdown
   `| a | b |\n|---|---|\n| 1 | 2 |\n\n::: {.question #a}\n**Why?**\n:::\n`
   through Pandoc with `questions.lua`, `-M theme=modern`,
   `downloads.box_colours()` and the reference document, as the checkpoint
   test runs it. Assert: two `w:tbl` in `word/document.xml`; the text
   between the first `</w:tbl>` and the second `<w:tbl>` is, whitespace
   aside, exactly one paragraph, and it is the same paragraph that follows
   the box (the box's own gap, read from the output, not typed in the
   test).
2. `test_word_tables_never_touch`: for every `converted()` document, its
   built `word/document.xml` has no `</w:tbl>` followed, whitespace aside,
   by `<w:tbl>` or `<w:tbl ` (`assertNotRegex`, `r"</w:tbl>\s*<w:tbl[\s>]"`).

Run both against the current filter and the current build: test 1 fails
(the tables touch), test 2 fails on `ph211-uncertainty-handout` only.
Commit the tests alone.

## Task 2: the fix

In `tools/filters/questions.lua`:

1. Move the gap paragraph's text out of `word_box` into a module-level
   `local GAP` (same string, `twips(1.5)` = 339), used by `word_box` for
   the gap after the box.
2. Add a third filter table after the Div pass:
   `Blocks = function(blocks)`; return `nil` unless `FORMAT == "docx"`;
   build a new list, and before a block that is a `RawBlock` of format
   `openxml` whose text starts with `<w:tbl>`, when the block before it is
   a `Table`, insert `pandoc.RawBlock("openxml", GAP)`. Return the new
   list only if something was inserted, else `nil`.
3. Extend the comment over `word_box` (lines 38 to 41): the gap also goes
   before a box that follows a table, since Word joins two tables that
   touch (D-0179); Pandoc separates its own tables but cannot see the box.

Both tests from task 1 pass after a rebuild. Commit the fix.

## Task 3: verify

1. With `.superpowers/sdd/verify-env.sh` exported: the CI sequence
   (em-dash check, word check and number check on the converted files,
   `python tools/quarto_build.py`, `python -m unittest discover -s tests`).
   All green.
2. Compare every built Word download's `word/document.xml` with the copies
   of main's 6599a5f build (scratchpad `survey/`), with each build's
   checkout path normalized: identical except PH 211 Lab 3, whose only
   difference is one gap paragraph between the stopwatch table and
   Question 7's box.
3. Render the new PH 211 Lab 3 `.docx` through Word (scratchpad
   `render.ps1`, read-only copy): 15 tables, 10 pages; look at the table's
   pages.

## Task 4: draft PR

Squash-mergeable branch with the spec, D-0179, the plan, the tests and the
fix. PR body: cause, bisect table, survey, the Word render numbers, and the
owner's ruling quoted. Read `verify` on the PR.
