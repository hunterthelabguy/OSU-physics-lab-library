# Executing critique, pass 4: Lab Handbook plan revision 2.3

Saved by the main session from the agent's final message, 2026-11-19.
Ordered by the owner past the cap of three ("Promote, then do a fourth
pass."). Agent: general-purpose, Opus, xhigh effort; 334,205 tokens, 169
tool uses, 7,183 s. A first try on Fable stopped at once on the account's
usage-credit limit.

Main-session note: PR #86, which the agent read as open, merged on
2026-11-19 at 19:07 UTC, after the agent's check, with #88 and #90
(main's run green). Findings B2 and 1 are read in that light in the plan's
pass-4 section.

Read: 64a8799
Base sha: 64a8799bc556546551812cb8738961cd26f8f439 (`lab-handbook-spec`, main bff3394 merged in; `git diff bff3394` on the capstone handout and Lab 3 is empty, so the base gate at plan:12 holds).
Environment: Windows 11 Enterprise 10.0.26200, Git Bash (MINGW64), Python 3.12.10, Pandoc 3.10 (Quarto's bundled copy), Quarto 1.10.18, git 2.55.0.windows.3.
Tasks executed: 4 of 4, each as written, in a throwaway worktree of 64a8799 on branch `critique-scratch-handbook-4`. No F commits.

- The full Verify, verbatim from plan block 01, ran after T1, T3 and T4 in the scratch tree. Each exited 0: 354, 362 and 366 tests.
- T2's narrower verify passed: 4 tests, then the build plus `test_downloads` and `test_quarto_site` (72 tests), with the full Verify's exports (finding 3).
- The full Verify minus the rebuild at the T2 boundary: exit 0, 358 tests. Every task boundary is green, measured.
- Every red step failed exactly as the plan predicts, T1's included (pass 3's B1 is fixed).
- gh, read-only: PR #89 `OPEN`, so D-0196's gate still fires. Main's head bff3394; run 44414519194 `success`.

## What revision 2.3 broke

**B1. The new rewrap rule produces a 111-column CLAUDE.md bullet. Low, mechanical, CONFIRMED.** plan:310 says "rewrap each changed paragraph or bullet to its own widest line before the edit". The "One Markdown source" bullet's widest line is 111 characters (CLAUDE.md:148). Applied literally, the bullet reflows to lines of 98 to 111 characters; lines over 80 in CLAUDE.md go from 12 to 18. Revision 2.2's "about 76" was right. The other targets are identical when rewrapped at 75.

**B2. The new "Not folded" rationale is false against the record. Medium, needs-ruling, CONFIRMED (gh).** plan:749 declines pass 3's unasserted-constraint nit: "a test would guard a form nobody writes". PR #86 (D-0184, owner-approved 2026-11-16, head 599b3c3) sets `status: ruled-change` on `curriculum/ph212/ph212-data-analysis-handout.md` and adds `ruled_omissions`, `ruled_additions` and `ruled_equations`.

**B3. Nit, CONFIRMED.** plan:310's "so line 21's neighbours are not touched": line 21 is in the template section; the paragraph lands about line 265. Harmless.

Checked and not broken: `DOC_TARGET` in `bad_links` (no real source link fails; external, local and `mailto:` links left alone; Quarto cross-references are Cite nodes; the widened fixture passes); T1's build-first step (241 s; red now shows `SystemExit not raised`); the re-sorted question-id pin (valid JSON, 20 keys, sorted; `REBASELINED` sorted after T3 and T4); the em-dash docstring, `HeldToLab7`'s docstring, D-0198 ruled with the reading list updated.

## Findings, ranked

1. **Medium, needs-ruling, CONFIRMED: a second `ruled-change` file is in flight, and the plan does not know it.** D-0195 (4) and T1 (plan:274-286) treat D-0169's file as the one ruled-change file. With #86's handout change applied on top of T1 as written (`probes/pr86_probe.sh`): both Word checks print `skip`, so D-0184's three declarations become dead text; `check_em_dash` passes; `test_rebaselined_files_are_pinned` fails. Whichever lands second goes red; if #86 is fixed only by adding itself to `REBASELINED`, it ships front-matter lists that violate plan:29 and D-0195 (3), and nothing asserts their absence. Owner's call: the order (T1 first with #86 rebuilt under D-0195, or #86 first with T1's D-0169 step generalised to both files), and whether `Rebaselined` asserts that no `ruled-change` file carries `ruled_omissions`, `ruled_additions` or `ruled_equations`. Agent's lean: T1 first, plus the assertion.
2. **B1. Low, mechanical, CONFIRMED.**
3. **Low, mechanical, CONFIRMED: T2's build-and-test step (plan:480) does not run as written.** T2's Verify sets only `PANDOC` (plan:330). The build then deletes `build/quarto-site` and stops on `CHROME`; `test_downloads` also needs `PDFTOTEXT`. With the full exports it passed.
4. **Low, mechanical, CONFIRMED: `bad_links` accepts generated heading identifiers, but spec 4.4 (handbook spec:254-257) says "explicit identifiers".** Reading with `render.FROM + "-auto_identifiers"` flags `[x](a#plain-heading)`, and the real tree after T4 stays clean (`probes/explicit_ids_probe.py`).
5. **Low, CONFIRMED: `DOC_TARGET`'s comment "any link aimed at another document" (plan:360) overclaims.** `a.md#x`, `../ph21x/a.md#x`, `a/#x` and a bare `a` are neither rewritten nor flagged. No source has one today.
6. **Nits.** plan:7 dates revision 2.3 2026-11-18 but quotes the owner on 2026-11-19. The reading list omits D-0199. plan:566 runs `make_handbook.py` from the repo root while the script is kept outside the repo. PLAUSIBLE: T3's and T4's commit bodies cite rulings in this repo while T1's new words say a ruled change's ruling lives in the instructor repo; name which ledger. Outside the plan: CLAUDE.md:62 says Quarto is not on PATH, but `quarto` resolves in this shell.

**This pass is NOT CLEAN.** Findings 1 to 5 each need a plan edit.

## Claims checked, all CONFIRMED at 64a8799

The line numbers the plan cites in `tools/check_unchanged.py`, `tools/check_numbers.py`, `tools/check_em_dash.py`, `.github/workflows/verify.yml` (the em-dash step runs with stdlib only), `tools/media.py`, `tools/filters/media.lua`, `site/landing.md`, D-0169's file, `docs/conversion-spec.md`, `tests/test_quarto_site.py`, `tests/test_downloads.py` and `tests/test_headings.py`. Capstone handout: 379 lines split, index 283 the Appendix B heading, each swap target once, two media paths, no U+2014, hashes match. Lab 3: 285 lines split, every asserted index holds, no U+2014. All 41 declared images match. Handbook HTML download 169,306 bytes, cap `190_000`. Lab 3's PDF: 10 pages, heading and lead-in on page 9, the two links alone on page 10, both `/URI`s present.

## Built result against intent

The checks skip D-0169's file, then the handbook, then Lab 3, each with the exact message. Flipping PH 211 Lab 1's status fails the pin. `HeldToLab7` fails on a change to either side alone and passes on both. Handbook page: one `<h1>`, the seven ids on real `h2` elements in D-0190's order, both icons keep Word's alt text. The word diff shows only the listed changes. Lab 3's page, Word, HTML and PDF hold both library addresses. Unasserted runtime changes: Lab 3's page loses its generated `#required-plot-elements` and `#linearization` anchors; the landing card text is not tested. Nothing a ruling forbids. Not delivered: D-0196's paragraph (by design) and finding 1. Scope: every commit's paths in its Files list. Dependency edges hold.

## Edits to the plan (agent's list)

1. plan:310: a stated width (76), "PH 211" kept together; drop the line-21 clause.
2. PRs section and T1: name PR #86 and the owner's ruling on finding 1; correct plan:749's rationale; add the no-lists assertion if ruled.
3. plan:480: the build and tests with the full exports.
4. plan:371: `parsed()` reads with `-auto_identifiers`; add a plain heading and `[auto](a#plain-heading)` to the fixture.
5. plan:360: narrow the comment, or widen the selector.
6. Nits: plan:7's date; D-0199 in plan:11; plan:566's run line; which ledger T3's and T4's commits cite.

## Patch folder, tripwire, scratch

Patches `0001-T1-as-written.patch` to `0004-T4-as-written.patch` and `probes/` (setup and run scripts, per-task apply scripts, and the pr86, link-target, link-form, explicit-id, Lab 3 PDF, built, held and switch probes). Tripwire printed nothing. The grep found only the noreply identity, CLAUDE.md's `%LOCALAPPDATA%` line, `env.sh`'s `$LOCALAPPDATA` and an `example.org` fixture. Worktree removed, branch deleted; no server started; two of the agent's own wait loops stopped by task id. Full Verify runs took 1,198 s, 1,299 s and 1,236 s; wall time about 2 h.
