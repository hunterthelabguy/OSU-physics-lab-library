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

- Render a converted file in both presentations:
  `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe" python tools/render.py <file.md>`
  writes `build/<theme>/<id>.html`, theme embedded, `build/` not committed.
- Themes are `themes/faithful.css` (original page settings) and
  `themes/modern.css` (evidence review plus WCAG 1.4.8). One Markdown source
  feeds both (ledger 28); never copy content into a second file.
- Question numbers are generated at render time from document order by
  `tools/filters/questions.lua`. No number is stored in the source.
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
