# Re-baselining at the first ruled change: design

- **Status:** approved by the owner, 2026-11-18 ("Approve and promote").
  Spec and ledger only; no code, no plan.
- **Question (D-0194 (2)):** what should `tools/check_numbers.py` compare
  once a ruled change (D-0168) edits a handout's question list?
- **Answer:** nothing. From a handout's first ruled change on, its own
  Markdown is the baseline, and neither Word check runs on it (D-0195).
- **Entries:** D-0195 and D-0196, ruled 2026-11-18.
- **Revision 2, 2026-11-18.** Revision 1 (commit 02696d9) answered the
  question with `ruled_numbering`, a list of question-list edits declared
  against Word's anchors, and five entries. The owner's review set the
  premise aside, so revision 2 replaces it. Those entries were never
  promoted or merged, and their numbers are reused here.

## 1. The problem

`compare()` pairs Word's labels with the converted lab's items in document
order. A ruled change that removes, adds or reorders a question short of
the list's end therefore cannot pass (D-0194 (1)), and loosening the check
to let it through is ruled out (D-0168 (3)). D-0168 kept both Word checks
running on changed handouts, with each changed passage declared in front
matter, so that the site could say every difference from the original is
listed and ruled.

## 2. The owner's ruling

Revision 1 proposed extending that proof to question lists. The owner, on
reading the plain-language summary:

- "Seems unnecessary to have these checks since the Markdown file is the
  SSOT from here on out. Each edit to the markdown handouts should still be
  recorded, though, but this seems overkill."
- "Ok but my point is that this claim is no longer necessary. Whatever
  "the original Word handout" is becomes irrelevant to students as soon as
  we stop using that version. Why mention it at all?"
- "Can these ruling still not be preserved in the instructor repo?"
- To the rule as worded in section 3: "Confirmed, rewrite the spec".

The Word comparison proved that the conversions were faithful. A handout
that has deliberately moved on has nothing left for that proof to serve.

## 3. The rule (D-0195)

> A handout is checked against its Word original until its first ruled
> change. From that change on, its own Markdown is the baseline: no Word
> comparison runs on it, changes are reviewed in the PR diff, and each
> change cites its ruling in the instructor repo. The question-id pin still
> fails on any question added, removed or reordered until it is updated
> with a ruling.

What this means in the repo:

- **`status` is the switch.** A file with `status: converted` is checked
  against Word as now: the word check, the number check and their
  declarations (`ruled_omissions`, `ruled_additions`, `ruled_equations`,
  spans). The first ruled change to a handout sets `status: ruled-change`
  in the same PR, and from that commit on both Word checks skip the file.
  D-0178 said nothing reads `status`; after this, the checks do.
- **What counts as a ruled change** is unchanged: anything beyond format,
  in D-0168 (1)'s sense. Format fixes declared during conversion, D-0133's
  redactions and D-0167's equation fixes, leave a file `converted`
  (D-0178), and their declarations stay.
- **The record of a change** is the PR's diff, a commit message that cites
  the ruling by its instructor-ledger number, and the ruling itself in the
  instructor repo's ledger. That ruling records who drafted the new wording
  and who approved it (D-0168 (4)'s standard, which moves with it). No
  front-matter list of changed passages is kept for a ruled change.
- **The pin is unchanged.** `tests/question-ids.json` still applies to
  every file with a `source_file`, so adding, removing or reordering a
  question or checkpoint fails until the pin is updated, with an entry
  naming the numbers that moved (D-0077). It does not see parts.
- **Numbers** come from `questions.lua` as always. After a ruled change
  nothing compares them with Word's, and nothing needs to.
- **`source_file` stays** in a ruled-change file's front matter, as the
  record of where the handout came from.

## 4. What the build changes

This is a list for the plan that follows approval, not the plan.

1. `tools/check_unchanged.py` and `tools/check_numbers.py` skip a file
   whose `status` is `ruled-change` and print why, for example
   `skip FILE (ruled-change: its own Markdown is the baseline, D-0195)`,
   so a local run over every file stays honest about what it checked. The
   CI selection in `.github/workflows/verify.yml` can stay as it is.
2. D-0193's interim stop becomes moot for handouts. It stays for the Lab
   Handbook's step A (section 5).
3. `ph211-describing-an-experiment-handout.md`, the one `ruled-change` file
   today (D-0169), drops its `ruled_omissions` and `ruled_additions`.
   Nothing reads them any more, and D-0169 keeps the record. Another
   session has uncommitted work on this file in the shared checkout, so the
   build coordinates with it first.
4. The em-dash scan (`tools/check_em_dash.py`, D-0103) treats a
   `ruled-change` file as a published source, since its new wording is the
   site's own. Measured 2026-11-18: D-0169's file has no U+2014. PH 212
   Lab 2's original has one, which a later ruling on that handout decides.
5. The words that describe the old mechanism are amended:
   - `CLAUDE.md`'s "Conversion first, then ruled changes" line;
   - `docs/conversion-spec.md`'s "Content-unchanged check" and the `status`
     comment in its front-matter template;
   - the public page (section 6).
6. Tests: a `ruled-change` fixture is skipped by both tools with the
   message; a `converted` fixture is checked exactly as today; the pin test
   still fails on a reordered `ruled-change` file.

## 5. Consequence for the Lab Handbook plan (not ruled here)

The handbook plan (`origin/lab-handbook-spec`, D-0188 to D-0193) has two
steps:

- **Step A** is a conversion of PH 211 Lab 7's Appendix B, checked against
  Word, with a span omission (D-0189) for everything before it. It still
  needs D-0189 and D-0193's whole-list stop, because it is a conversion.
- **Step B**, a ruled change, is then re-baselined, and the checks stop.

What this spec does remove is the need for spans in the **appendix cuts
from the handouts themselves**. A cut from a converted handout is a ruled
change, so it is simply an edit reviewed in its diff. D-0189's rationale
counted seven appendix sections that needed spans for exactly those cuts.
Whether the handbook plan should drop or narrow D-0189 is that plan's call.
This spec only tells the session that owns it.

## 6. Public wording (D-0196)

The live "How this site works" says that a second program "compares each
question's number with the number Word shows. They must match exactly".
It also says that, for changed handouts, "The same check still runs on
every handout and passes only if the words match the original apart from
the listed passages". Both stop being true at the first re-baselined
handout. PR #89 cuts the page to a short version with no paragraph on the
checks.

- If #89 merges before the build, the build adds no public wording.
- If the build comes first, its PR replaces that paragraph and brings the
  new wording to the owner in that PR.

Either way, the page makes no claim about the Word originals for changed
handouts.

## 7. Considered and declined

- **Revision 1's `ruled_numbering`.** Each question-list edit declared
  against Word's anchors, with structure compared after the edits. The
  owner: "this seems overkill"; the proof it keeps serves no reader once a
  handout has moved on.
- **D-0168 as written, with front-matter lists for every ruled change.**
  They repeat the diff, and the claim they support is no longer made.
- **Re-baselining against the last approved Markdown by a tool.** A
  comparison with a stored copy is the PR diff over again.
- **Retiring the Word checks for every file now.** The conversions not yet
  landed (PH 213 Lab 6, PR #61; the handbook's step A) still need them.
- **Keeping rulings for handout changes in this repo's public ledger.** The
  owner asked for the instructor repo. The cost, recorded so it is a
  choice: the public record of who drafted each new wording goes private.
  The public page still says the site was built with Claude.
