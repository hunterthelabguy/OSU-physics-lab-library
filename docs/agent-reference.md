# Agent reference: read the section for the task

Moved out of `CLAUDE.md` on 2026-10-01 so that file loads only what every
session needs. `CLAUDE.md` says when to read each section below. The text
is moved, not rewritten.

## Site content

- Site content: `site/landing.md` is the landing copy, `site/courses.md`
  holds the course index data in front matter, `site/site.css` is the shared
  chrome.
- One converted file on its own, no site chrome, is the lab's HTML
  download, `build/quarto-site/labs/<id>/<id>.html` (D-0054). Phase 4
  deleted `tools/render.py`'s file mode with the old build (D-0061, call 2).
- Themes: `themes/faithful.css` (original page settings) and
  `themes/modern.css` (evidence review plus WCAG 1.4.8).

## Quarto details

- Which Pandoc, CI side: CI's step "Use the Pandoc bundled with Quarto"
  finds the binary next to the resolved `quarto` executable and exports it
  as `PANDOC`; it fails unless exactly one `pandoc` is under that folder's
  `tools`, which held on the Linux runner at the first run of PR #15
  (reported 3.10). `tests/test_one_pandoc.py` fails when `PANDOC` is not
  Quarto's, comparing `--version` against `quarto pandoc --version`, never
  a literal. Phase 4 deleted the standalone Pandoc 3.11 install,
  `PANDOC_OLD_BUILD` and the tree test with the old build (D-0061), and
  `test_ci_uses_quartos_pandoc` fails if any step names a standalone Pandoc.
- Chrome (D-0036), in full: the driver checks the Quarto version, then
  dresses every page with the chrome rendered by Pandoc from
  `tools/template.html` and `tools/template-site.html`, the templates the
  old build used and phase 4 kept (`tools/quarto_chrome.py`, D-0061). Three
  body settings in `_quarto.yml` (`section-divs: false`,
  `anchor-sections: false`, `wrap: auto`) make Quarto's `<main>` content
  byte-identical to the old build's (the fixture `test_bodies_unchanged`
  reads), and the driver swaps Quarto's `<main class="content" ...>` for
  the bare `<main>` the templates write. D-0038's pieces are pinned by
  their words, read from `render.py` and the templates
  (`tests/test_quarto_chrome.py::ChromePieces`). `tests/test_site_chrome.py`
  reads `build/quarto-site/` and runs in "Tests" (D-0042);
  `test_footer_as_ruled` ignores script blocks because Quarto's inline link
  handler contains a `mailto:` regex that no setting removes (D-0041).
- No navbar and no search (D-0037); math is MathML (D-0040:
  `html-math-method: mathml`, pinned by `tests/test_quarto_config.py`;
  Quarto's default loads MathJax from a CDN, which fails `NoThirdParty`).
  `website.search` defaults on even with no navbar, and `search: false`
  does not remove the markup or `search.json` in 1.10.18, so
  `strip_search()` in `tools/quarto_build.py` does (D-0043). Quarto copies
  the sim's raw source page into the output before `post()` overwrites it,
  so `strip_search` skips pages without Quarto's generator meta tag.
- After a squash merge `git branch -d` refuses; the PR's commits stay at
  `refs/pull/<n>/head`, so `-D` is safe. `gh pr merge --squash
  --delete-branch` removes the local branch too, so `-D` then reports it
  not found.

## Checking a built page

- Check built pages over a local HTTP server, not `file://`. The desktop
  app's preview pane renders a local file as a processed snapshot, which
  drops injected markup: a sim's banner reads as missing when it is in fact
  in the file. `python -m http.server 8733 --directory build/quarto-site`
  and load `http://127.0.0.1:8733/`.
- Start that server from the repo root with `--directory`, never by changing
  into `build/quarto-site`. A process whose working directory is inside it
  makes the next build fail on Windows when it clears the directory.
- Measure layout with a script in the page rather than by eye: the pane
  scales a wide emulated viewport down, so a correct layout can look wrong in
  a screenshot.
- The pane caches a page per origin, and a reload can still serve the old
  copy after a rebuild. Serve each round on a new port, and confirm the CSS
  you just wrote is in the page (look for a declaration only the new version
  has) before trusting a measurement. One round of this session's centering
  work was measured against a stale page.
- Give `--directory` an absolute path. A background shell does not always
  start in the repo root, and a relative path there silently serves the
  wrong folder.
- A server started in the background with `&` outlives the shell. Stop it
  by its command line (`Get-CimInstance Win32_Process`, match `http.server
  <port>`) and confirm the port no longer answers. To run
  `tools/measure_chrome.js` without pasting it, copy it to `build/` (ignored),
  fetch it in the page, strip its leading `await` and `eval` the rest; delete
  the copy after.
- A viewport size set on one tab does not apply to a tab opened after it;
  set the size on the tab you are about to measure.
- To see what Word draws (the question and checkpoint boxes), print a
  scratchpad copy to PDF through Word's automation in PowerShell 5.1
  (`Documents.Open` with `[ref]` arguments, `ExportAsFixedFormat(path, 17)`,
  `Close`/`Quit`, then stop only the WINWORD process ids that appeared after
  `New-Object`) and render pages with poppler's `pdftoppm` beside
  `PDFTOTEXT`; `-gray` gives a PGM whose rows measure box edges in pixels.
- A fixture page (Pandoc `-s --embed-resources --css themes/modern.css`)
  can be checked in the pane by copying it into the ignored `build/` and
  serving that folder; the pane will not act on a `file://` tab. Delete the
  copy after.
- Comparing downloads with production: Pages answers `<file>.html` with a
  308 to the extensionless path, so fetch with `curl -L`; a local Windows
  build writes CRLF where CI writes LF, so strip `\r` before `cmp`. Compare
  the Word file's `word/document.xml` and `styles.xml`, not the zip, and the
  PDF by `pdftotext` output.

## Measuring and keeping the measured match

- Measuring: `tools/measure_chrome.js` loads every page in same-origin
  iframes and returns 375 px scroll widths (with each page's client
  width), banner heights, contrast ratios, the sim bar fit, and under
  `courses` the course index and course pages at 375, 1440 and 1920 px:
  the boxes of main, the h1, the intro, tiles, tabs, the lab table and its
  columns, the collapse, Download all and the footnote, and the lines the
  descriptions set with the collapse open (D-0069, D-0070). Its old-build
  comparison was removed with the old build's last reference, 2026-10-06.
  CI does not run it. Serve the `build/` folder from the repo root with an
  absolute path on a port not used before in the session
  (`python -m http.server <port> --directory <absolute path to build>`;
  the sandbox's `.claude/launch.json` holds one configuration per port for
  `preview_start`), open `http://127.0.0.1:<port>/quarto-site/` in the
  browser pane, run the file's text in the pane's JavaScript tool, and
  stop the server after. A page taller than its frame gives 15 px to the
  scrollbar, so record the client width beside a box.
- Keeping the measured match: the quarto-only block is mostly `revert`
  rules at Bootstrap's own specificity (Bootstrap's reboot, undone). Its
  load-order dependency (Bootstrap, then `site.css`, then `themes/*.css`)
  is written in the block's own comment and guarded by
  `tests/test_quarto_chrome.py::PageShell`, which also guards the single
  `#quarto-content` opener. The reverts cover only the element types
  measured against the old build, so when a page brings a new one (nested
  lists, sub and sup, code, blockquote, hr, caption, table borders), measure
  it first with `tools/measure_chrome.js` plus an injected element and add a
  revert. That measurement compared against the old build, which phase 4
  deleted (D-0061); what replaces it as the reference is not yet chosen.
  Measured 2026-10-01: `strong` (on all six pages) and an injected
  `b`, in a paragraph and in an h2, already match; `dd` did not (Bootstrap's
  `margin-left: 0` and `margin-bottom: .5rem`) and now has a revert, pinned
  by `QuartoOnlyCss::test_dd_margins_reverted`. Quarto's hover-preview
  script queries `main.content`, which is null on the bare `<main>`
  (null-guarded, silent). Quarto adds table classes inside `<main>` on
  how-this-was-made: the styles match, the markup is not byte-identical,
  and `test_bodies_unchanged` covers lab pages only.

## Widths

Two, on purpose (ledger 56 to 58, D-0070). `--chrome-measure` is 68
characters, the evidence review's reading measure, and governs anything read
as prose. `--chrome-shell` is the page frame: 72rem on document pages (the
`:root` value) and 96rem on site pages (set on `body.site-page`), where the
course tiles and the lab table use all of it. On the course index and course
pages (body class `courses`) the prose track sits at the shell's left edge;
elsewhere it is centered (D-0029). Document reading columns stay at the
measure and grow their type above 1440 px instead. Do not widen a reading
column to fill a screen; that number is an owner decision, not a styling
one. A table's description column is not a reading column: the owner chose
it wider than the measure (D-0070).

## Deploy

- Production is Cloudflare Pages, Direct Upload project `osu-physics-labs`
  in the owner's own account: `https://osu-physics-labs.pages.dev/`,
  unlisted (ledger 37, 48; D-0047 to D-0050). Cut over 2026-10-01.
- `.github/workflows/verify.yml`, job `deploy` (needs `verify`): downloads
  the folder `verify` tested (artifact `quarto-site`, `_quarto.yml`'s
  `output-dir`), runs the pinned `npx --yes wrangler@<version> pages deploy`
  (the pin lives in `tests/test_create_project_workflow.py`), then
  `tools/check_deployed.py` against the deployment URL once and, on a push
  to `main`, against the `pages.dev` alias with `--wait 120` (D-0060: the
  alias can serve the previous deployment for seconds after "Deployment
  complete", so that step reruns the whole check every 5 s until one
  complete run passes; its last line gives the attempts and seconds, the
  measured lag). A push to `main` is production; a
  pull request from this repository is a preview (its own URL, `noindex`
  by default, public); a fork's pull request deploys nothing.
- Settings, never in the repo: secrets `CLOUDFLARE_API_TOKEN` (Account,
  Cloudflare Pages, Edit) and `CLOUDFLARE_ACCOUNT_ID`, which Claude never
  reads or handles; repository variable `CLOUDFLARE_PAGES_PROJECT`. Only
  `verify.yml` and `create-pages-project.yml` may name a secret (tested).
- To stand the site up in another account: set the two secrets and the
  variable, run "create Pages project" once from the Actions tab (it sets
  the production branch to `main`; the dashboard cannot create an empty
  Direct Upload project), then push to `main`.
- `check_deployed.py` sends its own user agent: Cloudflare refuses Python's
  default one with a 403 (error 1010). To check a deployment by hand,
  compare against that run's artifact (`gh run download <run> -n
  quarto-site`), never a local build: the Linux and Windows builds name the
  Bootstrap stylesheet with different hashes.
- Never run wrangler from this machine inside a Claude Code session:
  wrangler 4.146.0 detects an agent from environment variables and may
  turn a Pages deploy or create into a Workers one.
- Retired: Vercel project `osu-physics-lab-library`
  (`https://osu-physics-lab-library.vercel.app`). One project routing rule
  ("Moved to Cloudflare Pages", regex `^/(.*)$`, 308 to the same path on
  `pages.dev`) redirects every path, set in the project's settings
  2026-10-01; no file in the repo. Its build settings still run
  `tools/render.py --site`; phase 4 deleted that mode (D-0061), so the
  command now writes nothing, and `build/site/` is never made. What Vercel
  reports for such a build was not checked; a red Vercel status on `main`
  blocks nothing. Turning the builds off or deleting the project is
  the owner's (spec call 1). Every Vercel change needs the owner's word.

## Sims

- A sim is one self-contained HTML page in `sims/<id>/index.html` that must
  keep working opened from disk, offline: inline CSS and JS, no network, and
  a `default-src 'none'` Content Security Policy. Ledger 38 is why there is
  no framework here.
- The build injects the draft banner and a way back into the published copy
  only; the source file is never edited for the site. The injected bar is
  34 px tall at 1280x720 (measured 2026-09-21); the sim fits in 720 px with
  it. The sim's own file carries Open Sans Regular and Bold as data: URIs
  (D-0026); this is a change to the sim's own source, not injected chrome,
  so "the source file is never edited for the site" still holds.
- A sim ships its own no-dependency node test script beside it, and CI runs
  every one. A check whose file is not in this checkout is reported as
  skipped, never as a pass.
