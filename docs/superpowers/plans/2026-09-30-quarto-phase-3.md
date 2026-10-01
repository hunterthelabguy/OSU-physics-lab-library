# Quarto Migration Phase 3 Plan: one Pandoc

Status: draft for the owner, 2026-09-30. Nothing built. The calls at the end
need a ruling before Task 1; the ledger entries they produce are appended to
`DECISIONS.md` as proposed (D-0044 to D-0046).

**Spec:** `docs/quarto-migration-plan.md`, phase 3: "`check_unchanged.py`
reads Pandoc from `PANDOC`. CI sets it to Quarto's bundled binary (`quarto
pandoc`), so the word check and the site render use the same Pandoc. The
separate Pandoc 3.11 install step goes."

Ledger: D-0033, D-0044, D-0045, D-0046 (proposed); binds LEDGER 20, 39, 49, 53

## The premise, checked against the record

The phase 3 text assumes swapping in Quarto's Pandoc is a version-neutral
move. It is not: **Quarto 1.10.18 bundles Pandoc 3.10, not 3.11.**
`quarto --version` prints 1.10.18 and `quarto pandoc --version` prints
`pandoc 3.10`. The standalone install prints `pandoc 3.11`. So today the
Quarto pages' bodies are already rendered by 3.10, while the word check, the
old build (production), the chrome lift and the tests use 3.11.

Probes, 2026-09-30, Windows, Quarto 1.10.18, reached through a scratchpad
shim that rewrites `PANDOC` calls to `quarto pandoc` (no repo file changed;
the builds were restored with 3.11 after, and the full verify sequence ran
green: em-dash scan clean, word check ok, suite OK, chrome contract OK):

1. **Word check, same result.** `check_unchanged.py` on the one converted
   file prints the same line under both: 989 words identical, bold identical
   on 943. The handout's syntax tree from `-t json` is equal under both
   (blocks and meta; both report pandoc-api-version 1.23.1.2).
2. **Old build, byte-identical.** `render.py --site` under 3.10 equals the
   3.11 build on all 9 files.
3. **`quarto pandoc` truncates large stdout.** A standalone,
   `--embed-resources` render of the logo returned 178,569 bytes on stdout,
   the same in three runs, where the same command with `-o` wrote 243,174.
   The standalone 3.11 binary gives 243,083 bytes either way. Through
   that route the Quarto build's chrome lift cut the logo's data URI out of
   five pages, and `tests/test_quarto_dress.py::OldChrome::test_document_page`
   failed (88 of 89). Not probed on Linux; not traced (Quarto's install
   folder is outside the boundary).
4. **Quarto build, byte-identical when the output goes to a file.** With
   every captured call rerouted through `-o` and a temp file, the Quarto
   build under 3.10 equals the 3.11 build on all 29 files, and the suite
   passes 89 of 89.
5. **Cost of the wrapper.** One word check: 1.0 s direct, 1.5 s through
   `quarto pandoc`. Old site build: 6.4 s against 10.4 s.

Two consequences. First, "CI sets it to `quarto pandoc`" cannot be done
literally: the tools call `[PANDOC, ...]` as one executable, and the
command form needs code at seven call sites (five in tools, two in
tests) and loses output (probe 3).
The tools should get the bundled binary's path instead (call 3). Second,
production builds on Vercel download Pandoc 3.11 by a project setting
(CLAUDE.md, Deploy). Removing 3.11 from CI entirely would make the "Site
builds" step verify the production pages with a Pandoc production does not
use. Today that difference is zero bytes (probe 2), but nothing would keep
it zero (call 1).

## Plan, assuming the leans below are ruled

Failing tests first. Each task is one commit on a branch; the phase is one PR
through `verify`, squash merge, then `git branch -D`.

**Task 1: red.** New file `tests/test_one_pandoc.py`:
- `test_pandoc_is_quartos`: the first line of `"$PANDOC" --version` equals
  the first line of `"$QUARTO" pandoc --version`. Fails today, locally and in
  CI (3.11 against 3.10). A missing `PANDOC` or `QUARTO` is a failure, never a
  skip (LEDGER 53 by analogy).
- `test_old_build_pandoc_reads_the_same_tree` (call 2): for every converted
  file (the CI rule: front matter naming `source_file`), the `-t json` blocks
  and meta from `PANDOC` equal those from `PANDOC_OLD_BUILD`. Green from
  birth (probe 1); it is a guard for the window until phase 4, and fails when
  `PANDOC_OLD_BUILD` is unset.

New test in `tests/test_quarto_config.py::Version`:
- `test_ci_uses_quartos_pandoc`: `verify.yml` exports `PANDOC` from the
  Quarto install before the "Content unchanged" step, and the standalone
  Pandoc is named only by the "Site builds" step and the tree test. Fails
  today.

**Task 2: green.** `.github/workflows/verify.yml`:
- A step after "Install Quarto 1.10.18" finds the bundled binary next to the
  `quarto` executable, prints its `--version`, fails if it is missing, and
  writes `PANDOC=<path>` to `$GITHUB_ENV`. The Linux layout of the bundle is
  not verified from this machine; the PR's first CI run is the probe, and
  Task 1's version test is the check.
- "Install Pandoc 3.11" stays, renamed to say it serves the old build until
  phase 4. "Site builds" and the tree test get `PANDOC_OLD_BUILD` (and "Site
  builds" its `PANDOC`) set to that install.
- No tool's code changes. `check_unchanged.py`, `render.py`,
  `quarto_chrome.py` and the tests already read `PANDOC`.

**Task 3: docs.** CLAUDE.md: the Verify line and the Build bullets say which
Pandoc each step uses and how to set both variables locally; add probe 3 to
the Quarto lessons ("never route `PANDOC` through `quarto pandoc`").
`docs/quarto-migration-plan.md`: phase 3 marked done with the amendment
(D-0046 moves the 3.11 removal to phase 4); phase 4 gains "delete the 3.11
install and `PANDOC_OLD_BUILD`". `docs/conversion-spec.md`, Tools: one dated
line added under the 2026-09-19 line, which stays. STATE.md Focus.

**Task 4: verify and land.** The full sequence locally with the new
variables, then the PR. No re-measurement: no reader-visible change, and
probes 2 and 4 show both builds byte-identical, so STATE.md's weights and
measurements stand.

## Numbered calls for the owner

1. **Which Pandoc the old build uses until phase 4 retires it.** Lean:
   keep the standalone 3.11 for the "Site builds" step only (D-0046); all
   else moves to Quarto's 3.10. Reason: CI keeps verifying the production
   pages with production's Pandoc, and the word check reads with the Pandoc
   the Quarto pages render with, which is the point of phase 3. Cost of the
   alternatives: (a) remove 3.11 now, as the plan says: CI verifies a
   toolchain production does not run, zero bytes apart today and unguarded
   after; (b) the owner changes the Vercel build command to Pandoc 3.10:
   a production setting change on a host being retired, and the 3.10
   download URL is not verified from here; (c) defer phase 3 into phase 4:
   the word check keeps reading with a different Pandoc than the Quarto
   pages for two more phases.
2. **The temporary tree-agreement test** (Task 1, second test). Lean: yes.
   Reason: under call 1's lean, production renders with 3.11 while the word
   check reads with 3.10; this test is what keeps "the check covers what
   production shows" true. Cost of the alternative: rely on probe 1, a single
   observation, for the whole window to the cutover. Cost of the test: one
   more variable in the local verify until phase 4.
3. **How the tools reach Quarto's Pandoc** (D-0045). Lean: `PANDOC` is the
   bundled binary's path; no code change. Reason: probe 3 (truncated stdout)
   and probe 5 (half a second a call). Cost of the alternative, a command in
   `PANDOC`: code at seven call sites, every captured call routed through
   a temp file, and one forgotten `-o` silently cuts output.
4. **How CI finds the binary.** Lean: derive it from the resolved `quarto`
   executable and fail loudly if absent. Reason: it follows the Quarto pin
   with no second literal. Cost of the alternative, a hardcoded path: one
   more thing to edit at each Quarto upgrade. Either way the Linux path is
   unverified until the first CI run.
5. **The local Windows path.** The bundled `pandoc.exe` is inside Quarto's
   install folder, outside `src`, where I do not look. Lean: you paste the
   path once (for example from `where.exe` or a directory listing you run),
   and I put it in CLAUDE.md. Cost of the alternative, a ruled one-folder
   exception to the boundary: a precedent for reading the install folder.
6. **LEDGER 20 and the conversion spec name Pandoc 3.11.** Lean: D-0044
   amends LEDGER 20 (frozen, not edited); the spec gets an additive dated
   line, its 2026-09-19 line kept. Cost of the alternative, editing the
   spec line: it erases the record of what the first conversion was checked
   with.
7. **What the version test compares against.** Lean: `quarto pandoc
   --version`, not a literal "3.10". Reason: a Quarto upgrade then moves
   Pandoc with no second pin, and the test still fails if `PANDOC` points at
   anything else. Cost of the alternative: a literal shows the version in the
   repo but must be edited in lockstep with the Quarto pin.

## Declined

- `quarto pandoc` as the value of `PANDOC` (probe 3; D-0045's alternative).
- A standalone Pandoc 3.10 install to match Quarto: a second copy that drifts
  at every Quarto upgrade.
- Tracing the stdout truncation into Quarto or Deno: outside the boundary,
  and the binary path avoids it.
- Upgrading Quarto to reach Pandoc 3.11: upgrades go in their own PR by rule,
  and which release bundles which Pandoc is not known from here.
- A Pandoc version check inside `tools/quarto_build.py` beside the Quarto
  check: the test already gates CI; a second guard adds code for no new case.
- Re-measuring chrome, print or weights: no page changes (probes 2 and 4).
- Any change to the Vercel project, unless call 1 rules (b).
