# OSU-physics-lab-library: agent runbook

Loaded every session, so it holds only what every session needs. Read the
named section of `docs/agent-reference.md` before the task it covers:
previewing or measuring a page, editing CSS (Widths), deploy or the
Cloudflare and Vercel projects, sims, and Quarto internals. Lines tagged
[phase 4] go when phase 4 deletes the old build.

## Shipping contract (read by /handoff)

- **Verify:** `python tools/check_unchanged.py <converted .md files>` with
  `PANDOC` set to the Pandoc bundled with Quarto (locally
  `C:\Program Files\Quarto\bin\tools\pandoc.exe`; D-0044), plus the
  no-em-dash scan outside `originals/`. CI job `verify` runs both on every
  push to main and every PR, then the builds and the tests. It checks words
  only, not structure; review structure by parse-tree block counts. Manual
  before any commit: no student-identifiable data. Which Pandoc each step
  uses, and the variables to export locally, are under Build, "Which
  Pandoc".
- **Landing rule:** code and converted content land via PR with green
  `verify` (charter floor 4), squash merge. Ledger and spec-only commits may
  land direct on `main`. Merging on GitHub stamps the account's primary email
  as merge author, which the owner accepts (ledger 36).
- **Living plan:** `DECISIONS.md` from 2026-09-21, under the decision
  ledger spec (`../OSU-lab-ops/docs/decision-ledger-spec.md`); this repo is
  its pilot. Agents append `proposed` entries only; the owner promotes in
  chat. `DECLINED.md` holds full declines and is not loaded by default.
  `STATE.md` is the one-screen handoff. `LEDGER.md` is frozen history:
  never appended to, still binding where not amended. The spec's validator
  does not exist; `tests/test_brand.py` asserts the ruled quantities.
- **Commit trailer:** none. Identity `hunterthelabguy` with the noreply email.
- **Remote:** `git@github-hunterthelabguy:hunterthelabguy/OSU-physics-lab-library.git`

## Build

- Production is the Quarto build (D-0033), deployed to Cloudflare Pages
  (reference: Deploy). Phases 2, 3 and 5 of `docs/quarto-migration-plan.md`
  are done; phase 4 is next.
- Which Pandoc (D-0044 to D-0046). Export before the verify sequence:
  `QUARTO="/c/Program Files/Quarto/bin/quarto.exe"`,
  `PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"`,
  `PANDOC_OLD_BUILD="$LOCALAPPDATA/Pandoc/pandoc.exe"` [phase 4], and for
  the downloads `CHROME` and `PDFTOTEXT` (below). `PANDOC` is Quarto's
  bundled 3.10; the word check, the Quarto build, the chrome lift and the
  tests all read with it. Never set `PANDOC` to the `quarto pandoc`
  command: its stdout truncates large output on Windows (D-0045). A
  missing tool fails the tests, never skips.
- Quarto site: `python tools/quarto_build.py` writes `build/quarto-site/`
  (Quarto 1.10.18 at `C:\Program Files\Quarto\bin\quarto.exe`, not on
  PATH). Generated pages (`/index.qmd`, `/courses/`, `/how-this-was-made/`,
  `/labs/`, `/sims/index.qmd`) are gitignored and rebuilt every run; never
  edit them. Its warning gate fails on any Quarto or Pandoc warning.
- Old site [phase 4]: `PANDOC="$PANDOC_OLD_BUILD" python tools/render.py --site`
  writes `build/site/`, which the tests also need. Pandoc 3.11 on that
  command only, because the retired Vercel project still builds it (D-0046).
  Rebuild it before running the suite after any template change: the parity
  tests compare against it.
- Downloads (D-0052 to D-0054): `tools/downloads.py`, run at the end of
  `tools/quarto_build.py`, writes `labs/<id>/<id>.md` (the source, byte for
  byte), `.docx`, `.html` and `.pdf`, all from modern, each with the draft
  banner and "Department of Physics, Oregon State University" in place of
  the logo. The HTML is a plain Pandoc render with no site chrome; the PDF
  is the built modern page printed by Chrome with the `@page` rules. Word's
  page header (the draft notice), footer, Letter page and question styles
  come from the committed `tools/reference.docx` (D-0057); rerun
  `tools/make_reference_docx.py` when one of those, `BANNER_MAIN` or the
  Pandoc version changes. Pandoc's `custom-style` reaches a Div's
  paragraphs, never its list items, so a block holding a list cannot be
  given a Word box that way (probe, 2026-10-01). The tests read the Word
  file's XML; only the owner, in Word, checks what it shows. The PDF
  needs `CHROME` (locally
  `/c/Program Files/Google/Chrome/Application/chrome.exe`; in CI the
  runner's `google-chrome`, the default); the tests need `PDFTOTEXT`
  (locally poppler's from winget, the path in
  `docs/superpowers/plans/2026-10-01-downloads-tasks.md`; in CI
  `poppler-utils`). Missing either is an error. When a lab is added,
  remeasure the HTML cap in `tests/test_downloads.py`.
- Chrome (D-0036): every Quarto page is dressed with the old templates'
  header and footer by `tools/quarto_chrome.py`. Never hand-edit the chrome
  in a Quarto page, and never copy the templates into a second file. Every
  Quarto-specific rule in `site/site.css` sits between its
  `quarto-only: start` and `quarto-only: end` comments, because that file
  is shared with the old build; `QuartoOnlyCss` requires each selector there
  to name `#quarto-content` or `.quarto-light`.
- Quarto traps: it reserves the `theme` metadata key, so the presentation
  travels as `theme-name`. Never use the Cosmo theme (it imports Google
  Fonts) and never enable `algolia:` search (a third-party CDN the scans
  cannot see). Quarto writes a `robots.txt` that allows indexing; override
  it (ledger 37). `title-block-style: none` only strips styling; the empty
  `title-block.html` partial is what leaves one `<h1>` per page, so never
  delete it. `{{< include >}}` merges the included file's front matter into
  page metadata, so a curriculum key that collides with a Quarto option
  (`lang`, `toc`, `css`, `date`, `author`) would change a page.
- Brand assets: the header and footer are two Pandoc partials,
  `tools/brandheader.html` and `tools/brandfooter.html`. Logo files in
  `site/brand/` are never edited (`tests/test_assets.py` pins each
  SHA-256). The header logo is one published PNG, kept out of
  `--embed-resources` by `data-external="1"` (D-0056); only the sim bar
  embeds a logo. Never pass a data: URI as a Pandoc `-M` value (past the
  Windows command-line limit). Open Sans in `site/fonts/` is rebuilt only by
  `tools/subset_fonts.py`.
- One Markdown source feeds both presentations, `themes/faithful.css` and
  `themes/modern.css` (ledger 28); never copy content into a second file.
  Question numbers come from `tools/filters/questions.lua` at render time;
  none is stored in the source. The "How this was made" page is lifted from
  `VISION.md`; the banner wording is `BANNER_MAIN` and `BANNER_DETAIL` in
  `tools/render.py`. Output stays host-agnostic static files (ledger 39).
- Tools not on PATH: Python 3.12 at
  `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`; the GitHub CLI at
  `C:\Program Files\GitHub CLI\gh.exe`. Node 24 is on PATH; the sim tests
  need it.

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent. Nothing that carries an
  answer key belongs here: the Electric Force instructor guide and build
  prompt stay out.
- Conversion phase: no content changes. Format only, proven by the
  content-unchanged check (docs/conversion-spec.md).
- Roles, not names. No em dashes. No invented record data. `grep -c` exits 1
  when it counts zero, so never chain a commit after the em-dash grep with
  `&&`; it silently skips the commit (bit twice, 2026-10-01).
- Original source files are in `../Unsorted Legacy Resources/` and are unvetted.
- In `site/site.css`, `body.site-page a` sets the link color and outranks the
  single-class chrome rules, so a chrome color must be scoped to its parent
  (`.osu-banner .osu-sitename`). D-0032 is one bug this caused in production.
- `ch` resolves against each element's own font, so a heading capped at
  `--chrome-measure` is wider than the shell. The prose column is a grid on
  `main` for that reason (D-0029), and grid items do not collapse margins:
  vertical spacing there is one-sided and adds up to the scale's steps.
- Design mockups from a review are kept as files under `docs/design/`, with a
  README saying which decisions each board became. They are mockups, never
  the source of truth for what the site does.
- Deploy: never run wrangler from this machine inside a Claude Code session,
  never touch the Cloudflare or Vercel projects or any secret without the
  owner's word, and compare a deployment only against CI's artifact, never a
  local build (reference: Deploy).
