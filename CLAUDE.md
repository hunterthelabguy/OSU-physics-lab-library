# OSU-physics-lab-library: agent runbook

## Shipping contract (read by /handoff)

- **Verify:** `python tools/check_unchanged.py <converted .md files>` with
  Pandoc on PATH (locally: `PANDOC=%LOCALAPPDATA%\Pandoc\pandoc.exe`), plus
  the no-em-dash scan outside `originals/`. CI job `verify` runs both on every
  push to main and every PR. It checks words only, not structure; review
  structure by parse-tree block counts. Manual before any commit: no
  student-identifiable data.
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
  build script fails `verify`.
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
- Quarto (D-0033, migration in progress): 1.10.18 at
  `C:\Program Files\Quarto\bin\quarto.exe`, not on PATH. Quarto reserves the
  `theme` metadata key for its page theme, so the presentation name travels
  as `theme-name` under Quarto. Never use the Cosmo theme: it imports Google
  Fonts. Quarto writes its own `robots.txt` that allows indexing; override it
  (ledger 37). Build it with `python tools/quarto_build.py` (set `QUARTO` and
  `PANDOC` locally; every front matter read shells out to Pandoc); output `build/quarto-site/`, checked by `tests/test_quarto_site.py`.
  Generated pages (`/index.qmd`, `/courses/`, `/how-this-was-made/`, `/labs/`,
  `/sims/index.qmd`) are gitignored and rebuilt every run; never edit them.
  Production still serves the old build. Learned in phase 1: `title-block-style:
  none` only strips styling; the empty `title-block.html` partial (wired under
  `template-partials:`) is what leaves one `<h1>` per page, so never delete it.
  `{{< include >}}` merges the included file's front matter into page
  metadata, so a curriculum key that collides with a Quarto option (`lang`,
  `toc`, `css`, `date`, `author`) would change a page. The warning gate in
  `tools/quarto_build.py` also catches Pandoc `[WARNING]` lines. Never enable
  `algolia:` search (its loader reaches a third-party CDN, which the HTML and
  CSS scans cannot see), and a page with math loads MathJax from a CDN, which
  fails `NoThirdParty`: a phase 2 item. After a squash merge `git branch -d`
  refuses; the PR's commits stay at `refs/pull/<n>/head`, so `-D` is safe.
- Site content: `site/landing.md` is the landing copy, `site/courses.md`
  holds the course index data in front matter, `site/site.css` is the shared
  chrome. The "How this was made" page is lifted from `VISION.md` at build
  time and is never retyped. The draft banner wording lives in
  `tools/render.py` as `BANNER_MAIN` and `BANNER_DETAIL`.
- Pandoc 3.11 lives at `%LOCALAPPDATA%\Pandoc\pandoc.exe` on this machine
  and is not on PATH in every shell; Python 3.12 is at
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
