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
