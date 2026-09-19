# Decision ledger

Dated, append-only. An entry wins over any document it amends. A wrong entry
is corrected by a new entry that cites it, never edited away. Open questions
are recorded as entries too, so the gap is on the record.

## 2026-09-19

1. **New repo.** The public reference library is its own repo, separate from
   the OSU demo catalog. Private until launch.
2. **Split by what can ever be public.** Two repos: this one (student-facing
   and public-safe material, plus the site; the only one that deploys) and
   `OSU-physics-lab-library-instructor` (instructor notes, rubrics, make-up
   data; private). Reason: git history is permanent, so material that might
   never be public must never enter a repo that will be.
3. **Instructor-material visibility is open.** Whether instructor notes and
   rubrics become public (useful to instructors at other institutions) goes to
   a faculty meeting. Gated access (passphrase or login) is deferred with it.
   If ever built, gating is server-side; a client-side passphrase on a static
   site protects nothing.
4. **OSU logistics get their own local layer.** The curriculum is written to
   be adoptable elsewhere; OSU-specific operations (submission platform,
   deadlines, room layout, help channels) are separated from it.
5. **Drift between duplicated passages** (for example the learning objectives,
   which appear in at least four documents with differing wording) is logged
   here, and the owner rules which wording is canonical. Nothing is silently
   reconciled.
6. **Format order.** Markdown source of truth first, then web, then Word.
7. **Pilot scope.** PH 211 Lab 1 (handout; its instructor notes and rubric go
   to the instructor repo), then Lab Guidance for Students, then the PH 21X
   Sample Lab Report. The two long documents are in scope because this is a
   proof of concept for faculty and graduate students, and they are the hard
   cases (Word equations, text-box annotations).
8. **License is open. Nothing publishes until it is settled.** Believed
   intended to be open, but no license text exists in the source material
   (the README's attribution line is redacted). To be raised with the
   previous coordinator and other faculty, together with whether the original
   authors are comfortable with the method (entry 10). Likely shape if open:
   Creative Commons for prose, MIT for code. Not ruled.
9. **Tools are named.** The owner drafts by voice with Wispr Flow and directs
   Claude (Anthropic) for conversion and tooling. Students and colleagues
   deserve to know how the work is done, and colleagues have asked how to do
   the same.
10. **AI-use standard for the migration phase.** No wording, curriculum,
    objectives, or conventions change. Claude converts format only. The
    content-unchanged check (see `docs/migration-spec.md`) proves it per
    document. Original Word files remain untouched and available, so anyone
    who declines AI-assisted material can teach from the originals and lose
    nothing. The project holds itself to the students' own AI policy:
    disclose use, keep reasoning human, the human answers for the work.
11. **Open: AI-use standard for the content-change phase.** When wording
    later changes, Claude may draft text. Owner's default, not yet ruled:
    drafted wording is marked as drafted, and the approving person is
    recorded in this ledger.
12. **Deferred:** a how-to guide for faculty who want to work this way. After
    the pilot proves the method.
13. **Amends 12.** The deferred write-up is for anyone, not only faculty, and
    is framed as how the owner did this work, for whoever is curious, not
    as a how-to guide. Still deferred until the pilot proves the method.
14. **Identifiers never encode sequence.** Lab order changes and labs get
    replaced. Ids are course code plus a descriptor unique enough never to be
    reused (for example `ph211-team-building-handout`); question ids are
    descriptors scoped to their document (for example
    `ph211-team-building:build-process`). Position is a separate editable
    `sequence` field; numbers students see are display only. Retired ids are
    listed here and never reissued. Supersedes the numbered examples in the
    first draft of the spec.
15. **Plain, neutral wording about method.** Avoid terms that read as
    machine authorship or as dismissive of the original work: "generated"
    becomes "built" or "converted"; "legacy" becomes "original" when
    describing the source documents; "AI-assisted material" becomes "the
    converted versions"; "migration" becomes "conversion" (the spec is now
    `docs/conversion-spec.md`). Name the specific tool (Claude) rather than
    the category (AI) when describing what was done.
16. **Name on the method page.** The public "How this was made" section names
    Hunter Reaves rather than "the owner": readers deserve to know whose
    method it is, and a role there reads as evasive. A deliberate exception
    to roles-not-names, limited to that section; roles everywhere else.
17. **Plain terms on public pages.** "The one copy we edit" replaces "source
    of truth", and "first example" replaces "pilot" or "proof of concept",
    on pages readers see. Technical terms stay in the spec and this ledger.
    "Claude may draft text" (entry 11) stays blunt on purpose.

## 2026-09-19 (PH211 Team Building conversion)

18. **Originals are committed.** Each original file lives byte for byte under
    `originals/` in the repo whose visibility it shares (the handout here;
    instructor notes and the full rubric workbook in the instructor repo),
    with its SHA-256 in the converted file's front matter. This makes the
    check reproducible in CI and makes "the originals remain" true on the
    record, not only on one machine.
19. **Handout blocks follow the glyph the reader sees.** Round bullets are
    actions, arrows are hints, per the handout's own legend. Word style names
    are not used for this: the original uses `Actionitem`, `ListParagraph`,
    and `Normal` for the same round bullet. Questions are
    `::: {.question #id}` blocks; their display number and bold come from
    document order at display time.
20. **Verification exists.** `tools/check_unchanged.py` plus a `verify`
    GitHub Actions workflow (Pandoc 3.11, the content-unchanged check on
    every converted file, and a no-em-dash scan outside `originals/`). From
    here, code and converted content land via PR with green `verify` (floor
    4); ledger and spec-only commits may still land direct. The check
    compares words only; structure is reviewed by parse-tree block counts.
    For the Team Building handout: 989 words identical; 5 questions, 7 action
    blocks, 3 hint blocks, 1 box. A deliberately altered copy (the original's
    typo "and the describe the goal" corrected) fails, as it should.
21. **No drift found in Team Building.** The 7 learning objectives match
    between handout and instructor notes (only "you" versus "students"
    differs, by audience). The rubric's question text matches the handout
    word for word.
22. **Observed, not changed (for the content-change phase).**
    (a) The handout title "Lab 1 – Team Building" and the instructor notes'
    "(Question 1)" to "(Question 5)" embed sequence numbers (see 14).
    (b) Part 3's discussion points use the round action bullet.
    (c) Handout typo: "and the describe the goal of the challenge".
    (d) OSU-local passages are not yet split out (see 4): Gradescope
    (handout Part 5, notes Part 5), and in the notes Wormhole, Canvas, the
    10-table seating, and the front desk.
    (e) The notes cite "a few sample contracts" in the lab folder. Three
    likely candidates are among the originals (`GoodLabPartnert.txt`,
    `List of terms.docx`, `Descriptive.pdf`); the PDF names a TA and a
    term, so it needs a ruling before conversion. None is converted yet.

## 2026-09-19 (bold fidelity)

23. **Bold is preserved exactly (owner ruling).** The current curriculum
    teaches students that bold marks what they must answer in the graded
    report; anything not bold carries no such obligation. A faithful
    conversion therefore keeps every word bold or not bold exactly as in the
    original. The owner does not endorse the convention and may revisit it
    in the content-change phase; it stays for now. Question text is stored
    explicitly bold in the Markdown, and display never adds or removes bold.
    Amends 19, whose "bold comes from display" clause is withdrawn; question
    numbers still come from document order.
24. **The check now compares bold.** Every word's bold state (bold, not
    bold, partly bold) must match; headings are exempt on both sides. Team
    Building handout: bold identical on 943 words. Unbolding the single word
    "Individually" in a test copy fails, as it should.
25. **Observed, not changed: bold is overloaded in the handout.** Besides
    the five graded questions, bold also marks an instruction
    ("Individually"), two clean-up actions ("Clean up anything you dropped on
    the floor", "Dispose of your structure..."), labels ("Activity goal:",
    "Learning goal: ..."), and an emphasized "not". Under the stated
    convention a student could read these as graded. For the content-change
    phase.
