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

### D-0093  Keep instructor notes and rubrics git-ignored in this repo
- status: declined
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: Instructor notes and rubric workbooks kept in this repo's working tree, git-ignored, never tracked.
- rationale: Declined by the owner in the critique round of 2026-10-07, choosing the private instructor repo (D-0081). As proposed (chat, 2026-10-06; spec 3.11): never tracked in a repo that will be public. Against it: an ignored file has no history, which the rubric lockstep needs; it is not durable (charter floor 12); a check that reads ignored files cannot run in CI and passes everywhere but one machine (floor 2); one `git add -f` would put answer keys into a public repo's permanent history.
- alternatives: tracked in the private instructor repo (D-0081, chosen).
- binds: spec 3.11 and section 7; LEDGER 2

### D-0094  A no-print pre-scan of the originals before any is read
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Before any in-scope original is read, a script prints counts and locations only (document properties, comment and revision authors, `people.xml`, email and nine-digit patterns); only flagged spots are read, by the main session or the owner (critique F3).
- rationale: Declined by the owner, 2026-10-07: "These are lab handouts; no student PII is in them. Is there still any need for a pre-scan?" With his word recorded as the vetting ruling (D-0084), the pre-scan's one remaining job, finding names in metadata, belongs to the strip (D-0086). As proposed: "never quoted in a report" protects the report, not the reader's context, so delegated vetting put unvetted text into more transcripts. A pre-scan cannot see a name in prose in any case.
- alternatives: the owner's word plus a stop-and-report line in readers' prompts (D-0084, chosen).
- binds: spec sections 6 and 9.1

### D-0095  Hold pass 6 until the paper-or-typed decision is made
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Passes 1 to 5 proceed; pass 6 (the template) starts only once typed reports are ruled, or once the owner rules that B ships regardless (critique F7).
- rationale: Declined by the owner, 2026-10-07: "B ships regardless and record the reason: if paper wins, the templates already exist and serve as the starting point for the paper worksheets." As proposed: if paper wins, the template has no user.
- alternatives: B ships regardless (D-0074, chosen).
- binds: spec 3.3 and section 6

### D-0096  No target term for the templates until the paper decision and the license settle
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Set no term for students to have the templates; revisit when the paper decision or the license (D-0073) settles (critique finding 5).
- rationale: Declined by the owner, 2026-10-07, choosing Winter 2027 with the template's own distribution ruling (D-0080). As proposed: two unruled gates stood between a template and a student, and a date set first would drive the pass order for a file the draft notice says is not for distribution.
- alternatives: Winter 2027, distribution ruled (D-0080, chosen); Spring 2027.
- binds: D-0052, spec call 4.3

### D-0097  Build the template after pass 3 rather than after all 18 conversions
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Amend rule 3.10: once pass 3 has converted the two hardest handouts and PH 211's six, build the template on those fixtures; every later lab gets one as it converts, and a structure first seen in pass 4 or 5 adds its case there.
- rationale: Declined by the owner, 2026-10-07: "3.10 holds; Winter slips" (D-0080). As proposed: the Winter 2027 target and the hardest-two-first order, both ruled the same day, were new evidence against 3.10, since the hardest structures would be converted by the end of pass 3.
- alternatives: 3.10 with a cut-off date; 3.10 holding and the date slipping (D-0080, chosen).
- binds: spec 3.10 and section 6

### D-0098  Cross-reference each converted handout against its instructor notes during the conversion passes
- status: declined
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Once per course in passes 3 to 5, a Sonnet dispatch compares each converted handout with its instructor notes; findings name misalignments only and land in the instructor repo (spec section 6; critique finding 10 kept it).
- rationale: Declined by the owner, 2026-10-07, who moved it to a separate pass after the rest of the work (D-0083), taking F12's point that in a format-only phase its findings change nothing, without F12's deletion: "F12 but instead of deleting it and waiting until content changes, we do it in a separate pass once the rest of the work is done."
- alternatives: deleted until content changes begin (F12); pass 7 with a named job (D-0083, chosen).
- binds: spec sections 6 and 7
