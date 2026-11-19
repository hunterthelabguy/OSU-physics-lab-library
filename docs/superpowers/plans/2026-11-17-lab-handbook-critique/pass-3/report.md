# Executing critique, pass 3: Lab Handbook plan revision 2.2

Saved by the main session from the agent's final message, 2026-11-18.
Agent: general-purpose, Opus, high effort; 283,108 tokens, 147 tool uses,
5,789 s. Pass 3 of three under the writing-plans cap.

Read: 6846606
Base sha: 6846606accdaa7c3e34cd3eb41f6a795633fd8a7 (`lab-handbook-spec`, with main bff3394 merged in). The capstone handout and Lab 3 are unchanged since bff3394.
Environment: Windows 11 Enterprise 10.0.26200, Git Bash (git 2.55.0.windows.3), Python 3.12.10, Pandoc 3.10 (the copy bundled with Quarto), Quarto 1.10.18.
Tasks executed: 4 of 4, each as written, in a throwaway worktree of 6846606 on the branch `critique-scratch-handbook-3`. There are no F commits: nothing blocked a later task.

What ran, and where:
- The plan's full Verify ran verbatim after T1, T3 and T4, and exited 0 each time: 354, then 362, then 366 tests.
- T2's narrower verify also passed: 4 tests, then the build and `test_downloads` plus `test_quarto_site` (72 tests).
- All red steps failed as the plan says except one: T1's image-hash test (B1 below).
- D-0196 gate: `gh pr view 89` returned `OPEN` (updated 2026-11-17T21:09:06Z), so PR 1 still stops for the owner's wording.
- Main's run 44414519194 (for bff3394) is `success`, as plan line 45 says.

## What revisions 2.1 and 2.2 broke

**B1. T1's own verify cannot run its new test on a fresh tree. Low, mechanical, CONFIRMED.**
- Revision 2.2 added `tests.test_downloads.MediaDownloads` to T1's verify (plan:81). But that module's `setUpModule` (`tests/test_downloads.py:56-58`) raises "build/quarto-site is missing" when no build exists.
- So on a fresh worktree the red step shows a `setUpModule` ERROR, not the predicted "`SystemExit` not raised" (plan:203). The green step ("expected: pass", plan:271) fails the same way.
- With an empty `build/quarto-site` folder made for the probe only, `test_a_changed_image_stops_the_build` failed exactly as predicted. After implementation the full Verify passed it.
- Not blocking, because the full Verify builds first. But T1's red/green step cannot show what it claims.

**B2. The plan builds on D-0198, but D-0198 is still `proposed` and the reading list omits it. Low, CONFIRMED by reading.**
- D-0198 is `status: proposed` (`DECISIONS.md:1940`).
- T1 writes "D-0198" into CLAUDE.md (plan:308) and calls the landing-card wording "approved 2026-11-18" (plan:293).
- The header's reading list (plan:10) still says D-0188, D-0190 to D-0192 and D-0195 to D-0197; D-0198 is missing.
- Nothing gates PR 1 on promotion. D-0197 was promoted before its plan ran (e1c82ab).

Checked specifically, nothing else broke:
- **`bad_links()`** reads header and div ids from Pandoc's tree. `test_bad_links_are_found` passes, with all five bad forms found.
- **The handbook's addresses** sit on real `<h2 id=...>` elements on the built page (`probes/built_probe.py`), not only in `data-anchor-id`.
- **The `REBASELINED` pin:** flipping PH 211 Lab 1 to `ruled-change` makes `check_unchanged` print `skip`, and the pin fails (`probes/switch_probe.sh`). T3 and T4 extend the pin in sorted order.
- **`media.build`'s image hash:** all 41 declared images match their front matter (`probes/image_hashes.py`), so the build is green.
- **`handbook_body()`, shared by the T3 script and `HeldToLab7`:** `HeldToLab7` fails when only the handbook changes and when only Lab 7 changes, and passes when both change (`probes/held_probe.sh`). By construction it cannot catch a defect inside `handbook_body()` itself; only the PR's word diff can, and that is read by a person. The word diff, now run through two files, works and shows exactly the listed changes, the two media paths included.
- **The D-0169 step without its guard:** its asserts hold, and the front matter that results parses.
- **The landing card:** applied as written.
- **The PDF test:** red before the cut, green after. Chrome's PDF holds both `/URI` strings uncompressed.

## Findings, ranked

1. **B1 above. Low, mechanical, CONFIRMED.** No F commit was needed.
2. **Low, CONFIRMED (`probes/link_gap_probe.py`): `<id>#<fragment>` links with a colon or dot in the fragment are neither rewritten nor flagged.** The links tried were `a#a:q1` (question ids carry a colon) and `a#x.y`. `media.lua`'s `^([%w%-]+)#([%w%-_]+)$` (plan:452) leaves both unchanged; `bad_links()`'s `DOC_LINK` (plan:357) ignores both. Each ships as a relative link that 404s on the site. D-0190 (3) says the test "fails on an unknown id or identifier". No source has such a link today.
3. **B2 above. Low, CONFIRMED.**
4. **Low, PLAUSIBLE: drawn figures in a future `ruled-change` file come from an original nothing pins.** D-0198 (4)'s reasoning ("the word check that compares pictures skips a ruled-change file") applies to drawn figures as well. `media.build` reads them from `source_file` (`tools/media.py:101,109`). Only `check_unchanged` verifies `source_sha256`, and it now skips `ruled-change` files. No `ruled-change` file has a drawn figure today. Three converted handouts do: PH 212 designing-experiments, PH 213 hypothesis-testing and PH 213 model-building. The first ruled change to any of them would publish figures drawn from an unpinned original. This is the owner's call.
5. **Nits, CONFIRMED.**
   - **Pin order:** `tests/question-ids.json` is sorted by id. T3 appends `ph21x-lab-handbook` after `ph21x-problem-solving-strategy` (plan:598-599). Revision 2.1 fixed the same order for `HTML_CAPS` but not here.
   - **Em-dash docstring:** T1's new text says a converted file "is skipped while its status is `converted`" (plan:251). The code skips any `source_file` file whose status is not `ruled-change`, including `checked` or no status. Better: "skipped unless its status is `ruled-change`".
   - **Unasserted constraint:** the Global constraint "carries no `ruled_omissions` or `ruled_additions`" (plan:28) is asserted by nothing.
   - **`HeldToLab7` docstring:** it says "The capstone pass deletes this class" (plan:541). Once it goes, `handbook_body`, `LAB7`, `ITEMS`, `SWAPS` and `OPENING` have no consumer left.
   - **Rewrap side effects:** rewrapping CLAUDE.md's "One Markdown source" bullet splits "PH" and "211" across a line break; `docs/conversion-spec.md:21` becomes a 115-character line; "Rewrap to the file's width" names no width. The agent used each paragraph's widest line before the insertion.

## Claims checked (step 1)

All CONFIRMED at 6846606: the line numbers the plan cites in `tools/check_unchanged.py`, `tools/check_numbers.py`, `tools/check_em_dash.py`, `.github/workflows/verify.yml`, `tools/media.py`, `tools/filters/media.lua`, `site/landing.md`, the D-0169 file, the capstone handout (378 lines, 379 split; index 283 the Appendix B heading; each swap target once; icon hashes and `source_sha256` match), Lab 3 (284 lines, 285 split; the script's asserted indexes), `tests/test_headings.py`, `tests/test_quarto_site.py` and `tests/test_downloads.py`. Content: no U+2014 in Lab 3, D-0169's file or capstone lines 284-378; all 19 curriculum `.md` files are converted and none sits outside `curriculum/`; the handbook's HTML download measures 169,306 bytes, so its cap is `190_000`.

## Built result against the specs' and rulings' intent

- **The Word checks** skip D-0169's file (after T1), then the handbook (after T3), then Lab 3 (after T4), each with the exact message.
- **D-0195 (1) to (4) and D-0198 (1) to (5):** delivered. D-0198 (6) is a step for PR 4's body.
- **The handbook page:** one `<h1>`, "Lab Handbook"; the seven ids on `h2` elements in D-0190's order; both icons keep Word's alt text. Spec 4.8's alt-text requirement is now held by `HeldToLab7` together with Lab 7's word check.
- **Lab 3:** the page, Word, HTML and PDF each hold both library addresses. The PDF still puts the heading and lead-in on page 9 and the two links on page 10, for the owner under D-0198 (6).
- **What a ruling requires that no task delivers:** D-0190 (3) only partly (finding 2); D-0196's paragraph, by design.
- **What a task does that a ruling forbids:** nothing found.
- **Scope:** every path each commit touched is in that task's Files list (T1: 13 files; T2: 2; T3: 8; T4: 4).

## Ordering and atomicity

Green at the T1, T3 and T4 boundaries by the full Verify; at T2 only the narrower verify ran, so that boundary is PLAUSIBLY green. The dependency edges hold: T3 needs T1's skip and T2's module; T4 needs T2's rewrite and T3's handbook (`bad_links` would flag Lab 3's links without the handbook).

## Edits to the plan (agent's list)

1. T1 Verify and its red/green step: run `python tools/quarto_build.py` first, or note that `MediaDownloads` needs a built `build/quarto-site`. Fix the red text to match.
2. T2, `bad_links`: also flag any target matching `^[A-Za-z0-9-]+#` that `DOC_LINK` does not match in full, or widen `media.lua` and `DOC_LINK` together. Add `a#a:q1` to `test_bad_links_are_found`.
3. Header: add D-0198 to the rulings executors read. PRs section: D-0198 is promoted before PR 1 opens.
4. T3: insert the `"ph21x-lab-handbook": []` pin before the strategy's entry, keeping the file sorted.
5. T1: the em-dash docstring says "skipped unless its status is `ruled-change`".
6. T3: `HeldToLab7`'s docstring says the capstone pass deletes the class and `handbook_body()`'s constants.
7. T1: give the rewrap width as each paragraph's widest line before the edit, and keep "PH 211" together.
8. Owner's call (finding 4): pin the original's hash in `media.build` when a document has drawn figures, or record that it is not pinned.

## Patch folder and tripwire

Patches `0001-T1-as-written.patch` to `0004-T4-as-written.patch` and `probes/` (plan-block extractor, env and verify scripts, per-task apply scripts, and the image-hash, link-gap, built-page, held and switch probes). The grep for home paths, names and secrets found only the repo's noreply commit identity, CLAUDE.md's `%LOCALAPPDATA%` line and the plan's own `$LOCALAPPDATA` variable. Tripwire `git log --format=%s 6846606..HEAD | grep -Ev '^(T[0-9]+ as written|F[0-9]+: )'` printed nothing.

## Scratch and durations

Scratch worktree removed, branch deleted; no server started, no process stopped, main checkout untouched, no student-identifiable data met. Full Verify runs took 1,135 s, 1,319 s and 1,270 s; wall time about 2 h 15 min.
