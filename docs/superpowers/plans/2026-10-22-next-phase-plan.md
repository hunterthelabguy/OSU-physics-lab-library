# OSU-physics-lab-library: PR status and next-phase plan

Planned 2026-10-22, read only. Sources: `git fetch` (origin/main at `9841f7a`,
2026-10-17), `gh pr list/view/checks`, `gh run list --branch main`, `STATE.md`,
`DECISIONS.md` (D-0141 to D-0155), `LEDGER.md` 10, 11, 20, 22,
`docs/agent-reference.md` (Course pages; Converting a handout),
`tools/check_unchanged.py`, and the transcripts of the three named sessions
(read with the session tools: last 40 messages of each, plus searches). Nothing
in any repo was changed.

Note added at landing, 2026-10-22: the lab-ops inventory that section 5 calls
untracked has since landed (OSU-lab-ops `5e1408c`, ledger 31), with Q-03
corrected to name #61. The force plate ruling's words, for section 4's
placeholder: "that's almost certainly a force plate, so we can continue with
that assumption for the inventory and have it earmarked when I work on the
library next."

## 1. PR status

Only one PR is open. Five from the queue session's pass 5 merged on
2026-10-17; none closed unmerged since 2026-10-15.

| PR | Title | Branch | CI (`gh pr checks`) | Mergeable | Waits on | Blocked by |
|---|---|---|---|---|---|---|
| #61 | PH 213 Lab 6: Capstone (pass 5; held for the owner's Word check) | `pass5-ph213-lab6` (head `a22fa6b`) | verify pass (8m6s), deploy pass (46s), at head `a22fa6b` | **CONFLICTING** (`DIRTY`) | **Hunter**: his Word and Google Docs check (D-0090, D-0149 call 3) | Conflicts in `tests/question-ids.json` and `tests/test_downloads.py` (`HTML_CAPS`) only, from #62 to #66 merging after its base `c67c0ad`; `site/courses.md` auto-merges (`git merge-tree`, no tree touched). Mechanical: take main's files, re-insert Lab 6's ids and cap in sorted order (recipe, "Merging in sequence"). After the rebase CI runs again, so green is not yet proven on the rebased head. |
| #62 | PH 213 Lab 5 | `pass5-ph213-lab5` | merged 2026-10-17 17:34Z | | | |
| #63 | PH 213 Lab 3 | `pass5-ph213-lab3` | merged 17:50Z | | | |
| #66 | Download tests: checkpoint boxes, nested contents items | `pass5-checkpoint-tests` | merged 18:00Z | | | |
| #65 | PH 213 Lab 4 | `pass5-ph213-lab4` | merged 21:05Z | | | |
| #64 | PH 213 Lab 1 | `pass5-ph213-lab1` | merged 21:14Z | | | |

What Hunter checks in #61 (from its body): Word's "0)" shown as Checkpoint 1
then Questions 1, 2, a restart to 1 to 5, Checkpoint 2; the landscape Rubric
section; the contents as 11 links; Appendix C in one column. Preview:
`https://pass5-ph213-lab6.osu-physics-labs.pages.dev/labs/ph213-capstone-handout/`
(`.docx` and `modern/`); not re-fetched today, so whether the preview is still
served is unverified. Observed in #61 and not changed: Appendix D missing from
the contents field; typos "Light senor", "You instructor"; presentation length
"five or six minutes" (Week 2) against "about five minutes" (Week 3).

Merge order: #61 is the only queue item, so it goes first, alone. Any PR this
plan adds (section 3, pass A) merges after it, one at a time, each after
main's run for the previous merge reports green.

Housekeeping, not blocking: six worktrees remain under `.superpowers/sdd/`
(`pass5-lab1`, `-lab3`, `-lab4`, `-lab5`, `-lab6`, `-tests`); five are for
merged branches. Old local branches `ledger-pilot-branding` (7 commits,
2026-09-21) and `site-tokens-and-print` (2, 2026-09-22) show as unmerged only
because squash merges leave the originals behind (inferred from dates and
subjects, not diffed). Removing either is a deletion: owner's word.

## 2. Main's deploy health

All 12 most recent `main` runs succeeded, the newest `39071180042` for
`9841f7a` (D-0151 to D-0155 and STATE), 10m16s, jobs `verify` and `deploy`
both success. No push to `main` since 2026-10-17 21:29Z, so nothing unread.
No failure to report.

Live defect in production, found by the queue session's late D-0090 review,
not by CI: PH 213 Lab 4's drawn figure (merged in #65) draws black on the page
with no background, about 1.2:1 in dark mode, failing WCAG 1.4.3 (text) and
1.4.11 (lines). Light mode and print are fine. Its fix awaits Hunter
(decision 2).

## 3. Proposed next phase, in order

What the record says is next. STATE: pass 5 ends when #61 merges after
Hunter's check; the stretch sandbox (D-0143 to D-0145, spec
`docs/superpowers/specs/2026-10-15-stretch-sandbox-design.md`) "waits until
pass 5 is done" (owner, 2026-10-17), its next steps writing-plans, an
executing critique, `/build`. D-0082 then has pass 6 (Word report template per
lab; D-0074, D-0080: after all conversions, Winter 2027 target that slips if
conversion does) and pass 7 (cross-reference against instructor notes and
rubrics, run from an instructor checkout; D-0083). D-0141
earmarks the capstone restructure, web-only rubric and page table of contents
as one pass "after all other pending work". The queue session's intent was
pass 5 as "next up in the queued work"; it ended with two things on Hunter:
the #61 check and the dark-mode figure call.

The other two sessions active today work only in
`OSU-physics-lab-library-instructor` (PH 212 capstone rework:
`reviews/2026-10-20-ph212-capstone-rework/`, instructor LEDGER 12 to 16, head
`6d16c9d`). Both state the library repo is untouched and read only, and
nothing in it is ruled (incline coast lab, resistive-law lab, fixed quantity
per table are proposals). No collision with passes A to D. The rework is
input to pass E (D-0141), and it bears on the sandbox's PH 212 capstone copy
(D-0145): the copy is a hashed fork, so a later rework does not break it, but
it would stop representing the course's handout.

**Pass A: clear the queue (one session, main session; no subagent).**
1. On Hunter's Word check of #61: rebase on main, resolve the two shared-file
   conflicts by taking main's and re-inserting Lab 6's entries, CI green,
   squash merge, read main's run. Append its hash entry (next free number;
   both hashes are in #61's body: original
   `d78901da6ec06fc2f1c184d6cabff469e715db68ccbb2042ff9302290998a000`,
   stripped `85f3878c4886976fc096b3ec1feded06a52604d15e5630cdac18a6d247b41d2d`). STATE: pass 5 complete, 19 labs.
2. If ruled (decision 2): a tool PR, `svg.drawn-figure { background: #fff }`
   in the theme, measured against the HTML download at 375 and 1440 px and in
   dark mode; merge; read main's run; its entry.
3. The force-plate PR (section 4); merge; read main's run.
4. Ask for promotion of D-0151 to D-0155 (paste each in chat) and the new
   entries; STATE refresh.
Depends on: Hunter's check (1), his call (2), his ruling of section 4 (3).
Steps 2 and 3 do not depend on 1 and can be prepared while the check is
pending, but merge after it.

**Pass B: build the stretch sandbox (one to two sessions).** writing-plans on
the ruled spec, the executing critique, then `/build`. Sonnet subagents fit
the plan's independent tasks (`tools/sandbox.py`, `tools/filters/stretch.lua`
and its five build rules, the sandbox course data and page, tests); the main
session keeps the shared files, the ledger and the measurements (44 px
control, 375 px, PDF all open). Depends on pass A step 1 (owner's ordering).

**Pass C: pass 6, the Word report template per lab (two sessions).** Session 1
by hand: the template generator on one or two labs, D-0079's probe parameters,
the owner's check. Session 2: one Sonnet subagent per course generating and
checking the remaining labs, the main session reviewing. Depends on every
conversion landed (#61), per D-0080. The open paper-or-typed decision does not
block it (D-0074).

**Pass D: pass 7, the cross-reference (one session).** From a checkout of the
instructor repo, per lab: rubric "Qn:" text and notes' question numbers
against the converted handout. One Sonnet subagent per course fits; findings
go to a named file in the instructor repo. The PH 213 capstone's instructor
notes and rubric (`Lab 6 - Capstone - Instructor notes.docx`,
`Lab 6 - Capstone - Rubric.xlsx`, seen by file name only) enter here, not in
the library.

**Pass E: D-0141's capstone pass (spec plus build, two or more sessions).**
The three capstones (PH 211 Lab 7, PH 212 Lab 6, PH 213 Lab 6) share one
skeleton ("List of Previous Labs in the PH 21X Curriculum", the equipment
appendix, the three-week shape), so they restructure together. Depends on:
all three on main (#61); Hunter's rulings on the PH 212 rework's proposals;
LEDGER 11 (the AI-use standard for the content-change phase, still open);
the PH 213 capstone material he is bringing (section 5). Opus for the spec and
critique; Sonnet for the build's independent tasks.

Order rationale: A unblocks everything and closes a live WCAG failure. B
before C follows the owner's own sequencing of the sandbox after pass 5 and is
already specced and ruled. If Winter 2027 is at risk, C can go before B
(decision 6).

## 4. The force-plate fix

Confirmed in the committed original: `unzip -p` of
`originals/PH211/Lab 7 - Capstone - Handout.docx`, `word/document.xml`
stripped of tags, reads "... Photogate Accelerometer Force pla Appendix B –
Reference Information". The converted file
`curriculum/ph211/ph211-capstone-handout.md` carries it at line 281 ("- Force
pla", last item of the `::: action` list under "[Electronic data taking
(Vernier)]{.underline}"). "Force plate" also sits at line 269, under "Other
items:". No other converted lab carries "Force pla".

**Completion, not de-duplication.** Change "Force pla" to "Force plate" and
leave the "Other items" entry alone. Reasons: Hunter's ruling says what the
cut word is, not that the item is redundant; three added letters is the
smallest content change, while deleting an item edits the author's list and
silently picks which category is right. Evidence on the category cuts both
ways: a Vernier force plate is an electronic sensor (fits the Vernier list),
yet PH 213's sibling capstone (#61, Appendix C) lists "Force plate" once,
under "Other items", and no force plate under Vernier. Whether the lab owns
one kind or two is an inventory fact (lab-ops Q-09) that the walk will
settle. The duplicate is recorded as observed, not changed, for pass E, where
the appendix will be rewritten anyway.

**How it lands.** Precedent: no wording of an original has been changed so
far. Typos were recorded "observed, not changed (for the content-change
phase)" (LEDGER 22c), D-0103 declined a ruled dash change as a content change,
and the only declared departures are D-0133's redaction markers in
`ph212-extending-a-model-handout.md`. The mechanism exists for exactly this:
`check_unchanged.py` allows a difference only when declared in front matter
(`ruled_omissions`, `ruled_additions`), each with a ledger reference, and
fails a stale declaration. The original stays untouched (LEDGER 10; its hash
and `source_sha256` unchanged).

One trap: `remove_passage` removes the first occurrence. A bare
`ruled_additions: "Force plate"` would remove line 269's item, and the word
diff would then fail. So both declarations carry the preceding word:

```yaml
ruled_omissions:
  - text: "Accelerometer Force pla"
    ledger: "D-NNNN"
ruled_additions:
  - text: "Accelerometer Force plate"
    ledger: "D-NNNN"
```

and line 281 becomes `- Force plate`. Read from the source: with both
declared, both sides reduce to "... Photogate Appendix ..."; unverified by
running, since this job could write only this file. Run the word and number
checks before the PR. Lands as its own PR (converted content, charter floor 4),
not direct to main. No effect on `tests/question-ids.json`, `HTML_CAPS`
(three bytes under a 1.10 cap) or the number check (an action bullet carries
no label).

Proposed entry (number from the file's last at append time; D-0156 if it
lands before #61's hash entry). Hunter's exact words are not in any file I
read; the rationale line holds a placeholder for his verbatim quote.

> ### D-NNNN  PH 211 Lab 7's "Force pla" is completed as "Force plate": the conversion's first ruled change to an original's words
> - status: proposed
> - proposed-by: claude
> - date: 2026-10-22
> - decision: In `curriculum/ph211/ph211-capstone-handout.md`, Appendix A, the last item of the "Electronic data taking (Vernier)" list reads "Force pla", a truncation present in the original (`originals/PH211/Lab 7 - Capstone - Handout.docx`, whose `document.xml` reads "Accelerometer Force pla" before the Appendix B heading), not a conversion error. The item becomes "Force plate". It is a completion: three letters added, the item kept in its list; the "Force plate" item under "Other items" is left as it is. The front matter declares the change as `ruled_omissions` "Accelerometer Force pla" and `ruled_additions` "Accelerometer Force plate", each citing this entry; both carry "Accelerometer" because the word check removes a declared passage's first occurrence and "Force plate" already occurs under "Other items". The original and its hash are unchanged (LEDGER 10). Observed, not changed, for D-0141's capstone pass: a force plate is listed twice in the appendix, and PH 213's capstone lists it once, under "Other items".
> - rationale: The owner, 2026-10-22: "[verbatim ruling to be quoted]". Context (Claude): the truncation is in the original, so the conversion carried it faithfully; the lab-ops inventory already carries the item as a force plate (`OSU-lab-ops/inventory/ph21x-source-discrepancies.md`, Q-09). LEDGER 11's standard for drafted wording does not arise: the completed word is the owner's.
> - alternatives: de-duplication, deleting the Vernier list's item (a larger edit that picks a category the record does not settle); held for D-0141's capstone pass (leaves a broken word on a published page meanwhile); editing the committed original (breaks LEDGER 10 and the survey's hash).
> - binds: LEDGER 10; LEDGER 11; LEDGER 22; D-0103; D-0133; D-0141; curriculum/ph211/ph211-capstone-handout.md
> - test: CI's word check on the lab passes only with both declarations; either one alone, or a stale one, fails.

## 5. The PH 213 capstone: timing

Premise check: "the library has five PH 213 labs and no capstone" is true of
`main` only. The PH 213 capstone handout is converted and waiting in #61
(`curriculum/ph213/ph213-capstone-handout.md`, its stripped original
`originals/PH213/Lab 6 - Capstone - Handout.docx`, 4 pictures, a landscape
rubric, Appendix C's equipment list of about 85 items without quantities or
shelf locations). `site/courses.md` already lists PH 213 Lab 6 "Capstone",
"Three-week project ...", under "Not yet converted". The sentence and Q-03's
question "Is there a PH 213 capstone handout the library has not taken in?"
come from the lab-ops discrepancies file, which missed #61. That file sits in
`OSU-lab-ops/inventory/`, which `git status` shows untracked (charter floor 12:
not landed).

So the handout comes in at pass A step 1, gated only on Hunter's Word check.
What else "the PH 213 capstone material" can mean, and where each kind goes:
- the equipment list with legacy shelf locations (the handbook's "one working
  list", lab-ops Q-03): lab-ops inventory, not the library;
- the instructor notes and rubric (in the old materials by file name): the
  instructor repo, pass 7 (pass D);
- `Lab 6 Capstone - Example presentations` (folder name only, not opened):
  likely student work, so FERPA-gated; not imported without a ruling;
- a revised handout of his own: a content change, input to pass E with the
  other two capstones and the PH 212 rework, never a re-conversion over #61.

## 6. Decisions for Hunter

1. **Word and Google Docs check of #61.** Lean: do it now; it gates pass 5's
   close, the sandbox, the template pass and the capstone pass.
2. **Lab 4's figure in dark mode.** Lean: white background on
   `svg.drawn-figure` (Word's paper, 21:1), as the queue session proposed;
   recolouring departs from Word's colours. It is a live WCAG 1.4.3 and
   1.4.11 failure.
3. **Force plate: completion or de-duplication.** Lean: completion (section
   4); the duplicate goes to pass E.
4. **Force plate: now, or held for pass E.** Lean: now, through the declared
   difference the check already supports; it is the first ruled content change
   of the conversion phase, and the entry says so. Cost of holding: a broken
   word on a published page for a pass with no date.
5. **What the PH 213 capstone material is.** Lean: treat #61 as the library's
   capstone handout and route the new material by kind (section 5). The
   example presentations stay out until you rule.
6. **Sandbox (pass B) before the template (pass C), or the reverse.** Lean:
   sandbox first, your own ordering, and it is ruled and specced; swap if
   Winter 2027 for the templates looks tight.
7. **Promote D-0151 to D-0155** (four hash records and #66's test fix, all
   proposed 2026-10-17). Lean: promote; each records what D-0086 orders, and
   D-0155 is a tests-only fix CI proved.

Not verified: the #61 preview still served; Hunter's verbatim force-plate
words; the force-plate declarations by running the check; the two September
branches' content against main.
