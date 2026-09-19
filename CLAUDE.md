# OSU-physics-lab-library: agent runbook

## Shipping contract (read by /handoff)

- **Verify:** `python tools/check_unchanged.py <converted .md files>` with
  Pandoc on PATH (locally: `PANDOC=%LOCALAPPDATA%\Pandoc\pandoc.exe`), plus
  the no-em-dash scan outside `originals/`. CI job `verify` runs both on every
  push to main and every PR. It checks words only, not structure; review
  structure by parse-tree block counts. Manual before any commit: no
  student-identifiable data.
- **Landing rule:** code and converted content land via PR with green
  `verify` (charter floor 4), squashed locally as the noreply identity and
  pushed to `main`, then the PR is closed with the landing commit. GitHub's
  web merge rejects the noreply address as author and otherwise stamps the
  account's primary email. Ledger and spec-only commits may land direct.
- **Living plan:** `LEDGER.md`, dated and append-only.
- **Commit trailer:** none. Identity `hunterthelabguy` with the noreply email.
- **Remote:** `git@github-hunterthelabguy:hunterthelabguy/OSU-physics-lab-library.git`

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent.
- Conversion phase: no content changes. Format only, proven by the
  content-unchanged check (docs/conversion-spec.md).
- Roles, not names. No em dashes. No invented record data.
- Original source files are in `../Unsorted Legacy Resources/` and are unvetted.
