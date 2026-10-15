# Stretch survey of the 14 converted handouts

Agent output, kept as delivered: a read-only survey by a subagent (Opus,
medium effort) on 2026-10-15, at `ac833da`, which the owner asked for. It
estimates how much of each handout could collapse under the rules ruled that
day, and recommends labs for the sandbox. The main session spot-checked four
claims against the files, and all four held: the landscape fence at PH 212
Capstone line 180, four pictures in its slope section, the three anchor links
into appendix headings, and the box with a heading inside it in PH 211 Data
Analysis. Where the design (`2026-10-15-stretch-sandbox-design.md`, section
7) differs, the design wins. It adds the rule that no heading sits in a tail,
which changes some of the ranges below.

Every number is approximate.

**Method.**
- The survey read all 14 handouts in full and did not change the repo.
- Word counts use the rule in the session's `stretchable.py`: whitespace
  tokens, skipping fence lines, table rules and images. The per-lab totals
  match that script (40,507 words in all).
- Line numbers are file line numbers.
- "Tail" is the text that collapses; the lead is not counted.

**Conventions.**
- **Learning Objectives:** the lead is the "This lab activity is designed to
  help you practice…" sentence and the tail is the list of skills, so the
  learning goal stays visible.
- **Appendices:** each subsection is its own stretch, led by its heading, so
  the headings stay visible as a table of contents and every anchor target
  stays visible.

## 1. Summary table

| Lab | Total | Main | Appx | Collapsible main (words, %) | Collapsible appx (words, %) |
|---|---|---|---|---|---|
| ph211-team-building | 993 | 993 | 0 | 179 (18%) | n/a |
| ph211-data-analysis | 2848 | 2670 | 178 | 515 (19%) | 0 (0%) |
| ph211-uncertainty | 2424 | 1965 | 459 | 75 (4%) | 426 (93%) |
| ph211-hypothesis-testing | 3104 | 2522 | 582 | 304 (12%) | 545 (94%) |
| ph211-designing-an-experiment | 3091 | 2348 | 743 | 361 (15%) | 692 (93%) |
| ph211-describing-an-experiment | 3007 | 1984 | 1023 | 160 (8%) | 880 (86%) |
| ph211-capstone | 2984 | 1825 | 1159 | 388 (21%) | 880 (76%) |
| ph212-data-analysis | 2732 | 2732 | 0 | 447 (16%) | n/a |
| ph212-extending-a-model | 2670 | 2022 | 648 | 192 (9%) | 526 (81%) |
| ph212-designing-experiments | 4767 | 3635 | 1132 | 201 (6%) | 998 (88%) |
| ph212-hypothesis-testing | 1834 | 1022 | 812 | 191 (19%) | 687 (85%) |
| ph212-sharing-and-comparing | 2721 | 1674 | 1047 | 85 (5%) | 904 (86%) |
| ph212-capstone | 4733 | 3446 | 1287 | 814 (24%) * | 1037 (81%) |
| ph213-hypothesis-testing | 2599 | 2263 | 336 | 355 (16%) | 313 (93%) |

\* The grading rubric, one stretch, accounts for 535 of ph212-capstone's 814
words. Without it the lab is at about 8%.

- **Appendices:** 76 to 94% collapsible wherever they exist.
- **Main paths:** 4 to 24% collapsible. Most of a main path is questions,
  procedure, or text a question points to ("read the box above", "the method
  below", "the list above").

## 2. Candidates per lab

Each line reads: line range (lead to end of tail), "lead", tail words, kind,
and why it is safe.

### ph211-capstone

- 40–42 "#### If you miss Week 1…" (heading inside a box), 46 words.
  Explicitly optional (conditional): logistics for absent students, and the
  heading says who it is for.
- 49–54 "This lab activity is designed…", 41 words. Framing; no question uses
  it.
- 98–106 "#### Remember, an experiment always:" (inside a box), 90 words.
  Review; nothing points to it.
- 109–111 "To get started, you'll use the hypothesis…", 34 words. Framing; the
  visible lead carries the instruction.
- 155–164 "#### Analysis Methods:" (inside a box), 177 words. Review; the tail
  holds an action list. These are analysis reminders, not procedure, and no
  question cites them.
- Appendix, 880 words in all, every part reference collapsed behind a visible
  heading:
  - 296–305 Required Plot Elements, 78 words.
  - 307–329 Linearization, 233 words.
  - 331–335 What is Uncertainty, 136 words.
  - 337–348 Sources, 98 words.
  - 350–356 "**Predictions, Hypotheses…**" (a paragraph lead inside the
    Sources section), 147 words.
  - 368–378 Variables and Parameters, 188 words.

Not worth it: the Appendix B intro list (288–294), 29 words.

Not collapsible:
- Appendix A equipment list (224–282, 131 words): it is an equipment list,
  Equipment (58) and Part 2 (133) link to it, and the design question needs
  it.
- Tips for Graphical Analysis (358–366): a hint.
- Table 79–84: the action at 76 uses it.
- Line 145: guidance for a question, and a single block, so there is no tail.

### ph211-data-analysis

- 18–20 "**Experimental goal:** Analyze position…", 60 words. Framing.
- 26–32 the Learning Objectives list, 39 words. Framing.
- 43–49 "## Installing Excel Software (optional)", 127 words. Explicitly
  optional; the lab computers have Excel.
- 116–136 "In Part 2, you tried a few…", 234 words. Theory. The tail holds the
  whole Linearization box (a `###` heading and a nested action) plus line
  136. No question points to it, and the model statement (140–144) stays
  visible.
- 162–168 "### Why Linearize?" (inside a box), 55 words. Theory.

Not collapsible:
- The R² paragraphs (87–91, 98 words): hint 103 says "use the above
  information about interpreting the R² value".
- The Plotting box (74–83): hint 111 points to "the box on the previous
  page", and the box holds a hint.
- The models (140–144, 190–194): the questions need them.
- The Part 5 how-to (233–237): a graded plot needs it.
- Line 186: it carries the class data-sharing procedure.
- The appendix data table: Part 5 uses it.

### ph211-describing-an-experiment

- 25–32 "**Experimental goal: Find the coefficient…**", 94 words. Framing (an
  overview of the activity).
- 38–42 the Learning Objectives list, 31 words. Framing; marginal.
- 69–71 "Two objects in contact but not moving…", 35 words. Theory; marginal.
- Appendix, 880 words: the same six subsections as the capstone, at
  229–238, 240–262, 264–268, 270–281, 283–289 (a paragraph lead) and 301–311.

Not collapsible:
- The friction theory (73–91): hint 81 points to "the expression above",
  line 75 defines μs, and the hints cut the passage into pieces with no tails.
- Lines 103–105: the reproducibility standard the question is graded on.
- The force-sensor steps (134–141): procedure, pointed to by the action at
  115 and the hint at 163.
- The Graphical Analysis tips: a hint.

### ph211-designing-an-experiment

- 46–48 the goal, 37 words. Framing.
- 54–60 the Learning Objectives list, 46 words. Framing.
- 129–133 "Recall from the Hypothesis Testing lab…", 90 words. Review; the model
  (135–139) stays visible.
- 153–163 "### Variables and Parameters" (inside a box), 188 words. Supportive:
  the question uses this vocabulary but does not point to the box.
- Appendix, 692 words: 289–298, 300–322 (the `_Linearization` anchor on the
  lead), 324–328 (the `_What_is_Uncertainty?` anchor on the lead), 330–341,
  and 343–349.

Not collapsible:
- The Graphical Analysis tips box: it holds hints.
- The uncertainty method (187–204): question 180 says "method described
  below".
- The slope method (251–263): question 248 says "method below".

### ph211-hypothesis-testing

- 22–24 the goal, 70 words. Framing.
- 30–35 the Learning Objectives list, 36 words. Framing.
- 53–55 "A new housing development is being built…", 67 words. Framing (the
  story); the hypotheses (57) and the figure stay visible.
- 72–78 "### Predictions, Hypotheses, and Models" (inside a box), 131 words.
  Review.
- Appendix, 545 words: 229–238, 240–262 (hint 131's anchor sits on the
  lead), 264–268 and 270–281.

Not collapsible:
- Lines 57–63: the hypotheses and the figure.
- Line 69: the department head's advice, which question b tests.
- The uncertainty-source list (105–112): question 117 says "items from the
  list above".
- The Part 6 scenario numbers.

### ph211-team-building

- 18–22 the goal and two motivation paragraphs, 102 words. Framing.
- 46–54 the Learning Objectives list, 44 words. Framing.
- 121–127 "Your group will briefly present…", 33 words. The tail is an optional
  list of possible discussion points; marginal.

Not collapsible: the legend box (24–40), which holds a hint and explains the
markup; the Part 1 and Part 2 action steps; the clean-up notes at 115 and
146.

### ph211-uncertainty

- 31–33 the goal, 35 words. Framing.
- 39–45 the Learning Objectives list, 40 words. Framing.
- Appendix:
  - 232–240 "#### To add error bars…", 115 words. Procedural how-to; question
    198 points only to "the appendix" as a place.
  - 251–260 Required Plot Elements, 78 words.
  - 262–284 Linearization, 233 words.

Not worth it: the quotation at 178–180, 17 words.

Not collapsible:
- The What is Uncertainty box (71–77): question 84 says "Read the box above".
- The sources list (91–98): hint 145 points to it.
- Line 100, the "human error" paragraph: a single block between protected
  blocks.
- The stopwatch table (124–138) and Figure 1: questions use them.

### ph212-capstone

- 45–62 "This lab activity spans two weeks…", 98 words. Framing plus
  explicitly optional; the tail holds two lists and the "If you miss Week 1"
  box.
- 68–76 the Learning Objectives list, 36 words. Framing.
- 128–130 "Your lab should investigate quantitative relationships…", 67 words.
  Supportive. Line 130 contains "cite any sources", which hint 234 repeats
  visibly.
- 134–136 "**Model 1 – Drag**", 57 words. Theory; the t₀ fitting note (138)
  and the equations stay visible.
- 182–190 "#### Remember, an experiment always:" (a box inside `::: landscape`),
  94 words. Review.
- 197–205 "The following criteria will be used to grade…", 462 words.
  Reference; the tail is the rubric pipe table, inside the landscape div.
- Appendix, 1037 words:
  - 364–373 Required Plot Elements, 78 words.
  - 375–379 What is Uncertainty, 136 words.
  - 381–394 Sources, 166 words.
  - 406–418 "**Linearization comes in handy…**" (a paragraph lead), 146 words.
  - 420–450 Assumptions, including the reliable-experiment list, 313 words.
  - 452–464 Finding uncertainty in a slope, 69 words, with 4 pictures.
  - 466–474 Propagation, 129 words, with `$$`.

Not worth it: the Linearization heading's tail at 398 (22 words, cut short by
a hint).

Not collapsible:
- The custom-fit box (82–109): hints, and how-to for getting Pro.
- The SKIP box (111–119): see section 6.
- The options table (37–43) and the phenomena list (123–126): question 219
  links to them.
- The model equations, notes and task lists (138–178).
- The approval list (247–253).

### ph212-data-analysis

- 40–48 the Learning Objectives list, 36 words. Framing.
- 62–74 "## Installing Excel Software", 133 words. An optional install; the lab
  computers have Excel.
- 195–197 "**Error bars**", 69 words. Theory.
- 221–225 "Fitting a function to a dataset…", 120 words. Theory.
- 260–264 "**Linearization comes in handy…**" (inside a box), 89 words. Theory.

Not collapsible:
- The legend box: it holds a hint.
- The What is Uncertainty box: it sits inside a question, which points to it.
- The plot box (182–193): question 228 says "box on the previous page", and
  the box holds a hint.
- The Excel error-bar steps (199–205): how-to for the graded plot at question
  208.
- The model (241–245).
- Line 247: a single block before a box that holds a hint.

### ph212-designing-experiments

- 31–33 the overview, 31 words. Framing; marginal.
- 43–49 the Learning Objectives list, 49 words. Framing.
- 66–68 "### Introduction: Designing a Combustion Engine", 78 words. Framing;
  the task (70) and the system (72) stay visible.
- 105–107 "**Your goal in this part…**", 43 words. Framing.
- Appendix:
  - 376–410 "## Appendix A – Derivation…", 311 words. Theory, with 4 `$$`
    equations; line 82 points to "the end of this handout" only as a place.
  - 421–430 Required Plot Elements, 78 words.
  - 432–436 What is Uncertainty, 136 words.
  - 438–451 Sources, 166 words.
  - 463–475 "**Linearization comes in handy…**" (a paragraph lead), 146 words.
  - 477–496 Assumptions, 161 words.

Not collapsible:
- The Estimating Uncertainty box (114–127): questions 136, 143, 170 and 177
  say "method described above".
- The Describing box (213–224): question 227 says "Read the box above".
- The analysis steps (254–259).
- The slope methods (337–351): question 329 says "methods below", and they
  include a drawn figure.
- The model (76–86).

### ph212-extending-a-model

- 54–58 "### Graphical Analysis Pro" (inside a box), 35 words. Supportive; it
  stops before line 60 (see section 6).
- 87–94 "### What is a Model?" (inside a box), 157 words. Theory.
- Appendix, 526 words: Required Plot Elements (250–259, 78 words), What is
  Uncertainty (261–265, 136), Sources (267–280, 166) and "**Linearization
  comes in handy…**" (292–304, 146).

Not worth it: the intro at 27–29 (29 words), the Learning Objectives at 35–39
(27 words), and the Linearization heading's tail at 284 (22 words).

Not collapsible:
- The introduction (70): question 114 asks about "the real-world problem
  described in the introduction".
- The Assumptions box: it sits inside a question.
- The design text (139–157): question 161 says "Read the information above".
- The error-bar paragraphs (172–176): question 179 says "Read the paragraph
  above".

### ph212-hypothesis-testing

- 25–33 "In a reliable **scientific experiment**, you should:" (a paragraph
  lead inside a box), 147 words. Review: general rules rather than this lab's
  steps, and no question points to them.
- 40–45 the Learning Objectives list, 44 words. Framing.
- Appendix, 687 words: 152–161, 163–167, 169–182, 194–206 (a paragraph
  lead) and 208–227.

Not collapsible:
- The "How to connect carts" box (66–70): operating how-to.
- The cart-handling hint (56–58).
- Lines 62–64: line 64 sets the short-time-scale condition.

### ph212-sharing-and-comparing

- 31–33 the goal, 40 words. Framing.
- 39–44 the Learning Objectives list, 45 words. Framing.
- Appendix, 904 words:
  - Required Plot Elements (209–218, 78 words).
  - What is Uncertainty (220–224, 136).
  - Sources (226–239, 166).
  - "**Linearization comes in handy…**" (251–255, 89).
  - "### Why Linearize?" (257–263, 55).
  - Assumptions (265–294, 311).
  - Finding uncertainty in a slope (296–308, 69, with 4 pictures).

Not collapsible:
- The Part 1 wave-fact hints.
- The variable text (78–90) and the rearrange block (101–115): procedure.
- The propagating box (157–172): question 175 says "equation above", and the
  box holds a hint.
- The whiteboard list (180–185): instructions.

### ph213-hypothesis-testing

- 24–26 "A CRT accelerates and deflects a beam…", 54 words. Theory.
- 32–37 the Learning Objectives list, 31 words. Framing; marginal.
- 49–59 "## Understanding the CRT", 270 words. Theory. The tail holds the
  three-stage list (with inline math) and stops before the schematic (61),
  which instruction 111 points to.
- Appendix:
  - "**[Required Plot Elements]**" (241–250, 78 words, a paragraph lead).
  - "**[Linearization]**" (252–273, 235 words, a paragraph lead).
  - Or one stretch led by `## Appendix – Reference Information`, tail
    236–273, 333 words (99%).

Not collapsible:
- The "Using the CRT" box (81–101): operation and safety, which line 150
  points to.
- The schematic (61).
- The maximum-voltage box.
- The Sources box (172–193): question 169 says "box below".
- The prediction lists (121–128) and the recap (197–204): the Part 4
  questions are answered against them.
- The Part 1 derivation (65–73, 151 words, the only `$$` candidate in PH
  213): line 69 defines Ψ, which three questions extract.

## 3. Mechanism coverage

Codes:

| Code | Case |
|---|---|
| H | heading lead |
| P | paragraph lead |
| L | list in the tail |
| $$ | display math |
| F | picture |
| T | table |
| B | box in the tail |
| A | action in the tail |
| N | nested div in the tail |
| iB | stretch inside a box |
| Ls | landscape |

| Lab | Cases |
|---|---|
| ph211-capstone | H, P, L, A, N, iB (three times); appendix stretches per subsection, including a paragraph lead inside a heading's section. B is possible only if 29–43 is used as one stretch (72 words). |
| ph211-data-analysis | H (`##`), P, L, B (a box with a `###` heading and a nested action in the tail), A, N, iB |
| ph211-describing | H, P, L, A |
| ph211-designing | H, P, L, A, iB; anchor targets on stretch leads |
| ph211-hypothesis | H, P, A, iB; an anchor target on a lead |
| ph211-team-building | P, L, A |
| ph211-uncertainty | H (`####`), P, L, A; the `.numbered` div sits next to the stretches, not inside one |
| ph212-capstone | H, P, L, B (45–62), A, N, iB, $$, F (4 pictures), T (the rubric), Ls (2 stretches inside the landscape div) |
| ph212-data-analysis | H (`##`), P, L, A, iB |
| ph212-designing | H (`##`, `###`, `####`), P, L, $$, A |
| ph212-extending | H, P, L, A, iB |
| ph212-hypothesis | P (inside a box), H, L, A, iB; 22–34 instead gives B (154 words) |
| ph212-sharing | H, P, L, A, F |
| ph213 | P, H (49 or 234), L, A, inline math. No $$ (unless 65–73), and no B, F, T or Ls. |

No drawn figure is collapsible in any lab; both drawn figures (ph212-designing
341 and ph213 159) are protected.

## 4. Repetition across labs

Approximate figures, from verbatim lines of 6 or more words:

| Repeated text | Size | Where |
|---|---|---|
| Required Plot Elements plus the Linearization core | about 200 words | 13 labs (all but team-building) |
| "What is Uncertainty?" (two paragraphs) | about 123 words | 11 labs; in the main path inside a box in ph211-uncertainty and ph212-data-analysis |
| The PH 212 Sources, "human error" paragraph and Linearization prose | about 124 words | all 6 PH 212 labs and PH 213; a main-path box in ph213 |
| The PH 211 "Predictions, Hypotheses, and Models" and Linearization variants | about 200 words | ph211 capstone, describing, designing and hypothesis |
| Variables and Parameters | about 200 words | ph211 capstone and describing (appendix), designing (a main-path box) |
| The sources list | about 60 words | 10 labs |
| Assumptions | about 120 words | 4 PH 212 labs |

Also shared:
- **ph212 capstone and sharing:** about 160 words (the reliable-experiment
  list and the slope method). The propagation text is in the capstone's
  appendix and in a main-path box in sharing.
- **The two capstones:** about 140 words (the "If you miss Week 1" and
  "Remember, an experiment always" boxes).
- **The two data-analysis labs:** about 106 words (the plot rules and the R²
  text).
- **ph211-uncertainty and ph212-data-analysis:** about 98 words (the Excel
  error-bar steps). They are collapsible in the first lab's appendix and
  protected in the second's main path.
- **The submit paragraph:** about 35 words in all 14 labs; it stays visible.

## 5. Recommendation

**(a) Mechanism coverage with the fewest labs.**

- **PH212H: ph212-capstone alone.**
  - It is the only lab with a table, landscape, pictures, display math, a box
    in a tail, a stretch inside a box, and heading and paragraph leads.
  - It lacks only a drawn figure, which no lab can supply.
  - It is the hardest case for the PDF: long, and with a landscape page.
  - Runner-up: ph212-designing (`$$`, and a three-level heading appendix). It
    would need a second lab for pictures, a table and landscape.
- **PH211H: ph211-data-analysis.** No PH 211 lab can show `$$`, a picture, a
  table or landscape, so one lab is enough. This one has:
  - the hardest accessibility case (a box with a heading inside a collapsed
    tail);
  - a `##` heading lead and a stretch inside a box;
  - the largest PH 211 main-path total (515 words);
  - an appendix that must stay fully open beside collapsed main-path text.
  - Runner-up: ph211-capstone (11 stretches, a richer appendix pattern). Its
    box-in-tail case needs the less natural 29–43 lead, and PH212H already
    covers its appendix pattern.
- **PH213H: ph213-hypothesis-testing**, the only choice.
  - It exercises paragraph leads (including the appendix's bold
    pseudo-headings), a heading lead (49, or the whole appendix led at 234),
    lists, actions and inline math.
  - It cannot show `$$` without collapsing the Ψ definition, and has no box,
    picture or table in any stretch.

**(b) The density test.**
- ph212-capstone has the largest raw share (24%), but 65% of it is one
  rubric table, so it would mostly test whether students open the rubric.
- **ph211-capstone** is the best prose test: 21% over 5 stretches, all
  review or framing, and nothing new.
- The runner-up, ph211-data-analysis, has the most collapsible words (515,
  19%). But that text is first-exposure linearization theory, which mixes a
  pedagogy question into the reading question.

## 6. Design issues

1. **Anchor links into stretches.**
   - Links to `_What_is_Uncertainty?` and `_Linearization`: ph211-designing
     184 and 215, and ph211-hypothesis 131. A link to
     `_Phenomena_to_Investigate`: ph212-capstone 219.
   - This is safe only if each target heading is a stretch lead or sits
     outside every stretch. A single stretch over a whole appendix would hide
     the targets inside a closed `<details>`.
   - Don't rely on browsers auto-opening on fragment navigation; test it.
2. **Heading levels in ph212-designing.** `### Appendix B` sits under `##
   Appendix A`. A filter that scoped stretches by heading level would swallow
   Appendix B into Appendix A's derivation stretch, so ranges must end
   explicitly, or appendix headings must act as boundaries.
3. **ph212-capstone's landscape div crosses a section.** It opens (180)
   before `### Evaluation` and closes (206) before `## Week 1`. A stretch
   there must nest inside the div and never cross its fence. Collapsing the
   rubric (535 words with its lead, 15% of the main path) is a policy call.
4. **ph212-capstone's "SKIP THIS IF YOU DID IT IN THE PRE-LAB" box
   (111–119).** It is explicitly optional but holds a hint, so it cannot
   collapse whole. Collapsing only line 114 (53 words) would leave the hint
   visible without its download link. The survey excluded it; it needs a
   ruling.
5. **ph212-extending's Graphical Analysis Pro box.** After the D-0133 ruled
   omissions, line 60 ("…go to") and the hint ("The activation code for Pro
   is") dangle. Only 56–58 collapse.
6. **Hints split the ph212 Linearization sections.** The definition list is
   a `::: hint`, so the section cannot collapse behind its heading. The
   stretch starts at the "Linearization comes in handy" paragraph instead,
   leaving a visible heading, then a visible hint, then a collapse. Every
   "Tips for Using Graphical Analysis" section stays fully visible.
7. **Page-based pointers.** ph211-data-analysis hint 111 and ph212-data-analysis
   question 228 point to "the box on the previous page". Those boxes stay
   visible, but the pointers assume the PDF's page layout.
8. **Same text, different verdicts.**
   - The Excel error-bar steps are collapsible in ph211-uncertainty's
     appendix but protected in ph212-data-analysis's main path.
   - Required Plot Elements is collapsible in appendices (the appendix-as-place
     rule), though several questions ask for "all the required elements".
9. **Headings inside a collapsed tail** (ph211-data-analysis 116–136,
   ph212-capstone 45–62) drop out of heading navigation while the stretch is
   closed. Check this for accessibility.
10. **Data notes.**
    - No `.checkpoint` block exists in any of the 14 handouts, so that part
      of rule 3 is untested.
    - ph212-data-analysis 225 ends with "Other techniques include" and no
      continuation; the original reads that way.
    - The ph213 prediction list at 199–204 repeats 121–126 word for word, and
      stays visible because Part 4's questions are answered against it.
11. **Learning Objectives tails are 27 to 49 words**, at the 30-word line.
    ph212-extending's falls under it, and several others clear it by 1 to 5
    words. If the 44 px control is the bar, they are marginal everywhere.

Scratch files, in the session's scratchpad and not in the repo:
`stretch_ranges.py` (tail counts), `repeats.py` (the repetition counts) and
`alt.py` (the alternative ranges).
