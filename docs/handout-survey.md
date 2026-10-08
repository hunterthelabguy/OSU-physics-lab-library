# Handout survey: pass 1

Status: measured and read 2026-10-07 (pass 1, D-0082, D-0085). The table and
counts are facts about the originals. Ruled the same day ("I agree with all
your leans"): the leans of sections 3, 6, 7, 9 and 10 stand as written, and
the markup rules moved to `docs/conversion-spec.md` (D-0100 to D-0107). Where this file and
`DECISIONS.md` differ, the ledger wins. The path is Claude's proposal; D-0085
names no file.

This file holds nothing drawn from instructor notes, rubric workbooks or the
course-wide "Lab Guidance for Instructors" (spec 9.7, D-0081). It holds no
person's name, no link target and no originals path beyond the spec's
relative one.

## 1. Scope and method

**Files read.** These are the files D-0084 clears, under `../Old Reference
Material/21X Lab Curriculum/`:

- the 19 handouts: PH 211 Labs 1 to 7, PH 212 Labs 1 to 6, PH 213 Labs 1 to 6;
- the three curriculum summaries, PH 211's having been read already on
  2026-09-19 (LEDGER 45);
- the four course-wide files.

Nothing outside that list was opened. No reader met anything resembling a
student record. Each reader's prompt said to stop and report only the file
and location if it did; none stopped.

**Machine counts** come from each original's Word XML, read by scripts kept
in the session scratchpad and not committed, as STATE's page-weight script
was. Every count below is the XML's:

- **Hash and dashes.** SHA-256 of the file; U+2014 in `w:t` and `m:t` across
  every `word/` part.
- **Numbering.** Word's numbering is read from `numPr` and `numbering.xml`.
  A paragraph's list and its level are inherited separately through the style
  chain.
- **Objects.** Equations are counted as `m:oMath`, display ones being those
  inside `m:oMathPara`. Pictures are `w:drawing` elements, and alt text is a
  non-empty `wp:docPr descr`. Tables are `w:tbl`, text boxes `w:txbxContent`.
  Shapes (`wps:wsp`, `wpg:wgp`), fields, content controls, header text and
  hyperlink hosts were counted too.
- **Identity parts**, D-0086's list, are recorded as present or absent, never
  their values.

"Pandoc" throughout means Quarto's bundled Pandoc 3.10 (D-0044).

**Reading.** Four Sonnet readers (PH 211, PH 212, PH 213, course-wide) read
Pandoc Markdown extractions in full, with a fixed output format. Each
paragraph that Word numbers in a question list carried an anchor, as follows:

- `o7` is the seventh top-level paragraph of the question lists in document
  order.
- `o7.2` is the second level-1 paragraph under it, and `o7.2.1` a level-2 one.
- `xN` is a bold numbered paragraph in some other list.
- `BN` is the Nth bold paragraph that is neither numbered nor a heading, in
  that handout's order.

Anchors are positions, not Word's labels. Where a handout's numbering is
simple (section 3), `oN` is Word's "N)". The readers classified every
anchored item and B paragraph. Their reports were read in the main session;
the structure codes below are theirs, checked against the counts.

## 2. The table

Key:

- "Word's question list" counts its top-level paragraphs and its parts
  (levels 1 and 2).
- "D-0078" gives the verdict ("simple" when no counted feature is present),
  the features, and the numbers Pandoc prints on those same paragraphs, as
  runs.
- "Objects" counts equations, pictures (all `w:drawing`, those with alt text
  in brackets), tables (one-cell boxes included) and text boxes.
- Structures use spec section 5's codes S1 to S8 and this survey's S9 to S17
  (section 4), by anchor.
- "Weeks" comes from the handout's Week headings and the summary's
  "(Two weeks)" marks. "1" means neither marks more.
- "Gradescope named" means the handout says to add every member when
  submitting through Gradescope.

| Handout | SHA-256 | U+2014 | Word's question list | D-0078 | Objects | Structures (anchors) | Deliverable | Weeks | Submissions | Report items not answers |
|---|---|---|---|---|---|---|---|---|---|---|
| PH 211 Lab 1: Team Building | `49617ff874c0e2147a73bbfb39db38272e53be360ae10430a17e6a5358608091` | 0 | 5 top, 0 parts | simple; none. Pandoc's numbers: 1-5 | 0 equations (0 display); 0 pictures (0 with alt text); 1 tables; 0 text boxes | S7 B1-B4. Legend box with a sample "1)" item (legend-question, existing) | Question report | 1 (no week headings) | 1 group report (Gradescope named, add every member) | o2 sketches (one per member, one team plan) |
| PH 211 Lab 2: Data Analysis | `112c2c0675829438c17b0a50c8a67615709b85f1c926cddca88ba96259a3a2ec` | 0 | 9 top, 16 parts | simple; none. Pandoc's numbers: 1-9 | 29 equations (2 display); 0 pictures (0 with alt text); 4 tables; 0 text boxes | S1 o3.2, o3.3, o5.4 (numbered actions); S3 o3 (5 parts), o4 (4), o5 (5), o6 (2); S4 o8, o9 (bold bullet prompts); S5 o3.1-o3.5, o4.1, o5.3, o5.5, o6; S8 o3, o5; S14 three one-cell boxes, given data table; S15 two empty content controls | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o2, o3.4, o5.2, o5.5, o7 plots; o4.4 typed calculation; o9 one paragraph per member |
| PH 211 Lab 3: Uncertainty | `421e2df388f532c4140f07c26815737393c4e6583ffb4e473a81c79d9ce1b960` | 0 | 14 top, 7 parts | simple; none at question level; o13's parts x1-x3 sit in a second list; two appendix entries use the question list's third level. Pandoc's numbers: 1-14 | 6 equations (1 display); 4 pictures (4 with alt text); 2 tables; 0 text boxes | S1 o10.1, o10.2 (method options), o14.0.1, o14.0.2 (appendix entries); S3 o9 (1 part), o10 (2), o11 (2), o13 (x1-x3); S4 o14; S5 o11.2; S6 a lettered list between o3 and o4 cites questions 3, 4, 5; S11 B8, B10 (blank table cells to fill); S12 photo before o1, pictures in table cells; S14 fill-in table after o6 | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o6 fill-in table; o9 data table; o12 plot with error bars |
| PH 211 Lab 4: Hypothesis Testing | `54daee77e5e4e0ea8cbbadced928c4f312c3e09418af73eb56c3c54e47b505f1` | 0 | 11 top, 13 parts | simple; none. Pandoc's numbers: 1-11 | 9 equations (1 display); 1 pictures (1 with alt text); 1 tables; 0 text boxes | S3 o3 (2), o4 (2), o6 (3), o7 (3), o9 (3); S4 o11; S5 o5; S6 o6.3 cites part b; o3, o3.1, o9.1, o9.2 cite unnumbered lettered lists (a-f, A-C) by letter; a hint with a display equation after o3.2; S12 one figure; S15 one empty content control | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o1 drawing; o5 data table; o7.3 two or more plots |
| PH 211 Lab 5: Designing an Experiment | `4330e4267d0cb2e4b80d28db091c3bbaae8792ae55ecc78b7a0960169ec273f0` | 0 | 9 top, 18 parts | simple; none. Pandoc's numbers: 1-9 | 11 equations (1 display); 11 pictures (11 with alt text); 2 tables; 0 text boxes | S3 o1 (3), o2 (2), o3 (3), o5 (3), o6 (3), o7 (4); S4 o1, o5 (bullet questions answered later); S5 o5; S8 o1, o3.1, o7; S12 eleven pictures (inline icons, screenshots); S14 two key-concept boxes | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o6.2 data table; o7.1 plots with error bars |
| PH 211 Lab 6: Describing an Experiment | `27d2c3ed2b33ce873960c5be409a756f7fd23882e60247a7b90afe35383b5229` | 0 | 17 top, 7 parts | not simple; second list among report items (x1-x4, label "N.", restarted); sub-part level redefined by an override (lettering under o1, o6, o7). Pandoc's numbers: 1-7 | 16 equations (0 display); 2 pictures (2 with alt text); 0 tables; 0 text boxes | S1 o7.2 (action); S3 o1 (2), o6 (3), o7 (2); S5 o6.1, x3; S6 a bullet after o3 cites questions 1, 2, 3; S11 x1-x4 (bold numbered report items outside the question list); S12 two pictures; S16 a procedure document handed to another group (o1-o3, x1-x4), required headings in o4, o5, o6 | Question report and a shared procedure document | 1 (no week headings) | 1 group report (Gradescope named); the procedure document passes between groups in class | o4, x1 data tables; o5 another group's data, analysis and results |
| PH 211 Lab 7: Capstone | `e9b900c8e35fccda8a9adb9495945f505fb8ecab3cd9a748e813095965bab466` | 0 | 11 top, 19 parts | not simple; restart at question level (o8, first of Week 2); sub-part level redefined by an override. Pandoc's numbers: 1-7, 1, 8-10 | 5 equations (0 display); 2 pictures (2 with alt text); 4 tables; 0 text boxes | S3 o3 (3), o5 (5), o6 (2), o7 (2), o9 (2), o10 (3), o11 (2; conditional parts); S9 o8; S14 lookup table after o1, two boxes; S16 a report each week | Question report, in two weekly parts | 2 (Week headings; summary) | 2: Week 1 plan after instructor approval; Week 2 report (Gradescope named) | o3.2, o4 equations; o6.1 drawing; o8 data table; o9.1 sample calculation; o9.2 plots |
| PH 212 Lab 1: Data Analysis | `0329f26a1b76de0de520bf3bb3395fa938132dad5730d1a6d2829b792f173261` | 0 | 16 top, 11 parts | not simple; sub-part level set by a style (3 paragraphs: o4.2, o13.1, o13.2). Pandoc's numbers: 1-19 | 17 equations (2 display); 0 pictures (0 with alt text); 4 tables; 0 text boxes | S1 o4 (read the box; its parts o4.1, o4.2 answer), o6.1.1, o6.1.2 (method options); S3 o3 (2), o4 (2), o6 (3), o13 (2); S4 o16; S5 o6.2, o8, o12, o13.1; S6 o4.2 cites 6, o6.2 cites 4, o14 cites 11 (each right only under Word's numbering); S8 o6.2; S10 o4.2, o13.1, o13.2; S14 a box between o4 and o4.1 | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o2 drawing; o5, o7 data tables; o8, o10, o12 plots; o16 one paragraph per member |
| PH 212 Lab 2: Extending a Model | `ae4d80de932b2bb5f0cc4fe3e306d4ac7301e8a49ebb37d54e37364de109e82d` | 1 | 9 top, 8 parts | not simple; sub-part level set by a style (8 paragraphs: every lettered part). Pandoc's numbers: 1-17 | 10 equations (1 display); 1 pictures (0 with alt text); 3 tables; 0 text boxes | S1 o2 (read the box; parts o2.1, o2.2 answer); S3 o3 (2), o5 (2), o7 (2); S5 o3.1, o5.1; S8 o3.1; S10 o2.1, o2.2, o3.1, o3.2, o5.1, o5.2, o7.1, o7.2; S12 one icon without alt text; S14 a box between o2.1 and o2.2; S15 a content control holding "Assumptions:"; S17 a software activation code | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o1 drawing; o5.2 data table; o6 plot |
| PH 212 Lab 3: Designing Experiments | `62d6708bf2b2cd6bea3f0170dab8ce92b09eb5a20ffd9f27fdb23486879fda6f` | 0 | 24 top, 19 parts | not simple; sub-part level set by a style (19 paragraphs); restart at question level (o12, first of Week 2). Pandoc's numbers: 1-25, 1, 26-42 | 29 equations (5 display); 6 pictures (4 with alt text); 2 tables; 0 text boxes | S3 o1 (2), o4 (3), o5 (3), o7 (3), o8 (3), o21 (3), o22 (2); S4 o11; S5 o4.3, o5.3, o7.3, o8.3, o21.3, o22.2; S9 o12; S10 19 parts; S11 B15 (continues o21.3); S12 four screenshots; S13 two drawn shapes; S14 a box holding a three-level list; S16 a report each week | Question report, one per week | 2 (Week headings; summary) | 2: one group report each week (Gradescope named) | o2, o10, o12, o22.1 equations; o17 data table; o19 plot |
| PH 212 Lab 4: Hypothesis Testing | `048b10bf3cab6a7f88e381658489df3ff5bf59b4230398cf27934b5df2d8da2c` | 0 | 11 top, 3 parts | simple; none. Pandoc's numbers: 1-11 | 5 equations (0 display); 1 pictures (0 with alt text); 2 tables; 0 text boxes | S3 o5 (3); S6 o8, o11 cite "previous question" (no number); S12 one icon without alt text | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o2 data and value; o4 sketch; o5.1 drawing; o7 data table; o9 plot |
| PH 212 Lab 5: Sharing & Comparing | `1757716444fe6517ae53d8cfa0c9ab1fb86e506fb2b22ddbd4006b05c1fb33ea` | 0 | 8 top, 4 parts | not simple; sub-part level set by a style (4 paragraphs: o3.1, o3.2, o5.1, o5.2). Pandoc's numbers: 1-12 | 15 equations (1 display); 4 pictures (4 with alt text); 1 tables; 0 text boxes | S3 o3 (2), o5 (2); S6 o4, o5 cite the question below and above (no number); S10 o3.1, o3.2, o5.1, o5.2; S12 four screenshots; S14 a box with a display equation between o6 and o7; S16 a class whiteboard (not submitted) | Question report | 1 (no week headings) | 1 group report (Gradescope named); a whiteboard shown in class | o3, o7 equations; o4 data table and a sketch per mode; o6 plot (if used) |
| PH 212 Lab 6: Capstone | `68d4f8dfcda02ae7f10a005ce37ba2c5485259d0d17e30c7719256af9e0984ca` | 0 | 10 top, 24 parts | not simple; restart at question level (o5, first of Week 2); level 0 redefined by an override at o6 and o10; sub-part overrides. Pandoc's numbers: 1-4, 1, 1, 5-7, 2 | 21 equations (4 display); 4 pictures (4 with alt text); 6 tables; 0 text boxes | S3 o1 (5), o2 (3), o3 (5), o5 (2), o7 (3), o8 (2), o9 (2, with o9.2.1, o9.2.2); S4 o4 (five bold bullet questions); S6 Week 2's intro cites "Questions 1 and 2" (o5, o6); S8 o1.2, o3.4; S9 o5; S11 B11; S14 rubric table, options table, a practice box; S16 a report each week; S17 a link to a personal OneDrive document | Question report, one per week | 2 (Week headings; summary) | 2: Week 1 plan, Week 2 report (Gradescope named) | o2.1 sketch; o7.1, o7.2 data tables; o8.1 plots; o8.2 sample calculation; o10 one takeaway per member |
| PH 213 Lab 1: Data Analysis | `0ef396eb1ed513d3d60c0725b0df5e6044febd6097c5fc5fd9039293a4c8a3f5` | 0 | 6 top, 0 parts | simple; none. Pandoc's numbers: 1-6 | 7 equations (3 display); 0 pictures (0 with alt text); 2 tables; 0 text boxes | S4 o3, o6; S5 none as equations (o5 types symbols as italic text); S11 an unnumbered "Think about your result:" paragraph of questions between o5 and o6; legend box with a sample "1)" item | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o3 data table; o4 plot |
| PH 213 Lab 2: Hypothesis Testing | `36f41045875ea1bb0c1699a1ed50c7b18ae2d8e6397a0da37d05546aa069ab68` | 0 | 13 top, 4 parts | simple; none. Pandoc's numbers: 1-13 | 70 equations (3 display); 2 pictures (2 with alt text); 3 tables; 5 text boxes | S3 o2 (3), o7 (1); S5 o1, o2.1-o2.3, o3, o8, o10 (70 equations; Pandoc reads 69); S6 none by number ("Equation (2)", "the four predictions"); S7 B1-B7 and an unnumbered bold self-check question; S12 a photograph anchored inside o6; S13 the photograph's labels (8 shapes, 1 group, 5 text boxes); S14 a boxed warning, a box with a numbered list and a display equation; S15 SEQ figure numbers | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o2.1, o2.2 sketches; o7 data table; o8 plots |
| PH 213 Lab 3: Data Taking | `124a763be1fb64991954c769f6c99eba1c8b67d43fe63aa1e810799855934bf2` | 0 | 9 top, 0 parts | simple; none. Pandoc's numbers: 1-9 | 21 equations (4 display); 1 pictures (1 with alt text); 1 tables; 0 text boxes | S3 o9 (its prompts are two bold bullets, per member); S5 o2; S12 one figure; S14 a box with a display equation | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o1 sketch; o4, o7 drawings (photo or screenshot) |
| PH 213 Lab 4: Model Building | `09259a1b6297816d388b4743f64ac69b80e440afd83eaee9a2c726fb40d67f74` | 0 | 13 top, 4 parts | simple; none at question level; one sub-part Pandoc reads at the top level. Pandoc's numbers: 1-13 | 21 equations (3 display); 6 pictures (6 with alt text); 0 tables; 4 text boxes | S1 o10.1-o10.3 (case labels under o10; o11 asks about them); S3 o3 (1); S4 o8; S8 o10.1; S5 none in questions as equations (o6 types symbols as italic text); S6 o7 cites "the next question"; S12 four pictures; S13 a figure drawn from 11 shapes, 1 group, 4 text boxes, which Pandoc drops | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o3, o3.1 data tables; o5 plots; o12 recorded results |
| PH 213 Lab 5: Analysis and Testing | `bdffcaa9b7b5716ae8fd87621465952ba9bf976ee80d126418b78ea8cc778138` | 0 | 9 top, 1 parts | not simple; two lists among the questions (o1 alone; o2 to o9 in a list starting at 2); Pandoc reads the same numbers. Pandoc's numbers: 1-9 | 15 equations (2 display); 5 pictures (5 with alt text); 1 tables; 0 text boxes | S3 o2 (1); S12 five pictures; S15 a SYMBOL field whose stored result is the letter W | Question report | 1 (no week headings) | 1 group report (Gradescope named) | o1 circuit drawing; o2 data table (screenshot allowed); o7 plot |
| PH 213 Lab 6: Capstone | `d78901da6ec06fc2f1c184d6cabff469e715db68ccbb2042ff9302290998a000` | 0 | 9 top, 3 parts | not simple; three lists among the questions (o1-o3, o4-o8, o9); the first has no start value. Pandoc's numbers: 1-3, 1-5, 1 | 15 equations (2 display); 4 pictures (4 with alt text); 5 tables; 0 text boxes | S1 o1, o9 (actions); S3 o3 (3); S4 o3.3, o5, o7; S9 o4, o9; S14 rubric table, a box; S15 table of contents (11 entries), running header words, a bookmark; S16 Weeks 1 and 2 report, Week 3 presentation | Question report and a slide presentation | 3 (Week headings; summary) | 1 stated: the presentation file to a shared folder; the report's submission is not stated | o2 each member's list; o3.2 equipment list; o5 data; o6 plots |

Totals for the 18 handouts still to convert:

- 208 top-level question paragraphs and 161 parts;
- 322 equations (35 display), and every one of the 18 has some;
- 50 pictures in 15 handouts, 2 of them without alt text, plus 4 drawings
  that are shapes, not pictures;
- 43 tables and 9 text boxes;
- one U+2014.

PH 211 Lab 1's original is byte for byte the committed one (its SHA-256 equals
its front matter's), so D-0087's live-document rule has nothing to apply yet.

## 3. Numbering (D-0078)

D-0078 counts three features at the question level:

- a restart or override;
- more than one list among the questions;
- a label format other than "N)".

The survey found a fourth, which D-0078 does not name.

**The fourth feature: a sub-part's level set by a style.** In PH 212 Labs 1,
2, 3 and 5 the lettered parts carry a "Subquestion" style.

- The style is based on "Question" and sets only the level (`ilvl` 1); its
  list comes from "Question".
- The abstract list's level 1 names that style and labels "%2.", lower
  letter.
- Word therefore shows these paragraphs as "a." and "b." under their
  question.
- Pandoc applies the inherited list but not the style's level, so it prints
  them as top-level questions. Every later number shifts.

| Handout | Style-set parts | Word's top level | Pandoc's numbers |
|---|---|---|---|
| PH 212 Lab 1 | 3 | 16 | 1-19 |
| PH 212 Lab 2 | 8 | 9 | 1-17 |
| PH 212 Lab 3 | 19 | 24 | 1-25, 1, 26-42 |
| PH 212 Lab 5 | 4 | 8 | 1-12 |

The handouts' own cross-references side with Word, as PH 212 Lab 1 shows:

- o4.2 says "question 6" for statistical uncertainty, which is o6.
- o6.2 says "question 4" for the sources, which is o4.
- o14 says "question 11", which is o11.

Under Pandoc's numbers, 6 and 11 point at other items (o5 and o10). This also
corrects the spec's section 5 sample: its PH 212 item numbers (#4, #7, #13,
#14, #17, #19; L2 #2, #9, #13) came from a Pandoc extraction and are Pandoc's
numbers, not Word's.

**Verdicts.** Ten handouts are simple, and Pandoc prints Word's sequence on
them:

- PH 211 Labs 1 to 5;
- PH 212 Lab 4;
- PH 213 Labs 1 to 4.

Nine are not simple; under D-0078 each comes to the owner before its
conversion. For each, the look in Word that settles its labels:

1. **PH 211 Lab 6.** The bold "1." list in Part 4 (x1 to x4) is a second list
   among report items. Its sub-part lettering is redefined by an override, so
   check whether the letters restart at "a." under o1, o6 and o7.
2. **PH 211 Lab 7.** o8, the first of Week 2 ("Report your data in a table"),
   starts a new list instance at 1. Pandoc prints o8 as 1 and o9 as 8. Read
   the labels of o8 and o9.
3. **PH 212 Lab 1.** Confirm o4.2, o13.1 and o13.2 show as letters, and that
   the last question reads "16)".
4. **PH 212 Lab 2.** Confirm the parts show as letters and the last question
   reads "9)".
5. **PH 212 Lab 3.**
   - Confirm o1.1 and o1.2 show as letters.
   - The last Week 1 question (o11) should read "11)".
   - o12 starts a new instance at 1: read the labels of o12 and o13.
6. **PH 212 Lab 5.** Confirm the parts show as letters and the last question
   reads "8)".
7. **PH 212 Lab 6.** o5 starts Week 2 at 1, and o6 and o10 sit in a list
   instance whose level 0 is redefined. Pandoc prints 1, 1 for o5, o6 and 2
   for o10, while the Week 2 intro cites "Questions 1 and 2". Read o5 to o10.
8. **PH 213 Lab 5.** o1 is alone in one list; o2 to o9 are in another that
   starts at 2. Pandoc agrees (1 to 9). One glance confirms.
9. **PH 213 Lab 6.** Three lists: o1 to o3, o4 to o8, o9. The first list's
   level has no start value. ECMA-376's text, as Claude recalls it and did not
   re-read today, makes a missing start 0; Pandoc prints 1. Read o1, o4 and
   o9.

Below question level the readers also noted the following. Word's sub-part
letters are content on the faithful page, and the word check cannot see
them.

- PH 211 Lab 3's o13 takes its parts from a second list (x1 to x3), and two
  appendix entries carry the question list's third level.
- In PH 213 Lab 4, one part (o10.1) is printed by Pandoc at the top level.

**For pass 2a.** D-0078 builds the reader of Word's numbering (critique F1)
only where a count calls for it. The counts call for it in nine of 19, and in
four of PH 212's six. Section 10 carries the choice.

## 4. Structures

S1 to S8 are spec section 5's; S9 to S17 are new, each with a draft rule in
section 5. Where they were found:

| | Structure | Found in |
|---|---|---|
| S1 | Numbered item needing no answer: an action, a method option, a case label, an appendix entry | Top level: PH 213 L6 o1, o9. Parts: PH 211 L2 o3.2, o3.3, o5.4; L3 o10.1, o10.2, o14.0.1, o14.0.2; L6 o7.2; PH 212 L1 o6.1.1, o6.1.2; PH 213 L4 o10.1 to o10.3. "Read the box" items (PH 212 L1 o4, L2 o2) have answered parts, so they are stems |
| S2 | Stem whose answers are its parts | 53 items the readers marked S2, in 15 handouts. Under Word's levels every one heads its own parts (lettered; in PH 213 L3 o9, two bold bullets). None has its answers in the next numbered items; that shape came from Pandoc's misread (section 3) |
| S3 | Lettered parts, nested, lettering that restarts | 16 handouts: all but PH 211 L1 and PH 213 L1, L3. Three levels in PH 212 L1 (o6.1.1), L6 (o9.2.1) |
| S4 | Lists inside a question, often bold bullets that are prompts | PH 211 L2 o8, o9; L3 o14; L4 o11; L5 o1, o5; PH 212 L1 o16; L3 o11; L6 o2, o4; PH 213 L1 o3, o6; L3 o9; L4 o8; L6 o3.3, o5, o7 |
| S5 | Equations in a question | 10 handouts by the readers' marks: PH 211 L2 to L6, PH 212 L1 to L3, PH 213 L2, L3. All 18 to convert hold equations somewhere. Symbols typed as italic text, not equations: PH 213 L1 o5, L4 o6 |
| S6 | A question citing another | By number: PH 211 L3 (a lettered list cites 3, 4, 5), L6 (1, 2, 3); PH 212 L1 (6, 4, 11), L6 ("Questions 1 and 2"). By position only ("previous", "below", "next"): PH 212 L4, L5; PH 213 L4. By letter of an unnumbered list: PH 211 L4 |
| S7 | Bold that is not a question | Every handout (the B lists); PH 213 L2's unnumbered self-check question |
| S8 | Actions or hints between parts | PH 211 L2 o3, o5; L5 o1, o3.1, o7; PH 212 L1 o6.2; L2 o3.1; L6 o1.2, o3.4; PH 213 L4 o10.1 |
| S9 | Restart, or more than one list, at question level | PH 211 L7 o8; PH 212 L3 o12, L6 o5 (level 0 overridden at o6, o10); PH 213 L5 (two lists, continuing), L6 (three lists, first without a start value) |
| S10 | Part level set by a style that inherits its list | PH 212 L1 (3), L2 (8), L3 (19), L5 (4) |
| S11 | Report item outside any numbered item: a bold paragraph or list, a blank cell to fill | PH 211 L3 B8, B10 (blank cells); L6 x1 to x4; PH 212 L3 B15; L6 B11; PH 213 L1 ("Think about your result:") |
| S12 | Pictures: in or just before a question, inline icons, in table cells, screenshots in how-to steps | 15 handouts, 50 pictures. In a question: PH 213 L2 o6. Without alt text: PH 212 L2, L4 (one icon each) |
| S13 | Figures drawn from Word shapes, groups and text boxes, which Pandoc drops | PH 212 L3 (2 shapes); PH 213 L2 (the photograph's labels: 8 shapes, 1 group, 5 text boxes); PH 213 L4 (a figure of 11 shapes, 1 group, 4 text boxes; its "as shown here" points at nothing in Pandoc's output) |
| S14 | Tables and boxes: a box between a question's parts, a table to fill in, given and lookup tables, rubric tables printed in the student handout | Boxes between parts: PH 212 L1 o4, L2 o2. Fill-in: PH 211 L3. Rubric tables: PH 212 L6, PH 213 L6. 43 tables in the 18 to convert |
| S15 | Word furniture outside the body | Page-number headers in all 19; running header words in PH 213 L6; a table of contents field in PH 213 L6 (11 entries, words only); SEQ figure numbers in PH 213 L2; a SYMBOL field in PH 213 L5 whose stored result is "W"; content controls in PH 211 L2 (2, empty), L4 (1, empty), PH 212 L2 (1, holding "Assumptions:") |
| S16 | More than one deliverable or document | Weekly reports: PH 211 L7, PH 212 L3, L6. A procedure document passed between groups: PH 211 L6. A Week 3 presentation: PH 213 L6. A class whiteboard: PH 212 L5 |
| S17 | Content a public repo must not carry | PH 212 L2 (a software activation code), PH 212 L6 (a link to a personal OneDrive document); section 7 |

## 5. Markup rules

Ruled 2026-10-07 (D-0101) and moved to `docs/conversion-spec.md`,
"Markup rules per structure", the one copy. S13 changed on ruling: drawn
figures become SVG built from the original's shapes, with a PNG copy for
Word, in pass 2b.

## 6. Em dash and the symbol field (D-0085)

**U+2014.** One original holds one em dash: PH 212 Lab 2, Part 1, "a
model—a representation". The Statement on AI and labs holds another, which
matters only if pass 6 quotes it. CI fails on U+2014 in `curriculum/`, and
the word check fails on a changed word. Draft rule, lean A:

- **A.** The converted source keeps the original's character, and the em-dash
  scan skips files with a `source_file`. The word check already proves every
  character of their words is the original's. Format only; co-owned text
  keeps its authors' words (charter floor 9).
- **B.** A ruled change to another dash, declared in `ruled_additions` and
  `ruled_omissions`. That makes a content change in the format-only phase.

**SYMBOL field.** In PH 213 Lab 5 the text runs "Ohm (", then a SYMBOL field,
then ") = 1 V/A". The field asks for character 87 of the Symbol font, Ω, but
its stored result is the letter "W" in Times New Roman. What the student sees
is the owner's to read in Word.

- If Word shows Ω, the converted text holds Ω, and the word check needs to
  read a SYMBOL field's character (pass 2a) or an entry.
- If it shows W, the text holds W as written.

## 7. Content a public repo must not carry (S17)

Neither item is quoted here.

- **PH 212 Lab 2** has a box holding a software activation code and its
  link. Converted as written, the code enters a repo that will be public, and
  its history permanently.
- **PH 212 Lab 6** has the word "your" (Model 1, task 3) linked to a
  document in a personal OneDrive. Such paths usually carry a person's name.
  D-0086's strip list does not reach hyperlink targets. Pandoc keeps links,
  and the word check does not read them.

Both need the owner's ruling before those conversions: omit as a ruled
omission, replace, or keep. PH 211 Lab 2's one short link (rb.gy) hides its
target; it is not flagged, only noted. No other handout links to a personal
address or `mailto:`.

## 8. Originals: identity parts and the other cleared files

For pass 2a's strip (D-0086), presence only:

- **Every handout** has `creator` and `lastModifiedBy` in `core.xml` and a
  template path in `app.xml`.
- **Five** have `app.xml` Company: PH 211 Labs 1, 2 and 4; PH 212 Labs 4
  and 5.
- **None** has `people.xml`, comments, tracked changes, revision authors,
  `custom.xml`, or EXIF in a JPEG.
- The one identity-bearing link is section 7's.

The other cleared files, hashed for the record:

| File | SHA-256 | U+2014 |
|---|---|---|
| PH211/PH 211 Curriculum Summary.docx | `e0e2dd39392a35869ccae3d2be02f8b49c600f503b2c59b1a72d43a86dadcea7` | 0 |
| PH212/PH 212 Curriculum Summary.docx | `20a28ce8a43489ab513ee3652ec62edef22f0cab76f9b53ee88ab8a2f59da20e` | 0 |
| PH213/PH 213 Curriculum Summary.docx | `5cd7cc1d08b540c3462cd2f6e1789e87579700e454696d65789cc3c4901f5124` | 0 |
| Curriculum objectives.docx | `7254a5b109ac3ac97007946c3ad2c600e1606040021df97b23bc20d27dbf5013` | 0 |
| Lab Guidance for Instructors.docx | `bf32ddeb6fa09e0bea0df1543a1071d06f59df00802d2632ed894cf459ee6096` | 0 |
| Statement on AI and labs.docx | `e5aa1f065077d9a027209e59473880b50a977ccbbd3a80e550d8e132a18dce7b` | 1 |
| 21X Labs README_PII-stripped.txt | `7e58523beb53636c2e6feadd36cd5e52db69df98fdea9cdd66ea5e3bbc6bb83a` | 0 |

For pass 6, the AI statement's own title is "AI Use in Our Physics Lab". Its
file name is "Statement on AI and labs", the title D-0076 cites. It names no
course number, and asks for "a short note at the end of your report
describing how it helped", D-0076's quoted words.

## 9. The hardest two (pass 3)

Ranked by the rules each handout tests that others do not:

1. **PH 212 Lab 3.** Most numbering risk (19 style-set parts, Pandoc wrong
   from the second item on, and a Week 2 restart). It also has 29 equations
   (5 display), 4 screenshots and 2 drawn shapes, a box holding a three-level
   list, and two weeks with two submissions.
2. **PH 213 Lab 2.** Most equation and figure risk: 70 equations, of which
   Pandoc reads 69, and numbered display equations cited by number. Its
   labelled photograph (a group of 8 shapes and 5 text boxes) is anchored
   inside o6, with SEQ figure numbers, in a 3.07 MB file. D-0092's calls are
   already ruled for it.
3. PH 213 Lab 4: a drawn figure Pandoc drops entirely; case labels at part
   level.
4. PH 212 Lab 6: level-0 overrides and a Week 2 restart, 6 tables including a
   rubric, and the personal link.
5. PH 213 Lab 6: three lists, one without a start value, a contents field, a
   running header, three weeks.

Lean: pass 3 opens with PH 212 Lab 3 and PH 213 Lab 2. Between them they meet
every structure but S1 at the top level, S6, S8 and S17. D-0082's likely pair
was PH 213 Lab 2 and PH 212 Lab 1. PH 212 Lab 1's numbering and equation
hazards are smaller versions of Lab 3's (3 style-set parts to 19, 17
equations to 29, no pictures to 4). It alone has S6 by number, which PH 211
Labs 3 and 6 and PH 212 Lab 6 bring later.

## 10. Recount of passes (D-0082)

What the survey changes:

- **Pass 2a grows.** The number check needs Word's numbering for 9 of 19
  handouts, not Pandoc's. The em-dash rule (A) and possibly the SYMBOL field
  join it. The strip may grow by hyperlink targets (section 7).
- **Pass 2b is needed by 15 of 18 handouts** for pictures and by all 18 for
  equations. Three hold drawn figures (S13), whose rendering 2b or pass 3
  must place.
- **The conversion passes carry more per handout.** Every handout has
  equations, and nine wait on the owner's reading in Word.
- **Pass 6's scope narrows.** Five labs are not a single question report
  (S16).

The count of work units stays eight (1, 2a, 2b, 3, 4, 5, 6, 7). Sessions
against the owner's budget of six:

- **Eight**, one each: the plan as ruled.
- **Seven** (lean): pass 7 runs in pass 6's session once 6 merges. It is
  local, reads two checkouts and lands in the instructor repo (D-0083,
  D-0089).
- **Six**: also 2a and 2b in one session. 2b's gate is pass 1 alone, so the
  two are independent PRs, but 2a is the largest pass and both reach every
  download. Not recommended. Pairing 4 and 5 (ten handouts) is the other
  route to six, and is weaker: they are the handouts the S10 and S9 rules
  will first meet at volume.

## 11. Observed, not changed

Conversion changes no content (gate 8.5); these are recorded for the content
phase.

- PH 213 Lab 6's Appendix B lists the PH 21X labs. Its PH 213 rows disagree
  with the PH 213 summary: no "Model building" row, "Analysis and Testing"
  numbered 4, the capstone numbered 6 to 8.
- The PH 212 summary's "Lab descriptions" list calls Lab 1 "Data Skills"; its
  Activities table says "Data Analysis".
- Two "Part 4" headings each: PH 213 Labs 1 and 2.
- PH 211 Lab 4: a display formula in a hint after o3.2 lacks a delta in its
  second term.
- PH 212 Lab 1: a sentence before o10 ends "include" with nothing after it.
- PH 211 Lab 7: Appendix A's last equipment item is cut off.
- PH 213 Lab 6's presentation is "five or six minutes" in Week 2 and "about
  five minutes" in Week 3. Its contents field lists Appendices A to C; an
  Appendix D exists.
