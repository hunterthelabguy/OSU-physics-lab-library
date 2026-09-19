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

## 2026-09-19 (landing, style guide, evidence)

26. **Merges are local squashes.** GitHub's web merge wrote the account's
    primary email as author on e197aa8 (library) and ae70480 (instructor),
    and rejects the noreply address when asked to use it. Until the account
    setting changes, PRs are squashed locally as the noreply identity and
    pushed, and the PR is closed with the landing commit. Whether to rewrite
    those two commits is open, awaiting the owner.
27. **Style guide and skills matrix received** (previous coordinator, July
    2024), in the original materials; not yet converted or committed.
    Reviewed in `docs/presentation-evidence.md`, which lists six findings
    for owner judgment. Nothing there is ruled.

## 2026-09-19 (presentation rulings)

28. **The pilot ships two presentations of the same document.** One keeps the
    original page settings faithfully; one drops them and follows the
    evidence review, keeping only the meaning rules. Purpose: show a
    colleague the difference side by side and win agreement before any
    format change. Both come from the one Markdown source; the content is
    never copied into a second file, so the two can never drift.
29. **In the modernized presentation, graded questions get their own labeled
    block** and bold goes back to being emphasis. The faithful presentation
    keeps the original bold exactly (ledger 23), which still governs the
    source file and the check.
30. **Every resource offers downloads:** Markdown, HTML, Word, and PDF, all
    built from the Markdown, which stays the one copy we edit. Students read
    on screen today, so the site is the entry point, but print output is
    first class, not an afterthought: paper may become the graded artifact
    in the long run.
31. **The skills matrix becomes a data file** in the instructor repo, with
    descriptor ids for competencies and columns keyed to lab ids.
32. **Canonical competency list: deferred.** The owner will read the matrix
    and the instructor guide before ruling which wording wins (see 5, and
    the evidence review's finding 6).
33. **Observed while rendering: the legend contradicts the modern
    presentation.** The handout's legend box says "Bold, numbered items
    reference things that need to be included in your lab report", which
    describes the old cue. In the modern presentation, questions are labeled
    blocks and that sentence is wrong. Nothing was changed (conversion
    phase). Fixing it is a content change, and it is the clearest small
    example of why the two presentations cannot both be right forever.
34. **Renderer.** `tools/render.py` plus `themes/faithful.css`,
    `themes/modern.css`, `tools/template.html`, and
    `tools/filters/questions.lua`. Question numbers are generated at render
    time from document order, so reordering a lab renumbers safely.
    `--embed-resources` makes each output file stand alone. Output goes to
    `build/`, which is not committed. Word and PDF outputs are not wired up
    yet (30).
35. **Front matter gains `title`.** It holds the document's original title
    text and feeds the page title. Metadata is not part of the
    content-unchanged comparison, which reads the body.

## 2026-09-19 (session close: deploy and stack)

36. **Reversal: the commit email stays public.** Amends 26. The owner
    accepts the address appearing in public history; the risks (scraped
    address, spam, targeted phishing, correlation with other accounts) are
    judged acceptable. No history rewrite. PRs may merge on GitHub again,
    which stamps the account's primary address as merge author. Entries 23
    to 35 stand as written.
37. **The site deploys unlisted while the license is open.** Amends 8: an
    unlisted draft deploy is allowed, and public distribution is still not.
    Every page carries a visible banner saying draft, license pending, not
    for distribution, and the site asks search engines not to index it. The
    purpose is that the owner can open it anywhere, including to show a
    colleague, without carrying a laptop.
38. **Stack: Pandoc and a small build script; no framework yet.** The
    renderer already in the repo grows a script that builds every page and
    an index. Astro is deferred; the electric force tool does not require
    it, since a self-contained HTML tool can be its own page on a static
    site. Revisit when a tool needs shared layout, state, or its own build.
39. **The build stays host-agnostic.** Output is plain static files that any
    host serves. No platform-specific features, no platform SDK, no
    serverless functions, and no config that only one host understands.
    Moving to another host must be a settings change, not a rewrite.
40. **Hosting: a new Vercel project on its default URL**, deploying from
    `main` of this repo. Under 39, Vercel is only where it points today.
41. **The skills matrix is on hold.** Entry 31 still stands as the ruling;
    the work is deferred behind the landing page and site scaffolding. The
    question about the named person in its comments is unanswered and
    blocks conversion.
42. **First-pass site scope.** Landing page; Lab 1 in both presentations
    with a way to switch between them; a course index for PH 211, 212 and
    213 with Lab 1 filled in and the rest marked not yet converted; and the
    public "How this was made" page. Per-document downloads are not in this
    pass (30 still stands).

## 2026-09-19 (first site build)

43. **First site build.** `tools/render.py` grew into the build script.
    `--site` writes `build/site/`: the landing page, a course index, the
    public "How this was made" page, and every converted document in both
    presentations with a link that switches between them. Scope is exactly
    entry 42; per-document downloads are still out (30). Every page carries
    the draft banner and `noindex`, and `robots.txt` disallows everything
    (37). Links are relative, so the site opens from disk as well as from a
    host; output is plain static files and no host-specific config file is
    in the repo (39). The site build now runs in CI, so a broken build
    script fails `verify`.
44. **The method page is lifted from VISION.md at build time**, never
    retyped, so the public page and the vision cannot disagree (principle
    2). Landing copy lives in `site/landing.md`; the banner wording lives in
    `tools/render.py` as `BANNER_MAIN` and `BANNER_DETAIL`. The owner
    approved both wordings on 2026-09-19 before the first deploy.
45. **Course index data is quoted, not converted.** PH 211 lab numbers,
    titles and one-line descriptions come word for word from the Activities
    table of "PH 211 Curriculum Summary" in the original materials. They
    live in the front matter of `site/courses.md` and the page says on its
    face that they are quoted, not converted, because that document has not
    been converted and the content-unchanged check therefore does not cover
    them. Nothing is written for a lab that document does not list, the
    unimplemented Lab Skills practical included. PH 212 and PH 213 have no
    material in hand, so each is listed with no labs and a line saying so.
46. **Observed while building the site, not changed.**
    (a) VISION.md's method section says the original's text is compared with
    the Markdown's text; since entry 24 the check also compares bold on
    every word, so the public page understates what runs.
    (b) The same page says "No student data enters any repo, by rule";
    "repo" is jargon against entry 17's plain-terms rule.
    (c) Entry 33's legend contradiction is now visible on the live
    modernized page, where the legend's claim about bold is false. That is
    the comparison entry 28 exists to provoke, so it stays until the
    content-change phase.

## 2026-09-19 (first deploy)

47. **Deployed unlisted, 2026-09-19.** Vercel project
    `osu-physics-lab-library` on the personal account, deploying from `main`
    of this repo (entry 40). Production is
    `https://osu-physics-lab-library.vercel.app`, with
    `osu-physics-lab-library-hunterthelabguy.vercel.app` and the
    `git-main` URL as further aliases. First production deployment built
    commit 8377eac.
48. **Vercel Authentication was turned off; password protection stays off.**
    The new project came with Vercel Authentication on by default, which
    would have required a Vercel login to view and defeated entry 37's
    purpose, namely that the owner can open the site anywhere and show a
    colleague. The owner ruled on 2026-09-19 to leave password protection
    open as well. So unlisted means `noindex`, `robots.txt` and the banner,
    not access control: the default URL is guessable from the repo name, and
    anyone holding it can read the site. Revisit if the audience widens
    before the license settles.
49. **Build settings live in the project, not in the repo** (entry 39). No
    `vercel.json` or equivalent is committed, so nothing in the repo knows
    which host serves it. The settings are written down in `CLAUDE.md` so
    another host can be set up from the same three lines. Moving hosts stays
    a settings change.
