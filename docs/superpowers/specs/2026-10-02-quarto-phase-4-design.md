# Phase 4 design: retire the old build, keep the templates

Status: ruled as leaned, 2026-10-02 (D-0061: "Rule D-0060, D-0061 and the
download-all calls as leaned"). Not built yet. Call 1 is the owner's to
carry out; he is considering deleting the Vercel project outright, which
meets it.
Amends the phase 4 text of `docs/quarto-migration-plan.md`, which was written
before D-0036 and D-0054 made the Quarto build and the HTML download depend
on the templates it would delete. DECISIONS.md wins over this file.

## What phase 4 is for

Production is the Quarto build on Cloudflare Pages (D-0047). The old build,
`tools/render.py --site` writing `build/site/`, now does two jobs only: CI
builds it so the old-build comparisons have something to compare against,
and the retired Vercel project still builds it from `main` with Pandoc 3.11
(D-0046) behind its redirect. Phase 4 removes the old build and everything
that exists only to serve it, without removing any guard whose subject still
exists.

## What stays, and why

| Kept | Why it stays |
|---|---|
| `tools/template.html`, `tools/template-site.html` | `tools/quarto_chrome.py` renders every page's chrome from them (D-0036), and `tools/downloads.py` renders the HTML download through `template.html` (D-0054). |
| `tools/brandheader.html`, `tools/brandfooter.html` | The templates include them. |
| `tools/render.py`, the functions the Quarto build imports | `ROOT`, `PANDOC`, `THEMES`, `BANNER_MAIN`, `BANNER_DETAIL`, `THEME_NOTE`, `run`, `body_after_front_matter`, `site_vars`, `document_extras`, `converted_documents`, `course_index_markdown` (with `lab_entry`), `how_this_was_made`, `sims`, `render_sim`, `sims_index_markdown`, `redirect_page`, `METHOD_FOOTNOTE`, and what those call. Measured from `quarto_build.py`, `quarto_chrome.py` and `downloads.py` on 2026-10-02. |
| The `quarto-only` CSS block and `QuartoOnlyCss` | The HTML download embeds `site/site.css` through `template.html` without Quarto's markup, so the block still keeps Quarto-only rules out of a second consumer. Its comments change from "the old build" to "the HTML download". |
| `tests/test_site_chrome.py` (9 tests) | It is the brand contract (D-0042); it already passes against `build/quarto-site/` (9 of 9 at handoff). |
| `test_bodies_unchanged` and `tests/fixtures/main-bodies.json` | D-0010's guard. The Quarto `<main>` matches the fixture already (D-0036 probe), so it ports with no fixture change. |
| `tools/measure_chrome.js`, single-build measurements | Scroll width, banner height, contrast and sim bar fit still need measuring; only its two-build diff mode loses its reference. |

## What goes

1. `tools/render.py`: `render()`, `render_page()`, `build_site()`,
   `LANDING_FOOTNOTE`, the `--site` mode, and file mode (call 2). What remains
   is a module of shared functions; its docstring is rewritten to say so.
2. CI (`verify.yml`): the "Install Pandoc 3.11" step, the "Site builds" step,
   `PANDOC_OLD_BUILD` on "Tests", and the separate "Chrome contract against
   the Quarto build" step, folded into "Tests" once the contract defaults to
   the Quarto build.
3. `tests/test_one_pandoc.py::test_old_build_pandoc_reads_the_same_tree`
   (D-0046 said so); `test_pandoc_is_quartos` stays.
4. `tests/test_quarto_config.py::test_ci_uses_quartos_pandoc`: its old-build
   half (the `PANDOC` on "Site builds", `PANDOC_OLD_BUILD` on "Tests", the
   tree test's name) goes; its Quarto half stays and gains "no step names a
   standalone Pandoc".
5. `tests/test_quarto_chrome.py::ChromeParity`, its three comparisons:
   `test_every_page_has_an_old_twin`, `test_body_class_carried`,
   `test_bottom_chrome_matches_old_build`. They are replaced first (call 3).
   `test_landing_footnote_not_carried` stays.
6. `tests/test_fonts.py::Embedded::test_pages_embed_the_font`: it reads
   `build/site/index.html`, whose fonts are embedded; the Quarto pages link
   `site/fonts/` (0 `@font-face` in the Quarto landing page, measured on CI's
   artifact for `aab70bd`), and `Published::test_fonts_license_and_header_logo_only`
   already pins the published fonts (call 4).
7. `tests/test_site_chrome.py`: `SITE` defaults to `build/quarto-site/`;
   `SITE_DIR` goes; the "old build has none" sentence in `pages()` goes.
8. Docs: CLAUDE.md's `[phase 4]` lines (the `PANDOC_OLD_BUILD` export, "Old
   site"), the agent reference's one-file render line and two-build
   measuring text, the docstrings that say "old templates" or "phase 4 moves
   the templates" (`quarto_chrome.py`, `quarto_build.py`, `_quarto.yml`,
   `site/site.css`), the migration plan's phase 4 section marked done with
   a pointer here, and `docs/conversion-spec.md`'s Tools note.
9. Locally, `PANDOC_OLD_BUILD` leaves the verify sequence. Uninstalling the
   standalone Pandoc 3.11 from the owner's machine is the owner's, and
   optional.

The migration plan's item "update the How this was made text, which says
the site is built with Pandoc and one build script" is already met: that
sentence is `LANDING_FOOTNOTE`, the landing page's footnote, not carried
under Quarto (D-0038) and absent from production (`test_landing_footnote_not_carried`;
0 matches in the `how-this-was-made` page of CI's artifact). Phase 4 deletes
the constant. No new visible words.

## Calls for the owner

Each with the lean, the reason, and the cost of the other way.

1. **Vercel's Git builds go off before phase 4 merges.** Lean: yes, by the
   owner in Vercel's settings. Reason: Vercel posts a commit status on every
   push to `main` (seen on `78b3066`: "Vercel success"); once `--site` is
   gone, every commit would carry a red Vercel status, and the
   `osu-physics-lab-library.vercel.app` redirect is a project routing rule
   whose behavior after a failed build was not checked. Cost of not: a red
   mark on every commit, read as a broken build by anyone who looks,
   including a successor. Whether the redirect itself then stays or goes,
   and when, stays the owner's open item; phase 4 does not need it settled.
2. **File mode goes with site mode.** Lean: delete `render.py FILE.md`.
   Reason: its job, a standalone page of one lab with no site chrome, is
   now the HTML download (D-0054), built by the Quarto build with the
   Pandoc everything else uses; file mode would be the last caller of
   Pandoc 3.11's path in the docs. Cost of keeping it: a second one-file
   renderer to maintain, documented with a Pandoc the repo no longer pins.
3. **The parity tests are replaced by direct pins before they are deleted.**
   Lean: yes, in the same PR, tests first. Reason: D-0038's untested pieces
   (the document nav with "Course index" and the "Read it ..." switch, the
   presentation note, the "Both presentations" paragraph, the "How this was
   made" footnote) are guarded today only by comparison with the old build.
   Deleting the comparison without a replacement would leave them unguarded,
   and the repo would claim a check it no longer runs. The replacement
   asserts each D-0038 piece's words occur once on every page that should
   carry it, taken from `render.py` and the templates, never retyped, so a
   dress that drops a piece fails. Rendering the expected chrome with the
   call `quarto_chrome.py` makes was considered and dropped: it would test
   the lift against itself. The body class gets one
   assertion (`site-page` or the document class on every page, because
   `site/site.css` scopes rules to `body.site-page`). Cost of a bare
   deletion: four ruled chrome pieces with no test.
4. **The font embedding test is deleted, not ported.** Lean: delete.
   Reason: what it pins (fonts as `data:` URIs in the page) is the old
   build's method; the Quarto pages link the published WOFF2 files, which
   `Published` and `FontFiles` already pin. Cost of porting: a new test
   asserting the opposite of the old one, duplicating `Published`.
5. **The templates stay where they are, under their names.** Lean: no move,
   no rename. Reason: three tools and the docs name them by path; "old" is
   a word in the docs, not in the file names, so fixing the docs is enough.
   Cost of moving them: a churned diff and every reference to update, for
   no change in behavior.
6. **`render.py` keeps its name.** Lean: keep. Reason: the module still
   renders (the course index, the method page, sims, redirects); every
   import names it. Cost of a rename: import churn across three tools and
   the tests, in a phase whose purpose is deletion.
7. **D-0046 is superseded, not edited.** Lean: a new proposed entry,
   D-0061, records phase 4 as ruled here and names what it retires;
   D-0046 gets a `corrected:` line pointing to it. Reason: the ledger is
   append-only (charter floor 7).

## Order of work (one PR)

1. Replacement pins (call 3) land green while the old build still exists,
   so they are seen to pass against the same pages the parity tests pass.
2. Delete the parity tests, the tree test, the font embedding test and the
   old-build half of the CI Pandoc test.
3. Delete the old build: `render.py`'s dead functions and modes, the CI
   steps, `SITE_DIR`.
4. Docs and comments.
5. Verify: the sequence in CLAUDE.md without `PANDOC_OLD_BUILD` and without
   `render.py --site`; the test count falls by the deleted tests and rises
   by the pins, each named in the PR body; the chrome contract runs inside
   "Tests". The deploy job is untouched, so the alias check is its own
   design (D-0060), not phase 4's.

Precondition: call 1 done by the owner, and the owner's word that phase 4
goes before or after D-0051 (both edit `verify.yml`; whichever is second
rebases).

## Declined

- Deleting the templates as the plan's text says: the Quarto chrome and the
  HTML download are built from them (D-0036, D-0054).
- Keeping the old build for comparison only: it costs a second Pandoc in CI
  and in the docs, and the comparisons it feeds are replaced by direct pins.
- Porting the chrome to Quarto partials so the templates can go: a rewrite
  of working chrome with new parity risk, for no change a reader sees.
