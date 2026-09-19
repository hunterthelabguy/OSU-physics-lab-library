# OSU-physics-lab-library: agent runbook

## Shipping contract (read by /handoff)

- **Verify:** none exists yet. No code, no tests, no CI. Do not claim
  otherwise. Manual checks before any commit: no em dash bytes in the diff,
  no student-identifiable data, no instructor-only material.
- **Landing rule:** docs, spec, and ledger commits land direct on `main`
  (charter floor 4). Code, when it exists, lands via PR once CI exists.
- **Living plan:** `LEDGER.md`, dated and append-only.
- **Commit trailer:** none. Identity `hunterthelabguy` with the noreply email.
- **Remote:** `git@github-hunterthelabguy:hunterthelabguy/OSU-physics-lab-library.git`

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent.
- Migration phase: no content changes. Format only, proven by the
  content-unchanged check (docs/migration-spec.md).
- Roles, not names. No em dashes. No invented record data.
- Legacy sources are in `../Unsorted Legacy Resources/` and are unvetted.
