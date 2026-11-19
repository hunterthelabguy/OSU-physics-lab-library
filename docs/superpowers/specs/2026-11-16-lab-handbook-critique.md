# Lab Handbook design: hard critique

Status: critique of `2026-11-16-lab-handbook-design.md` (commit 379f6fc) by a fresh reviewer (Claude subagent), 2026-11-16. Read-only review; nothing else changed.
Read: the spec; CLAUDE.md; DECISIONS.md (D-0103, D-0141, D-0143 to D-0145, D-0160, D-0165, D-0168, D-0169, D-0178; D-0176 on branch `question-headings`); LEDGER.md 23; docs/conversion-spec.md; tools/check_unchanged.py, render.py, quarto_build.py, downloads.py, media.py, check_numbers.py, check_em_dash.py, filters/media.lua; .github/workflows/verify.yml; tests/test_downloads.py, test_download_all.py, test_quarto_site.py, test_quarto_chrome.py, test_question_ids.py, test_headings.py; docs/word-labels.json; PH 211 Labs 3 to 7 and PH 212's capstone handout; site/how-this-site-works.md; the instructor repo's review README, PH 211 cut list and ledger entries 51, 54, 55, 56 (read with `git show`). Ran the word and number checks on Labs 3 and 7, and the word check on an in-memory copy of Lab 3 with the cut applied (no file written). No student-identifiable data met.

## Verdict

The direction is right: a converted document checked against Lab 7's Word original is the only option that meets rulings 54.1 and 54.3 and keeps the site's verification claim honest. The spec is not buildable as written. Its trial cannot pass the word check (Lab 3's Linearization section holds five equations, and `ruled_omissions` removes words only), its claim that "everything else is the existing flow" is false for at least eight readers of `source_file`, and the range it proposes must cut five comparison streams, not one, plus a rule for the number check. Fix F1 to F3 by one check feature (a declared span omission that drops words, equations, pictures, drawings and tables together), drop the `sources:` list, and get four owner calls the spec does not yet have (Q1 to Q4) before a plan is written.

## Findings

**F1. The Lab 3 cut cannot pass the word check. Blocks approval.**
Spec 5.4 and 6.5 say the cut passes "with the declared passages". The Linearization section (handout lines 262 to 284) holds five of Lab 3's six equations (`$x$`, `$y$`, `$y = mx + b$`, `$y \propto x$`, `$\propto$`; the check reports "6 equations" for the file today). `ruled_omissions` removes a passage from the word sequence only (`tools/check_unchanged.py` 959 to 969); equations are a separate list compared by count and in order (701 to 704, 1000 to 1003), and `ruled_equations` excuses text, never the count (720 to 746; D-0167 (4)). Simulated in memory with every word run of the cut declared: `equations: original 6, converted 1`, and the five `[equation]` placeholders stay in the original's sequence. Worse, splitting the passage around equations leaves fragments such as "and", which `remove_passage` strips at its first occurrence anywhere in the file (684 to 691); the simulation removed an unrelated "and" earlier in Lab 3 (`insert after ...'make accurate measurements due to equipment': original '' -> converted 'and'`). Why it bites: this is the trial itself, and every later cut hits the same wall (Linearization in C6, C11, C17, C25; the two pictures in the Graphical Analysis tips, C21 and C29). The easy patch, letting omissions skip equations, is exactly the loosening CLAUDE.md ("Never loosen the check for a change") and D-0168 (3) forbid without a ruling. Cheapest fix: one new, ruled check feature, a span omission declared by heading (for example `from_heading`/`to_heading` under `ruled_omissions`), that removes the original's words, equations, pictures, drawings and tables in that span together, each span named and ledgered. It is the same machinery the handbook's range needs (F3), so it is one feature, not two.

**F2. "Everything else is the existing flow" is false; the nested `sources:` key breaks or hides the handbook from at least eight readers. Blocks approval.**
Spec 5.1 and 6.2 name only `render.converted_documents` and CI's selection. What reads `source_file` at the top level of front matter:
- Loud: `tools/media.py` 101, `doc["meta"]["source_file"]`, runs for any document with images (the handbook has two), so `quarto_build.generate()` (line 85) raises KeyError. `tools/check_numbers.py` 225, `doc["meta"]["source_file"]`, raises KeyError once CI selects the file. `tests/test_quarto_chrome.py` 116 (lab page count against the regex `converted()`) and 447 to 450 (published Markdown) fail.
- Silent: `tests/test_quarto_site.py` 30 to 35 finds converted files by the regex `^source_file:`; an indented `  - source_file:` does not match, so the page test and about 30 tests in `tests/test_downloads.py` that iterate `converted()` (the HTML cap at 531 to 536, self-contained HTML at 473 to 481, Word footer, page size, byte-for-byte Markdown) skip the handbook and stay green. `tests/test_question_ids.py` 51 to 54 uses `check_em_dash.converted()` (`line.startswith("source_file:")`, 35), so the handbook needs and gets no pin. `.github/workflows/verify.yml` 54 greps `^source_file:`.
Why it bites: the silent half is a repo lying about its verification (charter floor 2): tests pass that never ran on the new page. Cheapest fix: delete the list. A2 is a future consumer with no target date and no check, which the owner's 2026-10-09 rule on one-consumer abstractions excludes; none of A2's three documents is even in the repo. Keep `source_file` and `source_sha256` at the top level and add one key for the span (or use F1's span omission and add no key). Every reader above then works unchanged except the two checks.

**F3. A range must cut five streams, and the number check needs its own rule. Blocks approval.**
Spec 6.1 says the check takes "the original's content from `from_heading` to the end" and compares "words, bold, equations, pictures". `docx_content` (259 to 456) returns a flat character stream with no paragraph or heading boundaries, plus separate lists of equations, pictures and drawings; `word_tables` (833 to 851) reads every table in the document. Lab 7's original holds four `w:tbl`, and its converted file a two-column table at line 79, before Appendix B, so a words-only range fails `tables of more than one column: original 1, converted 0` (count inferred from the converted file; not run). Lab 7 happens to hold all five equations and both pictures inside Appendix B (the check reports 5 and 2 for the whole file), so a range that forgot equations would still pass here and break on the next source. The number check finds Lab 7's record by `parts_sha256` (check_numbers.py 233 to 235) and must place all 30 of its labels (verified run: "11 questions, 0 checkpoints and 19 parts"); the handbook has none, so it fails. `docs/word-labels.json` records anchors with no position, so a range cannot select labels. D-0168 (3) says both checks "keep running on every converted file, unchanged". Cheapest fix: the spec states that the span cuts words, bold, equations, pictures, drawings and tables; 6.1's fixture puts an equation, a picture and a two-column table before the heading; and the number check gets a D-0160 (4)-style rule (a document checked against part of an original may hold no question, checkpoint or `.numbered` block, and the ok line says so), ruled as an amendment of D-0168 (3).

**F4. The handbook folds a wording change into its own conversion. Fix before plan.**
Spec 5.1 creates the file with `status: ruled-change`, the new title and opening line, and omissions, in one step. D-0168 (1): "only after that handout's format-only conversion has landed: a change never folds into a conversion"; the charter's focus thread repeats it. Cheapest fix: two PRs. First the span conversion, `status: converted`, keeping Appendix B's heading, lead-in and list. Then the ruled change: title, opening line, the omitted lead-in and list, `ruled-change`. Or the owner rules an exception in words.

**F5. The handbook is a second copy of content, and the spec does not say so. Fix before plan.**
CLAUDE.md (Build): "One Markdown source feeds one presentation [...] never copy content into a second file." D-0144 read that rule as covering lab content and amended it "for `sandbox/` only". The handbook's Markdown repeats Lab 7's Appendix B Markdown (and Labs 4 to 6 section by section) until those cuts land; Lab 7's waits for D-0141's pass, "after all other pending work", with no date. Spec 4.7 deletes a different copy and is silent on this one. Mitigation that is real: every copy is checked against a Word original, so words cannot drift without a declared, ruled change. Cheapest fix: a proposed entry amending the rule for the handbook with an end condition (Lab 7's appendix cut), and a rule that a ruled change to a handbook section is applied to the remaining appendix copies in the same PR.

**F6. A1 is load-bearing, and the draft opening line asserts something the record contradicts. Fix before plan.**
`course: PH21X` lists the page under "For every course" (render.py 323 to 339), so PH 212 and PH 213 students meet PH 211's text while their own appendices differ. Checked on PH 212's capstone: Required Plot Elements and What is Uncertainty? match; Sources of Uncertainty differs in list form and items; Linearization differs (PH 212 ends "the other variable?" where PH 211 ends a question with "variable.", and emphasises *function*), so the "general" handbook publishes the uncorrected sentence. The draft opening line (5.1) says the ideas "are used in every PH 21X lab": PH 211 Lab 1 contains no "lineariz" or "uncertaint", Lab 2 no "uncertaint" (grep counts). Fix: the owner rules A1 before build (Q1); the opening line makes only a claim the record supports.

**F7. The D-0141 amendment rests on an unconfirmed reading. Fix before plan.**
Spec 9.4 proposes that "the rail leaves the capstone pass", and 5.2 builds stable deep links, part of D-0141 item 3, ahead of the "one design, specced and critiqued together". Instructor ledger 55: the question "Pull the table of contents forward, ahead of the capstone pass?" "got no direct answer [...] which Claude reads as a yes, to be confirmed". Section 3 lists four assumptions and omits this fifth. Fix: add it as A5 and ask (Q3).

**F8. The link mechanism overstates "every output" and misses three failure modes. Fix before plan.**
(a) The Markdown download is the source byte for byte (`downloads.markdown`; test_downloads.py 184 to 188), so it keeps `ph21x-lab-handbook#linearization`, which resolves to nothing. D-0165 (2) kept relative Markdown links because they work "inside the course zip"; this one does not, and the handbook is in no course zip at all: the course download lists `render.converted_labs`, which reads `site/courses.md` (render.py 160 to 162; test_download_all.py 63 to 68), where a PH21X document is not listed. Spec 6.6's question about "the course-wide page's place in that count" has the answer: none. (b) Every output, the page included, links at `render.LIBRARY_URL` (`https://osu-physics-labs.pages.dev/`, render.py 40), so a PR preview's Lab 3 links to production; if Lab 3's cut reaches main before the handbook, students get a 404. Bind the order: the handbook lands first. (c) A printed Lab 3 shows two underlined names and no address; with ruling 55.4 (no printed copies), the words "Lab Handbook" are a paper reader's only route. Validation: `media.lua` knows no document ids or page anchors (129 to 135); 5.3's build-time failure needs new metadata plumbing. Cheaper: a unit test that scans curriculum sources for `<id>#<anchor>` links and checks each against `converted_documents()` and the target's explicit ids.

**F9. Per-document parts the precedent carries are missing. Fix before plan.**
D-0160 (1) gave the course-wide strategy "an HTML cap" and "an empty question-id pin". Spec 6 has neither. `HTML_CAPS` (test_downloads.py 440 to 460) fails a document without a cap once F2 is fixed; CLAUDE.md says to measure and add it. Add both to 6.6.

**F10. The span's edges are undefined. Fix before plan.**
5.1 says the range runs "from that heading", and the front-matter comment declares only "the appendix's own lead-in and numbered list" as omissions. Either the heading paragraph "Appendix B – Reference Information" is outside the range or its three words must be omitted too. State which, and test it.

**F11. The heading promotion is justified by a rule that does not exist. Note.**
5.1 calls promoting "Predictions, Hypotheses, and Models" "the same [format call] the conversion made for titles". conversion-spec.md "Pass 3 additions" maps Word heading styles only; in Lab 7's original that paragraph has the default paragraph style, and the conversion kept it as `**[...]{.underline}**` (capstone line 350). The word check is blind to the change (heading bold is exempt, check_unchanged.py 13 to 14 and 987). The real reasons are better: `tests/test_headings.py` fails any new file that skips a level, so level 2 under `#` is required, and a styled pseudo-heading becoming a real one is a WCAG 1.3.1 gain. Say that, and put it to the owner as a format call.

**F12. Bold in the new lead-in and opening line sends the graded-item signal. Note.**
A4's "**Read the Lab Handbook.**" and 5.1's "**Read this first.**" are bold sentences outside any question. LEDGER 23: the curriculum "teaches students that bold marks what they must answer in the graded report". The ledger also says the owner may revisit the convention in this phase, so this is his call (Q6), not a defect.

**F13. Ledger statuses and one date. Note.**
D-0160, D-0165 and D-0168 are `status: proposed`; 4.4 says D-0165 "ruled the answer", and the spec leans on all three. D-0168's date field is 2026-11-06, not 2026-11-07. Promote them or say "proposed".

**F14. "Trial" has no pass criterion. Note.**
Section 1 says the build measures nothing; cut list call 5 calls Lab 3 "the trial of the mechanism". Name what passing means before Labs 4 to 6 (for example: verify green, the owner's Word and Google Docs check of the Lab 3 download, both links resolve on production). When students next use Lab 3 is UNVERIFIED (the term calendar is outside the folder this review may read).

**F15. The public verification sentence becomes loose under a range. Note.**
"How this site works": the check "passes only if the words match the original apart from the listed passages". A range passes the handbook with everything before Appendix B neither present nor listed. A declared span omission (F1) keeps the sentence literally true; a range needs a sentence on the page, which is new public wording.

**F16. The handbook pins Lab 7's original by hash. Note.**
If the capstone restructure (D-0141 item 1) replaces `originals/PH211/Lab 7 - Capstone - Handout.docx` in place, the handbook's check fails. Lab 7's own Markdown cut later does not affect it. Bind it in section 8.

**F17. Em-dash scan. Note.**
With a top-level `source_file`, `check_em_dash.converted()` skips the handbook, including its new title and opening line (D-0103's skip keys on `source_file`). Lab 6's ruled additions have the same gap today. No em dash is in the range now (the Lab 7 original has none).

## Premise table

| Spec claim (section) | Verdict |
|---|---|
| 30 passages, 3,762 words, 19% of PH 211 (1) | Confirmed against the cut list (C1 to C30; 337+577+734+1,059+1,055 = 3,762; 3,762/19,889 = 18.9%). repeats.py not run |
| Owner quotes, rulings 51, 54, 55, 56 (2) | Confirmed word for word against instructor ledger |
| `converted_documents` takes only files with `source_file` (4.1) | Confirmed, render.py 135 |
| check_unchanged compares whole file with whole original (4.1) | Confirmed, 919 to 1016 |
| PH21X documents get "For every course", a page and four downloads, no new code (4.2) | Confirmed for listing, page and downloads (render.py 323 to 339; quarto_build.py 115 to 144); not in any course zip |
| Three headings carry an explicit id kept from a Word bookmark (4.3) | Confirmed (Lab 4 line 240; Lab 5 lines 300, 324); Pandoc reads `{id="..."}` as the identifier (probed). A fourth exists in PH 212's capstone, line 142 |
| D-0165 ruled every output links at the library's address (4.4) | Partly wrong: D-0165 is proposed, and it keeps the Markdown download's link relative |
| Appendix copies agree except two pictures' alt text (4.5) | Mostly confirmed (Labs 3 to 7 Markdown diffed); Labs 6 and 7 also differ in the icons' Word size, 0.1437 against 0.1417 in, and one trailing period; image bytes identical |
| Lab 7's Appendix B holds all seven (4.5) | Confirmed, capstone lines 284 to 378 |
| D-0141 item 3 wording (4.6) | Confirmed, DECISIONS.md 1544 |
| D-0143 to D-0145: sandbox, "only through the wording-change phase", bench and phone wording, capstone earmark (4.6) | Confirmed (1566, 1567, 1577, 1588); D-0143 to D-0145 not built |
| D-0168 dated 2026-11-07 (4.6) | Wrong: entry dated 2026-11-06, status proposed |
| "Everything else [...] is the existing flow. One new feature" (5.1) | Wrong: F2, F3 |
| `status: ruled-change` per D-0178 (5.1) | Confirmed, D-0178 (1) |
| Predictions heading is "the same [call] the conversion made for titles" (5.1) | Wrong: F11 |
| Opening line "used in every PH 21X lab" (5.1) | Contradicted by grep counts: F6 |
| media.lua already has `library-url` (5.3) | Confirmed, 109 and 129 to 135 |
| The build fails on an unknown id or anchor (5.3) | Not existing; new plumbing needed, F8 |
| Lab 3 rows C1 to C3, 337 words; lines 242, 251, 262 (5.4) | Confirmed in handout and cut list |
| `.numbered` with anchors `o14.0.1 o14.0.2`; Word's labels still match (5.4) | Confirmed (handout 246; word-labels.json labels "1." and "2."); check_numbers compares markers only |
| Line 198 points at the Error Bars appendix (5.4) | Confirmed text; reading plausible |
| The word check passes Lab 3 with declared passages (6.5) | Wrong: F1, simulated |
| Accessibility: link text names the section; real headings; Word's alt text; same tab (5.5) | True of what would be built, once F11's promotion is made; 2.4.4 met by link text |
| Download count question (6.6) | Answered: course-wide documents are in no course download, F8 |
| Stretch survey 76 to 94% of an appendix (7) | Confirmed, D-0143 rationale |
| PH 212 drift: two of four sections match (8) | Confirmed on PH 212's capstone; PH 213 not compared |
| `OSU-lab-ops/lab-handbook/` exists (7) | UNVERIFIED; stated in instructor ledger 55 only |
| D-0176 decides a page's headings (8) | Confirmed exists, on branch `question-headings`, not on main |

## Options for 5.1

1. **Do nothing.** Appendices stay. Cost none. Fails ruling 54.1 and keeps 19% repeated text. Rejected by the record.
2. **Do less: no handbook; Lab 7 keeps the full appendix, Labs 3 to 6 link into it.** Put to the owner and not chosen (54.1). Also fails on its own terms: D-0141's pass will cut Lab 7's appendix and kill the links, and every cut still hits F1.
3. **The spec: a range under a `sources:` list.** One check feature as claimed, but in fact a list type eight readers do not understand (F2), a range across five streams (F3), a number-check rule, and still F1 for every cut. Highest cost of the viable options for no present benefit.
4. **Flat `source_file` plus `from_heading`.** Same as 3 without the list; every existing reader works. Still needs F3's five-stream range, the number-check rule, and separately F1's span omission for the cuts. Two check features.
5. **One span-omission feature serving both (recommended).** The handbook is a converted document of Lab 7 (`source_file` flat) that declares one ruled span omission, from the document's start to the Appendix B heading, plus its title and opening line; each appendix cut declares its spans the same way. One check feature, ruled once, used by all 30 rows; the public sentence in F15 stays true; F2 disappears. Still needs the number-check rule (F3). Failure mode: a span keyed by heading text cannot start at a styled pseudo-heading such as "Predictions, Hypotheses, and Models"; the cut list's rows C14, C20 and C28 start there and need either a `to_heading` on the next real heading or a word passage, which works because those spans hold no equations or pictures (Labs 5 to 7 Markdown).
6. **A new small Word original: Lab 7's docx truncated to Appendix B by the owner in Word, stripped and committed.** No check feature for the handbook. Costs a Word labels read (D-0102) for the new file's `parts_sha256`, a derived original whose fidelity to Lab 7 rests on one hand edit, and it does nothing for F1. Worth it only if the owner wants no check change at all and accepts that the cuts wait.
7. **A hand-written `site/` page.** No check and no downloads without new code; fails 54.3 and floor 2.

Verdict on the spec's recommendation: right family, wrong shape. Take option 5; option 4 if the owner prefers a range to a declared span.

## Questions only the owner can answer

1. **A1: list the handbook "for every course" now, with PH 211's text?** Recommend yes, as "general" asks, with the PH 212 and PH 213 differences ruled as rows before their cuts. Cost of the alternative (PH 211 only): no listing exists for a non-lab PH 211 document, so new code, and a rename later.
2. **The check: one ruled span-omission feature that drops words, equations, pictures, drawings and tables in a declared span, and a number-check rule that a span document holds no numbered blocks?** Recommend yes, as an amendment of D-0168 (3) recorded like D-0167. Cost of no: no section with an equation or picture can ever be cut, which is 7 of the 30 rows (the five Linearization rows C3, C6, C11, C17, C25 and the two Tips rows C21, C29).
3. **D-0141: do stable section addresses for the handbook go ahead of the capstone pass, and does the rail leave it?** Recommend yes for the addresses, rail as its own spec. Cost of no: the handbook's anchors wait for the pass "after all other pending work".
4. **Land the handbook in two steps under D-0168 (1), or rule an exception?** Recommend two PRs; the cost is one extra review. An exception sets the first precedent of a change folded into a conversion.
5. **Amend "never copy content into a second file" for the handbook until the appendices are cut?** Recommend yes with the end condition in F5. Cost of no: the handbook waits for Lab 7's appendix cut, which waits for D-0141's pass.
6. **Bold on the lead-in and opening line?** Recommend plain text, emphasis in the words, keeping LEDGER 23's signal intact until you revisit it. Cost of bold: students read "Read the Lab Handbook" as a graded item.

## Not checked

- Quarto's handling of a `<id>#<anchor>` link target before the filter rewrites it, and whether its link checker warns; UNVERIFIED.
- Where the current build puts heading ids: observed on `h2`/`h3`/`h4` in a local build under `OSU-physics-lab-library/build/` of unknown date, not rebuilt.
- The table-count failure in F3 was inferred from the code and the converted file, not run; F1 was run in memory.
- `repeats.py` and `audit.py` in the instructor repo were not run; the cut list's 125 against 121 words for the two Graphical Analysis copies is unexplained by my diff, which found only the alt text and size lines differ.
- PH 213's appendices were not compared with PH 211's.
- The term calendar (when Lab 3 next runs), the staff `OSU-lab-ops/lab-handbook/`, Word and Google Docs rendering, and any screen-reader run.
