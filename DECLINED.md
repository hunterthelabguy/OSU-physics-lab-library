# Declined decisions

Full entries for decisions the owner rejected, same format as `DECISIONS.md`,
which carries a one-line index of each. Not loaded by default; search it
before proposing anything resembling an indexed decline. Declines do not
expire; re-proposing one requires stated new evidence.

### D-0003  Name the site in text, never the logo
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Identify the site as "Oregon State University, Department of Physics" in plain text, and never use the official logo.
- rationale: Declined because the owner answered "yes, we're going to put the official logo on it" when offered text only as one of the options (D-0002). The option came from the first brainstorm round, where text-only naming looked like the safe way to follow the policy against unit logos. It was also meant to keep a draft site from looking university-endorsed.
- alternatives: logo after the license settles, or logo now; timing is open in D-0011.
- binds: site/, tools/render.py

### D-0017  Add a light grid pattern to the header area
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Use the brand guide's basic grid pattern, at low contrast, in the landing page header area only.
- rationale: Declined by the owner in chat 2026-09-21; no reason was stated. As proposed: It is the brand guide's approved "feels like OSU" element. Only the landing page gets it, because sims have no height to spare.
- alternatives: no pattern.
- binds: site/landing

### D-0021  Keep the system font inside sims
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Pages built by the site use Open Sans (D-0006), but the published sims and their injected bar keep the system font stack.
- rationale: Declined by the owner in chat 2026-09-21: "Sims can adjust their font." How is open in D-0026. As proposed: A spec gap caught before code. The sim's Content Security Policy is `default-src 'none'` with no `font-src`, which blocks every font, embedded ones included. The policy lives in the sim's source, which LEDGER 51 keeps byte for byte. So D-0006's "keeps sims inside their no-network policy" cannot mean sims get Open Sans.
- alternatives: add `font-src data:` to the sim's policy (edits the untouchable source); rewrite the policy in the published copy only (the copy would no longer match the file that ships to students).
- binds: D-0006, tools/render.py (SIM_CHROME)
