# Quarto migration plan (D-0033)

Written 2026-09-30 after the two spikes in `docs/quarto-spike-2026-09-30.md`.
Status: draft for the owner's review. Each phase is one PR through `verify`
(charter floor 4). Production stays on the old build and the Vercel project
(ledger 40, 47) until phase 5; phases 1 to 4 run Quarto in CI only, so
nothing a reader sees changes until the cutover.

## Principle: the tests are the contract

`tests/` already asserts the ruled quantities: logo files unaltered and
linked, the Physics top strip, the draft banner and noindex on every page,
the ruled footer, sim bodies unchanged, the sim bar, embedded fonts. The
migration keeps every one of those tests passing against the Quarto output,
or drops a test only by a ruling recorded in DECISIONS.md. "Branding is not
load-bearing" (owner, 2026-09-30) licenses simplifying the chrome; it does not
license a test silently going red. Quarto writes `build/quarto-site/`,
beside the old `build/site/`, and the chrome suite reads it through
`SITE_DIR` (corrected 2026-09-30: an earlier draft said Quarto would write
`build/site/` with no path changes; phase 1 built it beside the old build
instead).

## Phase 1: Quarto builds beside the old build

Implementation plan: `docs/superpowers/plans/2026-09-30-quarto-phase-1.md`.

- `_quarto.yml` at the repo root with an explicit `render:` list, because
  Quarto otherwise renders every Markdown file in the project (LEDGER.md,
  DECISIONS.md, `docs/`, the curriculum sources themselves). Output goes to
  `build/quarto-site/`, beside the old `build/site/`. Quarto 1.10.18 pinned
  in CI.
- One driver, `tools/quarto_build.py`, generates the wrapper pages
  (`labs/<id>/modern/index.qmd`, `faithful/index.qmd`, and the landing,
  course index, method and sims pages) from the same sources and functions
  `render.py` uses today, runs Quarto, then writes the sim copies with the
  bar, our own `robots.txt`, and the redirect stubs. Generated files are
  gitignored and never hand-edited. Today's URLs are kept.
- `questions.lua` reads `theme-name`, falling back to `theme`, so both
  builds share it unchanged in behavior.
- Theme: Quarto `default`. Never Cosmo or any theme that imports a remote
  font.

**Exit criterion (fixed 2026-09-30).** The brand tests cannot pass until
phase 2 rebuilds the chrome, so phase 1 does not gate on them. It merges
when: the old build and its full suite stay green and keep feeding
production; the Quarto build succeeds with no warning line; and a new
blocking suite, `tests/test_quarto_site.py`, passes against
`build/quarto-site/` (expected pages, noindex and `robots.txt`, one `<h1>`
per page, question numbering, sim byte identity plus the bar, no
third-party resources, document words identical to the old build). The
existing chrome suite also runs against the Quarto output in a
non-blocking CI job; its failures are phase 2's to-do list, and no test is
edited to pass.

## Phase 2: chrome rewrite

Status: done 2026-09-30 (PR #14). Implementation plan:
`docs/superpowers/plans/2026-09-30-quarto-phase-2.md`.
Rulings: D-0036 to D-0042 (ruled 2026-09-30 on the owner's chat ruling),
building on D-0029 to D-0032. D-0043 (the driver strips Quarto's search
leftovers after render) was ruled 2026-10-01.

- Fix the doubled page title (one `#` heading per page). Done in phase 1.
- Rebuild the draft banner, top strip, footer and landing hero against
  Quarto's markup, driven by the failing tests from phase 1 and by new
  parity tests for the chrome no test covered (D-0038). The chrome is lifted
  from the old templates, not rewritten (D-0036).
- Re-measure what STATE.md records (sim bar fits 1280x720, 375 px phone width
  without sideways scroll, contrast ratios) and write new numbers there.
- Exit (D-0042): the chrome suite passes against the Quarto build and runs
  in `verify`; no brand test dropped. Done: the suite passes 9 of 9 against
  both builds and is the last step of the `verify` job, and the
  non-blocking `chrome-on-quarto` job is gone.

## Phase 3: one Pandoc

Status: done 2026-10-01 (PR #15). Rulings: D-0044 to D-0046 (ruled
2026-10-01). Implementation plan:
`docs/superpowers/plans/2026-09-30-quarto-phase-3.md`.

`check_unchanged.py` reads Pandoc from `PANDOC`. CI sets it to Quarto's
bundled binary (`quarto pandoc`), so the word check and the site render use
the same Pandoc. The separate Pandoc 3.11 install step goes.

Premise corrected 2026-09-30 while planning: Quarto 1.10.18 bundles Pandoc
3.10, not 3.11, and `quarto pandoc` truncates large stdout on Windows. Plan
(draft, calls open): `docs/superpowers/plans/2026-09-30-quarto-phase-3.md`,
with D-0044 to D-0046 proposed. Under D-0046 the 3.11 install stays for the
old build until phase 4.

Amended 2026-10-01 (ruled): `PANDOC` is the bundled binary's path, found in CI
next to the resolved `quarto` executable, never the `quarto pandoc` command
(D-0045). The sentence "The separate Pandoc 3.11 install step goes" does not
hold until phase 4 (D-0046): the install stays, for the old build's "Site
builds" step and `test_old_build_pandoc_reads_the_same_tree` only, because
production is built with 3.11. Tests: `tests/test_one_pandoc.py` and
`tests/test_quarto_config.py::Version::test_ci_uses_quartos_pandoc`. The Linux
layout of Quarto's bundle, unverified when this was planned, held at the PR's
first CI run: exactly one `pandoc` under the resolved `quarto` executable's
`tools` folder, reporting 3.10. No tool's code changed, and no page changed: the old build is byte-identical under both
Pandocs and the word check reads 989 words identical (bold on 943) under both,
so nothing was re-measured.

## Phase 4: retire the old build

Runs after phase 5's cutover, not before: until then the old build is what
production serves.

Delete the page-assembly half of `tools/render.py`, `template.html`,
`template-site.html` and the brand partials once nothing imports them. Also
delete the standalone Pandoc 3.11 install in `verify.yml`, `PANDOC_OLD_BUILD`,
and `test_old_build_pandoc_reads_the_same_tree` (D-0046).
Switch the chrome suite to `build/quarto-site/`, make the old build's
job go away, and update CLAUDE.md's Build section and the "How this was made" text, which
says the site is built "with Pandoc and one build script".

## Phase 5: new host (D-0034)

GitHub Actions builds, then uploads `build/site/` to Cloudflare. Needs a
deploy-scoped Cloudflare API token, which the owner creates and stores as a
repo secret; Claude never handles it. Old Vercel URL gets a redirect or a
notice before it is switched off.

Planned 2026-10-01 (draft, calls open):
`docs/superpowers/plans/2026-10-01-quarto-phase-5.md`, with D-0047 to D-0049
proposed and the owner's side in `docs/quarto-phase-5-owner-checklist.md`.
Corrections to the text above: the folder is `build/quarto-site/`, not
`build/site/` (the old build, until phase 4); Cloudflare Pages needs a
`404.html` or answers unknown paths with the landing page; and the Vercel
redirect must be in place before phase 4 merges.

## Later, enabled by the move

Search, sidebar navigation, listing pages for courses and sims, Word
downloads via `format-links` (shown working in spike 2), and standalone HTML
downloads via a second small render (also shown working).

## Watch items

- **"variable used before declaration."** Printed once, by the first render
  of the standalone-download project in spike 2. Three later renders of the
  same file, one with the project cache cleared, printed nothing, and the
  output was the same size (127,512 bytes) with and without the warning.
  Most likely a one-time cache-warming message from Quarto's own tooling;
  tracing it further means reading Quarto's install folder, which is outside
  the working boundary. Mitigation instead of a trace: a CI step scans the
  Quarto render log and fails on any warning line, so if it ever recurs it surfaces with a full log at
  the moment it matters.
- Page weight falls: shared `site_libs/` and fonts are fetched once per
  visit instead of embedded in every page (today about 380 KB per page).
  Measure before and after.
- Quarto releases often. Upgrade the pinned version on purpose, in its own
  PR, never as a side effect.
