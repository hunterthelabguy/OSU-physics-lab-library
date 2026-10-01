# OSU-physics-lab-library: agent runbook

## Shipping contract (read by /handoff)

- **Verify:** `python tools/check_unchanged.py <converted .md files>` with
  `PANDOC` set to the Pandoc bundled with Quarto (locally
  `C:\Program Files\Quarto\bin\tools\pandoc.exe`; D-0044), plus the
  no-em-dash scan outside `originals/`. CI job `verify` runs both on every
  push to main and every PR, then the builds and the tests. It checks words
  only, not structure; review structure by parse-tree block counts. Manual
  before any commit: no student-identifiable data. Which Pandoc each step
  uses, and the three variables to export locally, are under Build, Quarto,
  "Which Pandoc".
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

- Build the whole site:
  `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe" python tools/render.py --site`
  writes `build/site/`: landing page, course index, "How this was made", and
  every converted document in both presentations. Relative links throughout,
  so it serves from any host and opens from disk. CI runs it too, so a broken
  build script fails `verify`. This is the old build, which keeps the
  standalone Pandoc 3.11 (set inline on this command only) because production
  is built with it (D-0046); the rest of the repo reads with Quarto's.
- Every site page carries the OSU header and footer via two Pandoc partials,
  `tools/brandheader.html` and `tools/brandfooter.html`. Logo files live in
  `site/brand/` and must never be edited; `tests/test_assets.py` pins each
  file's SHA-256. Open Sans lives in `site/fonts/` and is rebuilt only by
  `tools/subset_fonts.py` (one-time tool; ordinary deploys use the committed
  WOFF2 files). The Python test suite (`tests/`) needs `build/site/` to
  exist and runs after the site build in CI.
- Render one converted file on its own, no site chrome:
  `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe" python tools/render.py <file.md>`
  writes `build/<theme>/<id>.html`, theme embedded, `build/` not committed.
- Themes are `themes/faithful.css` (original page settings) and
  `themes/modern.css` (evidence review plus WCAG 1.4.8). One Markdown source
  feeds both (ledger 28); never copy content into a second file.
- Question numbers are generated at render time from document order by
  `tools/filters/questions.lua`. No number is stored in the source.
- Quarto (D-0033, migration in progress; phases 2 and 3 are done, phase 5 is
  next, then phase 4, in `docs/quarto-migration-plan.md`). Production still
  serves the old build.
  - Setup: 1.10.18 at `C:\Program Files\Quarto\bin\quarto.exe`, not on PATH.
    It bundles Pandoc 3.10 (not 3.11) at `C:\Program Files\Quarto\bin\tools\pandoc.exe`
    (owner-supplied 2026-10-01). Never set `PANDOC` to the `quarto pandoc`
    command: its stdout truncates large output on Windows (D-0045).
    Quarto reserves the `theme` metadata key for its page theme, so the
    presentation name travels as `theme-name` under Quarto. Never use the
    Cosmo theme: it imports Google Fonts. Quarto writes its own `robots.txt`
    that allows indexing; override it (ledger 37). Never pass a data: URI as a
    Pandoc `-M` value (the logo is about 234 KB, past the Windows
    command-line limit), use the path plus `--embed-resources` as render.py
    does.
  - Which Pandoc (phase 3; D-0044 to D-0046). Export three variables before
    the verify sequence: `QUARTO="/c/Program Files/Quarto/bin/quarto.exe"`,
    `PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"` and
    `PANDOC_OLD_BUILD="$LOCALAPPDATA/Pandoc/pandoc.exe"`. `PANDOC`, Quarto's
    bundled binary, is what the word check, `tools/quarto_build.py`, the
    chrome lift and the tests read with, so the check reads with the Pandoc
    the Quarto pages render with; `tests/test_one_pandoc.py` fails when it is
    not Quarto's, comparing `--version` against `quarto pandoc --version`,
    never a literal. `render.py --site` is the one exception: run it with
    `PANDOC="$PANDOC_OLD_BUILD"` on that command, as CI's "Site builds" does,
    because production builds with 3.11. `PANDOC_OLD_BUILD` is read only by
    `test_old_build_pandoc_reads_the_same_tree`, which asserts both Pandocs
    read every converted file to the same syntax tree. A missing tool fails
    these tests, never skips. CI's step "Use the Pandoc bundled with Quarto"
    finds the binary next to the resolved `quarto` executable and exports it
    as `PANDOC`; it fails unless exactly one `pandoc` is under that folder's
    `tools`, which held on the Linux runner at the first run of PR #15
    (reported 3.10). Phase 4 deletes the 3.11 install, `PANDOC_OLD_BUILD` and that
    test with the old build.
  - Build with `python tools/quarto_build.py` (set `QUARTO` and `PANDOC`
    locally; every front matter read shells out to Pandoc); output
    `build/quarto-site/`, checked by `tests/test_quarto_site.py`. Generated
    pages (`/index.qmd`, `/courses/`, `/how-this-was-made/`, `/labs/`,
    `/sims/index.qmd`) are gitignored and rebuilt every run; never edit them.
    The warning gate in `tools/quarto_build.py` also catches Pandoc
    `[WARNING]` lines. After a squash merge `git branch -d` refuses; the PR's
    commits stay at `refs/pull/<n>/head`, so `-D` is safe.
  - Chrome (D-0036): the driver checks the Quarto version, then dresses every
    page with the old build's chrome, lifted from the old templates by Pandoc
    (`tools/quarto_chrome.py`). Never hand-edit the chrome in a Quarto page,
    and never copy the templates into a second file. Three body settings in
    `_quarto.yml` (`section-divs: false`, `anchor-sections: false`,
    `wrap: auto`) make Quarto's `<main>` content byte-identical to the old
    build's, and the driver swaps Quarto's `<main class="content" ...>` for
    the bare `<main>` the old templates write. Every Quarto-specific rule in
    `site/site.css` sits between its `quarto-only: start` and
    `quarto-only: end` comments, because that file is shared with the old
    build; `tests/test_quarto_chrome.py::QuartoOnlyCss` requires each
    selector there to name `#quarto-content` or `.quarto-light`.
    `tests/test_site_chrome.py` runs against both builds and gates `verify`
    (D-0042); `test_footer_as_ruled` ignores script blocks because Quarto's
    inline link handler contains a `mailto:` regex that no setting removes
    (D-0041).
  - No navbar and no search (D-0037); math is MathML (D-0040:
    `html-math-method: mathml`, pinned by `tests/test_quarto_config.py`;
    Quarto's default loads MathJax from a CDN, which fails `NoThirdParty`).
    Never enable `algolia:` search (its loader reaches a third-party CDN,
    which the HTML and CSS scans cannot see). `website.search` defaults on
    even with no navbar, and `search: false` does not remove the markup or
    `search.json` in 1.10.18, so `strip_search()` in `tools/quarto_build.py`
    does (D-0043). Quarto copies the sim's raw source page into the
    output before `post()` overwrites it, so `strip_search` skips pages
    without Quarto's generator meta tag.
  - Learned in phase 1: `title-block-style: none` only strips styling; the
    empty `title-block.html` partial (wired under `template-partials:`) is
    what leaves one `<h1>` per page, so never delete it. `{{< include >}}`
    merges the included file's front matter into page metadata, so a
    curriculum key that collides with a Quarto option (`lang`, `toc`, `css`,
    `date`, `author`) would change a page.
  - Learned in phase 3 (probed 2026-09-30, Windows; plan in
    `docs/superpowers/plans/2026-09-30-quarto-phase-3.md`): the phase 3 text
    assumed Quarto's Pandoc was 3.11 and it is 3.10, so check what a tool
    bundles before writing it into a plan. Routed through `quarto pandoc`, a
    standalone `--embed-resources` render of the logo came back as 178,569 of
    243,174 bytes on stdout (the same with `-o`: all 243,174), which cut the
    logo from five dressed pages and failed
    `test_quarto_dress.py::OldChrome::test_document_page`. So never route
    `PANDOC` through `quarto pandoc` (D-0045); the command appears only in
    the version test, for one line of output. Each call also costs about half
    a second more. Not probed on Linux, and not traced into Quarto or Deno.
    The old build and the word check come out the same under 3.10 and 3.11
    today (9 files byte-identical; 989 words, bold on 943); the tree test is
    what keeps that true until phase 4.
  - Probed 2026-09-30 for phase 2 (plan in
    `docs/superpowers/plans/2026-09-30-quarto-phase-2.md`):
    `include-before-body` lands inside `<main>`; `minimal: true` drops
    Bootstrap and `<main>` too; the inline `mailto:` regex is unconditional
    in Quarto's after-body script.
  - Measuring: `tools/measure_chrome.js` loads every page of both builds in
    same-origin iframes and returns the computed-style differences, 375 px
    scroll widths, banner heights, contrast ratios and the sim bar fit. CI
    does not run it. Serve the `build/` folder from the repo root with an
    absolute path on a port not used before in the session
    (`python -m http.server <port> --directory <absolute path to build>`),
    open `http://127.0.0.1:<port>/quarto-site/` in the browser pane, run the
    file's text in the pane's JavaScript tool, and stop the server after. It
    samples the first match of each of its 25 selectors only. On index.html
    at 1440 and 375 px it reports two `.site-foot` "missing in quarto" rows;
    that is expected (the landing footnote is not carried, D-0038).
  - Keeping the measured match: the quarto-only block is mostly `revert`
    rules at Bootstrap's own specificity (Bootstrap's reboot, undone). Its
    load-order dependency (Bootstrap, then `site.css`, then `themes/*.css`)
    is written in the block's own comment and guarded by
    `tests/test_quarto_chrome.py::PageShell`, which also guards the single
    `#quarto-content` opener. The reverts cover only the element types
    measured against the old build, so when a page brings a new one (nested
    lists, sub and sup, code, blockquote, hr, caption, table borders), measure
    it first with `tools/measure_chrome.js` plus an injected element and add a
    revert. Measured 2026-10-01: `strong` (on all six pages) and an injected
    `b`, in a paragraph and in an h2, already match; `dd` did not (Bootstrap's
    `margin-left: 0` and `margin-bottom: .5rem`) and now has a revert, pinned
    by `QuartoOnlyCss::test_dd_margins_reverted`. Quarto's hover-preview
    script queries `main.content`, which is null on the bare `<main>`
    (null-guarded, silent). Quarto adds table classes inside `<main>` on
    how-this-was-made: the styles match, the markup is not byte-identical,
    and `test_bodies_unchanged` covers lab pages only.
- Site content: `site/landing.md` is the landing copy, `site/courses.md`
  holds the course index data in front matter, `site/site.css` is the shared
  chrome. The "How this was made" page is lifted from `VISION.md` at build
  time and is never retyped. The draft banner wording lives in
  `tools/render.py` as `BANNER_MAIN` and `BANNER_DETAIL`.
- The standalone Pandoc 3.11, the old build's (`PANDOC_OLD_BUILD`), lives at
  `%LOCALAPPDATA%\Pandoc\pandoc.exe` on this machine and is not on PATH in
  every shell; Python 3.12 is at
  `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`. Node 24 is on PATH
  and the sim tests need it. The GitHub CLI is not on PATH: it is at
  `C:\Program Files\GitHub CLI\gh.exe`.
- Output stays host-agnostic static files (ledger 39).

### Checking a built page

- Check built pages over a local HTTP server, not `file://`. The desktop
  app's preview pane renders a local file as a processed snapshot, which
  drops injected markup: a sim's banner reads as missing when it is in fact
  in the file. `python -m http.server 8733 --directory build/site` and load
  `http://127.0.0.1:8733/`.
- Start that server from the repo root with `--directory`, never by changing
  into `build/site`. A process whose working directory is inside `build/site`
  makes the next `--site` build fail on Windows when it clears the directory.
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
- A viewport size set on one tab does not apply to a tab opened after it;
  set the size on the tab you are about to measure.

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent.
- Conversion phase: no content changes. Format only, proven by the
  content-unchanged check (docs/conversion-spec.md).
- Roles, not names. No em dashes. No invented record data.
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

## Deploy

- Vercel project `osu-physics-lab-library`, deploying from `main`. Production
  is `https://osu-physics-lab-library.vercel.app`, unlisted (ledger 37, 47).
- Vercel Authentication and password protection are both off (ledger 48).
  Unlisted means `noindex` plus the banner, not access control.
- The build settings are in the project, not in this repo (ledger 39, 49).
  To set the same thing up on any host:
  - Framework: none. Install command: `echo no install step`.
  - Build command: `curl -sSL -o p.tgz https://github.com/jgm/pandoc/releases/download/3.11/pandoc-3.11-linux-amd64.tar.gz && tar xzf p.tgz && PANDOC=$PWD/pandoc-3.11/bin/pandoc python3 tools/render.py --site`
  - Output directory: `build/site`.

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
- Nothing that carries an answer key belongs here, because this repo will be
  public. The Electric Force instructor guide and build prompt stay out.

## Widths

Two, on purpose (ledger 56 to 58). `--chrome-measure` is 68 characters, the
evidence review's reading measure, and governs anything read as prose.
`--chrome-shell` is 72rem, the page frame, and card lists may use all of it.
Document reading columns stay at the measure and grow their type above
1440 px instead. Do not widen a reading column to fill a screen; that number
is an owner decision, not a styling one.
