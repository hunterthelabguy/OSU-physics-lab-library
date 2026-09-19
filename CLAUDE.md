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
- **Living plan:** `LEDGER.md`, dated and append-only.
- **Commit trailer:** none. Identity `hunterthelabguy` with the noreply email.
- **Remote:** `git@github-hunterthelabguy:hunterthelabguy/OSU-physics-lab-library.git`

## Build

- Build the whole site:
  `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe" python tools/render.py --site`
  writes `build/site/`: landing page, course index, "How this was made", and
  every converted document in both presentations. Relative links throughout,
  so it serves from any host and opens from disk. CI runs it too, so a broken
  build script fails `verify`.
- Render one converted file on its own, no site chrome:
  `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe" python tools/render.py <file.md>`
  writes `build/<theme>/<id>.html`, theme embedded, `build/` not committed.
- Themes are `themes/faithful.css` (original page settings) and
  `themes/modern.css` (evidence review plus WCAG 1.4.8). One Markdown source
  feeds both (ledger 28); never copy content into a second file.
- Question numbers are generated at render time from document order by
  `tools/filters/questions.lua`. No number is stored in the source.
- Site content: `site/landing.md` is the landing copy, `site/courses.md`
  holds the course index data in front matter, `site/site.css` is the shared
  chrome. The "How this was made" page is lifted from `VISION.md` at build
  time and is never retyped. The draft banner wording lives in
  `tools/render.py` as `BANNER_MAIN` and `BANNER_DETAIL`.
- Pandoc 3.11 lives at `%LOCALAPPDATA%\Pandoc\pandoc.exe` on this machine
  and is not on PATH in every shell; Python 3.12 is at
  `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`.
- Output stays host-agnostic static files (ledger 39).

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent.
- Conversion phase: no content changes. Format only, proven by the
  content-unchanged check (docs/conversion-spec.md).
- Roles, not names. No em dashes. No invented record data.
- Original source files are in `../Unsorted Legacy Resources/` and are unvetted.

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
