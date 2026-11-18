# Numbers under ruled changes: design

- **Status:** proposed, for the owner's approval. Spec and ledger only; no
  code, no plan.
- **Question (D-0194 (2)):** what should `tools/check_numbers.py` compare
  once a ruled change (D-0168) edits a handout's question list?
- **Entries:** D-0195 to D-0199, all `proposed`, in `DECISIONS.md` on this
  branch.
- **Gate:** approved before the first restructure PR or capstone-pass PR
  (D-0141) that edits a question list opens. D-0193's stop is the interim
  check, and it stays until this is built (D-0199).

## 1. The problem

`compare()` pairs Word's labels (`docs/word-labels.json`) with the
converted lab's rendered items in document order, then compares each
displayed number with Word's. A ruled change that removes, adds, splits or
reorders a question or a part anywhere short of the list's end shifts every
pair after it, so it cannot pass. The check must never be loosened to let it
through (D-0168 (3)). The next two pieces of work both edit question lists:
the cognitive-load restructure (questions rewritten, decisions turned into
cues) and the capstone pass (D-0141).

## 2. What the record says

Read for this spec: `CLAUDE.md`; D-0102, D-0110, D-0112, D-0122, D-0168,
and D-0189 to D-0194 from `origin/lab-handbook-spec`; `tools/check_numbers.py`;
`docs/word-labels.json`; `docs/handout-survey.md` sections 1 to 3;
`tests/question-ids.json` and `tests/test_question_ids.py`;
`tools/filters/questions.lua`; and, for restarts and checkpoints, PH 213
Lab 6 on PR #61's branch.

- **Anchors are positions.** `oN` is the Nth top-level paragraph of the
  question lists, `oN.M` a part under it, `oN.M.K` one level down, `xN` a
  bold numbered paragraph in another list (survey section 1). Each record
  in `docs/word-labels.json` is Word's `ListString` at each anchor, in
  document order.
- **Questions already have identity.** Every question and checkpoint block
  carries a unique descriptor id, pinned in order in
  `tests/question-ids.json` (D-0077). Measured 2026-11-17 on the 18
  converted handouts: the k-th pinned block is Word's k-th top-level anchor
  in every file, 194 against 194.
- **Parts have none.** Below the top level, the 18 records hold 158
  o-anchors: 156 parts (6 of them at the second level, in PH 212 Labs 1
  and 6) and PH 211 Lab 3's two `.numbered` appendix entries. A part is a
  Pandoc ordered-list item, which has no attribute to carry an anchor.
- **Restarts follow from the labels.** A question anchor whose number is
  no higher than the previous question anchor's is a Word restart. Run
  over all 19 records, that rule finds exactly the survey's restarts:
  PH 211 Lab 7 o8, PH 212 Lab 3 o12, PH 212 Lab 6 o5, PH 213 Lab 6 o4 and
  o9.
- **Checkpoints are compared without a number.** `compare()` accepts a
  checkpoint at any top-level anchor and compares no number (D-0112,
  call 3). Whether an anchor is a question or a checkpoint is recorded
  only by the pin, as `[kind, id]`.
- **Numbers are rendered, never stored.** `questions.lua` counts questions
  in document order, resets at `.restart`, and counts checkpoints apart.
  The number check reads those rendered labels and does not keep a second
  copy of the numbering rule (D-0112, rationale).

## 3. Critique of the lean in D-0194 (3)

D-0194 (3) leaned on writing each Word anchor onto its item while the file
is still a straight conversion, then comparing by anchor.

- **C1. Half of it already exists.** Question ids pair one-to-one with
  Word's top-level anchors in every converted file, so 194 attributes in
  the sources would add nothing.
- **C2. Parts have nowhere to hold an anchor.** Marking 156 parts would
  mean an empty span in each one, inside student-facing source that the
  restructure is about to rewrite. That is the most expensive part of the
  lean, and it lands where most of the edits will be.
- **C3. After a change, check what produces the numbers, not the numbers.**
  An expected number computed from Word's rule would be a second numbering
  rule, which D-0102 and D-0112 declined. After a change, the check compares
  structure (identity, kind, level, order, restart placement) and leaves the
  numbers to `questions.lua`.
- **C4. "A removal whose words stay" needs no new Word read.** With
  identity explicit, a question whose `.question` block is unwrapped shows
  up as a missing Word item and fails unless it is declared. Whether its
  words stay is the word check's job (`ruled_omissions`). A decision turned
  into a plain cue is therefore a declared removal, and Word's paragraph
  text is never needed.
- **C5. Gap: parts reordered within a question.** Without per-part
  identity, swapping b and c passes on structure. Rubrics and Gradescope
  outlines refer to "3b".
- **C6. Restarts need an owner.** If a ruling removes PH 211 Lab 7's o8,
  nothing says where Week 2's `.restart` goes.
- **C7. Anchors outside the question lists.** PH 211 Lab 3's x1 to x3 are
  o13's parts. PH 211 Lab 6's x1 to x4 are report items. o14.0.1 and
  o14.0.2 are the `.numbered` appendix contents.
- **C8. After a full rewrite, the check proves one thing.** Every Word
  item is kept or listed as a ruled change. The live "How this site works"
  says the number check "compares each question's number with the number
  Word shows. They must match exactly", which is false for an edited list.
- **C9 (found while drafting). Retyping is caught by the pin, not by this
  check.** The kind an anchor was converted to (question or checkpoint) is
  recorded only in the pin. The number check accepts either kind at a kept
  anchor, as it does today, so an undeclared retype fails the pin test
  (D-0077), not this check. Section 5.4 states this rather than building a
  third record of conversion kinds.

## 4. Approaches

**A. Declarations against Word's ordered list (recommended; ruled,
D-0196).** No marks in the source. A file whose list is edited declares
each change to its numbered structure in front matter, `ruled_numbering`,
each entry with a ledger reference. The check applies the declarations to
Word's ordered anchors to get the expected structure, then compares in
order as it does today. A file with no declarations runs today's
`compare()` unchanged.

- Cost: errors are reported by position ("Word's o6 expected as the 5th
  question, found #x") rather than at the item.
- Gain: nothing to edit in the 18 converted files, and one place per
  handout where its list changes are listed, next to `ruled_omissions`.

**B. Anchors marked in the source (D-0194's lean).** Each question block
carries `anchor="oN"` and each part an empty span, all written in one
mechanical PR that the in-order check proves. After that, the check
compares anchor sets, with removals and additions declared.

- Declined in round 1 (Q2): the marks for questions duplicate the pinned
  ids (C1), and the marks for parts are 156 spans in student-facing source
  that authors would have to keep intact through rewrites (C2). The only
  gain is error messages at the item.

**C. The pin as the authority.** `tests/question-ids.json` grows to hold
parts and each item's anchor. The check compares file to pin in order, and
pin to Word as a set in which every anchor is accounted for.

- Declined in rounds 1 and 2 (Q2, Q7): a second, hand-kept copy of the
  structure, and it moves the link to Word into a test fixture.

## 5. Design (approach A)

### 5.1 Declarations

A file whose numbered structure differs from its original's carries
`ruled_numbering` in front matter. Every entry has `ledger`, the entry that
rules it. The entry kinds:

```yaml
ruled_numbering:
  - remove: o5                 # a top-level Word anchor, gone from the list
    ledger: "D-0nnn"
  - add: lab:new-question-id   # a question or checkpoint block not from Word
    after: o4                  # a Word anchor, an added id, or "start"
    ledger: "D-0nnn"
  - move: o9                   # a kept top-level anchor out of Word's order
    after: o7                  # same forms as add's
    ledger: "D-0nnn"
  - retype: o1                 # a kept top-level anchor's kind changes
    to: checkpoint             # or question
    ledger: "D-0nnn"
  - restart: lab:new-question-id   # a question restarting where Word does not
    replaces: o8                   # only when a Word restart is removed or retyped
    ledger: "D-0nnn"
  - parts: o3                  # a kept anchor or an added id
    sequence: [o3.1, new, o3.3]
    ledger: "D-0nnn"
```

- `restart` may name `none` with `replaces`, when a ruling removes a week
  split.
- A `sequence` lists the question's parts in order. Each item is a Word
  part anchor of that same question, `new`, or a one-key mapping from
  either of those to its own sequence one level down, for example
  `[o6.1, {o6.2: [o6.2.1, new]}, new]`.
- A part anchor left out of a sequence is removed. A part anchor listed out
  of Word's order is moved, and the declaration itself names the
  re-lettering (D-0196).
- A question with no `parts` entry keeps Word's parts exactly.
- An added question with parts needs a `parts` entry made of `new` items.
- PH 211 Lab 3's x1 to x3 are named in o13's sequence like any part
  (D-0195).
- Successive ruled changes add entries. An earlier entry is never edited
  away (charter floor 7). If a later ruling undoes one, both stay, and the
  later entry's ledger says so.

### 5.2 Building the expected structure

1. Take the record's top-level o-anchors in order, each with its Word parts
   tree (o and x anchors under it, as today's in-order matching places them).
2. Apply the `remove`, `move` and `add` entries one at a time, in the
   order the front matter lists them. An `after` must name an item already
   in the list at that point.
3. Mark each item's kind. A retyped anchor takes its declared kind. Any
   other kept anchor accepts either kind, as `compare()` does now (C9). An
   added item takes the kind of its block, checked against the pin by
   D-0077's test.
4. Mark restarts. A kept anchor that is a Word restart (section 2's rule)
   and still a question must carry `.restart`. A `restart` entry's item must
   carry it. Any other `.restart` fails.
5. Replace the parts tree of each item named by a `parts` entry with its
   sequence.

### 5.3 The comparison

Against the rendered items (`rendered_items()`, unchanged):

- **Top level:** in order, the same count, the same kind where it is
  declared or added, the added block's id at each added item, `.restart`
  exactly where step 4 puts it. Question and checkpoint labels must have
  the form "Question N" and "Checkpoint N", and their numbers are not
  compared with Word's (D-0195).
- **Parts of an unedited question:** in order, at Word's levels, each
  marker equal to Word's label, which is today's comparison. Letters
  restart under each question in every original (survey section 3), so
  removing or adding a question elsewhere leaves them right.
- **Parts of an edited question:** the declared tree's shape (count per
  list, nesting). Each list's markers run from its first item in the marker
  style Word uses at that level in this original ("a.", "i."). That is a
  list's own start, not Word's restart semantics.
- **Report items and `.numbered`:** compared exactly as today, in order,
  against the x anchors no `parts` sequence claims and the anchors their
  `.numbered` list names.

### 5.4 Stops

Each stop prints the entry it reads and names D-0196.

- A declaration names an anchor the record lacks, names a top-level anchor
  twice (in `remove`, `move` or `retype`), or names a part anchor outside
  its own question's sequence.
- An `after` does not resolve.
- An `add` id is already used in the file or matches a Word-derived item.
- An entry has no `ledger`.
- A `restart` without `replaces` names a Word restart.
- A Word restart is removed or retyped and no `restart` entry `replaces`
  it.
- A declaration names a report-item x anchor or a `.numbered` anchor. A
  change to those waits for an amendment (D-0195).
- `ruled_numbering` appears in a PDF original's file (D-0160).

### 5.5 What does not change

- A file with no `ruled_numbering` runs today's `compare()` exactly. CI's
  `verify` on the 18 converted files is the regression check.
- `questions.lua` is unchanged.
- The pin stays one row per question and checkpoint. D-0077's rule reads
  "an entry naming the numbers and letters that moved" (D-0197).
- The word check is unchanged. A removed question's words leave through
  `ruled_omissions`, and an added question's words arrive through
  `ruled_additions`.

### 5.6 Public wording (D-0198)

PR #89 cuts "How this site works" to a short page with no paragraph on the
checks. If it merges before this is built, no public wording changes here.
If this lands first, its PR changes the sentence quoted in C8 to say that
every question Word numbers is kept in Word's order or listed as a ruled
change in the handout's own file. That wording comes to the owner for a
ruling in the PR.

### 5.7 The checks that pin it

Fixture tests in `tests/test_check_numbers.py`, in the file's existing
style: fixture originals made by Pandoc, labels written in the test, plus
skeleton cases against real records.

- No `ruled_numbering`: results identical to today's on every existing
  fixture.
- A middle question: removed and declared passes; removed and not declared
  fails.
- An added question: declared passes; not declared fails; a duplicate id
  stops.
- A moved question: declared passes; not declared fails.
- A retype declared and done passes; declared and not done fails.
- PH 211 Lab 7's real record:
  - o8 removed without a `restart` entry stops;
  - with `restart` naming o9 it passes;
  - a `.restart` left on o9 with no entry fails.
- Parts:
  - an unedited question's swapped parts fail;
  - a declared re-lettering passes;
  - a `new` part passes;
  - a nested sequence passes (PH 212 Lab 1's o6.1.1 shape);
  - a sequence naming another question's part stops.
- PH 211 Lab 3's real record: x1 to x3 in o13's sequence pass.
- PH 211 Lab 6's real record: a declaration naming x2 stops.
- Every stop in 5.4 has its own case.

## 6. Out of scope and known gaps

- **Cross-references in the text** ("question 6", PH 212 Lab 1's o4.2) go
  stale when numbers move. No check reads them. Each ruling that moves
  numbers must edit them as declared passages. Not built here; flagged for
  the restructure plan.
- **Report items (PH 211 Lab 6) and `.numbered` (PH 211 Lab 3)** keep
  today's comparison, and any declaration naming them stops (D-0195).
- **Undeclared retype** is caught by the pin, not by this check (C9).

## 7. Considered and declined

- Comparing displayed numbers with numbers computed from Word's rule after
  a change. This is the second numbering rule that D-0102 and D-0112
  declined (round 1, Q1).
- Anchors marked in the source (approach B; round 1, Q2).
- Part count and level only, with no per-question sequence. A swap passes
  silently (round 1, Q3).
- Report items and `.numbered` included now. Two more declaration kinds,
  and no ruling yet needs them (round 1, Q4).
- `.restart` left to the author. A removed o8 would renumber Week 2 on
  from Week 1 with nothing to catch it (round 2, Q5).
- A retype as a removal plus an addition. That records a deletion where
  only the label changed (round 2, Q6).
- The pin extended to parts (approach C; round 2, Q7).
- A record of each anchor's conversion kind for this check. That would be
  a third copy beside the pin and the file, for the one handout (PH 213
  Lab 6) whose conversion made checkpoints (C9).
- A new Word read of paragraph text. C4 removes the need.
- Retiring the number check once a file leaves `converted`. That drops
  the proof that kept questions keep Word's structure (D-0194,
  alternatives).
