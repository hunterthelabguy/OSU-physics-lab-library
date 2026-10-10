# State

Volatile handoff, capped at one screen. Updated 2026-10-10.

**Pass 4 (2026-10-09): the rest of PH 212; complete (D-0142).**
- Merged: redaction tool #51, Lab 5 #54, print-keep and download fixes #57
  and #58 (D-0138), Lab 1 #52, Lab 2 #56, Lab 4 #53. Hash records D-0134 to
  D-0137 (proposed).
- Lab 6 #55 merged after the owner's Word check (D-0142); its rubric at
  Word's column shares (#59, D-0139) on Word's landscape page (#60,
  D-0140). Next: pass 5, the rest of PH 213; propose its PR split first.
- Earmarked, a pass after all other pending work (D-0141): capstone
  restructure, web-only rubric, page table of contents.
- Open: measure. 68ch measured a median 80 characters a line (321 lines,
  six labs, 1440 px), so "true 80" is today's; a table break-out for
  the web rubric's side-scroll awaits the owner.
- Labs 2 and 6 carry the activation code (Lab 6 in a link target, missed by
  the survey) and Lab 6 the OneDrive target: committed stripped and
  redacted, marker `[removed under D-0104]`. Only the main session opens
  the unredacted copies.
- The owner's task list is `docs/owner-tasks.md` (removed links, missing
  alt text); add to it as passes 4 and 5 go.

**Pass 3 (2026-10-08): PH 211 Labs 2 to 7 merged; the hardest two held.**
- Merged: PH 211 Lab 6 #40, Lab 5 #42, Lab 4 #44, Lab 7 #41, Lab 3 #48,
  Lab 2 #49 (subagent conversions, reviewed). Tool PRs first, each with
  made-up fixtures (D-0119 call 4): tests #36, number check #38 (D-0122),
  Symbol font and course zip #39 (D-0123), table grid #43 (D-0130), font
  test #45, print test #46, block quotes #47, table scroll #50.
- #37, PH 212 Lab 3 and PH 213 Lab 2, merged 2026-10-09 (`706dcdf`) after
  the owner's Word and Google Docs check (D-0131). Pass 3 complete. Next:
  pass 4, the rest of PH 212; propose its PR split first.
- Ruled this pass: D-0119 (seven PRs), D-0120 (Heading 1 outline, math-font
  text, box alt text, Q15 photo as is), D-0122, D-0123, D-0130. Proposed:
  D-0121 and D-0124 to D-0129 (hash records).
- Seen, not changed: PH 211 Lab 2's PDF ends page 10 on its table's label
  "Distance (m)", the table on page 11 (a print rule could keep them).

**Pass 2b (2026-10-08): merged, #35 `25b6283`; 286 tests.**
- LibreOffice measured, not faithful (no label survives); our own
  `tools/figures.py` instead (D-0117, ruled). Within 0.11 pt of Word's
  PDFs on every label of PH 213 Labs 2 and 4. LibreOffice uninstalled
  locally (owner, 2026-10-08); CI never installs it.
- Pictures at Word's size and crop, `images:` front matter,
  `tools/media.py list|extract` for conversion; figures inline on pages,
  PNG in Word; `--resource-path`, `--mathml`; per-lab HTML caps; no new
  CSS revert (measured). Pass 2b's own calls: D-0118, ruled 2026-10-08.
- For pass 5's Word check: PH 213 Lab 4's "ℓ" is an l in Script MT Bold,
  which CI's Linux PNG lacks.
- Next: pass 3 (PH 212 Lab 3 and PH 213 Lab 2 first, D-0105). Its
  figures' docPr ids: PH 213 Lab 2 `188406814`; PH 212 Lab 3 `484604076
  2090172472 475339996 389621496`; PH 213 Lab 4 `24` (Text Box 2 `217` is a
  box).

**Pass 2a (2026-10-07), done:** checks #31, Word box #33, faithful retired
#34 (D-0112 to D-0116, ruled).

**Focus (2026-10-07):** the conversion of the remaining 18 PH 21X handouts,
then a Word report template per lab, then a cross-reference against the
instructor notes. The critique is done (steps 2 and 3 with the owner,
2026-10-07): the canon is section 11 of
`docs/superpowers/specs/2026-10-06-handout-conversion-and-templates-design.md`,
entered as D-0074 to D-0092 (ruled 2026-10-07) and D-0093 to D-0098 (declined,
`DECLINED.md`); the critique file records where each finding went. Eight
passes (D-0082): 1 survey, 2a checks, 2b downloads, 3 the hardest two then
PH 211, 4 PH 212, 5 PH 213, 6 template, 7 cross-reference; recounted after
the survey. Templates target Winter 2027 and slip if conversion does
(D-0080). Probe parameters are in D-0079; the probe files stay in
the ignored `build/probe-report-template/`.

**Pass 1 done and ruled 2026-10-07.** The survey is
`docs/handout-survey.md`; the markup rules are in `docs/conversion-spec.md`
(D-0101). The rulings, D-0099 to D-0107, all ruled ("I agree with all your
leans"):
- drawn figures become SVG in pass 2b, LibreOffice measured first;
- the number check compares Word's own labels, read by Word's automation
  (D-0102);
- an original's em dash is kept;
- PH 212 Lab 2's activation code is omitted and Lab 6's personal link loses
  its target;
- pass 3 opens with PH 212 Lab 3 and PH 213 Lab 2;
- eight passes in seven sessions;
- course names come from the handouts' course lines (a site PR, not made).

Word's labels for all 19 read 2026-10-07 (`docs/word-labels.json`,
survey section 3). PH 213 Lab 6 shows students "0)", a checkpoint
(D-0109, D-0110 below). PH 213 Lab 5's symbol is Ω. Ruled the same day: the faithful page
is retired (D-0108, its own PR in 2a, public wording redrafted for the
owner first), and a numbered item needing no answer is "Checkpoint N"
(D-0110; pace markers earmarked, D-0111) in a question-like block of another palette colour, picked on a board
(D-0109), so "0)" is never shown. Next: passes 2a and 2b; 2b's gate is
pass 1 alone.

**Focus (2026-10-01):** Phase 5 cutover done. Production is the Quarto build
on Cloudflare Pages, `https://osu-physics-labs.pages.dev/` (project
`osu-physics-labs` in the owner's own account; name from the repository
variable `CLOUDFLARE_PAGES_PROJECT`). PR #17 (deploy job, `tools/check_deployed.py`,
404 page) and PR #18 (hand-run `create-pages-project.yml`) merged; 134 tests.
The first production run passed `check_deployed.py` against the deployment
URL and the `pages.dev` alias: every file byte for byte, unknown paths 404
with `404.html`, so Pages does not rewrite the HTML. Cloudflare refuses
Python's default user agent (error 1010); the check names itself. The owner
checked production on a phone and printed Lab 1 in both presentations
(2026-10-01): fine. The old Vercel URL redirects there (308, path kept).
Downloads merged 2026-10-01, PR #19 squashed as `bbfa9b6` (D-0052 to
D-0056): four files per lab from modern, the department line in each, the
header logo published once; 148 tests; `verify` and the preview `deploy`
green on the PR's head. Demo 2026-10-06. Then two design passes, ruled as
leaned 2026-10-01 ("Rule your way on all of them and build it"), merged as
PR #20, squashed `6ee86ee` (D-0057 to D-0059, ruled 2026-10-02; 158 tests): the
Word file's draft notice is a page header, its footer size is on a Footer
style, its page is Letter at 0.75 in, its body takes the modern page's
spacing, and questions are the page's tinted, orange-ruled box; the owner
checked both builds in Word ("Looks right in Word, merge it"). The PDF's
keep rules already worked (probe: no split in 40 offsets, 50 with the
rules off), so no CSS was added and a print test pins them. The download
links are four buttons (mockups and measurements in
`docs/design/2026-10-01-download-control/`). Next: phase 4, spec written
2026-10-02 for ruling (its plan text deletes the templates that D-0036 and D-0054 now
depend on; it retires `build/site`, Pandoc 3.11, the tree test and the
old-build comparisons, not the templates).
Plans: `docs/superpowers/plans/2026-10-01-quarto-phase-5.md`.

**Previous focus:** phases 2 and 3 of the Quarto migration (PR #14, #15,
#16); site design review of 2026-09-22 (PR #11, #12, boards in
`docs/design/2026-09-22-review/`).

**Build pass done 2026-10-02 to 03 (squash merges, all `main` runs green):**
D-0060 PR #21 `ad5057f` (alias `--wait 120`; on `main`, attempt 1 in 3.7 s,
then attempt 2 in 10.1 s on `37d526a`: the lag, caught); D-0061 phase 4 PR
#22 `37d526a` (old build gone; a stray `build/site/...` logo copy that
production served now 404s); D-0068 rows PR #25 `490240e` (one lab per row
on the reading column; a 22 px `ul` indent fixed); D-0067 Download all PR
#23 `8dbb8b7` (a quiet button after each course's list opens a dialog of
opt-in formats; one stored zip written in the page). 186 tests. Vercel's
check fails on every PR (its build runs the deleted `--site`); blocks nothing.

**Done 2026-10-06: "How this site works" (D-0072, ruled; PR #29, `c3c8620`).** The
owner approved the draft ("Say 'are being written' and build it"); it ships
from `site/how-this-site-works.md` at `/how-this-site-works/`, the old
address redirecting. Open for the account holder: what the Cloudflare
account records, and its AI-crawler block (dropped from the page, not
guessed). The history below was the drafting step.

**Drafting step, same day.** The owner
asked (2026-10-06) to re-frame the "How this was made" page: the build
explained first, the AI use disclosed plainly in the body, a new title and
address with the old one redirecting, and its own source file. Draft for his
line edits: `docs/superpowers/plans/2026-10-06-how-this-site-works.md`;
nothing is built until he approves the text. Found while drafting, in the
same file: the landing page still says downloads are not built.

**Done 2026-10-06: course pages, built, merged, all three entries ruled.**
PR #26, squashed `67b9baa` (D-0069, D-0070): the course index is three
tiles; one page per course at `/courses/ph211/` and so on, with course
tabs; PH 211's converted lab in a Lab, Title, Description table across a
96rem shell (site pages only), the other seven under "Not yet converted
(7)" until converted (owner: "Collapse stands"). PR #28, squashed `f65b1d4`
(D-0071; it replaces #27, which GitHub closed when #26's merge deleted its
base branch): "Download PH 211 files" beside the h1, the formats under
"Handouts", and "Close"; a handout counts as four files (owner: "Four
files"), so PH 211 shows it. Both `main` runs green; the alias served all
39 files byte for byte (1 attempt; then 2 attempts, 9.4 s). 207 tests.
Measurements in D-0070 and D-0071; boards and rulings in
`docs/design/2026-10-06-course-pages/`. Not built: the "Lab files" group,
which waits on how a CSV or a simulation attaches to a lab.

**Earlier next: the four items of 2026-10-03, planned, nothing built.** Plan:
`docs/superpowers/plans/2026-10-03-four-items.md` (`9f2b6df`, Q5 note
`a06da83`), five PRs: 1 course links (no script), 3 dialog close and
failure words, 4a the word check learns equations and images, 4b PH 213
Lab 2, 2 wide site pages after mockups. Every PR waits on its questions,
Q1 to Q17 in the plan; the owner has answered none yet. The owner's
left-hand contents idea (links or a select that scrolls) is under Q5: mock
it first. Vetted 2026-10-03: the PH 213 handout holds no student data; its
`core.xml` names two people (Q16 gates committing it). Since then the
course pages replaced item 1 and calls 2.1 and 2.2, and D-0071 built item
3's "Close" (Q8); item 3's failure words (Q9), the copy opened from disk
(Q10) and a busy state (Q11) remain, as do items 4a and 4b.

**Awaiting owner:**
- Line-edit and approve the "How this site works" draft (D-0072); say
  whether the landing page's stale download lines ride in the same PR.
- How a CSV or a simulation attaches to a lab, and whether the sims catalog
  is the source for simulations (D-0071's "Lab files" group waits on it).
- Seen by measuring, not ruled (D-0070): the header's content shifts 121 px
  at 1440 px (192 px at 1920 px) between site pages (96rem) and lab pages
  (72rem); PH 211's h1 takes 4 lines at 375 px. A lab page's "Course index"
  link now lands on the chooser, one tap short of its course's page.
- Promote D-0067 (words approved 2026-10-03: "Words are fine. Go ahead and
  merge.") and D-0068. D-0062 to D-0066 (public flip, logo, domain, cold
  test) are another session's, proposed.
- Not done: a Download all zip opened on a real phone.
- Vercel: delete the project, the owner's leaning (2026-10-02); it ends the
  redirect, the Git builds and the commit statuses. When he says it is done,
  record it (an entry amending D-0049, the spec's call 1, the agent
  reference's Vercel paragraph, lab-ops' `lab-handbook/lab-library-site.md`).
- Before Winter 2027, a TA estimate of minutes per report (D-0091).
- A second handout to convert: answered 2026-10-03, PH213 Lab 2 (Next,
  item 4). Since 2026-10-07, pass 3 opens with the two hardest by the
  survey, likely PH 213 Lab 2 and PH 212 Lab 1 (D-0082). Earlier candidates: PH212 Lab 1 (17 equations, 4 tables, no
  images); Lab Guidance for Students has 9 images and 54 equations
  but is not a lab. The content check must count equations first
  (`docs/conversion-spec.md`).
- Originals' Word metadata names authors (`creator`, `lastModifiedBy`,
  set in the committed PH211 original and the PH212 file): strip before
  committing, and does PH211's history need it (see D-0062)? Strip ruled
  2026-10-07 for every identity part, both repos (D-0086); the
  history question stays D-0062's.
- Not built, for a later ruling: a Word box for the legend and the hint
  arrow (D-0057: `custom-style` misses list items; the arrow would be a
  character in the text). The legend's "arrow" and "Boxed" stay unmet in
  Word until then.
- Downloads: check production on a phone (the four download buttons,
  each file, the PDF footer); the owner does not treat the 2026-10-06 demo
  as a deadline; PR #19 and PR #20 merged
  without a phone check of the preview.
- Open, the owner's: paper or typed reports. Either typed (since
  2026-10-06, a Word report template per lab is the typed path, spec rule
  3.1; the browser-only worksheet is held), or paper handouts completed
  individually during lab, one per group graded at random each week,
  replacing the group lab report. His drivers: peer accountability, answers
  free of AI text, the 1 h 50 min lab, and any outside work moved to
  simulation-based prelabs. He has not decided; the template work is ruled
  separate from this decision (spec rule 3.3), and since 2026-10-07 ships
  either way (D-0074).
- Phase 5 is done, Task 4 included (2026-10-01): migration plan marked,
  CLAUDE.md Deploy rewritten, successor page
  `OSU-lab-ops/lab-handbook/lab-library-site.md` (lab-ops ledger 29).
  Open from lab-ops' hosting plan (driver 3, AI training): Cloudflare's
  AI-training crawler setting has not been checked for `osu-physics-labs`;
  it is a dashboard setting, the owner's to look at.
- D-0051 (actions to current majors) is built after downloads or before, as
  the owner says; it waits on nothing.
- Two design items were deliberately not built, pending a ruling:
  moving the nav into the orange bar (D-0004 mirrors the Physics site), and a
  new hero headline (the mockup's wording was never approved).
- Carried: the D-0012 heads-up to University Marketing; the draft note to
  OSU IT by role (library address, custom domain), offered, never sent; the
  pilot comparison feature and verdict date (spec section 8).

**Measurements (Quarto build, 2026-09-30):** `build/quarto-site/`, built fresh,
served from `build/` over HTTP and measured in the browser pane by
`tools/measure_chrome.js`, which loads each page of both builds in same-origin
iframes at fixed sizes. Page weights come from a script kept in the session
scratchpad, not committed: the page file, every linked stylesheet and script
that exists in the build, and the four WOFF2 fonts, in bytes.
- Old build versus Quarto, computed style and box of 25 chrome and content
  selectors on the six pages at 1440 and 375 px: two rows differ. `.site-foot`
  is missing in Quarto on index.html at 1440 px and at 375 px; that is D-0038
  (the landing footnote is not carried). Nothing else differs.
- Sim bar at 1280x720: bar 34 px, page 720 px, fits: true.
- Phone width 375 px, scrollWidth: 360 on /, /courses/, /how-this-was-made/,
  /sims/, and both ph211 team-building handout pages (modern and faithful).
  The measurement runs in a 375 px iframe whose own vertical scrollbar takes
  15 px (clientWidth 360, innerWidth 375, checked on the landing and faithful
  pages of both builds), so 360 means nothing scrolls sideways.
- Draft banner at 1440 px: 39 px closed, 107 px open, the same on all six pages.
- Landing prose column at 1440 px (`main > p`): left 363 px, right 378 px.
- Contrast, computed from the rendered page with the WCAG formula, the same on
  all six pages: draft banner 11.86:1, site name 4.56:1. Landing hero only:
  title 11.8:1, lead 8.19:1, button 4.56:1.
- Page weights in bytes: `build/site/` page; Quarto page; Quarto first visit (the
  page, every linked file and all four fonts; an upper bound, since a browser
  fetches only the font faces a page uses):
  - landing: 388501; 256206; 1159320
  - course index: 388518; 256359; 1159473
  - how-this-was-made: 387355; 255356; 1158470
  - sims index: 385619; 253568; 1156682
  - modern handout: 396679; 261916; 1169060
  - faithful handout: 395419; 261790; 1167066

**Measurements (2026-09-22):**
- Landing prose column at 1440 px: left 362 px, right 378 px (the 16 px
  difference is the scrollbar). Before centering: 136 px and 643 px.
- Draft banner at 1440 px: 39 px closed, 107 px open. Was 110 px.
- Phone width 375 px: scrollWidth 375 on the landing page with the hero.
- Contrast, computed with the WCAG formula: white on Star Canvas 11.8:1,
  Moondust on Star Canvas 8.19:1, white on Beaver Orange 4.56:1.

**Measurements (2026-09-21, branding refresh):**
- Sim bar at 1280x720: bar 34 px, page 720 px, fits: true.
- Phone width (375 px, scrollWidth <= 375): true on /, /courses/,
  /how-this-was-made/, /sims/, /labs/ph211-team-building-handout/modern/.
- Page weights (largest five, post-font embedding):
  - modern handout: 381 KB
  - faithful handout: 380 KB
  - course index: 373 KB
  - landing: 373 KB
  - how-this-was-made: 372 KB
  - published sim (fonts as data: URIs, no site CSS): 341 KB

**Pilot measures (spec section 6):**
- Spec gaps caught before code: 8. Logo variant versus banner colors
  (D-0013, D-0020); PNG versus ruled SVG (D-0014); off-palette count three,
  not six (D-0008); sim policy blocks fonts (D-0021); orange draft banner
  stacked on orange brand banner (D-0022); copyright wording would assert
  ownership (D-0023); italics and weights 600, 650 and 500 (D-0027);
  base64 data can trip the sim's banned-word check (D-0028).
- Owner corrections: 1. D-0021 flipped: sims may change their font.
- Proposed entries promoted without edits: 4 of 9 reviewed in round 1
  (D-0011, D-0012, D-0014, D-0015); 1 declined without a stated reason
  (D-0017); 4 left proposed (D-0013, D-0016, D-0018, D-0019). Round 2:
  4 of 6 promoted without edits (D-0020, D-0022, D-0023, D-0024); 1
  reversed (D-0021); 1 held for a question (D-0025). Round 3: D-0025 and
  D-0026 ruled; the owner narrowed D-0025 to a Latin and Greek subset.
  Round 4: D-0027 and D-0028 ruled without edits.

**Not built:** the ledger validator (spec section 6, D-0019). Only
`tests/test_brand.py` runs.

**Commits on branding-refresh (7fb7b82..54663d3):**
- `982f860` Palette-only chrome colors (T1)
- `08f9a0c` Luminance draft banner (T2)
- `69f9897` Commit the three official logo files (T3)
- `7af0e13` Header and footer on every site and document page (T4)
- `95b4d87` Slim black sim bar (T5)
- `63714c8` Sim bar logo under border-box fix (T5 fix)
- `20b4462` Self-host Open Sans, subset to Latin and Greek (T6)
- `54663d3` Embed Open Sans in the Electric Force sim (T7)
