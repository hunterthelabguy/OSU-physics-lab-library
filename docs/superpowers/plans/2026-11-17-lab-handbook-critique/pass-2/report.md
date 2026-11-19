# Executing critique, pass 2: Lab Handbook plan

Saved by the main session from the agent's final message, 2026-11-18. Opus,
xhigh effort; the first try on Fable failed on the usage-credit limit.

Read: 21d2f59 (plan revision 2). Base: 21d2f59, which is `lab-handbook-spec` with main at bff3394 merged in at d89a4b3. The branch head, e1c82ab, differs only in `DECISIONS.md` (D-0197 promoted).
Environment: Windows 11 Enterprise 10.0.26200, Git Bash (git 2.55.0.windows.3), Python 3.12.10, Pandoc 3.10 (the copy bundled with Quarto), Quarto 1.10.18.
Tasks executed: 4 of 4. Each was executed verbatim in a throwaway worktree of 21d2f59. I made no F commits. Two plan steps failed, but neither blocked a later task: T3's word-diff command, and T1's guard path when it is run from outside a sibling folder. T1's D-0169 step was skipped, because the plan's own rule says to skip it when the guard prints anything.

Each full Verify ran verbatim and passed: after T1 (353 tests), after T3 (360) and after T4 (363). T2's own verify also passed (4 tests, then the build and `test_downloads` plus `test_quarto_site`, 71 tests).

D-0196 gate: `gh pr view 89 --json state` returned `OPEN`, last updated 2026-11-17T21:09:06Z. The gate therefore fires today, so PR 1 stops for the owner's wording.

## What the revision broke

**B1. D-0195 (4)'s first build item is not delivered today, and the plan's own Global constraint is false after T1. Medium, needs-ruling, CONFIRMED.**
- The rule: D-0195 (`DECISIONS.md:1911`) requires dropping D-0169's `ruled_omissions` and `ruled_additions`. The plan's constraint (plan line 25) says a `ruled-change` file "carries no `ruled_omissions` or `ruled_additions`".
- What the plan does: T1 (plan line 226) makes the drop conditional on `git -C ../OSU-physics-lab-library status --short -- <file>`.
- What the guard printed against the real main checkout: ` M curriculum/ph211/ph211-describing-an-experiment-handout.md`. Per the plan's rule I skipped the step, so after T1 the file is `ruled-change` and still holds both lists. Nothing tracks the gap.
- What that uncommitted work is:
  - The main checkout is on branch `problem-solving-strategy`. That branch last committed the file at c4be651 (2026-10-08), which is before D-0169.
  - The working copy's mtime is 2026-11-07.
  - Its hunks are at body lines 136 to 144, outside the front-matter lists.
- The guard protects nothing. An edit in this worktree cannot touch that checkout's working tree, and the other session's hunks would not conflict with lines 12 to 66.
- The relative path only resolves from a sibling folder. From the scratch tree it printed `fatal: cannot change to '../OSU-physics-lab-library'` (exit 128). From any `.superpowers/sdd/<name>` worktree it fails the same way. Either error "prints anything", so the step is skipped for the wrong reason.
- The numbering spec (line 93) asked the build to coordinate with the other session first; the plan turned that into a silent skip.
- The plan's script itself works: run on a copy, its asserts held and the resulting front matter parses.

**B2. D-0191's premise is false after D-0197, and nothing replaces it. Low-medium, needs-ruling, CONFIRMED by reading.**
- Both D-0191's rationale (`DECISIONS.md:1870`) and handbook spec lines 295 to 296 say "every copy is checked against a Word original, so none can drift".
- After T3 the handbook is `ruled-change` from birth and both checks skip it, while Labs 4 to 7 stay `converted`. The handbook can now drift from those copies with no check failing.
- T1's CLAUDE.md insertion (plan line 255) records the exception but not D-0191's operative rule, which is that a change reaches every copy in the same PR.

**B3. A required test is dropped without a ruling. Low, mechanical, CONFIRMED.**
- D-0195's test field (`DECISIONS.md:1915`) and numbering spec 4.6 (line 105) require "the pin test still fails on a reordered `ruled-change` file".
- No task delivers it. The self-review (plan line 594) maps "item 6" to T1 as a whole.
- `probes/pin_probe.py` shows the behaviour holds: the pin ignores `status`, so a swapped copy of Lab 6 fails it. The behaviour is untested.

**B4. D-0197 (1)'s word diff cannot be produced as written. Low, mechanical, CONFIRMED.**
- The plan's command (line 488) fails on Git for Windows: `error: Could not access '/proc/256/fd/63'`, exit 1. `git diff --no-index` cannot read process substitution there.
- Run through two files instead, the diff shows the listed changes plus two image-path rewrites (`ph211-capstone-handout-media/` to `ph21x-lab-handbook-media/`). Those are missing from the plan's "What changes" list (line 487) and from D-0197 (1)'s list, so "it must show only the changes listed above" is false.

**B5. Pass-1 finding 7 is marked "carried" (line 607) but only half carried. Low, CONFIRMED.**
- The HTML download is now tested.
- The PDF `/URI` test that pass 1 proposed is declined in a test comment (line 554), not by a ruling, although D-0190 (2) names the PDF.
- Measured: the PDF holds both addresses.

**B6. A stale premise. Note, CONFIRMED.**
- Plan line 42 says main's run failed on 2026-11-17. The failing run is 43979536449 (2026-11-16, step "Hand the tested folder to deploy").
- Main's latest run, 44414519194 for bff3394, passed both verify and deploy. PR 4's "if main's deploy is still failing" condition does not hold today.

The other pass-1 findings are carried as recorded:
- 4: the cap factor of 1.10 is used.
- 9: line numbers are right.
- 11: there is one address list, through `test_lab_handbook.ADDRESSES`.
- 3: the CLAUDE.md exception is added, but see B2.
- 6: still true (finding 9 below).
- 12: handled by the D-0196 gate.

## Findings (ranked)

1. **Medium, needs-ruling, CONFIRMED. `status: ruled-change` is an unguarded off switch for both Word checks.**
   - `probes/switch_probe.py` used a copy of PH 211 Lab 1 with one body word changed. As `converted`, `check_unchanged` fails (exit 1). With only the status line changed, both checks print `skip` and exit 0.
   - Nothing names which files are re-baselined, and CI stays green. A conversion PR can flip the line with no other trace.
   - Lean: pin the set in a test, with the ruling for each file, as `tests/question-ids.json` pins questions. Flipping a file would then edit a test in the diff.

2. **Low, mechanical, CONFIRMED. The new `tests/test_check_em_dash.py` duplicates `tests/test_question_ids.py:85-104` (class EmDashScan).**
   - `test_repository_is_clean` is the same test as `test_published_sources_have_none`, and the converted-file case repeats D-0103's test.
   - `.github/workflows/verify.yml:35-36` tells readers the scan's fixture test lives in `test_question_ids.py`.
   - Fix: add one test, `test_ruled_change_is_scanned`, to that class and drop the new file.

3. **Low, mechanical, CONFIRMED. The link validator and the rewriter disagree.**
   - `probes/link_forms.py` found three link forms that `media.lua` rewrites to a library address but `bad_links()` never sees:
     - an uppercase id (`PH21X-lab-handbook#...`);
     - a link with a title;
     - the angle-bracket form `<id#ident>`.
   - A wrong id in any of these forms passes the test and ships a broken link. No source uses these forms today. The patterns are at plan lines 301 and 359; the Lua pattern is `^([%w%-]+)#`.

4. **Low, CONFIRMED. Image provenance in a `ruled-change` file is checked by nothing.**
   - `tools/media.py:103-107` copies images without hashing them; only `files:` entries are hashed (lines 117 to 123). The word check that compared pictures is now skipped for these files.
   - So the handbook's two `images:` sha256 values, and those in Lab 3 and Lab 6, are front-matter claims that nothing verifies.
   - Spec 4.8's "icons keep Word's alt text" is also asserted by nothing after T3. The build does keep both alt texts.

5. **Low, mechanical, CONFIRMED. The tools' own usage text is not amended.**
   - `tools/check_unchanged.py:65-66` still reads "Differences are allowed only when declared in front matter and ruled in a ledger".
   - The `tools/check_numbers.py` docstring does not mention the skip.
   - In `verify.yml`, the em-dash step comment (35-36) and the "Content unchanged" step comment are now incomplete.
   - T1 amends only CLAUDE.md and `docs/conversion-spec.md`.

6. **Low, CONFIRMED. The D-0196 gate fires today (#89 OPEN), and the plan gives that work no home.**
   - The Files table has no row for `site/how-this-site-works.md`, so an executor would edit outside it.
   - PLAUSIBLE, owner's call: `site/landing.md:25-26` ("how it is checked against the original") is covered by neither D-0196 nor #89, whose diff touches only the how-this-site-works page.

7. **Low, mechanical, CONFIRMED. The red-step text at plan line 176 is wrong.**
   - `check_unchanged`'s skip test errors with `FileNotFoundError` on `missing.docx`, not with an `AttributeError` for `SKIP`. The `AttributeError` comes only from `test_status_forms`.
   - `test_converted_is_still_checked` passes before the change, so it is a guard, not a red test.

8. **Low, CONFIRMED. A third copy of an existing helper.** `converted_sources()` (plan line 305) duplicates `tests/test_quarto_site.py:30-35` (`converted()`), and `render.converted_documents()` does the same job.

9. **Low, CONFIRMED in the build. Lab 3's PDF still splits the appendix.** The PDF has 10 pages. The appendix heading and the lead-in end page 9, and the two links stand alone on page 10. This is pass-1 finding 6, still held for the owner.

10. **Nits, CONFIRMED.**
    - CLAUDE.md:141 is left at about 150 characters, because the insertion is not rewrapped.
    - "At the end of" a test file must mean before its `if __name__` guard.
    - `HTML_CAPS` is sorted by id, so "after the strategy's entry" breaks the order; it is also written in the `190_000` form.
    - Self-review line 599 says the capstone "has 379 lines". `wc -l` gives 378; 379 is the split count. The same off-by-one applies to Lab 3 (284 against 285).
    - The new `media.lua` comment paragraph needs a `--` separator line.

## Claims checked (step 1)

All of these are CONFIRMED at 21d2f59.

**Line numbers and file shapes**
- `check_unchanged.py`: `FROM` is at line 112 and `main` at 1019.
- `check_numbers.py`: `import zipfile` is at line 41 and `main` at 243.
- `check_em_dash.py`: the docstring is lines 7 to 10. The text to replace spans three lines, so a literal replace needs a rewrap.
- `media.lua`: the comment is lines 28 to 30 and `Link` is lines 129 to 135.
- `test_quarto_site.py:22` is `import render`, and the tests folder is on `sys.path` at line 19.
- `test_downloads.py:179` is `MarkdownAndWord`, with its helper method at 182. `HTML_CAPS` uses the factor 1.10 (line 435).
- `question-ids.json`: the last entry is at line 234.
- Capstone handout: Appendix B is at 284, the lead-in at 286 and the list at 288 to 294; the swaps' target lines occur once each.
- Lab 3: lines 11, 242, 244, 246 to 249 and 251 are as the script asserts.
- D-0169's file: lines 11, 12, 41 and 67 are as the plan says.
- `test_headings`: Lab 3's skips are at 29, 232 and 251, so 29 and 232 remain after the cut.

**Content claims**
- There is no U+2014 in Lab 3, in D-0169's file, or in capstone lines 284 to 378.
- The icon hashes and `source_sha256` match Lab 7's front matter.
- No source has an `<id>#<ident>` link today.
- `media.lua` runs at `pre-ast` (`tools/quarto_build.py:128`).
- `render.py:135` requires `source_file`.
- The course-index test covers the handbook automatically, through `render.course_wide`.
- The capstone handout and Lab 3 are unchanged since bff3394.
- The `PDFTOTEXT` path in the Verify exists.

**Stale**
- Main's run status (B6).

## Built result against the specs' intent (after T4)

- **The Word checks on every file, before T1 and after T4.**
  - The 16 `converted` files give identical lines from both checks.
  - D-0169's file and Lab 3 change from `ok` to `skip ... (ruled-change: its own Markdown is the baseline, D-0195)`, and the handbook adds a skip line. The message is exactly the plan's.
- **The em-dash scan.** With an em dash injected into every curriculum file, the scan reports exactly the three `ruled-change` files. The real repository scans clean.
- **The handbook page.**
  - One `<h1>`, "Lab Handbook".
  - The seven `h2` ids are in D-0190's order, and all seven contents links are present.
  - Both icons keep Word's alt text.
- **The handbook downloads.**
  - Markdown: 7,899 bytes, the source byte for byte.
  - Word: 16,306 bytes, with 7 internal links that match 7 bookmarks.
  - HTML: 169,306 bytes against a cap of 190,000, with the 7 links and 7 ids.
  - PDF: 111,844 bytes, with 8 `/Dest` entries.
- **The course index.** Under "For every course" it lists "Lab Handbook" and then the problem-solving strategy.
- **Lab 3.**
  - The page, the Word file, the HTML download and the PDF (`/URI`) each hold both library addresses.
  - The Markdown download keeps the source form, as declared.
  - The HTML download shrank from 282,263 to 279,213 bytes.
- **The handbook's body against capstone lines 284 to 378.** It differs only by D-0197 (1)'s changes plus the two media paths (B4).
- **What no task delivers:** B1, B3, and B2's same-PR rule.
- **What a task does that a ruling forbids:** nothing found.

## Ordering and atomicity

- T1 and T2 touch disjoint files.
- T3 needs T1. Without the skip, the base `check_unchanged` gives the handbook 12 problems; the first is `original 'Capstone – Putting' -> converted 'Lab Handbook Every lab ...'`.
- T3 needs T2, because `test_quarto_site` imports `test_lab_handbook`.
- T4 needs:
  - T1, because the cut fails the word check;
  - T2, because without the rewrite the red step's link tests fail;
  - T3, because without the handbook, `bad_links` would flag Lab 3's links.
- The tree was green at the T1, T3 and T4 boundaries, by the full Verify. At T2 only the plan's narrower verify ran; the boundary is PLAUSIBLY green.

## Edits to the plan

1. T1, the D-0169 step: get a ruling.
   - (a) Drop the lists regardless; the other session's hunks are at body lines 136 to 144 of a pre-D-0169 version.
   - (b) If a guard stays, read the main checkout's path from `git worktree list --porcelain` (its first entry), tell a git error apart from a dirty file, and write a tracked follow-up so D-0195 (4) still gets done.
2. T1: add D-0195's pin test for a reordered `ruled-change` file to `tests/test_question_ids.py` (the shape of `probes/pin_probe.py`).
3. T1: drop `tests/test_check_em_dash.py`. Add `test_ruled_change_is_scanned` to `EmDashScan` and fix the Files table row.
4. T1: correct the red-step text (finding 7).
5. T1: amend the docstrings of `check_unchanged.py` (lines 63 to 75) and `check_numbers.py`, and both comments in `verify.yml`.
6. T1, needs-ruling: pin the set of re-baselined files (finding 1).
7. T2: make `bad_links` read link targets from Pandoc's syntax tree and apply `media.lua`'s pattern, or narrow the Lua pattern to `LINK`'s.
8. T2: reuse `test_quarto_site.converted()` instead of adding a third helper.
9. T3: produce the word diff through two files outside the repo, then run `git diff --no-index --word-diff a.md b.md`. Add the media-path rewrite to "What changes" (and to D-0197 (1)'s list, if the owner wants the ledger exact).
10. T3, needs-ruling (D-0191): either a test that holds the handbook's sections equal to Lab 7's lines 296 to 378 under the script's swaps until the capstone pass, or a ruling that drift is caught by review only.
11. T3: put the `HTML_CAPS` entry before the strategy's, written as `190_000`.
12. T4: assert the PDF's `/URI` links, or record the decline as a ruling.
13. PRs section:
    - Update main's run status: green at bff3394, run 44414519194.
    - Say that the D-0196 gate fires today.
    - Add a Files row for `site/how-this-site-works.md` in PR 1.
14. Owner's calls: the `site/landing.md:25-26` card (finding 6), and whether `media.build` should hash images too (finding 4).
15. Nits (finding 10).

## Patch folder and tripwire

- Patch folder: `docs/superpowers/plans/2026-11-17-lab-handbook-critique/pass-2/`.
- Patches: `0001-T1-as-written.patch` to `0004-T4-as-written.patch`.
- `probes/` holds `extract.py` (reads the plan's code blocks at 21d2f59); the `apply_t*` and `write_*` scripts that applied each block; `checks.sh`, `verify.sh`, `t2_step.sh` and `build.sh`; and the probes `built_probe.py`, `em_dash_probe.py`, `pin_probe.py`, `switch_probe.py` and `link_forms.py`.
- The probes hold no home paths, names or secrets. The patch headers carry the repo's commit identity, the noreply address, as pass 1's did.
- Tripwire: `git log --format=%s 21d2f59..HEAD | grep -Ev '^(T[0-9]+ as written|F[0-9]+: )'` printed nothing (grep exit 1). All four subjects are "T<n> as written".

## Scratch artefacts left

- The scratch worktree is removed and branch `critique-scratch-handbook-2` is deleted. `lib-strip` is unchanged apart from the untracked pass-2 folder.
- Left in the session scratchpad (not durable): check outputs and Verify logs, the plan's scripts as written, the word-diff inputs, the D-0169 script run on a copy, the base `check_unchanged`.
- No server was started and no process was stopped. No student-identifiable data was met. The main checkout was only read (`status`, `log`, `diff` hunk headers).

## Durations (cost log)

| Step | Seconds |
|---|---|
| Baseline: both checks, 19 files, at 21d2f59 | 67 |
| T1 red, 3 test modules (78 tests) | 148 |
| T1 green, same | 148 |
| T1 full Verify (353 tests; tests 968 s) | 1,288 |
| T2 red and green | about 3 |
| T2 build, then `test_downloads` and `test_quarto_site` (71 tests) | 899 |
| T3 build for the HTML measure | 254 |
| T3 full Verify (360 tests; tests 958 s) | 1,319 |
| T4 full Verify (363 tests; tests 958 s) | 1,282 |
| After-T4 checks | about 67 |

Wall time about 2 h; 161 tool uses, 314,317 tokens (from the harness).
